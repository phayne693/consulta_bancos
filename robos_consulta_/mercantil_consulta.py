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
from captcha import resolver_captcha

# def bevi_download():
# definindo opcoes para o navegador
options = Options()
options.add_argument('--disabel-blink-features=AutomationControlled')
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


def robo_mercantil_consulta(cpf,api_key, sitekey, url, chave_secreta):
    try:
        navegador = webdriver.Chrome(service=page, options=opt)
        navegador.get('https://meumb.mercantil.com.br/login')
        time.sleep(3)
        #inserir login
        login = navegador.find_element(By.XPATH, '//*[@id="mat-input-0"]')
        login.send_keys('LEONARDOSP11-39220')
        #senha
        senha = navegador.find_element(By.XPATH, '//*[@id="mat-input-1"]')
        senha.send_keys('8BIVg3rS')
        captcha_solution = resolver_captcha(api_key, sitekey, url)
        if captcha_solution:
            print(f'ReCAPTCHA resolvido com sucesso: {captcha_solution}')
        else:
            print('Falha ao resolver o reCAPTCHA')
        time.sleep(2)
        #inserir resultado
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
        )
        navegador.execute_script(
            "document.querySelector('#g-recaptcha-response').innerHTML = "+"'"+captcha_solution+"'"
        )
        #teste
        # Localize o elemento iframe
        iframe_element = navegador.find_element(By.XPATH, '/html/body/div[5]/div[4]/iframe')
        # Faça a troca para o iframe
        navegador.switch_to.frame(iframe_element)
        time.sleep(5)
        # border = navegador.find_element(By.XPATH, '//*[@id="recaptcha-token"]')
        WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.ID, 'recaptcha-token'))
        )
        navegador.execute_script(
            "document.querySelector('#recaptcha-token').value = "+"'"+captcha_solution+"'"
        )
        time.sleep(5)
        # Agora, para voltar ao contexto principal do navegador, use switch_to.default_content()
        navegador.switch_to.default_content()
        #segundo iframe
        iframe_click = navegador.find_element(By.XPATH, '//*[@id="recaptcha"]/div/div/iframe')
        navegador.switch_to.frame(iframe_click)
        border = navegador.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')
        border.click()
        # #clicar n sou um robo
        # recaptcha = navegador.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')
        # recaptcha.click()
        # time.sleep(3)
        entrar
        entrar = navegador.find_element(By.XPATH, '/html/body/app-root/div/app-main-layout/main/app-login/div/section[1]/div/form/div[5]/button')
        entrar.click()
    except WebDriverException as e:
        navegador.quit()
        return {'error': str(e)}