"""
Módulo de estilos CSS para o Gerenciador de Certificados.
Contém todos os estilos customizados para o Streamlit.
"""


def get_css(tema_escuro: bool = False) -> str:
    """Retorna o CSS customizado para a aplicação."""
    
    if tema_escuro:
        return get_css_dark()
    
    return """
    <style>
    /* ==================== VARIÁVEIS DE CORES ==================== */
    :root {
        --primary-color: #1E3A5F;
        --secondary-color: #3D5A80;
        --accent-color: #4A90D9;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --light-bg: #f8f9fa;
        --dark-text: #212529;
        --muted-text: #6c757d;
        --border-color: #dee2e6;
        --shadow: 0 2px 8px rgba(0,0,0,0.1);
        --shadow-hover: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    /* ==================== HEADER ==================== */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 0.95rem;
    }
    
    /* ==================== CARDS DE MÉTRICAS ==================== */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--accent-color);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }
    
    .metric-card.total {
        border-left-color: var(--accent-color);
    }
    
    .metric-card.vencido {
        border-left-color: var(--danger-color);
        background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
    }
    
    .metric-card.atencao {
        border-left-color: var(--warning-color);
        background: linear-gradient(135deg, #fff 0%, #fffef5 100%);
    }
    
    .metric-card.valido {
        border-left-color: var(--success-color);
        background: linear-gradient(135deg, #fff 0%, #f5fff5 100%);
    }
    
    .metric-card.erro {
        border-left-color: var(--muted-text);
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--dark-text);
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: var(--muted-text);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ==================== SIDEBAR ==================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--light-bg) 0%, #fff 100%);
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    
    .sidebar-header {
        background: var(--primary-color);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sidebar-header h3 {
        margin: 0;
        font-size: 1.1rem;
    }
    
    /* ==================== PAINEL DE AÇÕES PENDENTES ==================== */
    .action-panel {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }
    
    .action-card {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .action-card.danger {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
        border-left: 4px solid var(--danger-color);
    }
    
    .action-card.warning {
        background: linear-gradient(135deg, #fffef5 0%, #fff3cd 100%);
        border-left: 4px solid var(--warning-color);
    }
    
    .action-card.info {
        background: linear-gradient(135deg, #f0f7ff 0%, #d6e9ff 100%);
        border-left: 4px solid var(--accent-color);
    }
    
    .action-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
    }
    
    .action-card p {
        margin: 0;
        font-size: 0.85rem;
        color: var(--muted-text);
    }
    
    /* ==================== BADGES/TAGS ==================== */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0.25rem;
    }
    
    .badge-success {
        background: var(--success-color);
        color: white;
    }
    
    .badge-warning {
        background: var(--warning-color);
        color: #212529;
    }
    
    .badge-danger {
        background: var(--danger-color);
        color: white;
    }
    
    .badge-info {
        background: var(--accent-color);
        color: white;
    }
    
    .badge-muted {
        background: var(--muted-text);
        color: white;
    }
    
    /* ==================== TABELA ==================== */
    .dataframe-container {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow);
    }
    
    /* ==================== BOTÕES ==================== */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow);
    }
    
    /* ==================== FORMULÁRIOS ==================== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.1);
    }
    
    /* ==================== ALERTAS ==================== */
    .custom-alert {
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .custom-alert.success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .custom-alert.warning {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
    }
    
    .custom-alert.error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .custom-alert.info {
        background: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    
    /* ==================== ANIMAÇÕES ==================== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* ==================== RESPONSIVIDADE ==================== */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
        }
        
        .main-header h1 {
            font-size: 1.4rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* ==================== EXPANDER CUSTOMIZADO ==================== */
    .streamlit-expanderHeader {
        background: var(--light-bg);
        border-radius: 8px;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        background: #e9ecef;
    }
    
    /* ==================== TABS ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.75rem 1.5rem;
        background: var(--light-bg);
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        border-bottom: 2px solid var(--accent-color);
    }
    
    /* ==================== PROGRESS BAR ==================== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--accent-color) 100%);
    }
    </style>
    """


def get_css_dark() -> str:
    """Retorna o CSS para tema escuro."""
    return """
    <style>
    /* ==================== VARIÁVEIS DE CORES - DARK MODE ==================== */
    :root {
        --primary-color: #4A90D9;
        --secondary-color: #3D5A80;
        --accent-color: #5BA3E0;
        --success-color: #4caf50;
        --warning-color: #ff9800;
        --danger-color: #f44336;
        --light-bg: #1e1e1e;
        --dark-text: #e0e0e0;
        --muted-text: #9e9e9e;
        --border-color: #424242;
        --shadow: 0 2px 8px rgba(0,0,0,0.3);
        --shadow-hover: 0 4px 16px rgba(0,0,0,0.4);
        --card-bg: #2d2d2d;
    }
    
    /* ==================== HEADER ==================== */
    .main-header {
        background: linear-gradient(135deg, #2d2d2d 0%, #1e1e1e 100%);
        color: #e0e0e0;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--accent-color);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 0.95rem;
    }
    
    /* ==================== CARDS DE MÉTRICAS ==================== */
    .metric-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--accent-color);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }
    
    .metric-card.total {
        border-left-color: var(--accent-color);
    }
    
    .metric-card.vencido {
        border-left-color: var(--danger-color);
        background: linear-gradient(135deg, #2d2d2d 0%, #3d2020 100%);
    }
    
    .metric-card.atencao {
        border-left-color: var(--warning-color);
        background: linear-gradient(135deg, #2d2d2d 0%, #3d3520 100%);
    }
    
    .metric-card.valido {
        border-left-color: var(--success-color);
        background: linear-gradient(135deg, #2d2d2d 0%, #203d20 100%);
    }
    
    .metric-card.erro {
        border-left-color: var(--muted-text);
        background: var(--card-bg);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--dark-text);
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: var(--muted-text);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ==================== SIDEBAR ==================== */
    .sidebar-header {
        background: var(--card-bg);
        color: var(--accent-color);
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        border: 1px solid var(--border-color);
    }
    
    .sidebar-header h3 {
        margin: 0;
        font-size: 1.1rem;
    }
    
    /* ==================== PAINEL DE AÇÕES PENDENTES ==================== */
    .action-panel {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }
    
    .action-card {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        background: var(--light-bg);
    }
    
    .action-card.danger {
        border-left: 4px solid var(--danger-color);
    }
    
    .action-card.warning {
        border-left: 4px solid var(--warning-color);
    }
    
    .action-card.info {
        border-left: 4px solid var(--accent-color);
    }
    
    .action-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        color: var(--dark-text);
    }
    
    .action-card p {
        margin: 0;
        font-size: 0.85rem;
        color: var(--muted-text);
    }
    
    /* ==================== BADGES/TAGS ==================== */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0.25rem;
    }
    
    .badge-success {
        background: var(--success-color);
        color: white;
    }
    
    .badge-warning {
        background: var(--warning-color);
        color: #212529;
    }
    
    .badge-danger {
        background: var(--danger-color);
        color: white;
    }
    
    .badge-info {
        background: var(--accent-color);
        color: white;
    }
    
    .badge-muted {
        background: var(--muted-text);
        color: white;
    }
    
    /* ==================== ALERTAS ==================== */
    .custom-alert {
        padding: 1rem 1.25rem;
        border-radius: 8px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .custom-alert.success {
        background: #1b3d1b;
        color: #81c784;
        border: 1px solid #2e5a2e;
    }
    
    .custom-alert.warning {
        background: #3d3520;
        color: #ffb74d;
        border: 1px solid #5a4a20;
    }
    
    .custom-alert.error {
        background: #3d2020;
        color: #ef9a9a;
        border: 1px solid #5a2020;
    }
    
    .custom-alert.info {
        background: #1e3a5f;
        color: #90caf9;
        border: 1px solid #2d5a8f;
    }
    
    /* ==================== ANIMAÇÕES ==================== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.3s ease-out;
    }
    </style>
    """


def render_header(titulo: str, subtitulo: str = "") -> str:
    """Renderiza o header estilizado."""
    subtitulo_html = f"<p>{subtitulo}</p>" if subtitulo else ""
    return f"""
    <div class="main-header animate-fade-in">
        <h1>🔐 {titulo}</h1>
        {subtitulo_html}
    </div>
    """


def render_metric_card(valor: int, label: str, tipo: str = "total") -> str:
    """Renderiza um card de métrica estilizado."""
    return f"""
    <div class="metric-card {tipo} animate-fade-in">
        <div class="metric-value">{valor}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def render_alert(mensagem: str, tipo: str = "info") -> str:
    """Renderiza um alerta customizado."""
    icons = {
        "success": "✓",
        "warning": "⚠",
        "error": "✕",
        "info": "ℹ"
    }
    icon = icons.get(tipo, "ℹ")
    return f"""
    <div class="custom-alert {tipo} animate-fade-in">
        <span>{icon}</span>
        <span>{mensagem}</span>
    </div>
    """


def render_badge(texto: str, tipo: str = "info") -> str:
    """Renderiza uma badge/tag estilizada."""
    return f'<span class="badge badge-{tipo}">{texto}</span>'


def render_action_card(titulo: str, descricao: str, tipo: str = "info") -> str:
    """Renderiza um card de ação pendente."""
    return f"""
    <div class="action-card {tipo}">
        <h4>{titulo}</h4>
        <p>{descricao}</p>
    </div>
    """


def render_section_title(titulo: str, icon: str = "") -> str:
    """Renderiza um título de seção."""
    return f"""
    <div class="section-title">
        {icon} {titulo}
    </div>
    """
