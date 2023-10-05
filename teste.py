import requests

url = 'https://www.google.com/recaptcha/enterprise/payload?p=06AFcWeA5QP-u6H2sZodkI23clpjRoHTwJysbShRGhAg5exSwWVHgxGcbEgb3Tih1CfBJWzBDdgQHrcvI3H_OVwbSXIkDoETx_BsGdSjDy-kugYGqewhC6eMxcwni9NZrnPri-ktHgB6-EJaoKICeAw96ugmy2nPHrnLIEI9cot3xBuos2brvMTFvzQNxa_qRMb0H4JgzaaV5vb6ZtMo3e3EXrQQi--hip0ZBFY443DB_VrXQ-zv0_4hI&k=6Lel6a0kAAAAACKcMiiuNJ1_kgRQl5Ec7imnWsrE'

def get_cookie(url):
    # Envia uma solicitação HEAD para obter apenas os cabeçalhos, incluindo os cookies
    response = requests.head(url)
    
    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Obtém os cookies do cabeçalho da resposta
        cookies = response.payload
        return cookies
    else:
        return None

cookies = get_cookie(url)
if cookies:
    print("Cookies obtidos com sucesso:", cookies)
else:
    print("Não foi possível obter os cookies.")
