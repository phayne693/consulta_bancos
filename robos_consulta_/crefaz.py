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


def crefaz_consulta(cpf):
    try:
        navegador = webdriver.Chrome(service=page, options=opt)
        navegador.get('https://crefazon.com.br/login')
        time.sleep(3)
        #insere login
        login = navegador.find_element(By.XPATH, '//*[@id="wrapper"]/div/div/div[2]/div/form/div[1]/div[2]/div/div/input')
        login.send_keys("CC030112836")
        #insere senha
        senha = navegador.find_element(By.XPATH, '//*[@id="wrapper"]/div/div/div[2]/div/form/div[2]/div[2]/div/div/input')
        senha.send_keys("DGD@IKDNJG")
        #entrar
        entrar  = navegador.find_element(By.XPATH, '//*[@id="wrapper"]/div/div/div[2]/div/form/button')
        entrar.click()
    
        input('teste')
    except WebDriverException as e:
        #caso de erro logout antes de fechar o navegador
        sair = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[1]/nav/ul/li/a/button')
        sair.click()
        time.sleep(3)
        navegador.quit()
        return {'error': str(e)}

if __name__ == '__main__':
    crefaz_consulta(cpf='43996081880')