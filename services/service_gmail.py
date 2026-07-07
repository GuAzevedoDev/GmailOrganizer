class EmailError(Exception):
  pass

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

  def classificar_label(self,corpo_gmail:str,LABELS:dict) -> str | None:
    pontuacao_labels = {}

    #Percorrer as palavras das labels que classificam
    for chave,palavras_labels in LABELS.items():
      for palavra_label in palavras_labels:

        #Se a palavra chave de alguma label tiver no corpo do gmail
        if palavra_label in corpo_gmail:

          #Adiciono +1 a chave na pontuação
          pontuacao_labels[chave] = pontuacao_labels.get(chave, 0) + 1

    if not pontuacao_labels:
        print(f"Nao foi encontrado nenhuma label para esse gmail")
        return

    maior_valor = max(pontuacao_labels.values())
    vencedores = []

    for nome_label,pontos in pontuacao_labels.items():
      if maior_valor == pontos:
        vencedores.append(nome_label)

    # Retornar apenas o nome limpo da label
    return vencedores[0]

  

class ProcessaEmailsService:
  def __init__(self,repo_infra:object,repo_classificador:object):
    self.repo_infra = repo_infra
    self.repo_classificador = repo_classificador

  def executar(self):
    LABELS = self.repo_classificador.gera_chaves()
    ids_gmails = self.repo_infra.listar_gmails_ids()
    labels_gmail = self.repo_infra.listar_labels()

    for id_gmail in ids_gmails:
      #Traz o corpo
      corpo_gmail = self.repo_infra.pegar_corpo_gmail(id_gmail)

      #Traz o nome da label indicada
      label_indicada = self.repo_classificador.classificar_label(corpo_gmail,LABELS)

      if label_indicada is None:
        continue

      #Pega o id da label indicada
      id_label = labels_gmail.get(label_indicada)

      #Altera para label indicada
      self.repo_infra.alterar_label(id_gmail,id_label)

      print(f"Email enviado para label {label_indicada}")


