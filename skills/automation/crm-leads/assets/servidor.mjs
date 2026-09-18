// Painel de leads — servidor local, sem nenhuma dependência.
// Serve os arquivos da PRÓPRIA pasta e grava o estado do funil em estado.json.
// Só escuta em 127.0.0.1 (ninguém de fora da máquina alcança).
//
// Uso:  node servidor.mjs [porta]

import http from "node:http";
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

const PASTA = path.dirname(fileURLToPath(import.meta.url));
const ARQ_LEADS = path.join(PASTA, "leads.json");
const ARQ_ESTADO = path.join(PASTA, "estado.json");
const PORTA_INICIAL = Number(process.argv[2]) || 7788;
const TENTATIVAS = 12;
const LIMITE_POST = 8 * 1024 * 1024; // 8 MB

const TIPOS = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".ico": "image/x-icon",
  ".md": "text/plain; charset=utf-8",
};

function lerJSON(arquivo, padrao) {
  try {
    let txt = fs.readFileSync(arquivo, "utf8");
    if (txt.charCodeAt(0) === 0xfeff) txt = txt.slice(1); // BOM do Windows
    return JSON.parse(txt);
  } catch {
    return padrao;
  }
}

// grava sem risco de arquivo pela metade: escreve num temporário e troca
async function gravarSeguro(arquivo, texto) {
  const tmp = arquivo + ".tmp";
  await fsp.writeFile(tmp, texto, "utf8");
  try {
    await fsp.copyFile(arquivo, arquivo + ".bak");
  } catch {}
  await fsp.rename(tmp, arquivo);
}

function responder(res, codigo, tipo, corpo) {
  res.writeHead(codigo, {
    "Content-Type": tipo,
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
  });
  res.end(corpo);
}

const servidor = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://127.0.0.1");
  const rota = decodeURIComponent(url.pathname);

  // --- API: dados (leads + estado) ---
  if (rota === "/api/dados" && req.method === "GET") {
    const leads = lerJSON(ARQ_LEADS, { leads: [] });
    const estado = lerJSON(ARQ_ESTADO, { versao: 1, leads: {} });
    return responder(
      res,
      200,
      TIPOS[".json"],
      JSON.stringify({ leads: leads.leads || leads || [], estado })
    );
  }

  // --- API: gravar estado do funil ---
  if (rota === "/api/estado" && req.method === "POST") {
    // junta os pedaços como BYTES e só depois decodifica:
    // concatenar como texto parte acento no meio quando o pedaço quebra num caractere de 2 bytes.
    const pedacos = [];
    let tamanho = 0;
    let estourou = false;
    req.on("data", (p) => {
      tamanho += p.length;
      if (tamanho > LIMITE_POST) {
        estourou = true;
        req.destroy();
        return;
      }
      pedacos.push(p);
    });
    req.on("end", async () => {
      if (estourou) return responder(res, 413, TIPOS[".json"], '{"ok":false}');
      try {
        const dados = JSON.parse(Buffer.concat(pedacos).toString("utf8"));
        if (!dados || typeof dados !== "object" || typeof dados.leads !== "object") {
          throw new Error("formato inesperado");
        }
        dados.versao = 1;
        await gravarSeguro(ARQ_ESTADO, JSON.stringify(dados, null, 2));
        responder(res, 200, TIPOS[".json"], '{"ok":true}');
      } catch (e) {
        console.error("  [erro ao gravar estado]", e.message);
        responder(res, 400, TIPOS[".json"], '{"ok":false}');
      }
    });
    return;
  }

  // --- arquivos estáticos da própria pasta ---
  if (req.method !== "GET") return responder(res, 405, "text/plain", "método não suportado");

  let alvo = rota === "/" ? "/painel.html" : rota;
  const caminho = path.join(PASTA, alvo);
  // trava de segurança: nada fora da pasta do painel
  if (!caminho.startsWith(PASTA + path.sep) && caminho !== path.join(PASTA, "painel.html")) {
    return responder(res, 403, "text/plain", "fora da pasta do painel");
  }
  try {
    const dados = await fsp.readFile(caminho);
    const tipo = TIPOS[path.extname(caminho).toLowerCase()] || "application/octet-stream";
    return responder(res, 200, tipo, dados);
  } catch {
    // dados.js só existe no modo sem servidor — 404 aqui é normal e silencioso
    return responder(res, 404, "text/plain", "não encontrado");
  }
});

function abrirNavegador(endereco) {
  try {
    if (process.platform === "win32") {
      spawn("cmd", ["/c", "start", "", endereco], { detached: true, stdio: "ignore" }).unref();
    } else if (process.platform === "darwin") {
      spawn("open", [endereco], { detached: true, stdio: "ignore" }).unref();
    } else {
      spawn("xdg-open", [endereco], { detached: true, stdio: "ignore" }).unref();
    }
  } catch {
    /* sem navegador: o endereço fica impresso no terminal */
  }
}

function subir(porta, restantes) {
  servidor.once("error", (e) => {
    if (e.code === "EADDRINUSE" && restantes > 0) return subir(porta + 1, restantes - 1);
    console.error("Não consegui subir o painel:", e.message);
    process.exit(1);
  });
  servidor.listen(porta, "127.0.0.1", () => {
    const endereco = `http://127.0.0.1:${porta}/`;
    const qtd = (lerJSON(ARQ_LEADS, { leads: [] }).leads || []).length;
    console.log("");
    console.log("  Painel de leads no ar:  " + endereco);
    console.log("  Leads carregados:       " + qtd);
    console.log("  Estado gravado em:      " + ARQ_ESTADO);
    console.log("");
    console.log("  Deixe esta janela ABERTA enquanto usa o painel.");
    console.log("  Pra fechar: clique aqui e aperte Ctrl+C.");
    console.log("");
    if (process.env.CRM_SEM_NAVEGADOR !== "1") abrirNavegador(endereco);
  });
}

subir(PORTA_INICIAL, TENTATIVAS);
