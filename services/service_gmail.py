from repositories.gmail_repository import GmailInfra

class ClassificadorService:

  def gera_chaves(self) -> dict:
    LABELS = {
      "CURRICULO": [
          "curriculo",
          "resume",
          "vaga",
          "entrevista",
          "processo seletivo",
          "gupy",
          "linkedin",
          "candidato"
      ],
      "COMPRAS": [
          "pedido",
          "compra",
          "nota fiscal",
          "rastreamento",
          "entrega",
          "mercado livre",
          "amazon",
          "shopee"
      ],
      "BANCOS": [
          "pix",
          "transferência",
          "saldo",
          "extrato",
          "nubank",
          "inter",
          "itau"
      ]
    }
    return LABELS

  def classificar_label(corpo_gmail,LABELS) -> str:
    pontuacao_labels = {}

    #Percorrer as palavras das labels que classificam
    for chave,palavras_labels in LABELS.items():
      for palavra_label in palavras_labels:

        #Se a palavra chave de alguma label tiver no corpo do gmail
        if palavra_label in corpo_gmail:

          #Adiciono +1 a chave na pontuação
          pontuacao_labels[chave] = pontuacao_labels.get(chave, 0) + 1

    if not pontuacao_labels:
        print(f"Nao foi encontrado nenhuma label para esse gmail {corpo_gmail}")
        return

    maior_valor = max(pontuacao_labels.values())
    vencedores = []

    for nome_label,pontos in pontuacao_labels.items():
      if maior_valor == pontos:
        vencedores.append(nome_label)

    # id_label = labels_gmail.get(vencedores[0])
    # Retornar apenas o nome limpo da label
    return vencedores[0]

  

class ProcessaEmailsService:
  def __init__(self,repo_infra,repo_mensagem):
    self.repo_infra = repo_infra
    self.repo_mensagem = repo_mensagem

  def executar(self):
    LABELS = self.repo_label.gera_chaves()
    ids_gmails = self.repo_infra.listar_gmails_ids()
    labels_gmail = self.repo_infra.service.listar_labels()

    for id_gmail in ids_gmails:
      corpo_gmail = self.repo_infra.pegar_corpo_mensagem(id_gmail)
      label_indicada = classificar_label(corpo_gmail,LABELS)
      repo_infra.alterar_label()
