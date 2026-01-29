"""
Módulo de serviço de email para o Gerenciador de Certificados.
Gerencia envio de notificações via SMTP Gmail.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime

import database as db


def get_email_template_html(
    razao_social: str,
    dias_restantes: int,
    data_vencimento: str,
    nome_escritorio: str
) -> str:
    """Retorna o template HTML do email de notificação."""
    
    # Define a cor baseada na urgência
    if dias_restantes <= 0:
        cor_destaque = "#dc3545"  # Vermelho - Vencido
        status_texto = "VENCIDO"
        mensagem_urgencia = "O certificado já está vencido e precisa ser renovado imediatamente."
    elif dias_restantes <= 7:
        cor_destaque = "#dc3545"  # Vermelho - Muito urgente
        status_texto = "URGENTE"
        mensagem_urgencia = "O prazo está muito próximo. Por favor, tome providências imediatas."
    elif dias_restantes <= 30:
        cor_destaque = "#ffc107"  # Amarelo - Atenção
        status_texto = "ATENÇÃO"
        mensagem_urgencia = "Recomendamos que a renovação seja providenciada o quanto antes."
    else:
        cor_destaque = "#28a745"  # Verde - Informativo
        status_texto = "AVISO"
        mensagem_urgencia = "Este é um aviso preventivo para que você possa se programar."
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
            <!-- Header -->
            <tr>
                <td style="background: linear-gradient(135deg, #1E3A5F 0%, #3D5A80 100%); padding: 30px; text-align: center;">
                    <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🔐 Certificado Digital</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;">Notificação de Vencimento</p>
                </td>
            </tr>
            
            <!-- Status Badge -->
            <tr>
                <td style="padding: 30px 30px 20px 30px; text-align: center;">
                    <span style="display: inline-block; background-color: {cor_destaque}; color: white; padding: 8px 20px; border-radius: 20px; font-size: 12px; font-weight: bold; letter-spacing: 1px;">
                        {status_texto}
                    </span>
                </td>
            </tr>
            
            <!-- Conteúdo Principal -->
            <tr>
                <td style="padding: 0 30px 30px 30px;">
                    <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        Prezado(a),
                    </p>
                    <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                        O certificado digital da empresa <strong>{razao_social}</strong> 
                        {"venceu" if dias_restantes <= 0 else "vencerá"} 
                        {f"há {abs(dias_restantes)} dias" if dias_restantes < 0 else f"em <strong style='color: {cor_destaque};'>{dias_restantes} dias</strong>"}.
                    </p>
                    
                    <!-- Card de Informações -->
                    <table width="100%" style="background-color: #f8f9fa; border-radius: 8px; margin: 20px 0;">
                        <tr>
                            <td style="padding: 20px;">
                                <table width="100%">
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">
                                            <span style="color: #6c757d; font-size: 14px;">Empresa:</span><br>
                                            <strong style="color: #333; font-size: 16px;">{razao_social}</strong>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">
                                            <span style="color: #6c757d; font-size: 14px;">Data de Vencimento:</span><br>
                                            <strong style="color: {cor_destaque}; font-size: 16px;">{data_vencimento}</strong>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #6c757d; font-size: 14px;">Dias Restantes:</span><br>
                                            <strong style="color: {cor_destaque}; font-size: 16px;">{dias_restantes if dias_restantes >= 0 else "Vencido"}</strong>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    
                    <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 20px 0;">
                        {mensagem_urgencia}
                    </p>
                    
                    <p style="color: #333; font-size: 16px; line-height: 1.6; margin: 20px 0 0 0;">
                        Por favor, providencie a renovação do certificado digital para evitar interrupções nos serviços que dependem dele.
                    </p>
                </td>
            </tr>
            
            <!-- Footer -->
            <tr>
                <td style="background-color: #f8f9fa; padding: 20px 30px; border-top: 1px solid #e9ecef;">
                    <p style="color: #6c757d; font-size: 14px; margin: 0; text-align: center;">
                        Atenciosamente,<br>
                        <strong style="color: #333;">{nome_escritorio}</strong>
                    </p>
                </td>
            </tr>
            
            <!-- Rodapé -->
            <tr>
                <td style="padding: 15px 30px; text-align: center;">
                    <p style="color: #999; font-size: 12px; margin: 0;">
                        Este é um email automático enviado pelo Sistema de Gerenciamento de Certificados Digitais.
                    </p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def testar_conexao_smtp(email: str, senha: str) -> Tuple[bool, str]:
    """
    Testa a conexão com o servidor SMTP do Gmail.
    
    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, senha)
        server.quit()
        return True, "Conexão estabelecida com sucesso!"
    except smtplib.SMTPAuthenticationError:
        return False, "Erro de autenticação. Verifique o email e a senha de aplicativo."
    except smtplib.SMTPConnectError:
        return False, "Não foi possível conectar ao servidor SMTP."
    except Exception as e:
        return False, f"Erro: {str(e)}"


def enviar_email(
    destinatario: str,
    assunto: str,
    corpo_html: str,
    remetente: str,
    senha: str
) -> Tuple[bool, str]:
    """
    Envia um email via SMTP Gmail.
    
    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    try:
        # Cria a mensagem
        msg = MIMEMultipart("alternative")
        msg["Subject"] = assunto
        msg["From"] = remetente
        msg["To"] = destinatario
        
        # Anexa o corpo HTML
        parte_html = MIMEText(corpo_html, "html", "utf-8")
        msg.attach(parte_html)
        
        # Conecta e envia
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
        
        return True, "Email enviado com sucesso!"
    except smtplib.SMTPAuthenticationError:
        return False, "Erro de autenticação SMTP."
    except smtplib.SMTPRecipientsRefused:
        return False, "Destinatário inválido ou recusado."
    except Exception as e:
        return False, f"Erro ao enviar email: {str(e)}"


def enviar_notificacao(
    codigo_cliente: str,
    email_destinatario: str,
    razao_social: str,
    dias_restantes: int,
    data_vencimento: str
) -> Tuple[bool, str]:
    """
    Envia uma notificação de vencimento para um cliente.
    
    Returns:
        Tupla (sucesso: bool, mensagem: str)
    """
    # Busca configurações
    configs = db.get_todas_configuracoes()
    
    smtp_email = configs.get("smtp_email", "")
    smtp_senha_encoded = configs.get("smtp_senha", "")
    nome_escritorio = configs.get("nome_escritorio", "Escritório de Contabilidade")
    
    if not smtp_email or not smtp_senha_encoded:
        return False, "Configurações de SMTP não definidas."
    
    # Decodifica a senha
    smtp_senha = db.decode_senha(smtp_senha_encoded)
    
    if not smtp_senha:
        return False, "Senha SMTP inválida."
    
    # Gera o assunto
    if dias_restantes <= 0:
        assunto = f"⚠️ URGENTE: Certificado Digital VENCIDO - {razao_social}"
    elif dias_restantes <= 7:
        assunto = f"⚠️ URGENTE: Certificado vence em {dias_restantes} dias - {razao_social}"
    else:
        assunto = f"📋 Aviso: Certificado vence em {dias_restantes} dias - {razao_social}"
    
    # Gera o corpo do email
    corpo_html = get_email_template_html(
        razao_social=razao_social,
        dias_restantes=dias_restantes,
        data_vencimento=data_vencimento,
        nome_escritorio=nome_escritorio
    )
    
    # Envia o email
    sucesso, mensagem = enviar_email(
        destinatario=email_destinatario,
        assunto=assunto,
        corpo_html=corpo_html,
        remetente=smtp_email,
        senha=smtp_senha
    )
    
    # Registra no histórico
    tipo = "vencido" if dias_restantes <= 0 else "vencimento_proximo"
    db.registrar_notificacao(
        codigo_cliente=codigo_cliente,
        tipo=tipo,
        sucesso=sucesso,
        mensagem_erro=None if sucesso else mensagem
    )
    
    return sucesso, mensagem


def processar_notificacoes_automaticas(
    certificados: List[Dict[str, Any]],
    dias_limite: int = 30
) -> Dict[str, Any]:
    """
    Processa e envia notificações automáticas para certificados próximos ao vencimento.
    
    Args:
        certificados: Lista de certificados com dados do DataFrame
        dias_limite: Enviar para certificados que vencem em até X dias
        
    Returns:
        Dicionário com estatísticas do processamento
    """
    resultados = {
        "total_processados": 0,
        "enviados_sucesso": 0,
        "enviados_erro": 0,
        "ignorados_sem_email": 0,
        "ignorados_ja_enviado": 0,
        "detalhes": []
    }
    
    # Verifica se notificação automática está ativada
    configs = db.get_todas_configuracoes()
    if configs.get("notificacao_automatica", "false") != "true":
        return resultados
    
    # Verifica se SMTP está configurado
    if not configs.get("smtp_email") or not configs.get("smtp_senha"):
        return resultados
    
    for cert in certificados:
        codigo = cert.get("Código", "")
        cliente_nome = cert.get("Cliente", "")
        dias_para_vencer = cert.get("Dias para Vencer")
        vencimento = cert.get("Vencimento", "")
        status = cert.get("Status", "")
        
        # Ignora certificados com erro
        if "Erro" in status:
            continue
        
        # Verifica se está dentro do limite de dias
        if dias_para_vencer is None or dias_para_vencer > dias_limite:
            continue
        
        resultados["total_processados"] += 1
        
        # Busca dados do cliente no banco
        cliente = db.get_cliente(codigo)
        
        if not cliente or not cliente.get("email"):
            resultados["ignorados_sem_email"] += 1
            resultados["detalhes"].append({
                "codigo": codigo,
                "cliente": cliente_nome,
                "status": "sem_email",
                "mensagem": "Cliente sem email cadastrado"
            })
            continue
        
        # Verifica se já foi enviada notificação recentemente
        if not db.pode_enviar_notificacao(codigo):
            resultados["ignorados_ja_enviado"] += 1
            resultados["detalhes"].append({
                "codigo": codigo,
                "cliente": cliente_nome,
                "status": "ja_enviado",
                "mensagem": "Notificação já enviada nos últimos 7 dias"
            })
            continue
        
        # Envia a notificação
        sucesso, mensagem = enviar_notificacao(
            codigo_cliente=codigo,
            email_destinatario=cliente["email"],
            razao_social=cliente_nome,
            dias_restantes=dias_para_vencer,
            data_vencimento=vencimento
        )
        
        if sucesso:
            resultados["enviados_sucesso"] += 1
            resultados["detalhes"].append({
                "codigo": codigo,
                "cliente": cliente_nome,
                "status": "enviado",
                "mensagem": f"Email enviado para {cliente['email']}"
            })
        else:
            resultados["enviados_erro"] += 1
            resultados["detalhes"].append({
                "codigo": codigo,
                "cliente": cliente_nome,
                "status": "erro",
                "mensagem": mensagem
            })
    
    return resultados
