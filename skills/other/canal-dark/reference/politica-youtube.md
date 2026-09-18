# politica-youtube.md — o que a skill pode prometer e o que ela é OBRIGADA a avisar

Este é o documento mais importante pra honestidade do produto. A skill MONTA o vídeo; ela não
garante monetização. E a política do YouTube descreve, com essas palavras, o output PADRÃO de
um pipeline de canal dark como NÃO monetizável. Por isso a skill exige o ângulo do usuário e
recusa alguns pedidos. Nada aqui promete renda.

## §angle — por que a tese do usuário BLOQUEIA a geração (Stage 2)

O que NÃO monetiza, verbatim (política de conteúdo inautêntico, atualizada em 15/07/2025):
"AI-generated content made with generic or unoriginal templates giving the impression of mass
production without adding the creator's original, authentic insights or perspective"
(https://support.google.com/youtube/answer/1311392).

O que MONETIZA (o caminho de saída), verbatim: "If you use automated tools or templates to help
create your content, the final product must still demonstrate your creative vision" e "the
substance of each video should be materially varied and deliver creative, educational, or other
value" (mesma fonte).

Tradução pra skill: IA não é o problema. O VP de Trust & Safety do YouTube, verbatim: "we're
agnostic to what any tools that are used to create the content... our policies are independent of
how the content is made" (https://www.youtube.com/watch?v=14Vm0CiyUVE). O problema é molde sem
ponto de vista. É por isso que, sem a tese do usuário, a skill não gera: o canal nasceria
demonetizado. A tese entra em ≥2 blocos, com as palavras dele.

CAMINHO DE SAÍDA (não trave quem não tem a tese na ponta da língua): se o usuário disser "faz do
jeito melhor", NÃO bloqueie de cara. Ajude a extrair um ângulo com 2–3 perguntas: "o que te
chamou atenção nesse assunto?", "qual opinião sua sobre isso a maioria discordaria?", "o que quase
todo mundo entende errado aqui?". Use os dados de demanda do Stage 1 pra sugerir ângulos concretos
(ex: "o outlier que medi foca em X — sua visão sobre X seria...?"). Só depois de tentar isso, se
ainda não sair nada original, você para. O bloqueio é o último recurso, não o primeiro.

## §recusas — o que a skill se recusa a fazer (bloqueia e explica com o link)

1. PERSONA DE IA em tema sensível. Verbatim: canais que usam "AI-generated personas to deliver
   information on sensitive topics... on topics such as health, legal issues, finances, or
   politics... will not be allowed to monetize" (mesma fonte 1311392). Exemplos oficiais: "An
   AI 'doctor' providing medical diagnoses", "AI-generated podcast hosts offering financial
   guidance, investment tips". São os nichos de maior CPM — e é por isso que a skill barra:
   deixar passar é entregar um canal que nasce desmonetizado. Ofereça a alternativa (narrar um
   CASO real de fraude financeira em vez de dar conselho de investimento, por exemplo).
   [CONFERIR] reconferir o texto exato dessa seção na página oficial antes de citar ao usuário.
2. SLIDESHOW de imagem sem narrativa. Verbatim na lista do que não monetiza: "Image slideshows,
   templated storylines, or scrolling text with minimal or no narrative".
3. LOTE. "gera 20 vídeos desse template" — recuse. As Diretrizes da Comunidade (que geram
   STRIKE, não só desmonetização) proíbem "Automated or synthetic mass-production: Using
   automated tools or AI to churn out high volumes of similar content with minimal changes"
   (https://support.google.com/youtube/answer/2801973). Um vídeo por vez, com variação forçada.
4. LEITURA de material de terceiro (Reddit, Wikipédia, notícia) sem camada própria. Verbatim:
   "Content that exclusively features readings of other materials you did not originally create"
   (política de conteúdo reutilizado). Reescreva com ângulo próprio, não leia na íntegra.
5. SUBIR no YouTube — a skill não faz (motivo técnico abaixo).
6. BAIXAR música — a skill não faz (Content ID; o usuário põe o mp3 na mão).
7. RASPAR o Pexels pra fugir da chave — proibido nos Termos do Pexels.

## §sensivel — temas sensíveis (gera, mas AVISA; não é recusa)

True crime, tragédia, violência, acidente, qualquer pessoa/evento real. Nicho dark legítimo e
comum — a skill gera, mas avisa ANTES, senão o usuário se frustra ou toma restrição:
1. A mídia é b-roll GENÉRICO do Pexels, nunca imagem real da cena do crime, da vítima ou do
   evento. A skill não busca nem consegue imagem real — diga isso na cara pra não criar
   expectativa falsa. Se o usuário precisa das imagens reais, ele traz e põe em `03-clipes/`
   (e a responsabilidade de direito de uso passa a ser dele).
2. Tema gráfico/chocante cai em restrição de anunciante (anúncio limitado ou nenhum), verbatim:
   conteúdo "shocking content... violence" entra em "limited or no ads"
   (https://support.google.com/youtube/answer/6162278). Não é desmonetização do canal, é menos
   anúncio naquele vídeo. Avise, não recuse.
3. Reconstituição REALISTA de algo que não aconteceu exige o rótulo de conteúdo sintético (ver
   §disclosure).
4. VETO DE ROSTO: o `midia.py` não deixa passar rosto identificável em contexto de crime/acusação
   — a licença do Pexels proíbe pessoa real aparecer "in a bad light". A skill mantém isso por
   padrão; não afrouxe.

## §disclosure — o rótulo de conteúdo alterado ou sintético (no PUBLICAR.txt)

A skill DECIDE e escreve o motivo. Fonte: https://support.google.com/youtube/answer/14328491.
NÃO precisa marcar quando: roteiro por IA, título por IA, thumbnail por IA, legenda gerada,
clonagem da PRÓPRIA voz. Verbatim da isenção: "Production assistance, like using generative AI
tools to create or improve a video outline, script, thumbnail, title, or infographic".
PRECISA marcar quando: cena realista de lugar/evento/pessoa real que não aconteceu, e música
gerada por IA.
[AMARELO] Narração TTS de narrador fictício (não clonada de pessoa real) não aparece em nenhuma
das duas listas — zona cinzenta. A skill diz isso e recomenda não marcar, deixando a decisão
com o usuário.
Alívio a informar, verbatim: "Disclosing AI content won't limit a video's audience or impact its
eligibility to earn money".

## §upload — por que a skill NÃO sobe no YouTube

Não é a cota (que mudou; blog que fala em "1600 unidades" está desatualizado). O bloqueio é
fatal, verbatim: "All videos uploaded via the videos.insert endpoint from unverified API
projects created after 28 July 2020 will be restricted to private viewing mode. To lift this
restriction, each API project must undergo an audit"
(https://developers.google.com/youtube/v3/docs/videos/insert). E o refresh token de projeto em
modo Testing expira em 7 dias. Pra um público leigo, isso é um campo minado. A skill entrega o
arquivo + o `PUBLICAR.txt`; o usuário arrasta no YouTube Studio (publica público na hora, sem
projeto no Google Cloud). Avise o limite de canal novo: sem verificação por telefone, só vídeo
de até 15 min (https://support.google.com/youtube/answer/71673).

## §ypp — entrar no Programa de Parceiros (informar sem prometer)

Verbatim: "Get 1,000 subscribers with 4,000 valid public watch hours in the last 12 months, or
1,000 subscribers with 10 million valid public Shorts views in the last 90 days"
(https://support.google.com/youtube/answer/72851). Bater a meta NÃO garante aprovação (há
revisão, ~1 mês). NÃO existe número público de quanto tempo até monetizar; qualquer número que
apareça em blog é invenção. NÃO cite RPM/CPM por nicho: as tabelas que circulam são de
fornecedor de software, sem metodologia.

## §copy — o que você NÃO pode prometer sobre o canal

Vale pro que a skill fala com o usuário e pro que o usuário for divulgar sobre o próprio canal
(se ele vender serviço de edição, por exemplo). Nunca dizer: "canal automático que monetiza",
"aprovado pelo YouTube" (não existe aprovação prévia), nem qualquer número de renda/RPM. A
formulação honesta: IA não é proibida; template genérico e produção em massa sem insight
próprio são. Fale do que a ferramenta FAZ, nunca do que a pessoa vai GANHAR.
