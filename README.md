# Gmail Organizer

Automação em Python que lê a caixa de entrada pela API do Gmail, classifica cada e-mail por palavras-chave e aplica a label correspondente — sem interface, roda pelo terminal.

```
========Iniciando automação========
Email enviado para label CURRICULO
Email enviado para label COMPRAS
Nao foi encontrado nenhuma label para esse gmail
Email enviado para label BANCOS
========Automação finalizada========
```

## O que ele faz

A cada execução:

1. autentica na conta pelo OAuth 2.0 (escopo `gmail.modify`);
2. lista os **10 e-mails mais recentes** da caixa de entrada, ignorando a lixeira;
3. lê o corpo de cada um (texto puro quando existe, HTML como alternativa);
4. pontua esse corpo contra as palavras-chave de cada label;
5. aplica no e-mail a label de maior pontuação.

A label é **adicionada** ao e-mail — ele continua na caixa de entrada, agora marcado. O script não arquiva, não move para a lixeira e não apaga nada.

## Como a classificação funciona

Cada label tem uma lista de termos, definida em `ClassificadorService.gera_chaves()`:

| Label | Termos |
|---|---|
| `CURRICULO` | curriculo, resume, vaga, entrevista, processo seletivo, gupy, linkedin, candidato |
| `COMPRAS` | pedido, compra, nota fiscal, rastreamento, entrega, mercado livre, amazon, shopee |
| `BANCOS` | pix, transferência, saldo, extrato, nubank, inter, itau |

Cada termo encontrado no corpo vale um ponto. Ganha a label com mais pontos; em caso de empate fica a primeira encontrada, e com zero ponto o e-mail não é tocado.

Para mudar as categorias, basta editar esse dicionário — nada mais no código depende dele.

## Arquitetura

Quatro camadas, uma responsabilidade cada:

```
main.py                         monta as peças e injeta as dependências
└── services/service_gmail.py
    ├── ProcessaEmailsService   orquestra o fluxo
    └── ClassificadorService    decide a label (não conhece a API)
└── repositories/gmail_repository.py
    ├── AutenticacaoGmail       OAuth e cache do token
    └── GmailInfra              chamadas à API do Gmail
```

O `main.py` recebe as instâncias prontas e as injeta no service, então trocar o classificador — ou a fonte dos e-mails — não encosta no resto do código. As falhas de rede da API são convertidas em `ConexaoError` com mensagem própria, em vez de vazar o `HttpError` cru do Google.

## Pré-requisitos

- Python 3.10 ou superior (o classificador usa a sintaxe `str | None`)
- Uma conta Google
- Um projeto no [Google Cloud Console](https://console.cloud.google.com/) com a **Gmail API** habilitada
- As labels `CURRICULO`, `COMPRAS` e `BANCOS` **já criadas no Gmail** — o script procura pelo nome e usa o id correspondente; ele não cria labels

## Configuração

### 1. Credenciais do Google

1. No Google Cloud Console, crie um projeto e habilite a **Gmail API**.
2. Em *Credenciais*, crie uma credencial do tipo **ID do cliente OAuth** → **App para computador**.
3. Baixe o JSON e salve como `credentials.json` na raiz do projeto.
4. Enquanto o app estiver em modo de teste, adicione sua conta em *Usuários de teste* na tela de consentimento.

### 2. Ambiente

```bash
git clone https://github.com/GuAzevedoDev/GmailOrganizer.git
cd GmailOrganizer

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Execução

```bash
python main.py
```

Na primeira vez o navegador abre para você autorizar o acesso. O token fica salvo em `token.pickle` e nas execuções seguintes ele só é renovado — o consentimento não se repete.

## Segurança

`credentials.json` e `token.pickle` dão acesso de leitura e escrita à sua conta de e-mail. Os dois estão no `.gitignore` e **nunca devem ser commitados**. Se um deles vazar, revogue o acesso em [myaccount.google.com/permissions](https://myaccount.google.com/permissions) e gere credenciais novas.

O escopo pedido é `gmail.modify`: permite ler mensagens e alterar labels, mas não permite excluir a conta nem apagar mensagens permanentemente.

## Limitações conhecidas

- **Processa 10 e-mails por execução** (`maxResults` fixo em `GmailInfra.listar_gmails_ids`), sem paginação.
- **A comparação diferencia maiúsculas de minúsculas**: um corpo escrito "Pix aprovado" não casa com o termo `pix`.
- **A busca é por substring**, então `inter` também casa dentro de "internet" e `entrega` dentro de "entregar" — o que gera falso positivo em alguns e-mails.
- **Não há reprocessamento**: e-mails já classificados numa execução anterior entram na contagem de novo se ainda estiverem entre os 10 mais recentes.
- As labels precisam existir antes; se uma delas não existir no Gmail, a chamada de atualização falha.

## Estrutura

```
.
├── main.py
├── requirements.txt
├── repositories/
│   └── gmail_repository.py
└── services/
    └── service_gmail.py
```
