from playwright.async_api import async_playwright
import logging
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração do logging
logger = logging.getLogger(__name__)

# Obtém o ambiente atual
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

async def run_playwright_script():
    logger.info(f"Iniciando execução do script do Playwright no ambiente {ENVIRONMENT.upper()}.")  # Log de início do script
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://www.mercadolivre.com.br/")
            title = await page.title()
            logger.info(f"Título da página obtido no ambiente {ENVIRONMENT.upper()}: {title}")  # Log do título da página
            await browser.close()
            return f"Título da página: {title}"
    except Exception as e:
        logger.error(f"Erro durante a execução do script do Playwright no ambiente {ENVIRONMENT.upper()}: {e}")  # Log de erro
        raise e