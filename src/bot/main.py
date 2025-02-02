# main.py
import asyncio
import os
import sys
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.playwright_scripts.example_script import run_playwright_script
from src.browser_manager import BrowserManager # Importe o BrowserManager
from src.session_manager import SessionManager  # Importe o SessionManager

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração do bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

# Inicializa o SessionManager
session_manager = SessionManager()

# Inicializa o bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Função para criar o menu de iniciar
def get_start_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Executar Script")],
            [KeyboardButton(text="Mercado Livre")],
            [KeyboardButton(text="Sobre o Bot")],
            [KeyboardButton(text="Ajuda")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

# Comando /start
@dp.message(Command("start"))
async def start(message: types.Message):
    logger.info(f"Usuário {message.from_user.id} iniciou o bot no ambiente {ENVIRONMENT.upper()}.")
    await message.answer(
        "Olá! Eu sou seu bot do Telegram integrado com Playwright. Escolha uma opção abaixo:",
        reply_markup=get_start_keyboard()
    )

# Comando para executar o script do Playwright
@dp.message(lambda message: message.text == "Executar Script")
async def run_script(message: types.Message):
    logger.info(f"Usuário {message.from_user.id} solicitou a execução do script no ambiente {ENVIRONMENT.upper()}.")
    if ENVIRONMENT == "development":
        await message.answer("Executando script do Playwright em modo de desenvolvimento...")
    else:
        await message.answer("Executando script do Playwright em modo de produção...")

    try:
        result = await run_playwright_script()
        logger.info(f"Script executado com sucesso no ambiente {ENVIRONMENT.upper()}. Resultado: {result}")
        await message.answer(f"Resultado do script: {result}")
    except Exception as e:
        logger.error(f"Erro ao executar o script no ambiente {ENVIRONMENT.upper()}: {e}")
        await message.answer(f"Erro ao executar o script: {str(e)}")

# Comando para iniciar uma sessão
@dp.message(Command("iniciar_sessao"))
async def start_session(message: types.Message):
    user_id = str(message.from_user.id)
    session_manager.start_session(user_id, "user@example.com")  # Substitua pelo e-mail do usuário, se necessário
    await message.answer("Sessão iniciada com sucesso!")

# Comando para Mercado Livre
@dp.message(lambda message: message.text == "Mercado Livre")
async def mercado_livre(message: types.Message):
    await message.answer("Por favor, envie um link do Mercado Livre (deve começar com 'https://www.mercadolivre.com.br/').")

# Processa o link do Mercado Livre
@dp.message(lambda message: message.text.startswith("https://www.mercadolivre.com.br/"))
async def process_mercado_livre_link(message: types.Message):
    user_id = str(message.from_user.id)
    link = message.text

    # Log: Link recebido
    logger.info(f"Usuário {user_id} enviou um link do Mercado Livre: {link}")
    
    # Envia uma mensagem de confirmação
    await message.answer(f"Link do Mercado Livre recebido: {link}. Processando...")

    try:
         # Aguarda a execução da coroutine
        result = await session_manager.browser_manager.process_mercado_livre_link(link)
        if result:
            await message.answer(result)
        else:
            await message.answer("Erro ao processar o link do Mercado Livre.")
    except Exception as e:
        logger.error(f"Erro ao processar link do Mercado Livre: {str(e)}")
        await message.answer("Erro ao processar o link do Mercado Livre.")

# Comando para enviar um link para processamento
@dp.message(Command("enviar_link"))
async def send_link(message: types.Message):
    user_id = str(message.from_user.id)
    link = message.get_args()
    if link:
        session_manager.send_link(user_id, link)
        await message.answer(f"Link enviado para processamento: {link}")
    else:
        await message.answer("Por favor, forneça um link após o comando /enviar_link.")

# Comando para obter o resultado do processamento
@dp.message(Command("obter_resultado"))
async def get_result(message: types.Message):
    user_id = str(message.from_user.id)
    result = session_manager.get_result(user_id)
    if result:
        await message.answer(f"Resultado do processamento: {result}")
    else:
        await message.answer("Nenhum resultado disponível no momento.")

# Comando para parar a sessão
@dp.message(Command("parar_sessao"))
async def stop_session(message: types.Message):
    user_id = str(message.from_user.id)
    session_manager.stop_session(user_id)
    await message.answer("Sessão parada com sucesso.")

# Comando para mostrar informações sobre o bot
@dp.message(lambda message: message.text == "Sobre o Bot")
async def about_bot(message: types.Message):
    logger.info(f"Usuário {message.from_user.id} solicitou informações sobre o bot.")
    await message.answer(
        "🤖 **Sobre o Bot**\n\n"
        "Este é um bot do Telegram integrado com Playwright para automação de tarefas.\n"
        "Ambiente atual: " + ENVIRONMENT.upper()
    )

# Comando para ajudar o usuário
@dp.message(lambda message: message.text == "Ajuda")
async def help_command(message: types.Message):
    logger.info(f"Usuário {message.from_user.id} solicitou ajuda.")
    await message.answer(
        "🆘 **Ajuda**\n\n"
        "Aqui estão os comandos disponíveis:\n"
        "- **Executar Script** : Executa o script do Playwright.\n"
        "- **Iniciar Sessão** : Inicia uma nova sessão para o usuário.\n"
        "- **Enviar Link** : Envia um link para processamento.\n"
        "- **Obter Resultado** : Obtém o resultado do processamento.\n"
        "- **Parar Sessão** : Para a sessão do usuário.\n"
        "- **Sobre o Bot** : Mostra informações sobre o bot.\n"
        "- **Ajuda** : Exibe esta mensagem de ajuda."
    )

# Inicialização do bot
async def main():
    logger.info(f"Iniciando o bot no ambiente {ENVIRONMENT.upper()}...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())