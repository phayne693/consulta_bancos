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


def robo_master_consulta(cpf):
    try:
        navegador = webdriver.Chrome(service=page, options=opt)
        navegador.get('https://autenticacao.bancomaster.com.br')
        time.sleep(3)
        #login
        login = navegador.find_element(By.XPATH, '//*[@id="mat-input-0"]')
        login.send_keys('FERNANDO.GIARINI35')
        #senha
        senha = navegador.find_element(By.XPATH, '//*[@id="mat-input-1"]')
        senha.send_keys('Loja7070*')
        senha.send_keys(Keys.TAB)
        entrar = navegador.find_element(By.XPATH, '/html/body/app-root/app-login/div/div[2]/mat-card/mat-card-content/form/div[3]/button[2]')
        entrar.click()
    except WebDriverException as e:
        navegador.quit()
        return {'error': str(e)}
