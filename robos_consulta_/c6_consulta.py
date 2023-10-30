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
from selenium.common.exceptions import StaleElementReferenceException
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
        try:
            alert = WebDriverWait(navegador, 5).until(
                EC.alert_is_present()
            )
            text = alert.text
            # print(text)
            alert.accept()
        except WebDriverException as e:
            print(str(e))
        finally:
            pass
        #move ate o elemento
        print('aqui')
        cadastro = navegador.find_element(By.XPATH,'//*[@id="navbar-collapse-funcao"]/ul/li[1]/a')
        ActionChains(navegador).move_to_element(cadastro).perform()
        #seleciona FGTS
        fgts = navegador.find_element(By.XPATH, '//*[@id="WFP2010_MPCDPRDB2CCP"]')
        fgts.click()
        # #insere CPF
        insere_cpf = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj2_UcDBasicos_UcDBasic1_txtCpfCnpj_CAMPO"]')
        insere_cpf.send_keys(cpf)
        insere_cpf.send_keys(Keys.TAB)
        time.sleep(3)
        try:
            confirmar = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj3_UcConfCanVlt_btnConfirmar_dvCBtn"]')
            confirmar.click()
            try:
                # print('bloco  1 try')
                alert = WebDriverWait(navegador, 2).until(
                    EC.alert_is_present()
                )
                text = alert.text
                # print(text)
                alert.accept()
                #se aceitar o alerta
                time.sleep(3)
                nome = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj2_UcDBasicos_UcDBasic1_txtNome_CAMPO"]')
                nome.send_keys('FULANO')
                #data nascimento
                nascimento = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj2_UcDBasicos_UcDBasic1_txtDtNasc_CAMPO"]')
                nascimento.send_keys('10/02/1950')
                #confirmar novamente
                confirmar = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_ctl01_fj3_UcConfCanVlt_btnConfirmar_dvCBtn"]')
                confirmar.click()
            except WebDriverException as e:
                # #logout antes de fechar
                # sair = navegador.find_element(By.XPATH, '//*[@id="ctl00_lk_Sair"]')
                # sair.click()
                # navegador.quit()
                # print('bloco 2 except')
                time.sleep(10)
                # Espere até que a animação "Aguarde" não seja mais visível
                # print('cheguei aqui')
                wait = WebDriverWait(navegador, 10)
                wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_UpdPrs"]')))
                #aguardar taberla para consulta
                def dialog(max_tentativas=3):
                    for tentativa in range(max_tentativas):
                        try:
                            obt_saldo = navegador.find_element(By.XPATH, '//*[@id="btnObterSaldo_txt"]')
                            obt_saldo.click()
                            try:
                                alert = WebDriverWait(navegador, 2).until(EC.alert_is_present())
                                text = alert.text
                                # print(text)
                                alert.accept()
                                print('Alerta tratado com sucesso')
                                if text == '9 - Trabalhador não possui adesão ao saque aniversário vigente na data corrente.':
                                    return {'success': False, 'message': text}
                            except:
                                print('Nenhum alerta encontrado')

                            # Checa a tabela
                            try:
                                tabela = WebDriverWait(navegador, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, '//*[@id="ctl00_cph_FJ1_JPCSFGTS_UcConsultaSaldoFGTS_grdResultadoSaque"]'))
                                )
                                # print('Tabela visível')
                                # Se a tabela estiver visível, continue com as ações nela
                                # Insira aqui as ações que você deseja realizar na tabela
                                # Esperar por até 10 segundos para a tabela ser visível
                                #insere tabela 0008
                                tabela_008 = navegador.find_element(By.XPATH, '//*[@id="ctl00_cph_FJ1_JP2_UCTFAV2_txtCODTAB_CAMPO"]')
                                tabela_008.send_keys('0008')
                                time.sleep(1)
                                tabela_008.send_keys(Keys.TAB)
                                time.sleep(3)
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
                                resumo = {
                                    'valor_total': valor_total
                                }
                                #converte o dicionario em json
                                retorno_json = json.dumps({'resumo': resumo})
                                # print(retorno_json)
                                #logout antes de fechar
                                sair = navegador.find_element(By.XPATH, '//*[@id="ctl00_lk_Sair"]')
                                sair.click()
                                navegador.quit()
                                return {'success': True, 'valor_total': valor_total }
                                return True  # Retorna True se a função for bem-sucedida
                            except:
                                #logout antes de fechar
                                sair = navegador.find_element(By.XPATH, '//*[@id="ctl00_lk_Sair"]')
                                sair.click()
                                navegador.quit()
                                return {'success': False, 'message':'Erro ao localizar a tabela'}

                        except Exception as e:
                            #logout antes de fechar
                            sair = navegador.find_element(By.XPATH, '//*[@id="ctl00_lk_Sair"]')
                            sair.click()
                            navegador.quit()
                            return {'success': False, 'message' : f"Erro ao obter saldo: {str(e)}"}

                    # print(f"Excedido número máximo de tentativas ({max_tentativas}).")
                    return {'success': False, 'message': 'A função falhou ou a tabela não está visível.' }  # Retorna False se não for bem-sucedida após as tentativas

                # Para usar a função:
                result = dialog()
                if result == 'Nenhum alerta encontrado':
                    # print('Erro na função.')
                    return {'success': False, 'message': 'Tabela não encontrada'}
                elif result == True:
                    print("A função foi bem-sucedida e a tabela está visível.")
                elif result:
                    return result
                else:
                    return {'success': False, 'message': 'A função falhou ou a tabela não está visível.' }
                return {'message': str(e)}
            finally:
                pass
        except WebDriverException as e:
            #logout antes de fechar
            # sair = navegador.find_element(By.XPATH, '//*[@id="ctl00_lk_Sair"]')
            # sair.click()
            # navegador.quit()
            # print('bloco 1')
            return {'error': str(e)}
        finally:
            pass
        

        
    except WebDriverException as e:
        #logout antes de fechar
        # print('bloco proncipal')
        sair = navegador.find_element(By.XPATH, '//*[@id="lnkSair"]')
        sair.click()
        navegador.quit()
        return {'success': False, 'message': str(e)}
