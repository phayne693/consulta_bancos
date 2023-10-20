// Importe as bibliotecas necessárias
import { launch } from 'puppeteer';
import * as path from 'path';

// import { Builder, By } from 'selenium-webdriver';
// import { Options } from 'selenium-webdriver/chrome';

async function main() {
  // Inicie o Puppeteer para resolver o reCAPTCHA
  const pathToExtension =path.join(path.resolve(),'2captcha-solver');
  
  const browser = await launch({ headless: false,
    ignoreHTTPSErrors: true,
    args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--ignore-certificate-errors',
        `--disable-extensions-except=${pathToExtension}`,
        `--load-extension=${pathToExtension}`]});
  const page = await browser.newPage();
  // Use Puppeteer para resolver o reCAPTCHA aqui
  await page.goto('https://meumb.mercantil.com.br/login')
  // Feche o Puppeteer
  // await browser.close();

}

main();
