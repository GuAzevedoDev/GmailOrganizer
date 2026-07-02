from repositories.gmail_repository import GmailInfra

# class ClassificadorService:

#     LABELS = {
#       "CURRICULO": [
#           "curriculo",
#           "resume",
#           "vaga",
#           "entrevista",
#           "processo seletivo",
#           "gupy",
#           "linkedin",
#           "candidato"
#       ],
#       "COMPRAS": [
#           "pedido",
#           "compra",
#           "nota fiscal",
#           "rastreamento",
#           "entrega",
#           "mercado livre",
#           "amazon",
#           "shopee"
#       ],
#       "BANCOS": [
#           "pix",
#           "transferência",
#           "saldo",
#           "extrato",
#           "nubank",
#           "inter",
#           "itau"
#       ]
#     }
#     return LABELS


# class Mensagem:
  #   def gera_chaves(self) -> dict:

# class Mensagem:


class ProcessaEmailsService:
  def __init__(self,repo_infra,repo_mensagem):
    self.repo_infra = repo_infra
    self.repo_mensagem = repo_mensagem

  def executar(self):
    ids_gmails = self.repo_infra.listar_gmails_ids()

    for id_gmail in ids_gmails:
      corpo_gmail = self.repo_infra.pegar_corpo_mensagem(gmail_id)
      
      label_indicada = 