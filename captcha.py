import requests
import time

def resolver_captcha():
    api_key = '97022095c1f46b1ed316fef6d5702431'
    site_url = 'https://meumb.mercantil.com.br/login'
    sitekey = '6Lel6a0kAAAAACKcMiiuNJ1_kgRQl5Ec7imnWsrE'

    response = requests.post(
        f'http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={sitekey}&json=1&pageurl={site_url}&here=now'
    )
    result = response.json()
    captcha_id = result['request']
    # print(result)
    # print(captcha_id)

    while True:
        response = requests.get(
            f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1'
        )
        result = response.json()
        if result['status'] == 1:
            # O captcha foi resolvido com sucesso
            captcha_solution = result['request']
            # print(captcha_solution)
            break
        elif result['request'] == 'CAPCHA_NOT_READY':
            # O captcha ainda não foi resolvido, aguarde um pouco e tente novamente
            time.sleep(5)
        else:
            # Algo deu errado
            print('Erro ao resolver o captcha')
            break
    return captcha_solution