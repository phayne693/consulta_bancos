 # from more_itertools import numeric_range
import undetected_chromedriver.v2 as uc
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
from selenium.common.exceptions import WebDriverException
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



def robo_pan_consulta(cpf):
    try:
        navegador = webdriver.Chrome(service=page, options=opt)
        navegador.get('https://accounts-sso.bancopan.com.br/auth/realms/pan-parceiros/protocol/openid-connect/auth?client_id=pancred-fimenu&redirect_uri=https%3A%2F%2Fpanconsig.pansolucoes.com.br%2FFIMENU%2Fsignin-oidc&response_type=code&scope=openid%20profile&state=OpenIdConnect.AuthenticationProperties%3Djn8t_50ThQa4oe8dUk3BPTpfkZeZ9l3g6l7smGIfoHecjZaVqHfhJAPxxPkSi0vW0eMYquWb_tYxMOuZTw8O0lEp67imGB6_FDeo_wgQgW96-UtdKwjtWX57dlK5cfnq3tQMaROZKQAlfIh55NqQtZ5yoARz_mndMoj3sy8S_G_pFUKIuCkkaoPBrgC8HDqgrbH8gfIx8iWJ-QP9-Tkotw&response_mode=form_post&nonce=638332370260385487.YWZmYWQ2ZDktMjA3ZC00ZmYyLThjMDUtZGZlMWJhZDZiNTNiZmQ0NGU5NzYtNmU2Ni00MGY3LThhYWItMTZmYzYzYjExNTg1&x-client-SKU=ID_NET461&x-client-ver=5.3.0.0')
        time.sleep(3)
        #login
        login = navegador.find_element(By.XPATH, '//*[@id="cpf-input"]/label/span[2]/input')
        login.send_keys('36418486870')
        time.sleep(4)
        loader = WebDriverWait(navegador, 10).until(
            EC.invisibility_of_element_located((By.XPATH, '/mahoe-loader'))
        )
        #parceiro
        abrir_parceiro = navegador.find_element(By.XPATH, '//*[@id="form-partner-value"]')
        abrir_parceiro.click()
        #selecionar parceiro
        parceiro = navegador.find_element(By.XPATH, '//*[@id="form-partner-0"]')
        parceiro = WebDriverWait(navegador, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form-partner-0"]'))
        )
        parceiro.click()
        #entrar
        entrar = navegador.find_element(By.XPATH, '//*[@id="formulario"]/app-login-form/form/div[2]/div/mahoe-button')
        entrar.click()
    except WebDriverException as e:
        navegador.quit()
        return {'error': str(e)}