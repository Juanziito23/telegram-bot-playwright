# browser_manager.py
import os
import json
from typing import Optional
from playwright.async_api import async_playwright

class BrowserManager:
    def __init__(self, cookie_dir: str):
        self.cookie_dir = cookie_dir

    def get_cookie_file(self, user_id: str) -> str:
        return os.path.join(self.cookie_dir, f'{user_id}_cookies.json')

    async def save_cookies(self, context, user_id: str) -> None:
        cookies = await context.cookies()
        cookie_file = self.get_cookie_file(user_id)
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f)

    async def load_cookies(self, context, user_id: str) -> None:
        cookie_file = self.get_cookie_file(user_id)
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
                # Adiciona os cookies ao contexto
                await context.add_cookies(cookies)
                print(f"Cookies carregados com sucesso de {cookie_file}")
        else:
            print(f"Arquivo de cookies não encontrado: {cookie_file}")

    async def process_mercado_livre_link(self, link: str) -> Optional[str]:
        try:
            async with async_playwright() as playwright:
                # Inicia o navegador
                browser = await playwright.chromium.launch(headless=False)  # Modo visível para ver a automação
                context = await browser.new_context()

                # Carrega os cookies do arquivo cookies.json
                await self.load_cookies(context, "default")

                page = await context.new_page()

                # Log: Iniciando navegação
                print("Navegando até a página de afiliados do Mercado Livre...")
                await page.goto("https://www.mercadolivre.com.br/afiliados/linkbuilder#menu-user")
                
                # Verifica se o usuário está logado
                if await page.query_selector("text=Entrar"):  # Verifica se o botão "Entrar" está visível
                    print("Usuário não está logado. Verifique os cookies.")
                    return "Erro: Usuário não está logado. Verifique os cookies."

                # # Log: Clicando no menu do usuário
                # print("Clicando no menu do usuário...")
                # await page.get_by_role("dialog", name="Kayk, menu").click()
                
                # # Log: Navegando até a seção de afiliados
                # print("Navegando até a seção de afiliados...")
                # await page.get_by_role("link", name="Afiliados").click()
                
                # Log: Clicando no campo de inserção de URLs
                print("Clicando no campo de inserção de URLs...")
                await page.locator("#linkbuilder div").filter(has_text="Insira 1 ou mais URLs separados por 1 linhaInsira 1 ou mais URLs das páginas de ").nth(3).click()
                
                # Log: Preenchendo o campo com o link enviado pelo usuário
                print(f"Preenchendo o campo com o link: {link}")
                await page.get_by_placeholder("Ex: https://www.mercadolivre.com.br/_Desde_49_Deal_afiliados-fashion_NoIndex_True").click()
                await page.get_by_placeholder("Ex: https://www.mercadolivre.com.br/_Desde_49_Deal_afiliados-fashion_NoIndex_True").fill(link)
                
                # Log: Clicando no botão 'Gerar'
                print("Clicando no botão 'Gerar'...")
                await page.get_by_role("button", name="Gerar").click()

                # 🔹 Aguarda um curto tempo para garantir que o link seja gerado
                await page.wait_for_timeout(2000)

                # 🔍 Lista todos os <div> e imprime seus valores
                # divs = await page.locator("div").all()
                # for index, div in enumerate(divs):
                #     text = await div.evaluate("el => el.textContent.trim()")
                #     print(f"🔍 <div> {index}: {text}")

                # generated_link = await page.evaluate("navigator.clipboard.readText()") - funnou
                
                #🔹 Captura o link diretamente do <div> onde ele aparece
                generated_link = await page.locator("div").nth(148).evaluate("el => el.textContent.trim()")
                print(f"✅ Link gerado: {generated_link}")


                # print(f"🔗 Link capturado da área de transferência: {generated_link}")


                
                # Log: Clicando no botão 'Copiar'
                print("Clicando no botão 'Copiar'...")
                await page.get_by_role("button", name="Copiar").click()

                                
                # Log: Link gerado e copiado com sucesso
                print("Link de afiliado gerado e copiado com sucesso!")

                 
                # Salva os cookies para uso futuro
                await self.save_cookies(context, "default")
                
                # Fecha a página e o navegador
                await page.close()
                await browser.close()

                # 🔹 Retorna o link capturado para o usuário
                return f"Link de afiliado gerado: {generated_link}"
                
                # return f"Link de afiliado gerado e copiado para o link: {link}"
        except Exception as e:
            # Log: Erro durante a execução
            print(f"Erro ao processar link do Mercado Livre: {str(e)}")
            return f"Erro ao processar o link: {str(e)}"