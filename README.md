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
```python
pip install -r requirements.txt
```
### Caso o Playwright não esteja instalado, rode:
```bash
playwright install
```
## 4️⃣ Configuração
### Crie um arquivo .env com o seguinte conteúdo:

```base
TELEGRAM_BOT_TOKEN=SEU_TOKEN_AQUI
ENVIRONMENT=production
COOKIE_DIR=cookies
```
## 5️⃣ Executando o bot
```python
python run_bot.py
```
# ⚙️ Funcionalidades

📌 **Comandos disponíveis**

| Comando              | Descrição                                      |
|----------------------|:---------------------------------------------- |
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
### 🔹 Gerenciamento de Sessões:
1. O SessionManager mantém sessões ativas para cada usuário. Ele recebe links, os processa e retorna os resultados.

### 🔹 Processamento de Links
2. O BrowserManager usa o Playwright para acessar páginas e gerar links de afiliados no Mercado Livre.

### 🔹 Integração com o Telegram
Usa Aiogram para interagir com os usuários e responder aos comandos.

### 📩 Contribuição
Se quiser contribuir, sinta-se à vontade para abrir issues e pull requests!

### 📝 Licença
Este projeto está sob a licença MIT.

- [x] #739
- [ ] Add delight to the experience when all tasks are complete :tada:

## 📝 Lista de Features

| Status   | Feature                              | Descrição                                                                 | Prioridade/Detalhes                                   |
|----------|--------------------------------------|---------------------------------------------------------------------------|-------------------------------------------------------|
| ✅       | Autenticação de Usuário             | Implementação do sistema de login e registro com validação de email.      | _Concluído em: 10/10/2023_                           |
| ✅       | Página de Dashboard                 | Criação da interface inicial do usuário com gráficos e estatísticas.      | _Concluído em: 12/10/2023_                           |
| ✅       | Integração com API Externa          | Conexão com a API de pagamentos para processamento seguro.                | _Concluído em: 14/10/2023_                           |
| 🚀       | Sistema de Notificações             | Desenvolver notificações em tempo real para eventos importantes.          | _Prioridade: Alta_                                    |
| ⬜       | Modo Escuro                         | Adicionar suporte ao tema escuro para melhorar a experiência do usuário.  | _Prioridade: Média_                                   |
| ⬜       | Testes Automatizados                | Configurar testes unitários e de integração para todas as funcionalidades.| _Prioridade: Alta_                                    |
| 🔍       | Upload de Arquivos                  | Implementação de upload de imagens e documentos com validação.            | [🔗 Ver detalhes no GitHub](https://github.com/octo-org/octo-repo/issues/740) |
| 🔍       | Melhoria na Performance             | Otimização do carregamento de páginas e redução do tempo de resposta.     | _Estimativa de conclusão: 20/10/2023_                |
| 🔍       | Integração com Redes Sociais        | Permitir login via redes sociais (Google, Facebook, etc.).               | _Estimativa de conclusão: 25/10/2023_                |

---

### 🎉 Próximos Passos
- **Celebração Final** 🎊  
  Quando todas as features forem concluídas, vamos adicionar um commit especial com o título "🎉 Projeto Finalizado!" :tada:




### 📝 **Observação Importante: Correção de Cookies para o Playwright**

Ao exportar os cookies do navegador usando a extensão **EditThisCookie**, você pode encontrar um erro ao tentar carregá-los no Playwright. O problema ocorre porque o campo `sameSite` no arquivo `cookies.json` está definido como `"no_restriction"`, que não é um valor válido para o Playwright.

#### **O que está errado?**
- O Playwright aceita apenas os seguintes valores para o campo `sameSite`:  
  - `"Strict"`  
  - `"Lax"`  
  - `"None"`  
- Além disso, alguns campos adicionais (como `id`, `storeId`, `hostOnly`, etc.) presentes no arquivo exportado não são necessários e podem ser removidos.

#### **Como corrigir?**
1. **Exporte os cookies** usando a extensão **EditThisCookie** e salve-os em um arquivo chamado `cookies.json`.
2. **Corrija o arquivo** ajustando os valores de `sameSite` para um dos valores válidos (`"Strict"`, `"Lax"` ou `"None"`).
3. **Remova campos desnecessários**, como `id`, `storeId`, `hostOnly`, entre outros, para garantir que o arquivo esteja limpo e compatível com o Playwright.
4. Utilize a IA **Qwen2.5-Max** para ajudar na correção do arquivo, caso necessário.

#### **Exemplo de Erro Encontrado**
```plaintext
playwright._impl._errors.Error: BrowserContext.add_cookies: cookies[0].sameSite: expected one of (Strict|Lax|None)