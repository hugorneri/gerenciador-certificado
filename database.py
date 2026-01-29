"""
Módulo de banco de dados SQLite para o Gerenciador de Certificados.
Gerencia clientes, configurações e histórico de notificações.
"""

import os
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import base64

# Caminho do banco de dados
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DATA_DIR, "certificados.db")


def get_connection() -> sqlite3.Connection:
    """Retorna uma conexão com o banco de dados."""
    # Cria o diretório data se não existir
    os.makedirs(DATA_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Inicializa o banco de dados criando as tabelas necessárias."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela de clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            razao_social TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            responsavel TEXT,
            observacoes TEXT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao DATETIME
        )
    """)
    
    # Tabela de configurações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    """)
    
    # Tabela de histórico de notificações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_cliente TEXT NOT NULL,
            data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
            tipo TEXT,
            sucesso BOOLEAN,
            mensagem_erro TEXT
        )
    """)
    
    # Insere configurações padrão se não existirem
    configuracoes_padrao = [
        ("smtp_email", ""),
        ("smtp_senha", ""),
        ("dias_notificacao", "30"),
        ("notificacao_automatica", "false"),
        ("nome_escritorio", "Escritório de Contabilidade"),
    ]
    
    for chave, valor in configuracoes_padrao:
        cursor.execute("""
            INSERT OR IGNORE INTO configuracoes (chave, valor) VALUES (?, ?)
        """, (chave, valor))
    
    conn.commit()
    conn.close()


# ==================== FUNÇÕES DE CLIENTES ====================

def get_cliente(codigo: str) -> Optional[Dict[str, Any]]:
    """Busca um cliente pelo código."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM clientes WHERE codigo = ?", (codigo,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def get_todos_clientes() -> List[Dict[str, Any]]:
    """Retorna todos os clientes cadastrados."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM clientes ORDER BY codigo")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def salvar_cliente(
    codigo: str,
    razao_social: str,
    email: Optional[str] = None,
    telefone: Optional[str] = None,
    responsavel: Optional[str] = None,
    observacoes: Optional[str] = None
) -> bool:
    """Salva ou atualiza um cliente."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Verifica se já existe
        cursor.execute("SELECT id FROM clientes WHERE codigo = ?", (codigo,))
        existe = cursor.fetchone()
        
        if existe:
            # Atualiza
            cursor.execute("""
                UPDATE clientes 
                SET razao_social = ?, email = ?, telefone = ?, 
                    responsavel = ?, observacoes = ?, data_atualizacao = ?
                WHERE codigo = ?
            """, (razao_social, email, telefone, responsavel, observacoes, 
                  datetime.now().isoformat(), codigo))
        else:
            # Insere
            cursor.execute("""
                INSERT INTO clientes (codigo, razao_social, email, telefone, responsavel, observacoes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (codigo, razao_social, email, telefone, responsavel, observacoes))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        print(f"Erro ao salvar cliente: {e}")
        return False


def deletar_cliente(codigo: str) -> bool:
    """Deleta um cliente pelo código."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM clientes WHERE codigo = ?", (codigo,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


# ==================== FUNÇÕES DE CONFIGURAÇÕES ====================

def get_configuracao(chave: str) -> Optional[str]:
    """Busca uma configuração pelo nome da chave."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = ?", (chave,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return row["valor"]
    return None


def get_todas_configuracoes() -> Dict[str, str]:
    """Retorna todas as configurações como dicionário."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT chave, valor FROM configuracoes")
    rows = cursor.fetchall()
    conn.close()
    
    return {row["chave"]: row["valor"] for row in rows}


def salvar_configuracao(chave: str, valor: str) -> bool:
    """Salva ou atualiza uma configuração."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)
        """, (chave, valor))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def salvar_configuracoes(configs: Dict[str, str]) -> bool:
    """Salva múltiplas configurações de uma vez."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        for chave, valor in configs.items():
            cursor.execute("""
                INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)
            """, (chave, valor))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


# ==================== FUNÇÕES DE CRIPTOGRAFIA SIMPLES ====================

def encode_senha(senha: str) -> str:
    """Codifica a senha em base64 (ofuscação básica)."""
    if not senha:
        return ""
    return base64.b64encode(senha.encode()).decode()


def decode_senha(senha_encoded: str) -> str:
    """Decodifica a senha de base64."""
    if not senha_encoded:
        return ""
    try:
        return base64.b64decode(senha_encoded.encode()).decode()
    except Exception:
        return ""


# ==================== FUNÇÕES DE NOTIFICAÇÕES ====================

def registrar_notificacao(
    codigo_cliente: str,
    tipo: str,
    sucesso: bool,
    mensagem_erro: Optional[str] = None
) -> bool:
    """Registra uma notificação enviada no histórico."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO notificacoes (codigo_cliente, tipo, sucesso, mensagem_erro)
            VALUES (?, ?, ?, ?)
        """, (codigo_cliente, tipo, sucesso, mensagem_erro))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def get_ultima_notificacao(codigo_cliente: str) -> Optional[Dict[str, Any]]:
    """Retorna a última notificação enviada para um cliente."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM notificacoes 
        WHERE codigo_cliente = ? AND sucesso = 1
        ORDER BY data_envio DESC 
        LIMIT 1
    """, (codigo_cliente,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def pode_enviar_notificacao(codigo_cliente: str, dias_espera: int = 7) -> bool:
    """
    Verifica se pode enviar notificação para o cliente.
    Retorna False se já foi enviada uma notificação nos últimos X dias.
    """
    ultima = get_ultima_notificacao(codigo_cliente)
    
    if not ultima:
        return True
    
    try:
        data_envio = datetime.fromisoformat(ultima["data_envio"])
        limite = datetime.now() - timedelta(days=dias_espera)
        return data_envio < limite
    except Exception:
        return True


def get_historico_notificacoes(limite: int = 100) -> List[Dict[str, Any]]:
    """Retorna o histórico de notificações."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM notificacoes 
        ORDER BY data_envio DESC 
        LIMIT ?
    """, (limite,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_estatisticas() -> Dict[str, int]:
    """Retorna estatísticas do sistema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total de clientes
    cursor.execute("SELECT COUNT(*) as total FROM clientes")
    total_clientes = cursor.fetchone()["total"]
    
    # Clientes com email
    cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE email IS NOT NULL AND email != ''")
    clientes_com_email = cursor.fetchone()["total"]
    
    # Total de notificações enviadas
    cursor.execute("SELECT COUNT(*) as total FROM notificacoes WHERE sucesso = 1")
    total_notificacoes = cursor.fetchone()["total"]
    
    # Notificações este mês
    cursor.execute("""
        SELECT COUNT(*) as total FROM notificacoes 
        WHERE sucesso = 1 AND data_envio >= date('now', 'start of month')
    """)
    notificacoes_mes = cursor.fetchone()["total"]
    
    conn.close()
    
    return {
        "total_clientes": total_clientes,
        "clientes_com_email": clientes_com_email,
        "total_notificacoes": total_notificacoes,
        "notificacoes_mes": notificacoes_mes
    }


# Inicializa o banco ao importar o módulo
init_database()
