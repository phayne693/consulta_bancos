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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import os
import glob
from selenium.common.exceptions import WebDriverException
import requests
from selenium.webdriver.common.alert import Alert
import undetected_chromedriver as uc
import json

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
        #move ate o elemento
        cadastro = navegador.find_element(By.XPATH,'//*[@id="navbar-collapse-funcao"]/ul/li[1]/a')
        ActionChains(navegador).move_to_element(cadastro).perform()
        #seleciona FGTS
        fgts = navegador.find_element(By.XPATH, '//*[@id="WFP2010_MPCDPRDB2CCP"]')
        fgts.click()
        # #insere CPF
        insere_cpf = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj2_UcDBasicos_UcDBasic1_txtCpfCnpj_CAMPO"]')
        insere_cpf.send_keys(cpf)
        #press TAB para carregar nome
        insere_cpf.send_keys(Keys.TAB)
        time.sleep(2)
        #verifica se precisa inserir nome e data nasc
        def aguarde_visivel():
            aguarde = navegador.find_element(By.XPATH,'//*[@id="ctl00_UpdPrs"]')
            return aguarde
        try:
            elemento_aguarde = aguarde_visivel()
            if elemento_aguarde.is_displayed:
                wait = WebDriverWait(navegador,10)
                wait.until_not(EC.visibility_of(elemento_aguarde))
                # print('passei if')
            else:
                #insere nome
                nome = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj2_UcDBasicos_UcDBasic1_txtNome_CAMPO"]')
                nome.send_keys('TESTE')
                #insere data nasc
                nascimento = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj2_UcDBasicos_UcDBasic1_txtDtNasc_CAMPO"]')
                nascimento.send_keys('10/02/1950')
                # print('passei else')
        except WebDriverException as e:
            return {'error': str(e)}
        #confirmas
        confirmar = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj3_UcConfCanVlt_btnConfirmar_dvCBtn"]')
        confirmar.click()
        time.sleep(10)
        # Espere até que a animação "Aguarde" não seja mais visível
        wait = WebDriverWait(navegador, 10)
        wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_UpdPrs"]')))
        # funcao para esperar a tabela
        def esperar_tabela():
            while True:
                try:
                    #obter saldo
                    obt_saldo = navegador.find_element(By.XPATH, '//*[@id="btnObterSaldo_txt"]')
                    obt_saldo.click()
                    # espera a tabela ser visivel
                    wait = WebDriverWait(navegador, 10)
                    tabela = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cph_FJ1_JPCSFGTS_UcConsultaSaldoFGTS_grdResultadoSaque"]')))
                    break
                except TimeoutException:
                    #alerta JS
                    try:
                        alert = navegador.switch_to.alert
                        alert.accept()
                    except NoAlertPresentException:
                        pass
        esperar_tabela()

        #insere tabela 0008
        tabela_008 = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_FJ1_JP2_UCTFAV2_txtCODTAB_CAMPO"]')
        tabela_008.send_keys('0008')
        time.sleep(1)
        tabela_008.send_keys(Keys.TAB)
        time.sleep(3)
        #simular por
        # select = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_FJ1_JP2_UCTFAV2_cboSimularPor_CAMPO"]')
        # valor = select.find_elements(By.TAG_NAME, 'option')
        # print(valor)
        # for options in valor:
        #     if options == 'T':
        #         options.click()
        select = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_FJ1_JP2_UCTFAV2_cboSimularPor_CAMPO"]')
        seletor = Select(select)
        #selecionar a opcao com T
        seletor.select_by_value('T')
        #calcular
        time.sleep(2)
        calcular = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_FJ1_JP2_UCTFAV2_btnCalcular_dvCBtn"]')
        calcular.click()
        # Espere até que a animação "Aguarde" não seja mais visível
        wait = WebDriverWait(navegador, 10)
        wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_UpdPrs"]')))
        time.sleep(5)
        # #pega os dados necessarios
        valor_total = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_FJ1_JP2_UCTFAV2_UCDG_GDDSP_ctl12_L3"]')
        valor_total = valor_total.text
        # resumo = {
        #     'valor_total': valor_total
        # }
        # #converte o dicionario em json
        # retorno_json = json.dumps({'resumo': resumo})
        # print(retorno_json)
        navegador.quit()
        return {'success': True, 'valor_total': valor_total }
    except WebDriverException as e:
        navegador.quit()
        return {'error': str(e)}
