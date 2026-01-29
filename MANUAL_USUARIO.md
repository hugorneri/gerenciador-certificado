# Manual do Usuário
## Gerenciador de Certificados Digitais
### Versão 2.1.0

---

## Sumário

1. [Introdução](#1-introdução)
2. [Primeiro Acesso](#2-primeiro-acesso)
3. [Dashboard Principal](#3-dashboard-principal)
4. [Cadastro de Clientes](#4-cadastro-de-clientes)
5. [Configurações](#5-configurações)
6. [Notificações por Email](#6-notificações-por-email)
7. [Importar e Exportar Dados](#7-importar-e-exportar-dados)
8. [Perguntas Frequentes](#8-perguntas-frequentes)

---

## 1. Introdução

O **Gerenciador de Certificados Digitais** é um sistema desenvolvido para facilitar o controle e monitoramento de certificados digitais (.pfx) de clientes de escritórios de contabilidade.

### Principais Funcionalidades:
- Leitura automática de certificados .pfx
- Monitoramento de datas de vencimento
- Cadastro de clientes com email para notificações
- Envio automático de alertas de vencimento
- Exportação de relatórios para Excel
- Tema claro e escuro

---

## 2. Primeiro Acesso

### 2.1 Iniciando o Sistema

1. Abra o terminal/prompt de comando
2. Navegue até a pasta do sistema
3. Execute o comando:
   ```
   streamlit run app.py
   ```
4. O navegador abrirá automaticamente com o sistema

### 2.2 Tela Inicial

Ao abrir o sistema, você verá:
- **Sidebar (lateral esquerda)**: Menu de navegação
- **Área principal**: Dashboard com informações dos certificados

---

## 3. Dashboard Principal

### 3.1 Cards de Métricas

Na parte superior, você encontra 5 cards com informações resumidas:

| Card | Descrição |
|------|-----------|
| **Total** | Quantidade total de certificados na pasta |
| **Vencidos** | Certificados já vencidos (vermelho) |
| **Atenção** | Certificados que vencem em até 30 dias (amarelo) |
| **Válidos** | Certificados com mais de 30 dias de validade (verde) |
| **Erros** | Certificados com problema de leitura |

### 3.2 Painel de Ações Pendentes

Logo abaixo das métricas, aparecem alertas quando há:
- Certificados vencidos que precisam de renovação
- Certificados próximos do vencimento
- Clientes sem email cadastrado (não receberão notificações)

Clique em **"Ver detalhes"** para expandir a lista completa.

### 3.3 Gráfico de Vencimentos

Clique em **"📊 Gráfico de Vencimentos"** para visualizar um gráfico de barras mostrando quantos certificados vencem em cada mês.

- **Barras vermelhas**: Meses já passados (vencidos)
- **Barras amarelas**: Próximos 30 dias
- **Barras verdes**: Mais de 30 dias

### 3.4 Tabela de Certificados

A tabela principal mostra todos os certificados com as colunas:
- **Código**: Código do cliente (extraído do nome do arquivo)
- **Cliente**: Razão social
- **Vencimento**: Data de vencimento do certificado
- **Dias**: Quantidade de dias até vencer (negativo se vencido)
- **Status**: Vencido, Atenção, Válido ou Erro
- **📧**: Indica se o cliente tem email cadastrado (✓) ou não (—)

#### Filtros Disponíveis:
- **Busca**: Digite código ou nome para filtrar
- **Status**: Filtre por Vencido, Atenção, Válido ou Erro
- **Email**: Filtre clientes com ou sem email cadastrado

#### Exportar para Excel:
Clique no botão **"📥 Exportar Excel"** para baixar a lista filtrada.

---

## 4. Cadastro de Clientes

### 4.1 Como Cadastrar

1. Na tabela de certificados, **clique na linha** do cliente desejado
2. O formulário de cadastro abrirá automaticamente no topo da página
3. Preencha os campos:
   - **Email** *(obrigatório para receber notificações)*
   - **Telefone** *(opcional)*
   - **Responsável** *(opcional)*
   - **Observações** *(opcional)*
4. Clique em **"💾 Salvar"**

### 4.2 Campos Automáticos

Os campos **Código** e **Razão Social** são preenchidos automaticamente com base no nome do arquivo do certificado e não podem ser editados.

### 4.3 Editar Cadastro Existente

Repita o processo acima. Se o cliente já estiver cadastrado, os dados atuais serão carregados automaticamente.

---

## 5. Configurações

Acesse as configurações clicando em **"⚙️ Configurações"** na sidebar.

### 5.1 Aba "Email SMTP"

Configure o envio de emails:

1. **Email do Remetente**: Seu email Gmail
2. **Senha de Aplicativo**: Senha gerada no Google (veja seção 6)
3. **Nome do Escritório**: Aparece no rodapé dos emails

Botões disponíveis:
- **💾 Salvar SMTP**: Salva as configurações
- **🔌 Testar Conexão**: Verifica se as credenciais estão corretas
- **👁️ Preview Email**: Visualiza como o email ficará

### 5.2 Aba "Notificações"

- **Dias para notificar**: Defina quantos dias antes do vencimento o sistema deve notificar (1-90 dias)
- **Notificação automática**: Ative para enviar emails automaticamente ao abrir o sistema

### 5.3 Aba "Importar/Exportar"

- **Exportar CSV**: Baixe todos os cadastros de clientes
- **Importar CSV**: Importe cadastros em lote

### 5.4 Aba "Sobre"

- Versão do sistema
- Estatísticas (clientes cadastrados, emails enviados)
- Atalhos úteis
- Histórico de notificações

---

## 6. Notificações por Email

### 6.1 Configurar Senha de Aplicativo do Google

Para enviar emails pelo Gmail, você precisa criar uma **Senha de Aplicativo**:

1. Acesse [myaccount.google.com](https://myaccount.google.com)
2. No menu lateral, clique em **Segurança**
3. Em "Como fazer login no Google", clique em **Verificação em duas etapas**
4. Ative a verificação (se não estiver ativa)
5. Volte para Segurança e clique em **Senhas de app**
6. Em "Selecionar app", escolha **Email**
7. Em "Selecionar dispositivo", escolha **Computador Windows**
8. Clique em **Gerar**
9. Copie a senha de 16 caracteres (exemplo: `abcd efgh ijkl mnop`)
10. Cole no sistema (campo "Senha de Aplicativo")

### 6.2 Envio Automático

Quando ativado:
- O sistema verifica certificados próximos ao vencimento
- Envia email para clientes com email cadastrado
- Não reenvia se já enviou nos últimos 7 dias

### 6.3 Envio Manual

1. Vá em **Configurações > Notificações**
2. Clique em **"📤 Preparar Envio de Notificações"**
3. Revise a lista de destinatários
4. Clique em **"✅ Confirmar Envio"**

---

## 7. Importar e Exportar Dados

### 7.1 Exportar Cadastros

1. Vá em **Configurações > Importar/Exportar**
2. Clique em **"📥 Exportar CSV"**
3. O arquivo será baixado automaticamente

### 7.2 Importar Cadastros

1. Prepare um arquivo CSV com as colunas:
   ```
   codigo,razao_social,email,telefone,responsavel,observacoes
   ```
2. Vá em **Configurações > Importar/Exportar**
3. Clique em **"Browse files"** e selecione o arquivo
4. Revise os dados na tabela
5. Clique em **"✅ Confirmar Importação"**

### 7.3 Exportar Lista de Certificados

No dashboard, clique em **"📥 Exportar Excel"** para baixar a lista de certificados em formato Excel.

---

## 8. Perguntas Frequentes

### O sistema não encontra os certificados
Verifique se o caminho da pasta está correto no arquivo `app.py` (variável `CAMINHO_CERTIFICADOS`).

### Erro na leitura do certificado
Pode ser:
- Senha no nome do arquivo está incorreta
- Arquivo corrompido
- Nome do arquivo não segue o padrão esperado

### Email não está sendo enviado
Verifique:
1. Se a senha de aplicativo está correta
2. Se testou a conexão e deu sucesso
3. Se o cliente tem email cadastrado
4. Se já não foi enviada notificação nos últimos 7 dias

### Como mudar o tema?
Na sidebar, use o toggle **"🌙 Tema Escuro"** para alternar entre tema claro e escuro.

### Como atualizar a lista de certificados?
Clique em **"🔄 Atualizar Dados"** na sidebar.

---

## Suporte

Em caso de dúvidas ou problemas, entre em contato com o administrador do sistema.

---

*Manual atualizado em Janeiro de 2026 - Versão 2.1.0*
