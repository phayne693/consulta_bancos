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

login = '36418486870_000148'
password = 'Loja6868*'
def robo_c6_consulta(cpf):
    try:
        navegador = webdriver.Chrome(service=page, options=opt)
        navegador.get('https://c6.c6consig.com.br/')
        time.sleep(3)
        #inserir login
        usuario = navegador.find_element(By.XPATH, '//*[@id="EUsuario_CAMPO"]')
        usuario.send_keys(login)
        #inserir senha
        senha = navegador.find_element(By.XPATH, '//*[@id="ESenha_CAMPO"]')
        senha.send_keys(password)
        time.sleep(3)
        #entrar
        entrar = navegador.find_element(By.XPATH, '//*[@id="lnkEntrar"]')
        entrar.click()
        #aceita dialogo
        # navegador.find_element(By.LINK_TEXT,'Usuário já autenticado em outra estação. Deseja desconectar-se da estação e conectar-se através desta?').click()
        # Wait for the alert to be displayed and store it in a variable
        alert = WebDriverWait(navegador, 2).until(
            EC.alert_is_present()
        )
        alert.accept()
        return {'success': True}
    except WebDriverException as e:
        navegador.quit()
        return {'error': str(e)}
