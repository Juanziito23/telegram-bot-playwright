# session_manager.py
from src.browser_manager import BrowserManager
from queue import Queue, Empty  # Importe Empty diretamente do módulo queue
from threading import Thread
from typing import Dict, Any
from dataclasses import dataclass
import logging
import os
from dotenv import load_dotenv
import sys
from playwright.sync_api import sync_playwright

# Carrega as variáveis de ambiente
load_dotenv()

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurações
COOKIE_DIR = os.path.join(os.path.dirname(__file__), os.getenv('COOKIE_DIR', 'cookies'))

if not os.path.exists(COOKIE_DIR):
    os.makedirs(COOKIE_DIR)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UserSession:
    link_queue: Queue
    result_queue: Queue
    thread: Thread

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
        self.browser_manager = BrowserManager(COOKIE_DIR)

    def start_session(self, user_id: str, user_email: str) -> None:
        if user_id not in self.sessions:
            link_queue = Queue()
            result_queue = Queue()
            thread = Thread(
                target=self._run_user_session,
                args=(user_id, user_email, link_queue, result_queue),
                daemon=True
            )
            self.sessions[user_id] = UserSession(link_queue, result_queue, thread)
            thread.start()
            logger.info(f"Sessão iniciada para o usuário {user_id}")

    def _run_user_session(self, user_id: str, user_email: str, 
                         link_queue: Queue, result_queue: Queue) -> None:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)  # Usando launch padrão
            context = browser.new_context()  # Cria um novo contexto
            try:
                while True:
                    try:
                        link = link_queue.get(timeout=1)
                        if link == 'STOP':
                            break
                        result = self.browser_manager.process_link(context, link)
                        if result:
                            result_queue.put(result)
                    except Empty:  # Use Empty diretamente
                        continue
            finally:
                context.close()
                browser.close()
                logger.info(f"Sessão encerrada para o usuário {user_id}")
    
    def send_mercado_livre_link(self, user_id: str, link: str) -> None:
        if user_id in self.sessions:
            self.sessions[user_id].link_queue.put(link)
            logger.info(f"Link do Mercado Livre enviado para o usuário {user_id}: {link}")

    def send_link(self, user_id: str, link: str) -> None:
        if user_id in self.sessions:
            self.sessions[user_id].link_queue.put(link)
            logger.info(f"Link enviado para o usuário {user_id}: {link}")

    def get_result(self, user_id: str) -> Any:
        if user_id in self.sessions:
            try:
                return self.sessions[user_id].result_queue.get_nowait()
            except Empty:  # Use Empty diretamente
                return None

    def stop_session(self, user_id: str) -> None:
        if user_id in self.sessions:
            self.sessions[user_id].link_queue.put('STOP')
            self.sessions[user_id].thread.join()
            del self.sessions[user_id]
            logger.info(f"Sessão parada para o usuário {user_id}")