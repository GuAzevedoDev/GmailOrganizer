dados = {
    "mimeType": "multipart/mixed",
    "parts": [
        {
            "mimeType": "image/png"
        },
        {
            "mimeType": "multipart/alternative",
            "parts": [
                {
                    "mimeType": "text/plain",
                    "body": "Olá, este é o corpo do e-mail."
                },
                {
                    "mimeType": "text/html",
                    "body": "<p>Olá</p>"
                }
            ]
        },
        {
            "mimeType": "application/pdf"
        }
    ]
}
lista_total = {}


def pega_mime(pai):
  if pai["mimeType"] == 'text/plain':
    plain_texto = pai['body']["data"]
    return plain_texto
  
  if pai["mimeType"] == 'text/html':
    html_texto = pai['body']["data"]

  if "parts" in pai:
    for filho in pai["parts"]:
      resultado = pega_mime(filho)
      if resultado != None:
        return resultado
      
    if resultado is None and html_texto:
        return html_texto

  


pega_mime(dados)