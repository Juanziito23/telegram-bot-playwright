import asyncio
import sys
import os

# Adiciona o diretório src ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot.main import main

if __name__ == "__main__":
    asyncio.run(main())