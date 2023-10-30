import undetected_chromedriver.v2 as uc
from selenium import webdriver
import time
from bs4 import BeautifulSoup
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
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.alert import Alert

def icred_solicitacao(cpf):
    # Configure Chrome options and preferences
    options = uc.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.headless = True  # Set headless to True or False as needed
    options.add_argument('--headless=new')
    options.add_argument('user-agent=fake-useragent')
    
    # Set download directory
    prefs = {"download.default_directory": "/home/jeferson/aws-puppeteer/clubeBeneficio"}
    options.add_experimental_option("prefs", prefs)

    # Initialize the Chrome web driver using undetected-chromedriver
    navegador = webdriver.Chrome(options=options)

    try:
        # Navigate to the ICred login page
        navegador.get('https://corban.icred.digital/login')
        time.sleep(3)

        mover = ActionChains(navegador)
        position_X = 393
        position_Y = 291
        mover.move_to_element_with_offset(navegador.find_element(By.TAG_NAME,'body'), position_X, position_Y).perform()

        # Tirar um screenshot da página inteira
        time.sleep(3)
        screenshot = navegador.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))

        # Recortar uma área de 30px em volta da posição do mouse
        x = position_X - 30
        y = position_Y - 30
        width = 5  # Largura de 60 pixels (30 pixels à esquerda + 30 pixels à direita)
        height = 5  # Altura de 60 pixels (30 pixels acima + 30 pixels abaixo)
        cropped_screenshot = screenshot.crop((x, y, x + width, y + height))

        # Take a screenshot
        screenshot_path = "mouse_position_screenshot.png"
        cropped_screenshot.save(screenshot_path)

        # Crie uma instância do ActionChains para realizar a ação
        positions_X = 576
        positions_Y = 352
        click_pos = ActionChains(navegador)
        click_pos.move_to_element(navegador.find_element(By.TAG_NAME, 'body'))
        click_pos.move_by_offset(positions_X, positions_Y)
        click_pos.click()  # Realize o clique

        click_pos.perform()  # Execute a ação
        # Perform login (uncomment and complete this part)
        # login = driver.find_element(By.XPATH, '//*[@id="username"]')
        # login.send_keys('YourUsername')
        # senha = driver.find_element(By.XPATH, '//*[@id="password"]')
        # senha.send_keys('YourPassword')
        # entrar = driver.find_element(By.XPATH, '//*[@id="my-form"]/div[3]/button')
        # entrar.click()
        navegador.implicitly_wait(10)
        time.sleep(5)
        page_source = navegador.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        div = soup.find('body')
        print(div)
    except Exception as e:
        print({'error': str(e)})
    finally:
        navegador.quit()

if __name__ == '__main__':
    icred_solicitacao(cpf='43996081880')

