# 🔐 Gerenciador de Certificados Digitais

Sistema de gerenciamento de certificados digitais (.pfx) desenvolvido em Python com Streamlit. Monitore a validade dos certificados, cadastre clientes e receba notificações automáticas de vencimento por email.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Funcionalidades

### Dashboard Principal
- **Métricas em tempo real**: Total de certificados, vencidos, próximos ao vencimento, válidos e erros
- **Painel de Ações Pendentes**: Alertas visuais para certificados que precisam de atenção
- **Tabela interativa**: Clique em qualquer linha para editar o cadastro do cliente
- **Filtros e busca**: Encontre certificados por código, nome, status ou email
- **Gráfico de vencimentos**: Visualize certificados por mês de vencimento
- **Exportar para Excel**: Baixe a lista de certificados em formato .xlsx

### Cadastro de Clientes
- Cadastro vinculado ao código do certificado
- Campos: Email, Telefone, Responsável, Observações
- Importação/Exportação em lote via CSV

### Notificações por Email
- Configuração SMTP Gmail com senha de aplicativo
- Envio automático ao abrir o sistema (configurável)
- Envio manual com confirmação
- Preview do template de email
- Histórico de notificações enviadas
- Anti-spam: não reenvia se já notificou nos últimos 7 dias

### Configurações
- Dias de antecedência para notificação (1-90 dias)
- Toggle de notificação automática
- Tema claro/escuro
- Importar/Exportar cadastros

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/gerenciador-certificado.git
cd gerenciador-certificado
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure o caminho dos certificados**

Edite o arquivo `app.py` e altere a variável `CAMINHO_CERTIFICADOS` para o caminho da sua pasta de certificados:
```python
CAMINHO_CERTIFICADOS = r"C:\Seu\Caminho\Certificados"
```

4. **Execute o sistema**
```bash
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`

### Acesso pela rede local

Para que outros PCs da rede acessem o sistema (ex.: `http://192.168.15.27:8501`), o projeto já inclui o arquivo `.streamlit/config.toml` com:

- **address = "0.0.0.0"** – servidor escuta em todas as interfaces
- **enableCORS = false** e **enableXsrfProtection = false** – evitam o erro "Failed to fetch dynamically imported module" ao acessar de outro computador

Reinicie o Streamlit após qualquer alteração na pasta do projeto. Outros usuários devem acessar usando o **IP da máquina** onde o servidor está rodando (ex.: `http://192.168.15.27:8501`).

> **Segurança:** Essas opções reduzem proteções (CORS/XSRF). Use apenas em rede interna confiável.

## 📁 Estrutura do Projeto

```
gerenciador-certificado/
├── app.py              # Aplicação principal (Streamlit)
├── database.py         # Módulo de banco de dados SQLite
├── email_service.py    # Serviço de envio de emails
├── styles.py           # Estilos CSS customizados
├── requirements.txt    # Dependências do projeto
├── README.md           # Este arquivo
├── MANUAL_USUARIO.md   # Manual do usuário
└── data/
    └── certificados.db # Banco de dados SQLite (criado automaticamente)
```

## 📄 Padrão de Nomenclatura dos Arquivos .pfx

O sistema espera que os arquivos sigam este padrão:

```
CÓDIGO - RAZÃO SOCIAL Senha SENHA.pfx
```

**Exemplo:**
```
02 - EMPRESA EXEMPLO LTDA Senha 1234.pfx
```

Onde:
- `02` = Código do cliente
- `EMPRESA EXEMPLO LTDA` = Razão social
- `1234` = Senha do certificado

## ⚙️ Configuração do Email (Gmail)

Para enviar notificações por email, você precisa configurar uma **Senha de Aplicativo** do Google:

1. Acesse [myaccount.google.com](https://myaccount.google.com)
2. Vá em **Segurança**
3. Ative a **Verificação em duas etapas** (se não estiver ativa)
4. Em **Senhas de app**, crie uma nova senha para "Email"
5. Copie a senha de 16 caracteres gerada
6. Cole no sistema em **Configurações > Email SMTP**

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** - Framework web para Python
- **[Pandas](https://pandas.pydata.org/)** - Manipulação de dados
- **[Cryptography](https://cryptography.io/)** - Leitura de certificados PKCS#12
- **[Plotly](https://plotly.com/)** - Gráficos interativos
- **[OpenPyXL](https://openpyxl.readthedocs.io/)** - Exportação para Excel
- **SQLite** - Banco de dados local

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📞 Suporte

Em caso de dúvidas ou problemas, abra uma [issue](https://github.com/seu-usuario/gerenciador-certificado/issues) no GitHub.

---

Desenvolvido com ❤️ para facilitar o gerenciamento de certificados digitais.
