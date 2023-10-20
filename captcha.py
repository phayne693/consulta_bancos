import requests
import time

def resolver_captcha_v2(api_key, sitekey_v2, url):
    # Enviar uma solicitação para criar um trabalho de resolução de reCAPTCHA
    response = requests.post(
        f'http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={sitekey_v2}&json=1&pageurl={url}&here=now'
    )
    
    result = response.json()
    
    if result['status'] == 1:
        captcha_id = result['request']
        
        # Aguardar até que o reCAPTCHA seja resolvido
        while True:
            response = requests.get(
                f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
            )
            result = response.json()
            if result['status'] == 1:
                # O reCAPTCHA foi resolvido com sucesso
                captcha_solution = result['request']
                return captcha_solution
            elif result['request'] == 'CAPCHA_NOT_READY':
                # O reCAPTCHA ainda não foi resolvido, aguarde um pouco e tente novamente
                time.sleep(5)
            else:
                # Algo deu errado
                print('Erro ao resolver o reCAPTCHA')
                return None
    else:
        # Algo deu errado ao criar o trabalho de resolução
        print('Erro ao criar o trabalho de resolução do reCAPTCHA')
        return None
    
def resolver_captcha_v3(api_key, sitekey_v3, url):
    # Enviar uma solicitação para criar um trabalho de resolução de reCAPTCHA
    response = requests.post(
        f'http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={sitekey_v3}&json=1&pageurl={url}&here=now'
    )
    
    result = response.json()
    
    if result['status'] == 1:
        captcha_id = result['request']
        
        # Aguardar até que o reCAPTCHA seja resolvido
        while True:
            response = requests.get(
                f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
            )
            result = response.json()
            if result['status'] == 1:
                # O reCAPTCHA foi resolvido com sucesso
                captcha_solution = result['request']
                return captcha_solution
            elif result['request'] == 'CAPCHA_NOT_READY':
                # O reCAPTCHA ainda não foi resolvido, aguarde um pouco e tente novamente
                time.sleep(5)
            else:
                # Algo deu errado
                print('Erro ao resolver o reCAPTCHA')
                return None
    else:
        # Algo deu errado ao criar o trabalho de resolução
        print('Erro ao criar o trabalho de resolução do reCAPTCHA')
        return None
    
    
def resolver_captcha_token(api_key, site_key_token, url):
    # Enviar uma solicitação para criar um trabalho de resolução de reCAPTCHA
    response = requests.post(
        f'http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key_token}&json=1&pageurl={url}&here=now'
    )
    
    result = response.json()
    
    if result['status'] == 1:
        captcha_id = result['request']
        
        # Aguardar até que o reCAPTCHA seja resolvido
        while True:
            response = requests.get(
                f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
            )
            result = response.json()
            if result['status'] == 1:
                # O reCAPTCHA foi resolvido com sucesso
                captcha_solution = result['request']
                return captcha_solution
            elif result['request'] == 'CAPCHA_NOT_READY':
                # O reCAPTCHA ainda não foi resolvido, aguarde um pouco e tente novamente
                time.sleep(5)
            else:
                # Algo deu errado
                print('Erro ao resolver o reCAPTCHA')
                return None
    else:
        # Algo deu errado ao criar o trabalho de resolução
        print('Erro ao criar o trabalho de resolução do reCAPTCHA')
        return None

def validar_recaptcha(chave_secreta, captcha_solution):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": chave_secreta,
        "response": captcha_solution
    }
    response = requests.post(url, data=payload)
    resultado = response.json()
    return resultado