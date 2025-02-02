# 📌 Bot de Automação com Playwright e Telegram

## Este bot utiliza o Playwright para automação de navegação e interage via Telegram. Ele pode processar links do Mercado Livre, executar scripts automatizados e gerenciar sessões de usuários.

### 🚀 Instalação

## 1️⃣ Pré-requisitos
### Certifique-se de ter instalado:

```bash 
Python 3.8+
pip
Playwright
dotenv
Aiogram (para interação com o Telegram)
```
## 2️⃣ Clonando o repositório
```bash
git clone https://github.com/Juanziito23/telegram-bot-playwright.git
cd seu-repositorio
```
## 3️⃣ Instalando dependências
```bash 
pip install -r requirements.txt
```
### Caso o Playwright não esteja instalado, rode:
```bash
playwright install
```
## 4️⃣ Configuração
### Crie um arquivo .env com o seguinte conteúdo:

```bash
TELEGRAM_BOT_TOKEN=SEU_TOKEN_AQUI
ENVIRONMENT=production
COOKIE_DIR=cookies
```
## 5️⃣ Executando o bot
```bash
python run_bot.py
```
# ⚙️ Funcionalidades

📌 **Comandos disponíveis**

| Comando              | Descrição                                      |
|                      | ---:                                           |
|----------------------|------------------------------------------------|
| `/start`             | Inicia o bot e exibe o menu principal          |
| `Executar Script`    | Roda um script Playwright                      |
| `/iniciar_sessao`    | Inicia uma nova sessão para o usuário          |
| `/enviar_link URL`   | Envia um link para processamento               |
| `/obter_resultado`   | Obtém o resultado do processamento             |
| `/parar_sessao`      | Para a sessão do usuário                       |
| `Mercado Livre`      | Permite processar links do Mercado Livre       |
| `Sobre o Bot`        | Exibe informações sobre o bot                  |
| `Ajuda`              | Lista os comandos disponíveis                  |

# 🛠️ Como funciona
🔹 Gerenciamento de Sessões
O SessionManager mantém sessões ativas para cada usuário. Ele recebe links, os processa e retorna os resultados.

🔹 Processamento de Links
O BrowserManager usa o Playwright para acessar páginas e gerar links de afiliados no Mercado Livre.

🔹 Integração com o Telegram
Usa Aiogram para interagir com os usuários e responder aos comandos.

📩 Contribuição
Se quiser contribuir, sinta-se à vontade para abrir issues e pull requests!

📝 Licença
Este projeto está sob a licença MIT.

- [x] #739
- [ ] https://github.com/octo-org/octo-repo/issues/740
- [ ] Add delight to the experience when all tasks are complete :tada:




Use a extensão chamada "EditThisCookie", para exportar os cookies do navegador para um arquivo cookies.json. Após isso você deve corrigir o arquivo em alguma IA, user a Qwen2.5-Max para corrigir, pois ele deve apresentar o erro abaixo: 
"playwright._impl._errors.Error: BrowserContext.add_cookies: cookies[0].sameSite: expected one of (Strict|Lax|None)" 
Breve explicação : O problema principal no seu arquivo cookies.json é que o valor do campo sameSite está definido como "no_restriction", que não é um valor válido para o Playwright. O Playwright aceita apenas os valores "Strict", "Lax" ou "None" para o campo sameSite. Além disso, alguns campos adicionais (como id, storeId, hostOnly, etc.) não são necessários e podem ser removidos.

Vou corrigir o arquivo para você, ajustando os valores de sameSite e removendo campos desnecessários.