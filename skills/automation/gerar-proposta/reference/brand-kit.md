# brand-kit.md — a marca do freelancer, salva uma vez e reusada

> A freelancer sends 5-20 proposals/month. The brand kit makes every proposal after the first
> instant and consistent (same logo, colors, contact, Pix key). It lives at the project root so
> it persists across sessions and proposals.

## Onde fica
`.claude/brand-kit-freelancer.md` (na raiz do projeto do usuário). É um arquivo simples com
frontmatter YAML. A skill lê no Step 2 e reusa em silêncio.

## Formato (schema)
```markdown
---
nome: "João da Silva"                  # nome de quem assina
empresa: "Studio JS"                   # nome do negócio (vai na capa); pode ser igual ao nome
email: "joao@studiojs.com.br"
whatsapp: "+55 11 98888-7777"          # como o cliente fala com ele
site: "studiojs.com.br"                # opcional
logo_path: "C:/Users/joao/marca/logo.png"   # opcional; PNG/JPG/SVG. Vira base64 na capa
pix_incluir: "nao"                     # sim|nao — incluir Pix+QR nas propostas? Default NÃO (Pix é opt-in)
pix_key: "joao@studiojs.com.br"        # opcional; chave Pix pra receber (só usada se pix_incluir=sim ou o usuário pedir)
pix_key_type: "email"                  # cpf|cnpj|email|phone|evp  (evita ambiguidade do CPF×celular)
pix_nome: "JOAO DA SILVA"              # nome do recebedor no Pix (<=25, maiúsculo); default = empresa
pix_cidade: "SAO PAULO"                # cidade do recebedor no Pix (<=15)
cor_dominante: "#f8fafc"               # opcional; senão a skill escolhe pela área do cliente
cor_secundaria: "#1e293b"
cor_acento: "#2563eb"
fonte_titulo: "'Helvetica Neue', Arial, sans-serif"   # opcional
fonte_corpo: "Georgia, serif"
---

Notas livres do freelancer (tom de voz, garantia padrão, o que sempre incluir, etc.).
```
Todos os campos são opcionais menos `nome`/`empresa`. Quanto mais preenchido, mais a proposta sai
pronta sem perguntar nada.

## Como usar
1. **Existe:** Read, use logo/cores/fonte/contato/Pix em silêncio. Não anuncie "carreguei seu
   brand kit" como se fosse mágica — só use. Uma linha leve no read-back ("usei sua marca salva") basta.
2. **Não existe:** NÃO trave pedindo setup. Monte a proposta com uma paleta sugerida (escolha pela
   ÁREA do cliente — tabela em `reference/design-system.md`) e fontes default. No FIM, ofereça
   salvar: *"Quer que eu salve sua marca (nome, logo, cor, chave Pix) num arquivo? Aí toda proposta
   nova já sai com a sua cara, sem você repetir."* Se o usuário toparem, escreva o arquivo com o que
   ele tiver dado.
3. **Usuário deu cor/logo na mensagem (sem brand kit):** use na hora e ofereça persistir.

## Sugestão de paleta quando não há marca
- Pegue o setor do CLIENTE (do serviço/dossiê) → use a linha correspondente da tabela de paletas
  em `reference/design-system.md`. Ex.: proposta de site pra clínica de estética → paleta saúde
  (verde profundo + acento verde). Proposta de tráfego pra loja → paleta tech (azul) ou a default.
- Diga em uma linha qual paleta você escolheu e por quê ("usei uma paleta sóbria de saúde porque o
  cliente é da estética; se quiser outra cor, me fala"). O usuário pode trocar com uma frase.
- Nunca use a forbid list (`reference/design-system.md`): nada de roxo-gradiente/arco-íris.

## Privacidade
O brand kit (e os dados do cliente) ficam só na máquina — a skill é offline. Vale dizer isso se o
usuário hesitar em salvar chave Pix/contato.
