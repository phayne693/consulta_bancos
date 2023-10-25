 # from more_itertools import numeric_range
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import glob
from selenium.common.exceptions import WebDriverException
import requests
from selenium.webdriver.common.alert import Alert
import undetected_chromedriver as uc
from captcha import resolver_captcha_v2
from twocaptcha import TwoCaptcha
from teste import captchaSolver

# def bevi_download():
# definindo opcoes para o navegador
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("UseAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# iniciando o servico
page = Service(ChromeDriverManager().install())
# localizacao falsa
location = '{"latitude": -23.5102, "logitude": -46.6590}'
# defininso as ocnfiguracoes do navegador
options.add_argument(f"--geolocation={location}")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_experimental_option("prefs", {
    "donwload.default.directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"
})
prefs = {"download.default_directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"}
opt = webdriver.ChromeOptions()
# opt.add_argument('--headless')
opt.add_experimental_option("prefs", prefs)


def robo_facta_consulta(cpf, api_key, sitekey_v2, url):
    try:
        navegador = webdriver.Chrome(service=page, options=opt)
        navegador.get('https://desenv.facta.com.br/sistemaNovo/login.php')
        time.sleep(3)
        #insere login
        login = navegador.find_element(By.XPATH, '//*[@id="login"]')
        login.send_keys("92415_36418486870")
        #insere senha
        senha = navegador.find_element(By.XPATH, '//*[@id="senha"]')
        senha.send_keys("Loja7070*")
        #entrar
        entrar  = navegador.find_element(By.XPATH, '//*[@id="btnLogin"]')
        entrar.click()
        time.sleep(4)
        #moce ate o icone hamburguer
        hamb = navegador.find_element(By.XPATH, '//*[@id="corpo"]/header/div/div/div/a[2]')
        ActionChains(navegador).move_to_element(hamb).click().perform()
        time.sleep(2)
        #move ate o menu lateral
        menu = navegador.find_element(By.XPATH,'//*[@id="main-nav"]/div/ul/li[2]/a')
        ActionChains(navegador).move_to_element(menu).click().perform()
        # in100 = WebDriverWait(navegador, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="main-nav"]/div/ul/li[2]/ul/li[8]'))
        # )
        # ActionChains(navegador).move_to_element(in100).click().perform()
        for i in range(5):
            menu.send_keys(Keys.TAB)
        in100 = navegador.find_element(By.XPATH,'//*[@id="main-nav"]/div/ul/li[2]/ul/li[8]/a')
        in100.send_keys(Keys.ENTER)
        #cclique consultar
        consultar = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-nav"]/div/ul/li[2]/ul/li[8]/ul/li[2]/a'))
        )
        consultar.send_keys(Keys.ENTER)
        navegador.implicitly_wait(6)
        #cpf
        documento = navegador.find_element(By.XPATH, '//*[@id="cpf"]')
        documento.click()
        documento.send_keys(cpf)
        #recaptcha
        captcha_solution_token = resolver_captcha_v2(api_key, sitekey_v2, url)
        if captcha_solution_token:
            print(f'ReCAPTCHA token resolvido com sucesso: {captcha_solution_token}')
        else:
            print('Falha ao resolver o reCAPTCHA')
        # #muda para o ifram
        # iframe_element = navegador.find_element(By.XPATH, '//*[@id="grecaptcha-beneficio"]/div/div/iframe')
        # navegador.switch_to.frame(iframe_element)
        # time.sleep(3)
        #insere token
        navegador.execute_script(
            "document.getElementById('g-recaptcha-response').innerHTML = "+"'"+captcha_solution_token+"'"
        )
        time.sleep(5)
        #consultar
        consultar = navegador.find_element(By.XPATH, '//*[@id="consultarDadosDataPrev"]')
        consultar.click()
        try:
            #pega o texto se estiver visível
            div_text = WebDriverWait(navegador, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="corpo"]/div[6]'))
            )
            div_elements = div_text.find_elements(By.TAG_NAME, 'div')
            for div_element in div_elements:
                font = div_element.find_element(By.TAG_NAME, 'font')
                text = font.get_attribute('textContent')
                #valida o texto
                if 'Cliente não possui token de autorização válido, será necessária a solicitação de autorização ao cliente.' in text:
                    #fecha o modal
                    modal = navegador.find_element(By.XPATH, '//*[@id="corpo"]/div[6]/div[2]/a')
                    modal.click()
                    #se nao houver permissao sair e fecha o browser
                    sair = navegador.find_element(By.XPATH, '//*[@id="corpo"]/header/div/div/div/div[2]/span/a')
                    sair.click()
                    time.sleep(3)
                    navegador.quit()
                    return {'success': False, 'message': text}
                elif 'Consulta realizada com sucesso!!':
                    #fecha o modal
                    modal = navegador.find_element(By.XPATH, '//*[@id="corpo"]/div[6]/div[2]/a')
                    modal.click()
                    #resultado dataprev
                    #nome
                    nome = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH,'//*[@id="resultadoDadosDataprev"]/p[1]'))
                    )
                    txt_nome = nome.get_attribute('textContent')
                    nome_cli = txt_nome.replace('Nome:', '').strip()
                    print(nome_cli)
                    #beneficio
                    beneficio = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="resultadoDadosDataprev"]/p[3]'))
                    )
                    txt_beneficio =  beneficio.get_attribute('textContent')
                    num_beneficio = txt_beneficio.replace('Nº Benefício:', '').strip()
                    print(num_beneficio)
                    #margem disponivel
                    margem_disponivel =  WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="resultadoDadosDataprev"]/p[9]'))
                    )
                    txt_margem  = margem_disponivel.get_attribute('textContent')
                    margem_disponivel = txt_margem.replace('Margem disponível:', '').strip()
                    print(margem_disponivel)
                    #margem cartao
                    margem_cartao = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="resultadoDadosDataprev"]/p[10]'))
                    )
                    txt_margem_cartao = margem_cartao.get_attribute('textContent')
                    margem_cartao = txt_margem_cartao.replace('Margem disponível do cartão:','').strip()
                    print(margem_cartao)
                    #margem rcc
                    margem_rcc = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="resultadoDadosDataprev"]/p[12]'))
                    )
                    txt_margem_rcc = margem_rcc.get_attribute('textContent')
                    margem_rcc = txt_margem_rcc.replace('Margem Disponível RCC:','').strip()
                    print(margem_rcc)
                    #fechar modal
                    fechar = navegador.find_element(By.XPATH, '//*[@id="btnModal"]')
                    fechar.click()
                    #sair apos consulta
                    sair = navegador.find_element(By.XPATH, '//*[@id="corpo"]/header/div/div/div/div[2]/span/a')
                    sair.click()
                    time.sleep(3)
                    navegador.quit()
                    #retorna as variaveis para o payload
                    resumo = {
                        'nome': nome_cli,
                        'beneficio': num_beneficio,
                        'margem_disponivel': margem_disponivel,
                        'margem_cartao': margem_cartao,
                        'margem_rcc': margem_rcc
                    }
                    return resumo
        except WebDriverException as e:
            # Aguarda até que o elemento modal desapareça
            wait = WebDriverWait(navegador, 10)
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.modal-backdrop.fade.in')))
            #caso de erro logout antes de fechar o navegador
            sair = navegador.find_element(By.XPATH, '//*[@id="corpo"]/header/div/div/div/div[2]/span/a')
            sair.click()
            time.sleep(3)
            navegador.quit()
            return {'error': str(e)}

    except WebDriverException as e:
        #caso de erro logout antes de fechar o navegador
        sair = navegador.find_element(By.XPATH, '//*[@id="corpo"]/header/div/div/div/div[2]/span/a')
        sair.click()
        time.sleep(3)
        navegador.quit()
        return {'error': str(e)}
