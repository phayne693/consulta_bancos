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
import re

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
options.headless = True
options.add_argument("--headless")
options.add_experimental_option("prefs", {
    "donwload.default.directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"
})
prefs = {"download.default_directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"}
opt = webdriver.ChromeOptions()
opt.add_experimental_option("prefs", prefs)


def crefaz_consulta(cpf, nome, nascimento, telefone, cep):
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
        time.sleep(5)
        entrar  = navegador.find_element(By.XPATH, '//*[@id="wrapper"]/div/div/div[2]/div/form/button')
        entrar.click()
        try:
            promocao = WebDriverWait(navegador,10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/button'))
            )
            promocao.click()
        except WebDriverException as e:
            print('Fim da promocao')
        #clica menu credito
        time.sleep(5)
        credito = WebDriverWait(navegador,10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="side-menu"]/ul[2]/li'))
        )
        # credito.click()
        ActionChains(navegador).move_to_element(credito).click().perform()
        #proposta
        proposta = navegador.find_element(By.XPATH, '//*[@id="side-menu"]/ul[2]/li/ul/li/a')
        ActionChains(navegador).move_to_element(proposta).click().perform()
        ActionChains(navegador).move_to_element(proposta).click().perform()
        # # #nova proposta
        nova_proposta = navegador.find_element(By.XPATH, '//*[@id="side-menu"]/ul[2]/li/ul/li/ul/li[1]/a')
        ActionChains(navegador).move_to_element(nova_proposta).click().perform()
        # ActionChains(navegador).move_to_element(nova_proposta).click().perform()
        #cpf
        cpf_cli = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div/div[2]/form/div[1]/div[1]/div/div[2]/div/div/input'))
        )
        cpf_cli.send_keys(cpf)#76941590653
        cpf_cli.send_keys(Keys.TAB)
        time.sleep(5)
        #se cpf já foi consultado
        try:
            alerta = WebDriverWait(navegador,10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div')))
            text = alerta.get_attribute('textContent')
            limpar_texto = text.replace('\n', '').strip().replace('OK','').strip()
            if limpar_texto == 'Você tem uma proposta em andamento para esse cliente, verifique em sua esteira de acompanhamento':
                confirmar = navegador.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/button')
                confirmar.click()
                time.sleep(3)
                # #teste para pegar o resultado
                # pesquisar = WebDriverWait(navegador, 10).until(
                #     EC.presence_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div[1]/div[2]/div/div/form/div/div[2]/div/button[1]'))
                # )
                # pesquisar.click()
                # time.sleep(3)
                # off = WebDriverWait(navegador, 10).until(
                #     EC.presence_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/div/table/tbody/tr[6]/td[1]/div/a/div[2]'))
                # )
                # off.click()
                # time.sleep(3)
                # #segue para pegar o que estiver disponivel
                # oferta = WebDriverWait(navegador, 10).until(
                #     EC.presence_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div/div'))
                # )
                # of_text = oferta.get_attribute('textContent')
                # # print(of_text)
                # #separa a frase
                # partes = of_text.split('R$')
                # if len(partes) > 1:
                #     palavra = partes[0].strip()
                #     print(palavra)
                #     numeros = re.findall(r'-?\d+\.\d+', partes[1])
                #     if numeros:
                #         valor = numeros[0].strip('[]\'')
                #         print(valor)
                #     else:
                #         print("Valor não encontrado na frase.")
                # else:
                #     print('Não foi possível separar a string')
                
                #logout
                sair = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[1]/nav/ul/li/a/button')
                sair.click()
                time.sleep(3)
                navegador.quit()
                # print(limpar_texto)
                return {limpar_texto}
            else:
                print(text)
        except WebDriverException as e:
            print(str(e))
        #nome
        nome_cli = WebDriverWait(navegador,10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div/div[2]/form/div[1]/div[2]/div/div[2]/div/div/input'))
        )
        nome_cli.send_keys(nome)#IVANDERLEI MENDES SILVA
        #nascimento
        nascimento_cli = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div/div[2]/form/div[2]/div[1]/div/div[2]/div/div/div/div/input')
        nascimento_cli.click()
        time.sleep(4)
        nascimento_cli.send_keys(nascimento)#16/04/1973
        #telefone
        telefone_cli = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div/div[2]/form/div[2]/div[2]/div/div[2]/div/div/input')        
        telefone_cli.send_keys(telefone)#38991915624
        #profissao
        profissao = navegador.find_element(By.XPATH, '//*[@id="rc_select_0"]')
        ActionChains(navegador).move_to_element(profissao).click().perform()
        profissao.send_keys('Assalariado')
        profissao.send_keys(Keys.TAB)
        #cep
        cep_cli = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div/div[2]/form/div[3]/div[1]/div/div[2]/div/div/input')
        cep_cli.send_keys(cep)#39520000
        cep_cli.send_keys(Keys.TAB)
        #avancar
        time.sleep(5)
        avancar = WebDriverWait(navegador,10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div/div[2]/form/div[4]/button'))
        )
        avancar.click()
        time.sleep(5)#//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]
        try:
            alerta = WebDriverWait(navegador,10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div')))
            text = alerta.get_attribute('textContent')
            limpar_texto = text.replace('\n', '').strip().replace('OK','').strip()
            if limpar_texto == 'Não foi possível aprovar essa solicitação. Veja mais detalhes acessando a proposta através da lista de acompanhamento':
                confirmar = navegador.find_element(By.XPATH, '/html/body/div[5]/div/div[3]/div/button')
                confirmar.click()
                time.sleep(3)
                #logout
                sair = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[1]/nav/ul/li/a/button')
                sair.click()
                time.sleep(3)
                navegador.quit()
            else:
                print(text)
        except WebDriverException as e:
            print(str(e))
        #segue para pegar o que estiver disponivel
        oferta = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/div[2]/div[1]/div/div/div'))
        )
        of_text = oferta.get_attribute('textContent')
        #separa a frase
        partes = of_text.split('R$')
        if len(partes) > 1:
            palavra = partes[0].strip()
            print(palavra)
            numeros = re.findall(r'-?\d+\.\d+', partes[1])
            if numeros:
                valor = numeros[0].strip('[]\'')
                print(valor)
            else:
                print("Valor não encontrado na frase.")    
        else:
            print('Não foi possível separar a string')
            #caso de erro logout antes de fechar o navegador
            sair = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[1]/nav/ul/li/a/button')
            sair.click()
            time.sleep(3)
            navegador.quit()
        #retorna o valor e sai do navegador
        sair = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[1]/nav/ul/li/a/button')
        sair.click()
        time.sleep(3)
        navegador.quit()
        return {'success': True, 'produto':palavra, 'valor': valor}
        
    except WebDriverException as e:
        #caso de erro logout antes de fechar o navegador
        sair = navegador.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[1]/nav/ul/li/a/button')
        sair.click()
        time.sleep(3)
        navegador.quit()
        # return {'error': str(e)}
        print(str(e))
