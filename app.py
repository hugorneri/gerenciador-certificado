"""
Gerenciador de Certificados Digitais (.pfx)
Dashboard Streamlit para monitorar validade de certificados digitais.
"""

import os
import re
import time
import warnings
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from io import BytesIO, StringIO

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from cryptography.hazmat.primitives.serialization import pkcs12

import database as db
import email_service as email_svc
from styles import get_css, render_header, render_metric_card, render_badge, render_action_card

# Suprime warnings de parsing BER/DER da biblioteca cryptography
warnings.filterwarnings("ignore", message=".*PKCS#12 bundle could not be parsed as DER.*")

# Caminho fixo da pasta de certificados
CAMINHO_CERTIFICADOS = r"G:\Drives compartilhados\CERTIFICADOS DIGITAIS"

# Caminho do manual do usuário (HTML)
PASTA_APP = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MANUAL_HTML = os.path.join(PASTA_APP, "MANUAL_USUARIO.html")

# Versão do sistema
VERSAO = "2.1.0"


def extrair_dados_nome_arquivo(nome_arquivo: str) -> Optional[dict]:
    """Extrai código, nome do cliente e senha do nome do arquivo .pfx."""
    padrao = r'^(\d+)\s*-\s*(.+?)\s+Senha\s+(.+?)\.pfx$'
    match = re.match(padrao, nome_arquivo, re.IGNORECASE)
    
    if match:
        return {
            'codigo': match.group(1).strip(),
            'cliente': match.group(2).strip(),
            'senha': match.group(3).strip()
        }
    return None


def ler_certificado(caminho_arquivo: str, senha: str) -> Optional[datetime]:
    """Abre o arquivo .pfx e retorna a data de vencimento do certificado."""
    try:
        with open(caminho_arquivo, 'rb') as f:
            pfx_data = f.read()
        
        private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
            pfx_data,
            senha.encode('utf-8')
        )
        
        if certificate is not None:
            return certificate.not_valid_after_utc
        return None
    except Exception:
        return None


def calcular_status(dias_para_vencer: int) -> str:
    """Calcula o status do certificado baseado nos dias para vencer."""
    if dias_para_vencer < 0:
        return 'Vencido'
    elif dias_para_vencer <= 30:
        return 'Atenção'
    else:
        return 'Válido'


def processar_certificados_com_progresso(caminho_pasta: str) -> pd.DataFrame:
    """Processa todos os certificados .pfx de uma pasta com barra de progresso."""
    dados = []
    
    if not os.path.exists(caminho_pasta):
        return pd.DataFrame(columns=['Código', 'Cliente', 'Vencimento', 'Dias para Vencer', 'Status'])
    
    try:
        arquivos = [f for f in os.listdir(caminho_pasta) if f.lower().endswith('.pfx')]
    except PermissionError:
        return pd.DataFrame(columns=['Código', 'Cliente', 'Vencimento', 'Dias para Vencer', 'Status'])
    
    if not arquivos:
        return pd.DataFrame(columns=['Código', 'Cliente', 'Vencimento', 'Dias para Vencer', 'Status'])
    
    # Barra de progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, arquivo in enumerate(arquivos):
        status_text.text(f"Processando: {arquivo[:50]}...")
        progress_bar.progress((i + 1) / len(arquivos))
        
        caminho_completo = os.path.join(caminho_pasta, arquivo)
        dados_arquivo = extrair_dados_nome_arquivo(arquivo)
        
        if dados_arquivo is None:
            dados.append({
                'Código': '?',
                'Cliente': arquivo,
                'Vencimento': None,
                'Dias para Vencer': None,
                'Status': 'Erro: Nome inválido'
            })
            continue
        
        data_vencimento = ler_certificado(caminho_completo, dados_arquivo['senha'])
        
        if data_vencimento is None:
            dados.append({
                'Código': dados_arquivo['codigo'],
                'Cliente': dados_arquivo['cliente'],
                'Vencimento': None,
                'Dias para Vencer': None,
                'Status': 'Erro na leitura'
            })
            continue
        
        hoje = datetime.now(timezone.utc)
        dias_para_vencer = (data_vencimento - hoje).days
        
        dados.append({
            'Código': dados_arquivo['codigo'],
            'Cliente': dados_arquivo['cliente'],
            'Vencimento': data_vencimento.strftime('%d/%m/%Y'),
            'Dias para Vencer': dias_para_vencer,
            'Status': calcular_status(dias_para_vencer)
        })
    
    # Limpa barra de progresso
    progress_bar.empty()
    status_text.empty()
    
    df = pd.DataFrame(dados)
    
    if not df.empty:
        df['_ordem'] = df['Dias para Vencer'].apply(
            lambda x: x if x is not None else float('inf')
        )
        df = df.sort_values('_ordem').drop('_ordem', axis=1)
        df = df.reset_index(drop=True)
    
    return df


@st.cache_data
def processar_certificados(caminho_pasta: str) -> pd.DataFrame:
    """Processa todos os certificados .pfx de uma pasta (com cache)."""
    dados = []
    
    if not os.path.exists(caminho_pasta):
        return pd.DataFrame(columns=['Código', 'Cliente', 'Vencimento', 'Dias para Vencer', 'Status'])
    
    try:
        arquivos = [f for f in os.listdir(caminho_pasta) if f.lower().endswith('.pfx')]
    except PermissionError:
        return pd.DataFrame(columns=['Código', 'Cliente', 'Vencimento', 'Dias para Vencer', 'Status'])
    
    for arquivo in arquivos:
        caminho_completo = os.path.join(caminho_pasta, arquivo)
        dados_arquivo = extrair_dados_nome_arquivo(arquivo)
        
        if dados_arquivo is None:
            dados.append({
                'Código': '?',
                'Cliente': arquivo,
                'Vencimento': None,
                'Dias para Vencer': None,
                'Status': 'Erro: Nome inválido'
            })
            continue
        
        data_vencimento = ler_certificado(caminho_completo, dados_arquivo['senha'])
        
        if data_vencimento is None:
            dados.append({
                'Código': dados_arquivo['codigo'],
                'Cliente': dados_arquivo['cliente'],
                'Vencimento': None,
                'Dias para Vencer': None,
                'Status': 'Erro na leitura'
            })
            continue
        
        hoje = datetime.now(timezone.utc)
        dias_para_vencer = (data_vencimento - hoje).days
        
        dados.append({
            'Código': dados_arquivo['codigo'],
            'Cliente': dados_arquivo['cliente'],
            'Vencimento': data_vencimento.strftime('%d/%m/%Y'),
            'Dias para Vencer': dias_para_vencer,
            'Status': calcular_status(dias_para_vencer)
        })
    
    df = pd.DataFrame(dados)
    
    if not df.empty:
        df['_ordem'] = df['Dias para Vencer'].apply(
            lambda x: x if x is not None else float('inf')
        )
        df = df.sort_values('_ordem').drop('_ordem', axis=1)
        df = df.reset_index(drop=True)
    
    return df


def aplicar_estilo(row: pd.Series) -> list:
    """Aplica estilo condicional baseado no status do certificado."""
    status = row.get('Status', '')
    
    if status == 'Vencido':
        return ['background-color: #ffebee; color: #c62828'] * len(row)
    elif status == 'Atenção':
        return ['background-color: #fff8e1; color: #f57f17'] * len(row)
    elif 'Erro' in status:
        return ['background-color: #fce4ec; color: #c62828'] * len(row)
    else:
        return ['background-color: #e8f5e9; color: #2e7d32'] * len(row)


def exportar_excel(df: pd.DataFrame) -> BytesIO:
    """Exporta o DataFrame para Excel."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Certificados')
    output.seek(0)
    return output


def exportar_cadastros_csv() -> bytes:
    """Exporta cadastros de clientes para CSV."""
    clientes = db.get_todos_clientes()
    if clientes:
        df = pd.DataFrame(clientes)
        df = df[['codigo', 'razao_social', 'email', 'telefone', 'responsavel', 'observacoes']]
        return df.to_csv(index=False).encode('utf-8')
    return "codigo,razao_social,email,telefone,responsavel,observacoes\n".encode('utf-8')


def criar_grafico_vencimentos(df: pd.DataFrame) -> go.Figure:
    """Cria gráfico de barras com certificados por mês de vencimento."""
    df_validos = df[~df['Status'].str.contains('Erro', na=False)].copy()
    
    if df_validos.empty:
        fig = go.Figure()
        fig.add_annotation(text="Sem dados para exibir", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    df_validos['Vencimento_dt'] = pd.to_datetime(df_validos['Vencimento'], format='%d/%m/%Y')
    df_validos['Mes_Ano'] = df_validos['Vencimento_dt'].dt.to_period('M').astype(str)
    
    contagem = df_validos.groupby('Mes_Ano').size().reset_index(name='Quantidade')
    
    cores = []
    hoje = datetime.now()
    for mes in contagem['Mes_Ano']:
        ano, mes_num = mes.split('-')
        data_mes = datetime(int(ano), int(mes_num), 1)
        if data_mes < hoje:
            cores.append('#ef5350')
        elif (data_mes - hoje).days <= 30:
            cores.append('#ffca28')
        else:
            cores.append('#66bb6a')
    
    fig = go.Figure(data=[
        go.Bar(
            x=contagem['Mes_Ano'],
            y=contagem['Quantidade'],
            marker_color=cores,
            text=contagem['Quantidade'],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Certificados por Mês de Vencimento",
        xaxis_title="Mês/Ano",
        yaxis_title="Quantidade",
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig


def obter_destinatarios_elegiveis(df: pd.DataFrame, dias_limite: int) -> List[Dict[str, Any]]:
    """Obtém lista de destinatários elegíveis para notificação."""
    destinatarios = []
    clientes_db = {c["codigo"]: c for c in db.get_todos_clientes()}
    
    for _, row in df.iterrows():
        codigo = row['Código']
        dias = row['Dias para Vencer']
        status = row['Status']
        
        if 'Erro' in status or dias is None:
            continue
        
        if dias > dias_limite:
            continue
        
        cliente = clientes_db.get(codigo)
        if not cliente or not cliente.get('email'):
            continue
        
        if not db.pode_enviar_notificacao(codigo):
            continue
        
        destinatarios.append({
            'codigo': codigo,
            'cliente': row['Cliente'],
            'email': cliente['email'],
            'dias': dias,
            'vencimento': row['Vencimento']
        })
    
    return destinatarios


def pagina_manual():
    """Renderiza a página do manual do usuário (HTML)."""
    st.markdown(render_header("Manual do Usuário", "Consulte o guia de uso do sistema"), unsafe_allow_html=True)
    
    if os.path.exists(CAMINHO_MANUAL_HTML):
        with open(CAMINHO_MANUAL_HTML, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=800, scrolling=True)
    else:
        st.warning(f"Arquivo do manual não encontrado: `{CAMINHO_MANUAL_HTML}`")
    
    st.markdown("---")
    if st.button("← Voltar ao Dashboard"):
        st.session_state.pagina = "dashboard"
        st.rerun()


def pagina_configuracoes():
    """Renderiza a página de configurações."""
    configs = db.get_todas_configuracoes()
    tema_escuro = configs.get("tema_escuro", "false") == "true"
    
    st.markdown(render_header("Configurações", "Gerencie as configurações do sistema"), unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📧 Email SMTP", "🔔 Notificações", "📁 Importar/Exportar", "ℹ️ Sobre"])
    
    with tab1:
        st.subheader("Configuração do Servidor SMTP (Gmail)")
        
        st.info("""
        **Como obter a senha de aplicativo do Google:**
        1. Acesse [myaccount.google.com](https://myaccount.google.com)
        2. Vá em Segurança → Verificação em duas etapas (ative se necessário)
        3. Em Senhas de app, crie uma nova senha para "Email"
        4. Copie a senha de 16 caracteres gerada
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            smtp_email = st.text_input(
                "Email do Remetente",
                value=configs.get("smtp_email", ""),
                placeholder="seu-email@gmail.com"
            )
        
        with col2:
            smtp_senha_atual = db.decode_senha(configs.get("smtp_senha", ""))
            smtp_senha = st.text_input(
                "Senha de Aplicativo",
                value=smtp_senha_atual,
                type="password",
                placeholder="xxxx xxxx xxxx xxxx"
            )
        
        nome_escritorio = st.text_input(
            "Nome do Escritório (aparece no rodapé do email)",
            value=configs.get("nome_escritorio", "Escritório de Contabilidade")
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar SMTP", type="primary", width="stretch"):
                db.salvar_configuracoes({
                    "smtp_email": smtp_email,
                    "smtp_senha": db.encode_senha(smtp_senha),
                    "nome_escritorio": nome_escritorio
                })
                st.success("Configurações salvas!")
        
        with col2:
            if st.button("🔌 Testar Conexão", width="stretch"):
                if smtp_email and smtp_senha:
                    with st.spinner("Testando..."):
                        sucesso, msg = email_svc.testar_conexao_smtp(smtp_email, smtp_senha)
                        if sucesso:
                            st.success(msg)
                        else:
                            st.error(msg)
                else:
                    st.warning("Preencha email e senha.")
        
        with col3:
            if st.button("👁️ Preview Email", width="stretch"):
                st.session_state.mostrar_preview_email = True
        
        # Preview do Email
        if st.session_state.get("mostrar_preview_email"):
            st.markdown("---")
            st.subheader("Preview do Email")
            html_preview = email_svc.get_email_template_html(
                razao_social="EMPRESA EXEMPLO LTDA",
                dias_restantes=15,
                data_vencimento="15/02/2026",
                nome_escritorio=nome_escritorio or "Escritório de Contabilidade"
            )
            components.html(html_preview, height=600, scrolling=True)
            if st.button("Fechar Preview"):
                st.session_state.mostrar_preview_email = False
                st.rerun()
    
    with tab2:
        st.subheader("Configurações de Notificação")
        
        dias_notificacao = st.slider(
            "Notificar certificados que vencem em até (dias):",
            min_value=1,
            max_value=90,
            value=int(configs.get("dias_notificacao", "30"))
        )
        
        notificacao_auto = st.toggle(
            "Enviar notificações automaticamente ao abrir o sistema",
            value=configs.get("notificacao_automatica", "false") == "true"
        )
        
        if st.button("💾 Salvar Notificações", type="primary"):
            db.salvar_configuracoes({
                "dias_notificacao": str(dias_notificacao),
                "notificacao_automatica": "true" if notificacao_auto else "false"
            })
            st.success("Salvo!")
        
        st.markdown("---")
        st.subheader("Envio Manual de Notificações")
        
        # Botão de enviar com confirmação
        if st.button("📤 Preparar Envio de Notificações", width="stretch"):
            df = processar_certificados(CAMINHO_CERTIFICADOS)
            destinatarios = obter_destinatarios_elegiveis(df, dias_notificacao)
            
            if destinatarios:
                st.session_state.mostrar_confirmacao_envio = True
                st.session_state.destinatarios_pendentes = destinatarios
            else:
                st.info("Nenhum certificado elegível para notificação.")
        
        # Modal de confirmação
        if st.session_state.get("mostrar_confirmacao_envio"):
            destinatarios = st.session_state.get("destinatarios_pendentes", [])
            
            with st.container():
                st.warning(f"**Confirmar envio de {len(destinatarios)} notificação(ões)?**")
                
                df_dest = pd.DataFrame(destinatarios)
                st.dataframe(
                    df_dest[['cliente', 'email', 'dias', 'vencimento']],
                    hide_index=True,
                    column_config={
                        "cliente": "Cliente",
                        "email": "Email",
                        "dias": "Dias",
                        "vencimento": "Vencimento"
                    }
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✅ Confirmar Envio", type="primary", width="stretch"):
                        with st.spinner("Enviando notificações..."):
                            sucesso = 0
                            erros = 0
                            for dest in destinatarios:
                                ok, _ = email_svc.enviar_notificacao(
                                    codigo_cliente=dest['codigo'],
                                    email_destinatario=dest['email'],
                                    razao_social=dest['cliente'],
                                    dias_restantes=dest['dias'],
                                    data_vencimento=dest['vencimento']
                                )
                                if ok:
                                    sucesso += 1
                                else:
                                    erros += 1
                        
                        st.session_state.mostrar_confirmacao_envio = False
                        st.success(f"Enviados: {sucesso} | Erros: {erros}")
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancelar", width="stretch"):
                        st.session_state.mostrar_confirmacao_envio = False
                        st.rerun()
    
    with tab3:
        st.subheader("Importar/Exportar Cadastros")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Exportar Cadastros")
            st.markdown("Baixe todos os cadastros de clientes em CSV.")
            
            csv_data = exportar_cadastros_csv()
            st.download_button(
                "📥 Exportar CSV",
                data=csv_data,
                file_name=f"cadastros_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                width="stretch"
            )
        
        with col2:
            st.markdown("##### Importar Cadastros")
            st.markdown("Importe cadastros de um arquivo CSV.")
            
            arquivo = st.file_uploader("Selecione o arquivo CSV", type=['csv'])
            
            if arquivo:
                try:
                    df_import = pd.read_csv(arquivo)
                    st.dataframe(df_import, hide_index=True)
                    
                    if st.button("✅ Confirmar Importação", type="primary", width="stretch"):
                        importados = 0
                        for _, row in df_import.iterrows():
                            if db.salvar_cliente(
                                codigo=str(row.get('codigo', '')),
                                razao_social=str(row.get('razao_social', '')),
                                email=str(row.get('email', '')) if pd.notna(row.get('email')) else None,
                                telefone=str(row.get('telefone', '')) if pd.notna(row.get('telefone')) else None,
                                responsavel=str(row.get('responsavel', '')) if pd.notna(row.get('responsavel')) else None,
                                observacoes=str(row.get('observacoes', '')) if pd.notna(row.get('observacoes')) else None
                            ):
                                importados += 1
                        st.success(f"{importados} cadastros importados!")
                except Exception as e:
                    st.error(f"Erro ao ler arquivo: {e}")
        
        st.markdown("---")
        st.markdown("**Formato do CSV:**")
        st.code("codigo,razao_social,email,telefone,responsavel,observacoes")
    
    with tab4:
        st.subheader("Sobre o Sistema")
        
        stats = db.get_estatisticas()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Versão", VERSAO)
            st.metric("Clientes Cadastrados", stats["total_clientes"])
        
        with col2:
            st.metric("Clientes com Email", stats["clientes_com_email"])
            st.metric("Notificações Enviadas", stats["total_notificacoes"])
        
        st.markdown("---")
        st.markdown(f"**Pasta de Certificados:** `{CAMINHO_CERTIFICADOS}`")
        
        st.markdown("---")
        st.subheader("Atalhos Úteis")
        st.markdown("""
        | Ação | Atalho |
        |------|--------|
        | Atualizar página | `F5` ou `Ctrl+R` |
        | Buscar na tabela | `Ctrl+F` |
        | Selecionar linha | Clique na linha da tabela |
        """)
        
        st.markdown("---")
        st.subheader("Histórico de Notificações")
        
        historico = db.get_historico_notificacoes(20)
        if historico:
            df_hist = pd.DataFrame(historico)
            df_hist = df_hist[['data_envio', 'codigo_cliente', 'tipo', 'sucesso', 'mensagem_erro']]
            df_hist.columns = ['Data', 'Código', 'Tipo', 'Sucesso', 'Erro']
            st.dataframe(df_hist, width="stretch", hide_index=True)
        else:
            st.info("Nenhuma notificação enviada ainda.")
    
    st.markdown("---")
    if st.button("← Voltar ao Dashboard"):
        st.session_state.pagina = "dashboard"
        st.rerun()


def modal_cadastro_cliente(codigo: str, razao_social: str):
    """Renderiza o modal de cadastro/edição de cliente."""
    cliente = db.get_cliente(codigo)
    
    # Valores iniciais (do banco ou vazios)
    email_inicial = (cliente.get("email") or "").strip() if cliente else ""
    telefone_inicial = (cliente.get("telefone") or "").strip() if cliente else ""
    responsavel_inicial = (cliente.get("responsavel") or "").strip() if cliente else ""
    observacoes_inicial = (cliente.get("observacoes") or "").strip() if cliente else ""
    
    st.subheader(f"📝 Cadastro: {razao_social}")
    
    # Form garante que os valores só são lidos no submit, evitando estado inconsistente
    with st.form(key=f"form_cadastro_{codigo}", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Código", value=codigo, disabled=True, key=f"cad_codigo_{codigo}")
            email_cliente = st.text_input(
                "Email *",
                value=email_inicial,
                placeholder="cliente@email.com",
                key=f"cad_email_{codigo}"
            )
            telefone = st.text_input(
                "Telefone",
                value=telefone_inicial,
                placeholder="(11) 99999-9999",
                key=f"cad_telefone_{codigo}"
            )
        
        with col2:
            st.text_input("Razão Social", value=razao_social, disabled=True, key=f"cad_razao_{codigo}")
            responsavel = st.text_input(
                "Responsável",
                value=responsavel_inicial,
                placeholder="Nome do responsável",
                key=f"cad_responsavel_{codigo}"
            )
        
        observacoes = st.text_area(
            "Observações",
            value=observacoes_inicial,
            placeholder="Anotações sobre o cliente...",
            key=f"cad_obs_{codigo}"
        )
        
        col_btn1, col_btn2, _ = st.columns([1, 1, 2])
        
        with col_btn1:
            submitted_salvar = st.form_submit_button("💾 Salvar")
        with col_btn2:
            submitted_cancelar = st.form_submit_button("❌ Cancelar")
    
    # Tratamento fora do form para poder fazer rerun
    if submitted_cancelar:
        st.session_state.cliente_selecionado = None
        st.rerun()
    
    if submitted_salvar:
        # Normaliza campos em branco para None
        email_cliente = (email_cliente or "").strip() or None
        telefone = (telefone or "").strip() or None
        responsavel = (responsavel or "").strip() or None
        observacoes = (observacoes or "").strip() or None
        
        if db.salvar_cliente(
            codigo=codigo,
            razao_social=razao_social,
            email=email_cliente,
            telefone=telefone,
            responsavel=responsavel,
            observacoes=observacoes
        ):
            st.success("Cliente salvo com sucesso!")
            st.session_state.cliente_selecionado = None
            st.rerun()
        else:
            st.error("Erro ao salvar cliente. Tente novamente.")


def renderizar_painel_acoes_pendentes(df: pd.DataFrame, clientes_db: dict):
    """Renderiza o painel de ações pendentes."""
    vencidos = df[df['Status'] == 'Vencido']
    atencao = df[df['Status'] == 'Atenção']
    sem_email = df[df['Email'] == "—"]
    
    # Só mostra se houver ações pendentes
    if len(vencidos) == 0 and len(atencao) == 0 and len(sem_email) == 0:
        return
    
    st.markdown("### ⚠️ Ações Pendentes")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if len(vencidos) > 0:
            st.markdown(
                render_action_card(
                    f"🔴 {len(vencidos)} Certificado(s) Vencido(s)",
                    "Requerem renovação imediata!",
                    "danger"
                ),
                unsafe_allow_html=True
            )
            with st.expander("Ver detalhes"):
                st.dataframe(
                    vencidos[['Código', 'Cliente', 'Vencimento']],
                    hide_index=True,
                    width="stretch"
                )
    
    with col2:
        if len(atencao) > 0:
            st.markdown(
                render_action_card(
                    f"🟡 {len(atencao)} Vencem em 30 dias",
                    "Programe a renovação.",
                    "warning"
                ),
                unsafe_allow_html=True
            )
            with st.expander("Ver detalhes"):
                st.dataframe(
                    atencao[['Código', 'Cliente', 'Dias para Vencer']],
                    hide_index=True,
                    width="stretch"
                )
    
    with col3:
        if len(sem_email) > 0:
            st.markdown(
                render_action_card(
                    f"📧 {len(sem_email)} Sem Email",
                    "Não receberão notificações.",
                    "info"
                ),
                unsafe_allow_html=True
            )
            with st.expander("Ver detalhes"):
                st.dataframe(
                    sem_email[['Código', 'Cliente']],
                    hide_index=True,
                    width="stretch"
                )
    
    st.markdown("---")


def pagina_dashboard():
    """Renderiza a página principal do dashboard."""
    # Header
    st.markdown(render_header(
        "Gerenciador de Certificados Digitais",
        "Monitore a validade dos certificados e receba alertas de vencimento"
    ), unsafe_allow_html=True)
    
    # Verifica se existe um cliente selecionado para edição
    if st.session_state.get("cliente_selecionado"):
        cliente_info = st.session_state.cliente_selecionado
        with st.expander("📝 Cadastro de Cliente", expanded=True):
            modal_cadastro_cliente(cliente_info["codigo"], cliente_info["cliente"])
        st.markdown("---")
    
    # Verifica caminho
    if not os.path.exists(CAMINHO_CERTIFICADOS):
        st.error(f"O caminho especificado não existe: `{CAMINHO_CERTIFICADOS}`")
        return
    
    # Processa certificados (com progresso na primeira vez)
    if "df_certificados" not in st.session_state:
        df = processar_certificados_com_progresso(CAMINHO_CERTIFICADOS)
        st.session_state.df_certificados = df
    else:
        df = processar_certificados(CAMINHO_CERTIFICADOS)
    
    if df.empty:
        st.warning("Nenhum arquivo .pfx encontrado na pasta especificada.")
        return
    
    # Executa notificações automáticas na inicialização
    if "notificacoes_enviadas" not in st.session_state:
        configs = db.get_todas_configuracoes()
        if configs.get("notificacao_automatica") == "true":
            dias_limite = int(configs.get("dias_notificacao", "30"))
            resultado = email_svc.processar_notificacoes_automaticas(
                df.to_dict('records'),
                dias_limite=dias_limite
            )
            st.session_state.notificacoes_enviadas = True
            
            if resultado["enviados_sucesso"] > 0:
                st.toast(f"📧 {resultado['enviados_sucesso']} notificação(ões) enviada(s)!")
    
    # Adiciona coluna de email cadastrado
    clientes_db = {c["codigo"]: c for c in db.get_todos_clientes()}
    df["Email"] = df["Código"].apply(
        lambda x: "✓" if x in clientes_db and clientes_db[x].get("email") else "—"
    )
    
    # Métricas
    total = len(df)
    vencidos = len(df[df['Status'] == 'Vencido'])
    atencao = len(df[df['Status'] == 'Atenção'])
    validos = len(df[df['Status'] == 'Válido'])
    erros = len(df[df['Status'].str.contains('Erro', na=False)])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(render_metric_card(total, "Total", "total"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_metric_card(vencidos, "Vencidos", "vencido"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_metric_card(atencao, "Atenção", "atencao"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_metric_card(validos, "Válidos", "valido"), unsafe_allow_html=True)
    with col5:
        st.markdown(render_metric_card(erros, "Erros", "erro"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Painel de Ações Pendentes
    renderizar_painel_acoes_pendentes(df, clientes_db)
    
    # Gráfico
    with st.expander("📊 Gráfico de Vencimentos", expanded=False):
        fig = criar_grafico_vencimentos(df)
        st.plotly_chart(fig, width="stretch")
    
    # Filtros e Busca
    st.markdown("### 📋 Certificados")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        busca = st.text_input(
            "🔍 Buscar",
            placeholder="Digite código ou nome do cliente...",
            label_visibility="collapsed"
        )
    
    with col2:
        filtro_status = st.selectbox(
            "Filtrar por Status",
            ["Todos", "Vencido", "Atenção", "Válido", "Erro"],
            label_visibility="collapsed"
        )
    
    with col3:
        filtro_email = st.selectbox(
            "Filtrar por Email",
            ["Todos", "Com Email", "Sem Email"],
            label_visibility="collapsed"
        )
    
    # Aplica filtros
    df_filtrado = df.copy()
    
    if busca:
        busca_lower = busca.lower()
        df_filtrado = df_filtrado[
            df_filtrado['Código'].str.lower().str.contains(busca_lower, na=False) |
            df_filtrado['Cliente'].str.lower().str.contains(busca_lower, na=False)
        ]
    
    if filtro_status != "Todos":
        if filtro_status == "Erro":
            df_filtrado = df_filtrado[df_filtrado['Status'].str.contains('Erro', na=False)]
        else:
            df_filtrado = df_filtrado[df_filtrado['Status'] == filtro_status]
    
    if filtro_email == "Com Email":
        df_filtrado = df_filtrado[df_filtrado['Email'] == "✓"]
    elif filtro_email == "Sem Email":
        df_filtrado = df_filtrado[df_filtrado['Email'] == "—"]
    
    # Botão de exportar (key única evita MediaFileStorageError ao navegar/rerun)
    col1, col2 = st.columns([1, 4])
    
    with col1:
        excel_data = exportar_excel(df_filtrado)
        st.download_button(
            "📥 Exportar Excel",
            data=excel_data,
            file_name=f"certificados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"download_excel_{int(time.time() * 1000)}"
        )
    
    st.markdown(f"*Exibindo {len(df_filtrado)} de {len(df)} certificados. Clique em uma linha para editar.*")
    
    # Tabela interativa com seleção de linha
    df_display = df_filtrado[['Código', 'Cliente', 'Vencimento', 'Dias para Vencer', 'Status', 'Email']].reset_index(drop=True)
    
    event = st.dataframe(
        df_display.style.apply(aplicar_estilo, axis=1),
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "Código": st.column_config.TextColumn("Código", width="small"),
            "Cliente": st.column_config.TextColumn("Cliente", width="large"),
            "Vencimento": st.column_config.TextColumn("Vencimento", width="small"),
            "Dias para Vencer": st.column_config.NumberColumn("Dias", width="small", format="%d"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Email": st.column_config.TextColumn("📧", width="small"),
        },
        height=400
    )
    
    # Verifica se uma linha foi selecionada
    if event.selection and event.selection.rows:
        idx = event.selection.rows[0]
        if idx < len(df_filtrado):
            linha = df_filtrado.iloc[idx]
            codigo = linha['Código']
            cliente = linha['Cliente']
            
            if codigo != '?':  # Ignora erros
                st.session_state.cliente_selecionado = {
                    "codigo": codigo,
                    "cliente": cliente
                }
                st.rerun()
    
    # Rodapé
    st.markdown("---")
    st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | Versão {VERSAO}")


def main():
    """Função principal do aplicativo Streamlit."""
    
    # Configuração da página
    st.set_page_config(
        page_title="Gerenciador de Certificados",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Carrega configurações
    configs = db.get_todas_configuracoes()
    tema_escuro = configs.get("tema_escuro", "false") == "true"
    
    # Aplica CSS customizado
    st.markdown(get_css(tema_escuro), unsafe_allow_html=True)
    
    # Inicializa estado da sessão
    if "pagina" not in st.session_state:
        st.session_state.pagina = "dashboard"
    
    if "cliente_selecionado" not in st.session_state:
        st.session_state.cliente_selecionado = None
    
    # Calcula métricas para sidebar (apenas se estiver no dashboard)
    vencidos = 0
    atencao = 0
    sem_email = 0
    
    if os.path.exists(CAMINHO_CERTIFICADOS):
        df_sidebar = processar_certificados(CAMINHO_CERTIFICADOS)
        if not df_sidebar.empty:
            clientes_db = {c["codigo"]: c for c in db.get_todos_clientes()}
            df_sidebar["Email"] = df_sidebar["Código"].apply(
                lambda x: "✓" if x in clientes_db and clientes_db[x].get("email") else "—"
            )
            vencidos = len(df_sidebar[df_sidebar['Status'] == 'Vencido'])
            atencao = len(df_sidebar[df_sidebar['Status'] == 'Atenção'])
            sem_email = len(df_sidebar[df_sidebar['Email'] == "—"])
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h3>🔐 Certificados</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Dashboard", width="stretch", 
                     type="primary" if st.session_state.pagina == "dashboard" else "secondary"):
            st.session_state.pagina = "dashboard"
            st.session_state.cliente_selecionado = None
            st.rerun()
        
        if st.button("⚙️ Configurações", width="stretch",
                     type="primary" if st.session_state.pagina == "config" else "secondary"):
            st.session_state.pagina = "config"
            st.rerun()
        
        if st.button("📖 Manual do Usuário", width="stretch",
                     type="primary" if st.session_state.pagina == "manual" else "secondary"):
            st.session_state.pagina = "manual"
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🔄 Atualizar Dados", width="stretch"):
            st.cache_data.clear()
            if "df_certificados" in st.session_state:
                del st.session_state.df_certificados
            st.session_state.notificacoes_enviadas = False
            st.rerun()
        
        st.markdown("---")
        
        # Badges de alertas
        st.markdown("**🚨 Alertas**")
        
        badges_html = ""
        if vencidos > 0:
            badges_html += render_badge(f"{vencidos} Vencidos", "danger")
        if atencao > 0:
            badges_html += render_badge(f"{atencao} Atenção", "warning")
        if sem_email > 0:
            badges_html += render_badge(f"{sem_email} Sem Email", "muted")
        
        if badges_html:
            st.markdown(badges_html, unsafe_allow_html=True)
        else:
            st.markdown("✅ Nenhum alerta")
        
        st.markdown("---")
        
        # Toggle tema escuro
        novo_tema = st.toggle("🌙 Tema Escuro", value=tema_escuro)
        if novo_tema != tema_escuro:
            db.salvar_configuracao("tema_escuro", "true" if novo_tema else "false")
            st.rerun()
        
        st.markdown("---")
        
        # Info rápido
        stats = db.get_estatisticas()
        st.markdown(f"""
        **📊 Resumo**
        - Cadastrados: {stats['total_clientes']}
        - Com email: {stats['clientes_com_email']}
        - Notif. (mês): {stats['notificacoes_mes']}
        """)
    
    # Renderiza página atual
    if st.session_state.pagina == "config":
        pagina_configuracoes()
    elif st.session_state.pagina == "manual":
        pagina_manual()
    else:
        pagina_dashboard()


if __name__ == "__main__":
    main()
