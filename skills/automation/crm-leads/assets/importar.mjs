// Painel de leads — junta leads novos na base sem duplicar e sem apagar o que você já mexeu.
// Sem nenhuma dependência.
//
// Uso:
//   node importar.mjs <arquivo.json|arquivo.csv>   junta os leads do arquivo na base
//   node importar.mjs --skip                       lista quem JÁ está na base (pra não reprospectar)
//   node importar.mjs --refazer-dados              só regenera o dados.js (modo sem servidor)
//
// A base fica em leads.json (fatos dos leads) e o funil em estado.json (coluna, marcas, anotações).
// Este script NUNCA escreve em estado.json: o que você mexeu no painel é intocável.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PASTA = path.dirname(fileURLToPath(import.meta.url));
const ARQ_LEADS = path.join(PASTA, "leads.json");
const ARQ_ESTADO = path.join(PASTA, "estado.json");
const ARQ_DADOS_JS = path.join(PASTA, "dados.js");

const CAMPOS = [
  "id","empresa","segmento","cidade","uf","telefone","whatsapp","email","email_confianca",
  "site","instagram","facebook","google_negocio","google_negocio_url","instagram_numeros",
  "redes_atividade","reputacao","responsavel","cargo_responsavel","confianca_decisor","origem_dado",
  "sinal_oportunidade","prova_url","prova_nota","gancho_abordagem","nota_calor","nota_detalhe",
  "tier","anuncio","situacao_cadastral","porte","abertura","tecnologia",
  "pendencias","lote","data_coleta","cnpj","fontes",
];

function lerJSON(arq, padrao) {
  try {
    let t = fs.readFileSync(arq, "utf8");
    if (t.charCodeAt(0) === 0xfeff) t = t.slice(1);
    return JSON.parse(t);
  } catch {
    return padrao;
  }
}

function semAcento(s) {
  return String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}
function digitos(s) {
  return String(s || "").replace(/\D+/g, "");
}

// Todas as identidades possíveis de um lead, em ordem de confiança:
// CNPJ > telefone/WhatsApp > empresa+cidade. O mesmo negócio é reconhecido por QUALQUER uma delas,
// senão o mesmo lead voltando com o telefone novo entraria como se fosse outro.
function chavesDe(l) {
  const ks = [];
  const cnpj = digitos(l.cnpj);
  if (cnpj.length === 14) ks.push("cnpj:" + cnpj);
  for (const f of [l.whatsapp, l.telefone]) {
    const fone = digitos(f);
    if (fone.length >= 10) ks.push("fone:" + fone.slice(-11));
  }
  const nome = semAcento(l.empresa).toLowerCase().replace(/[^a-z0-9]+/g, "");
  const cid = semAcento(l.cidade).toLowerCase().replace(/[^a-z0-9]+/g, "");
  if (nome) ks.push("nome:" + nome + "-" + cid);
  return ks.length ? ks : ["nome:sem-nome"];
}
function chaveDe(l) {
  return chavesDe(l)[0];
}

// CSV com ; ou , — aceita aspas e quebra de linha dentro do campo.
function lerCSV(texto) {
  if (texto.charCodeAt(0) === 0xfeff) texto = texto.slice(1);
  const sep = (texto.split("\n")[0].match(/;/g) || []).length >=
              (texto.split("\n")[0].match(/,/g) || []).length ? ";" : ",";
  const linhas = [];
  let campo = "", linha = [], aspas = false;
  for (let i = 0; i < texto.length; i++) {
    const c = texto[i];
    if (aspas) {
      if (c === '"' && texto[i + 1] === '"') { campo += '"'; i++; }
      else if (c === '"') aspas = false;
      else campo += c;
    } else if (c === '"') aspas = true;
    else if (c === sep) { linha.push(campo); campo = ""; }
    else if (c === "\n") { linha.push(campo); linhas.push(linha); linha = []; campo = ""; }
    else if (c !== "\r") campo += c;
  }
  if (campo || linha.length) { linha.push(campo); linhas.push(linha); }
  if (!linhas.length) return [];
  const cab = linhas.shift().map((h) => semAcento(h).trim().toLowerCase().replace(/\s+/g, "_"));
  return linhas
    .filter((l) => l.some((v) => String(v).trim()))
    .map((l) => {
      const o = {};
      cab.forEach((h, i) => { if (h) o[h] = (l[i] || "").trim(); });
      return o;
    });
}

function normalizar(bruto, loteFallback) {
  const l = {};
  for (const c of CAMPOS) if (bruto[c] != null && bruto[c] !== "") l[c] = bruto[c];
  // apelidos comuns vindos de planilha de fora
  if (!l.empresa) l.empresa = bruto.nome || bruto.negocio || bruto.razao_social || "";
  if (!l.whatsapp) l.whatsapp = bruto.celular || bruto.zap || "";
  if (!l.telefone) l.telefone = bruto.fone || bruto.tel || "";
  if (!l.sinal_oportunidade) l.sinal_oportunidade = bruto.sinal || bruto.motivo || "";
  if (!l.gancho_abordagem) l.gancho_abordagem = bruto.gancho || "";
  if (l.nota_calor != null) {
    const n = parseFloat(String(l.nota_calor).replace(",", "."));
    l.nota_calor = isFinite(n) ? n : "";
  }
  if (!l.tier && isFinite(Number(l.nota_calor))) {
    const n = Number(l.nota_calor);
    l.tier = n >= 70 ? "QUENTE" : n >= 45 ? "MORNO" : "FRIO";
  }
  if (!l.lote) l.lote = loteFallback || "";
  if (!l.data_coleta) l.data_coleta = new Date().toISOString().slice(0, 10);
  if (typeof l.fontes === "string" && l.fontes) l.fontes = l.fontes.split(/\s*\|\s*/).filter(Boolean);
  l.id = l.id || chaveDe(l);
  return l;
}

function gravarDadosJS(base, estado) {
  const conteudo =
    "// Gerado automaticamente. Serve pro painel funcionar mesmo aberto sem o servidor.\n" +
    "window.__CRM_DADOS__ = " + JSON.stringify({ leads: base.leads, estado }, null, 1) + ";\n";
  fs.writeFileSync(ARQ_DADOS_JS, conteudo, "utf8");
}

/* ---------------- execução ---------------- */
const arg = process.argv[2];
const base = lerJSON(ARQ_LEADS, { versao: 1, leads: [] });
if (!Array.isArray(base.leads)) base.leads = [];
const estado = lerJSON(ARQ_ESTADO, { versao: 1, leads: {} });

if (!arg || arg === "--ajuda" || arg === "-h") {
  console.log("uso: node importar.mjs <arquivo.json|csv> | --skip | --refazer-dados");
  process.exit(0);
}

if (arg === "--refazer-dados") {
  gravarDadosJS(base, estado);
  console.log("dados.js regenerado com " + base.leads.length + " leads.");
  process.exit(0);
}

if (arg === "--skip") {
  // Lista compacta pra prospecção NÃO trazer de novo quem já está na base.
  const linhas = base.leads.map((l) => {
    const s = estado.leads?.[l.id] || {};
    const marcas = (s.tags || []).join(",");
    return [
      l.empresa, l.cidade || "", digitos(l.whatsapp || l.telefone), digitos(l.cnpj),
      s.coluna || "novos", marcas,
    ].join(" | ");
  });
  console.log("JA_NA_BASE: " + base.leads.length);
  console.log("empresa | cidade | fone | cnpj | etapa | marcas");
  linhas.forEach((l) => console.log(l));
  process.exit(0);
}

const caminho = path.isAbsolute(arg) ? arg : path.resolve(process.cwd(), arg);
if (!fs.existsSync(caminho)) {
  console.error("Arquivo não encontrado: " + caminho);
  process.exit(1);
}
const cru = fs.readFileSync(caminho, "utf8");
let novosBrutos;
if (/\.csv$/i.test(caminho)) novosBrutos = lerCSV(cru);
else {
  const j = lerJSON(caminho, null);
  if (!j) { console.error("JSON inválido em " + caminho); process.exit(1); }
  novosBrutos = Array.isArray(j) ? j : j.leads || [];
}

const loteFallback = path.basename(caminho).replace(/\.(json|csv)$/i, "");
const porChave = new Map();
const indexar = (l) => chavesDe(l).forEach((k) => { if (!porChave.has(k)) porChave.set(k, l); });
base.leads.forEach(indexar);

let inseridos = 0, atualizados = 0, camposNovos = 0;
const tocadosMarcados = [];

for (const bruto of novosBrutos) {
  const novo = normalizar(bruto, loteFallback);
  if (!novo.empresa) continue; // linha sem nome de empresa não entra
  const existente = chavesDe(novo).map((k) => porChave.get(k)).find(Boolean);
  if (!existente) {
    novo.id = chaveDe(novo);
    base.leads.push(novo);
    indexar(novo);
    inseridos++;
  } else {
    // completa buraco: nunca sobrescreve informação que já estava lá
    let mexeu = false;
    for (const c of CAMPOS) {
      if (c === "id") continue;
      const vazio = existente[c] == null || existente[c] === "";
      if (vazio && novo[c] != null && novo[c] !== "") { existente[c] = novo[c]; mexeu = true; camposNovos++; }
    }
    if (mexeu) { atualizados++; indexar(existente); }
    const s = estado.leads?.[existente.id];
    if (s && (s.coluna !== "novos" || (s.tags || []).length)) {
      tocadosMarcados.push(existente.empresa + " (" + (s.coluna || "novos") + ")");
    }
  }
}

base.versao = 1;
base.atualizado_em = new Date().toISOString().slice(0, 16).replace("T", " ");
fs.writeFileSync(ARQ_LEADS, JSON.stringify(base, null, 1), "utf8");
gravarDadosJS(base, estado);

console.log("RESULTADO DA IMPORTACAO");
console.log("  leads novos:        " + inseridos);
console.log("  ja existiam:        " + (novosBrutos.length - inseridos));
console.log("  completados:        " + atualizados + " (" + camposNovos + " campos que estavam vazios)");
console.log("  total na base:      " + base.leads.length);
if (tocadosMarcados.length) {
  console.log("  ja estavam no funil (funil preservado): " + tocadosMarcados.slice(0, 10).join("; ") +
    (tocadosMarcados.length > 10 ? " ..." : ""));
}
