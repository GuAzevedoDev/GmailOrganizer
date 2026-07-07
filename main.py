from services.service_gmail import ProcessaEmailsService,ClassificadorService
from repositories.gmail_repository import GmailInfra

def main():

  print("========Iniciando automação========")

  #Instanciar infra
  repo_infra = GmailInfra()

  #Instanciar classificador
  repo_classificador = ClassificadorService()

  #Instanciar service
  repo_service = ProcessaEmailsService(repo_infra = repo_infra,repo_classificador = repo_classificador)

  #Executar automação
  repo_service.executar()

  print("========Automação finalizada========")
  
if __name__ == '__main__':
  main()