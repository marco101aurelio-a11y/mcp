"""
Master MCP Hub - Antigravity Central Orchestrator
Integra e orquestra os projetos do ecossistema:
1. Capvi IA / projetoseo2 (Acelerador de Lucratividade, Motor JAX de Finanças & SEO)
2. video_bot (Geração e renderização de vídeos em lote + TikTok)
3. blog automatico v2 (Artigos, SEO e WordPress)
4. previbilidade ads & Duvida (DRE Projetado, Ponto de Equilíbrio e Tráfego)
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

from mcp.server.mcpserver import MCPServer
import pandas as pd

# Inicialização do MCPServer (mcp 2.x)
mcp = MCPServer("Antigravity Central Hub")

# Diretórios base dos projetos do ecossistema
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
DIR_BLOG = WORKSPACE_ROOT / "blog automatico v2"
DIR_VIDEO = WORKSPACE_ROOT / "video_bot"
DIR_DUVIDA = WORKSPACE_ROOT / "Duvida"
DIR_PREVISIBILIDADE = WORKSPACE_ROOT / "previbilidade ads"
DIR_CAPVI = WORKSPACE_ROOT / "projetoseo2"
DIR_CAPVI_BACKEND = DIR_CAPVI / "olist-analytics-local"
DIR_CAPVI_FRONTEND = DIR_CAPVI / "seo-app"


# ==========================================
# 1. FERRAMENTAS DO HUB CENTRAL
# ==========================================

@mcp.tool()
def hub_status_projetos() -> Dict[str, Any]:
    """Retorna o status geral de todos os projetos conectados ao Hub Central MCP."""
    projetos = {
        "capvi_seo": {
            "nome": "Capvi IA — Acelerador de Lucratividade (Marketing & Financial Intelligence)",
            "existe": DIR_CAPVI.exists(),
            "caminho": str(DIR_CAPVI),
            "descricao": "Une Kotler, V4 AERM e Growth Hacking com motor JAX de alta performance (@jit). Realiza simulação de DRE Pro, análise de viabilidade SEO (IPM), ICE Score e CRM/RFM.",
            "frontend_react": {
                "existe": DIR_CAPVI_FRONTEND.exists(),
                "porta_padrao": 5173,
                "stack": "React + Vite + Tailwind CSS"
            },
            "backend_fastapi_jax": {
                "existe": DIR_CAPVI_BACKEND.exists(),
                "porta_padrao": 8000,
                "stack": "FastAPI + Google JAX + SQLAlchemy"
            },
            "status_geral": "Ativo e Integrado ao MCP" if DIR_CAPVI.exists() else "Não localizado"
        },
        "video_bot": {
            "nome": "video_bot — Fábrica de Vídeos Verticais e TikTok",
            "existe": DIR_VIDEO.exists(),
            "caminho": str(DIR_VIDEO),
            "descricao": "Geração automatizada de vídeos curtos em lote (Shorts/Reels/TikTok) com roteiros Claude 3.5, takes Pexels, render FFmpeg e postagem no TikTok (@som_do_infinito).",
            "videos_output": (
                len(list((DIR_VIDEO / "output" / "final").glob("*.mp4")))
                if (DIR_VIDEO / "output" / "final").exists()
                else len(list((DIR_VIDEO / "output").glob("*.mp4")))
            )
        },
        "blog_automatico_v2": {
            "nome": "blog automatico v2 — Fábrica de Artigos SEO",
            "existe": DIR_BLOG.exists(),
            "caminho": str(DIR_BLOG),
            "descricao": "Geração e publicação automatizada de artigos em Markdown orientados a SEO e palavras-chave com integração ao WordPress.",
            "posts_gerados": len(list((DIR_BLOG / "blog_posts").glob("*.md"))) if (DIR_BLOG / "blog_posts").exists() else 0
        },
        "previbilidade_ads": {
            "nome": "Previsibilidade Ads & Dúvida",
            "existe": DIR_PREVISIBILIDADE.exists() or DIR_DUVIDA.exists(),
            "caminho": str(DIR_PREVISIBILIDADE),
            "descricao": "Estratégia de tráfego pago, análise de DRE projetado e inteligência de campanhas Meta Ads."
        },
        "meta_ads": {
            "nome": "Meta Ads & Tráfego Pago (Conector & DRE Integrada)",
            "existe": (DIR_CAPVI_BACKEND / "src" / "services" / "meta_ads_service.py").exists(),
            "caminho": str(DIR_CAPVI_BACKEND / "src" / "services" / "meta_ads_service.py"),
            "descricao": "Conector da Meta Marketing API integrado ao MetaToFinanceConnector e FinanceEngine (JAX). Pronto para receber Google Ads no mesmo formato.",
            "status": "Conectado ao Hub MCP (Live + Contingência Inteligente)"
        }
    }
    return projetos


# ==========================================
# 2. FERRAMENTAS: BLOG AUTOMÁTICO V2
# ==========================================

@mcp.tool()
def blog_listar_posts(limite: int = 10) -> List[Dict[str, str]]:
    """Lista os posts de blog gerados em formato Markdown."""
    posts_dir = DIR_BLOG / "blog_posts"
    if not posts_dir.exists():
        return []
    
    arquivos = sorted(posts_dir.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    resultado = []
    for f in arquivos[:limite]:
        resultado.append({
            "nome_arquivo": f.name,
            "tamanho_bytes": str(f.stat().st_size),
            "modificado_em": str(f.stat().st_mtime)
        })
    return resultado

@mcp.tool()
def blog_ler_post(nome_arquivo: str) -> str:
    """Lê o conteúdo completo de um post de blog em Markdown."""
    post_path = DIR_BLOG / "blog_posts" / nome_arquivo
    if not post_path.exists():
        return f"Arquivo '{nome_arquivo}' não encontrado em blog_posts."
    return post_path.read_text(encoding="utf-8")

@mcp.tool()
def blog_disparar_geracao(palavra_chave: Optional[str] = None, tema: Optional[str] = None) -> str:
    """
    Dispara o processo de geração de blog posts utilizando o ambiente do blog automatico v2.
    Caso palavra_chave e tema sejam fornecidos, gera o post focado.
    """
    python_blog = DIR_BLOG / ".venv" / "Scripts" / "python.exe"
    if not python_blog.exists():
        python_blog = Path(sys.executable)

    script_main = DIR_BLOG / "main.py"
    if not script_main.exists():
        return "Script main.py do blog automatico v2 não encontrado."

    env = os.environ.copy()
    if palavra_chave:
        env["CUSTOM_KEYWORD"] = palavra_chave
    if tema:
        env["CUSTOM_THEME"] = tema

    processo = subprocess.run(
        [str(python_blog), str(script_main)],
        cwd=str(DIR_BLOG),
        capture_output=True,
        text=True,
        env=env,
        timeout=180
    )

    if processo.returncode == 0:
        return f"Geração concluída com sucesso!\nSaída:\n{processo.stdout[:1500]}"
    else:
        return f"Erro na execução da geração:\n{processo.stderr[:1500]}"


# ==========================================
# 3. FERRAMENTAS: VIDEO BOT
# ==========================================

@mcp.tool()
def video_listar_videos_gerados(limite: int = 15) -> List[Dict[str, Any]]:
    """Lista os vídeos (.mp4) mais recentes renderizados em video_bot (ordenados por data de criação)."""
    pastas = [DIR_VIDEO / "output" / "final", DIR_VIDEO / "output"]
    arquivos = []
    nomes_vistos = set()
    for pasta in pastas:
        if pasta.exists():
            for f in pasta.glob("*.mp4"):
                if f.name not in nomes_vistos:
                    nomes_vistos.add(f.name)
                    arquivos.append(f)
    arquivos.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    resultado = []
    for f in arquivos[:limite]:
        resultado.append({
            "nome_arquivo": f.name,
            "tamanho_mb": round(f.stat().st_size / (1024 * 1024), 2),
            "pasta": str(f.parent.relative_to(DIR_VIDEO))
        })
    return resultado

@mcp.tool()
def video_ler_roteiro_atual() -> Dict[str, Any]:
    """Lê o arquivo roteiro.json atual do video_bot com as falas e takes."""
    roteiro_path = DIR_VIDEO / "roteiro.json"
    if not roteiro_path.exists():
        return {"status": "erro", "mensagem": "roteiro.json não encontrado."}
    with open(roteiro_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Variável global para rastrear processo ativo de renderização
_processo_video_atual = None

@mcp.tool()
def video_gerar_video_com_tema(
    tema: str,
    script_name: str = "main.py",
    enviar_ao_tiktok: bool = False,
    modo_tiktok: str = "BY_DRAFT"
) -> str:
    """
    Gera um novo vídeo completo no video_bot com base no tema sugerido (ex: 'disciplina matinal', 'minimalismo e foco').
    Dispara em segundo plano para evitar timeout no celular/Spark e registra o progresso em tempo real.
    - enviar_ao_tiktok: se True, envia o vídeo gerado automaticamente ao TikTok após a renderização.
    - modo_tiktok: 'BY_DRAFT' (rascunho no app do TikTok - recomendado) ou 'DIRECT_POST' (direto no feed público).
    """
    global _processo_video_atual
    script_path = DIR_VIDEO / script_name
    if not script_path.exists():
        return f"Script '{script_name}' não encontrado na pasta video_bot."

    python_bin = Path(r"C:\Users\jpsec\AppData\Local\Programs\Python\Python312\python.exe")
    if not python_bin.exists():
        python_bin = Path(sys.executable)

    log_file = DIR_VIDEO / "last_render.log"
    msg_tiktok = f" (com envio automático ao TikTok: {modo_tiktok})" if enviar_ao_tiktok else ""
    log_file.write_text(f"[MCP] Iniciando pipeline de vídeo para o tema: '{tema}'{msg_tiktok}...\n", encoding="utf-8")

    cmd = [str(python_bin), str(script_path), tema]
    if enviar_ao_tiktok:
        cmd.append("--tiktok")

    env = os.environ.copy()
    if enviar_ao_tiktok:
        env["POSTAR_TIKTOK"] = "true"
        env["MODO_POSTAGEM_TIKTOK"] = modo_tiktok

    out_file = open(log_file, "a", encoding="utf-8", errors="replace")
    _processo_video_atual = subprocess.Popen(
        cmd,
        cwd=str(DIR_VIDEO),
        stdout=out_file,
        stderr=subprocess.STDOUT,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    detalhe_tiktok = (
        f"\n  5. Envio automático ao TikTok configurado: {'Rascunho no App (BY_DRAFT)' if modo_tiktok == 'BY_DRAFT' else 'Feed Público (DIRECT_POST)'}"
        if enviar_ao_tiktok else ""
    )

    return (
        f"🎬 Produção de vídeo INICIADA com sucesso para o tema: \"{tema}\"!\n\n"
        f"⚙️ Status: O pipeline está rodando em segundo plano no seu computador (evitando timeout no celular).\n"
        f"Etapas em andamento:\n"
        f"  1. Geração de roteiro poético com IA (Claude 3.5 Haiku)\n"
        f"  2. Criação de legendas e sobreposições\n"
        f"  3. Busca e download de takes visuais estéticos no Pexels\n"
        f"  4. Renderização FFmpeg (versões Shorts com texto + TikTok limpo){detalhe_tiktok}\n\n"
        f"💡 Dica: Você pode verificar o andamento a qualquer momento pedindo 'como está o status do vídeo?' (ferramenta video_status_renderizacao)."
    )

@mcp.tool()
def video_criar_e_enviar_rascunho_tiktok(tema: str) -> str:
    """
    CRIA UM VÍDEO 100% NOVO DO ZERO para o tema fornecido e envia automaticamente como RASCUNHO no TikTok.
    Fluxo completo executado no seu computador:
    1. M1: Gera conceito poético e frase inédita com Claude 3.5 Haiku
    2. M3: Gera legendas poéticas formatadas
    3. M4: Busca e baixa takes visuais estéticos no Pexels
    4. M5: Renderiza o vídeo em 9:16 (Shorts/TikTok) com color grading
    5. M6: Faz o upload automático desse novo vídeo diretamente para os Rascunhos (Inbox) do seu TikTok!
    NÃO usa nenhum vídeo antigo do acervo.
    """
    return video_gerar_video_com_tema(
        tema=tema,
        script_name="main.py",
        enviar_ao_tiktok=True,
        modo_tiktok="BY_DRAFT"
    )

@mcp.tool()
def video_status_renderizacao() -> str:
    """
    Verifica o status atual da renderização de vídeo em andamento no computador,
    mostrando a etapa atual e se os vídeos já foram finalizados.
    """
    global _processo_video_atual
    log_file = DIR_VIDEO / "last_render.log"
    if not log_file.exists():
        return "Nenhuma renderização recente encontrada."

    linhas = log_file.read_text(encoding="utf-8", errors="replace").splitlines()
    ultimas_linhas = "\n".join(linhas[-15:])

    rodando = False
    if _processo_video_atual is not None and _processo_video_atual.poll() is None:
        rodando = True

    status_str = "🔄 EM ANDAMENTO" if rodando else "🏁 FINALIZADO (ou aguardando novo disparo)"
    return f"Status da Máquina: {status_str}\n\nÚltimos logs da renderização:\n{ultimas_linhas}"

@mcp.tool()
def video_executar_script(nome_script: str, argumentos: Optional[str] = None) -> str:
    """
    Executa um script de geração de vídeo específico de video_bot (ex: 'main.py', 'gerar_3_variacoes.py').
    Permite passar argumentos adicionais como o tema.
    """
    script_path = DIR_VIDEO / nome_script
    if not script_path.exists():
        return f"Script '{nome_script}' não encontrado na pasta video_bot."

    python_bin = Path(r"C:\Users\jpsec\AppData\Local\Programs\Python\Python312\python.exe")
    if not python_bin.exists():
        python_bin = Path(sys.executable)

    cmd = [str(python_bin), str(script_path)]
    if argumentos:
        cmd.append(argumentos)

    processo = subprocess.run(
        cmd,
        cwd=str(DIR_VIDEO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300
    )

    saida = processo.stdout if processo.stdout else ""
    erros = processo.stderr if processo.stderr else ""

    if processo.returncode == 0:
        return f"Execução de {nome_script} concluída com sucesso!\n{saida[:1500]}"
    else:
        return f"Erro ao executar {nome_script}:\n{erros[:1500]}"



# ==========================================
# 4. FERRAMENTAS: TIKTOK (@som_do_infinito)
# ==========================================

@mcp.tool()
def tiktok_status_conexao() -> Dict[str, Any]:
    """Verifica se a conta do TikTok está conectada e se o token de acesso está ativo e válido."""
    try:
        import os
        antigo_cwd = os.getcwd()
        try:
            os.chdir(str(DIR_VIDEO))
            if str(DIR_VIDEO) not in sys.path:
                sys.path.insert(0, str(DIR_VIDEO))
            if str(DIR_VIDEO / "modules") not in sys.path:
                sys.path.insert(0, str(DIR_VIDEO / "modules"))
            import m6_tiktok
            token = m6_tiktok.carregar_token()
            if not token:
                return {"conectado": False, "mensagem": "Nenhum token encontrado em output/tiktok_token.json"}
            valido = m6_tiktok.obter_token_valido()
            return {
                "conectado": True,
                "token_valido": bool(valido),
                "escopo": token.get("scope", ""),
                "expira_em_segundos": token.get("expires_in", 0)
            }
        finally:
            os.chdir(antigo_cwd)
    except Exception as e:
        return {"conectado": False, "erro": str(e)}

@mcp.tool()
def tiktok_publicar_video(nome_arquivo_video: str, titulo: str, modo: str = "BY_DRAFT") -> Dict[str, Any]:
    """
    Publica um arquivo de vídeo ESPECÍFICO já existente no computador no perfil do TikTok.
    ATENÇÃO: Use apenas se o usuário pedir explicitamente para enviar um arquivo existente específico pelo nome.
    Para criar um vídeo NOVO do zero e enviar ao TikTok, use a ferramenta 'video_criar_e_enviar_rascunho_tiktok'.
    - nome_arquivo_video: nome do arquivo .mp4 existente (ex: 'video_shorts.mp4')
    - titulo: legenda/título da publicação com hashtags
    - modo: 'BY_DRAFT' (rascunho na caixa de entrada do app TikTok - recomendado) ou 'DIRECT_POST' (direto no feed público)
    """
    try:
        import os
        antigo_cwd = os.getcwd()
        try:
            os.chdir(str(DIR_VIDEO))
            if str(DIR_VIDEO) not in sys.path:
                sys.path.insert(0, str(DIR_VIDEO))
            if str(DIR_VIDEO / "modules") not in sys.path:
                sys.path.insert(0, str(DIR_VIDEO / "modules"))
            import m6_tiktok

            # Procura em output/final, depois output, depois relativo direto
            caminhos_tentativa = [
                DIR_VIDEO / "output" / "final" / nome_arquivo_video,
                DIR_VIDEO / "output" / nome_arquivo_video,
                DIR_VIDEO / nome_arquivo_video,
                Path(nome_arquivo_video)
            ]
            video_path = None
            for p in caminhos_tentativa:
                if p.exists() and p.is_file():
                    video_path = p
                    break

            if not video_path:
                return {
                    "status": "erro",
                    "mensagem": f"Arquivo '{nome_arquivo_video}' não encontrado nas pastas de saída (output/final ou output)."
                }

            resultado = m6_tiktok.publicar_video_tiktok(str(video_path), titulo=titulo, modo=modo)
            return resultado
        finally:
            os.chdir(antigo_cwd)
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

@mcp.tool()
def tiktok_obter_metricas(limite: int = 10) -> List[Dict[str, Any]]:
    """Obtém métricas dos vídeos publicados no TikTok (views, likes, comentários, compartilhamentos)."""
    try:
        import os
        antigo_cwd = os.getcwd()
        try:
            os.chdir(str(DIR_VIDEO))
            if str(DIR_VIDEO) not in sys.path:
                sys.path.insert(0, str(DIR_VIDEO))
            if str(DIR_VIDEO / "modules") not in sys.path:
                sys.path.insert(0, str(DIR_VIDEO / "modules"))
            import m6_tiktok
            return m6_tiktok.obter_metricas_videos(max_count=limite)
        finally:
            os.chdir(antigo_cwd)
    except Exception as e:
        return [{"erro": str(e)}]


# ==========================================
# 5. FERRAMENTAS: CAPVI IA / PROJETOSEO2 (MOTOR JAX & MARKETING FINANCEIRO)
# ==========================================

def _executar_capvi_jax_script(codigo_interno: str) -> Dict[str, Any]:
    """
    Executa um snippet Python no ambiente do projetoseo2 (.venv) para interagir
    diretamente com o MathIntelligenceJAX e retornar dados serializados em JSON.
    """
    python_capvi = DIR_CAPVI / ".venv" / "Scripts" / "python.exe"
    if not python_capvi.exists():
        python_capvi = Path(sys.executable)

    linhas_identadas = "\n".join("    " + l for l in codigo_interno.strip().splitlines())
    env_file = DIR_CAPVI_BACKEND / ".env"
    env_mcp = WORKSPACE_ROOT / "central_mcp" / ".env"
    script = (
        "import sys, json, os\n"
        "try:\n"
        "    from dotenv import load_dotenv\n"
        f"    load_dotenv(r'{str(env_file)}')\n"
        f"    load_dotenv(r'{str(env_mcp)}', override=True)\n"
        "except Exception:\n"
        "    pass\n"
        f"sys.path.insert(0, r'{str(DIR_CAPVI_BACKEND / 'src')}')\n"
        "try:\n"
        f"{linhas_identadas}\n"
        "except Exception as e:\n"
        "    print('JSON_START' + json.dumps({'erro': str(e)}) + 'JSON_END')\n"
    )

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        proc = subprocess.run(
            [str(python_capvi), "-c", script],
            cwd=str(DIR_CAPVI_BACKEND),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=25
        )
        saida = proc.stdout
        if "JSON_START" in saida and "JSON_END" in saida:
            json_str = saida.split("JSON_START")[1].split("JSON_END")[0]
            return json.loads(json_str)
        if proc.returncode != 0:
            return {"status": "erro", "detalhe": proc.stderr.strip() or "Erro na execução do processo JAX"}
        return {"status": "ok", "saida": saida.strip()}
    except Exception as exc:
        return {"status": "erro", "detalhe": str(exc)}


@mcp.tool()
def capvi_visao_geral() -> Dict[str, Any]:
    """
    Retorna a visão estrutural e arquitetura do Capvi SEO (projetoseo2):
    Camadas do Frontend, Backend, Motor Matemático JAX, Conectores e Benchmarks.
    """
    return {
        "projeto": "Capvi IA — Acelerador de Lucratividade & Marketing Inteligente",
        "pasta_raiz": str(DIR_CAPVI),
        "status_pasta": DIR_CAPVI.exists(),
        "camadas": {
            "frontend": {
                "pasta": str(DIR_CAPVI_FRONTEND),
                "porta": 5173,
                "stack": "React 18 + Vite + Tailwind CSS + Lucide Icons",
                "telas_principais": ["Dashboard Overview", "Estúdio de SEO e Finanças", "Wizard de Onboarding", "Chat com Capvi IA"]
            },
            "backend_api": {
                "pasta": str(DIR_CAPVI_BACKEND),
                "arquivo_principal": "src/main_api.py",
                "porta": 8000,
                "stack": "FastAPI + Uvicorn + SQLAlchemy + Supabase Client",
                "rotas": ["/finance/analyze/meta", "/finance/analyze/raw", "/agent/chat", "/api/v1/finance/profile"]
            },
            "cortex_jax": {
                "pasta": str(DIR_CAPVI_BACKEND / "src"),
                "arquivo_principal": "src/math_jax.py",
                "motores": {
                    "FinanceEngine": "Cálculo vetorial acelerado via JAX (@jit) de DRE Pro, EBITDA, Margem de Contribuição e Breakeven.",
                    "SEOEngine": "Cálculo de IPM (Índice de Potencial de Mercado) e simulação de volume/concorrência.",
                    "GrowthEngine": "Matriz ICE (Impacto, Confiança, Facilidade) para priorização de hipóteses.",
                    "RetentionEngine": "Análise de CRM RFM com escore padronizado Z-score.",
                    "OlistProcessor": "Refinaria de dados de e-commerce calibrando benchmarks de ticket médio."
                }
            }
        },
        "metodologia": "Kotler + V4 Company (AERM) + Growth Hacking",
        "benchmark_base": "Ticket Médio Real R$ 120,65 calibrado via Colab/JAX"
    }


@mcp.tool()
def capvi_simular_dre_financeiro(
    investimento: float,
    roas: float,
    custos_fixos: float,
    cogs_pct: float = 0.35
) -> Dict[str, Any]:
    """
    Simula o Demonstrativo do Resultado do Exercício (DRE Pro) via motor matemático JAX do Capvi IA.
    Calcula: Receita Bruta, COGS (custo mercadoria), Impostos (12%), Frete (7%), Taxa Marketplace (15%),
    Margem de Contribuição, EBITDA Final, Ponto de Equilíbrio (Breakeven) e Relação LTV/CAC.
    """
    codigo = f"""
from math_jax import MathIntelligenceJAX
m = MathIntelligenceJAX()
res = m.simulate_dre({investimento}, {roas}, {custos_fixos}, {cogs_pct})
print('JSON_START' + json.dumps(res) + 'JSON_END')
"""
    res = _executar_capvi_jax_script(codigo)
    if "summary" in res:
        return res

    # Fallback matemático direto com as fórmulas idênticas caso subprocesso falhe
    receita = float(investimento * roas)
    impostos = receita * 0.12
    frete = receita * 0.07
    marketplace = receita * 0.15
    cogs = receita * cogs_pct
    total_var = impostos + frete + marketplace + cogs
    mc = receita - total_var
    ebitda = mc - custos_fixos
    ebitda_pct = round((ebitda / receita * 100), 2) if receita > 0 else 0.0
    margem_mc_pct = mc / receita if receita > 0 else 0.0
    breakeven = round(custos_fixos / margem_mc_pct, 2) if margem_mc_pct > 0 else 0.0

    return {
        "summary": {
            "revenue": receita,
            "ebitda": ebitda,
            "ebitda_pct": ebitda_pct,
            "net_margin": round(ebitda / receita, 4) if receita > 0 else 0.0,
            "roas": roas,
            "breakeven": breakeven,
            "status": "LUCRO" if ebitda > 0 else "PREJUÍZO (Ajustar CAC/COGS)",
            "fonte": "motor_jax_fallback"
        },
        "detailed_dre": {
            "receita_bruta": receita,
            "investimento_ads": investimento,
            "custos_variaveis": {
                "total": total_var,
                "impostos": impostos,
                "frete": frete,
                "comissao_marketplace": marketplace,
                "cogs_produto": cogs
            },
            "margem_contribuicao": mc,
            "custos_fixos": custos_fixos,
            "ebitda_final": ebitda
        }
    }


@mcp.tool()
def capvi_analisar_palavra_chave_seo(
    palavra_chave: str,
    volume: Optional[int] = None,
    concorrencia: Optional[float] = None,
    cpc: Optional[float] = None,
    pais: str = "BR",
    motor_busca: str = "google"
) -> Dict[str, Any]:
    """
    Analisa uma palavra-chave sob a ótica do Capvi SEO utilizando o motor JAX.
    Calcula o IPM (Índice de Potencial de Mercado):
      IPM = (Volume * (1 - Concorrência/100)) / (CPC + 0.01)
    Classifica em:
      - 'Oceano Azul' (IPM > 10.000): Altíssima oportunidade de tráfego qualificado e baixo custo.
      - 'Zona de Crescimento' (3.000 <= IPM <= 10.000): Eficiência saudável com espaço para escala.
      - 'Mercado Maduro' (IPM < 3.000): Concorrência alta ou CPC elevado, exigindo diferenciação.
    Se volume/concorrência/cpc não forem informados, o motor JAX simula a inteligência de intenção.
    """
    if volume is not None and concorrencia is not None and cpc is not None:
        codigo = f"""
from math_jax import MathIntelligenceJAX
m = MathIntelligenceJAX()
res = m.analyze_keyword({volume}, {concorrencia}, {cpc})
res['palavra_chave'] = {json.dumps(palavra_chave)}
res['metricas_usadas'] = {{'volume': {volume}, 'concorrencia': {concorrencia}, 'cpc': {cpc}}}
print('JSON_START' + json.dumps(res) + 'JSON_END')
"""
        res = _executar_capvi_jax_script(codigo)
        if "score" in res:
            return res

        # Fallback direto
        score = (volume * (1 - concorrencia / 100.0)) / (cpc + 0.01)
        if score > 10000:
            clf, desc = "Oceano Azul", "IPM explosivo. Alta eficiência local."
        elif 3000 <= score <= 10000:
            clf, desc = "Zona de Crescimento", "IPM saudável. Espaço para escala."
        else:
            clf, desc = "Mercado Maduro", "IPM moderado. Exige diferenciação."
        return {
            "palavra_chave": palavra_chave,
            "score": round(float(score), 2),
            "classification": clf,
            "description": desc,
            "metricas_usadas": {"volume": volume, "concorrencia": concorrencia, "cpc": cpc}
        }
    else:
        codigo = f"""
from math_jax import MathIntelligenceJAX
m = MathIntelligenceJAX()
sim = m.simulate_keyword_metrics({json.dumps(palavra_chave)}, country={json.dumps(pais)}, engine={json.dumps(motor_busca)})
vol = sim.get('search_volume', 1000)
comp = sim.get('competition_index', 50.0)
cpc_val = sim.get('cpc', 1.50)
ana = m.analyze_keyword(vol, comp, cpc_val)
res = {{
    'palavra_chave': {json.dumps(palavra_chave)},
    'simulacao_mercado': sim,
    'analise_ipm': ana
}}
print('JSON_START' + json.dumps(res) + 'JSON_END')
"""
        res = _executar_capvi_jax_script(codigo)
        if "analise_ipm" in res:
            return res

        vol_est = 2500
        comp_est = 45.0
        cpc_est = 1.80
        score = (vol_est * (1 - comp_est / 100.0)) / (cpc_est + 0.01)
        return {
            "palavra_chave": palavra_chave,
            "simulacao_mercado": {"search_volume": vol_est, "competition_index": comp_est, "cpc": cpc_est, "country": pais, "engine": motor_busca},
            "analise_ipm": {
                "score": round(float(score), 2),
                "classification": "Zona de Crescimento",
                "description": "IPM saudável estimado pelo motor de contingência."
            }
        }


@mcp.tool()
def capvi_calcular_ice_growth(impacto: float, confianca: float, facilidade: float) -> Dict[str, Any]:
    """
    Calcula o ICE Score (Impacto x Confiança x Facilidade) para priorização de hipóteses de Growth Hacking.
    Notas de 1 a 10 para cada dimensão.
    """
    codigo = f"""
from math_jax import MathIntelligenceJAX
m = MathIntelligenceJAX()
res = m.analyze_growth({impacto}, {confianca}, {facilidade})
print('JSON_START' + json.dumps(res) + 'JSON_END')
"""
    res = _executar_capvi_jax_script(codigo)
    if "score" in res:
        return res
    score = float(impacto * confianca * facilidade)
    return {
        "score": score,
        "priority": "Alta" if score > 500 else "Média" if score > 200 else "Baixa",
        "action": "Executar Imediatamente" if score > 700 else "Validar MVP"
    }


@mcp.tool()
def capvi_obter_benchmarks() -> Dict[str, Any]:
    """
    Retorna os benchmarks consolidados e calibrados do Capvi SEO / base Olist e-commerce.
    Inclui ticket médio real calibrado (R$ 120,65), métricas de RFM e referências de mercado.
    """
    return {
        "ticket_medio_calibrado_br": 120.65,
        "base_dados_origem": "Refinaria JAX Olist (112k pedidos calibrados)",
        "rfm_referencias": {
            "recencia_media_dias": 142.5,
            "frequencia_media_pedidos": 2.14,
            "valor_monetario_medio": 184.50
        },
        "taxas_padrao_mercado": {
            "imposto_medio": 0.12,
            "frete_medio": 0.07,
            "comissao_marketplace": 0.15,
            "cogs_medio": 0.35
        },
        "segmentos_clientes": ["Campeões", "Leais", "Em Risco", "Perdidos"],
        "diretrizes_estrategicas": "Se Ticket Médio for R$ 120,65 e Margem Contribuição for > 35%, escala de tráfego é viável."
    }


# ==========================================
# 6. FERRAMENTAS: META ADS & TRÁFEGO PAGO
# ==========================================

@mcp.tool()
def meta_ads_status_conexao(
    ad_account_id: Optional[str] = None,
    access_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Verifica o status da conexão com a API do Meta Marketing (Facebook Ads).
    Checa se o token está ativo, se a conta de anúncios é acessível ou se o sistema está em modo contingência/simulação.
    - ad_account_id: opcional. Se não informado, busca do .env (META_AD_ACCOUNT_ID). Suporta formato com ou sem 'act_'.
    """
    codigo = f"""
from services.meta_ads_service import MetaAdsService
token_arg = {repr(access_token)}
svc = MetaAdsService(access_token=token_arg)
raw_acc = {repr(ad_account_id)} or os.getenv('META_AD_ACCOUNT_ID', '317590331118373')
ad_acc = str(raw_acc).replace('act_', '').strip()
acc_info = svc.get_account_info(ad_acc)
res = {{
    'sdk_inicializado': svc._initialized,
    'ad_account_id': ad_acc,
    'info_conta': acc_info,
    'status_conexao': 'ATIVA' if acc_info.get('success') else 'EXPIRADA_OU_CONTINGENCIA',
    'mensagem': (
        'Conexão ativa e autenticada com o Facebook Graph API.' 
        if acc_info.get('success') 
        else 'Token expirado ou inválido na Meta API. O modo de demonstração/mock inteligente está pronto para simular DRE e métricas.'
    )
}}
print('JSON_START' + json.dumps(res) + 'JSON_END')
"""
    return _executar_capvi_jax_script(codigo)


@mcp.tool()
def meta_ads_obter_metricas(
    periodo: str = "last_30d",
    ad_account_id: Optional[str] = None,
    usar_mock_se_falhar: bool = True,
    access_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Obtém métricas agregadas e detalhadas das campanhas de Meta Ads (Facebook/Instagram).
    Retorna: investimento total, impressões, cliques, compras, receita, ROAS, CAC, CPC, CPM e lista de campanhas.
    - periodo: 'today', 'yesterday', 'last_7d', 'last_14d', 'last_30d', 'this_month'
    - ad_account_id: opcional. Se não informado, busca do .env (META_AD_ACCOUNT_ID).
    - usar_mock_se_falhar: se True, caso a API da Meta retorne erro de token ou rate limit, utiliza dados de demonstração calibrados.
    """
    codigo = f"""
from services.meta_ads_service import MetaAdsService
token_arg = {repr(access_token)}
svc = MetaAdsService(access_token=token_arg)
raw_acc = {repr(ad_account_id)} or os.getenv('META_AD_ACCOUNT_ID', '317590331118373')
ad_acc = str(raw_acc).replace('act_', '').strip()
res = svc.get_campaign_metrics(ad_acc, date_preset={json.dumps(periodo)})
if (not res.get('success')) and {str(usar_mock_se_falhar)}:
    mock = svc.get_mock_data('demo')
    res = {{
        'success': True,
        'data': mock['data'],
        'modo': 'contingencia_mock',
        'aviso': 'Dados de demonstração utilizados (Token Meta expirado ou indisponível).',
        'erro_original': res.get('error')
    }}
else:
    res['modo'] = 'api_live'
print('JSON_START' + json.dumps(res) + 'JSON_END')
"""
    return _executar_capvi_jax_script(codigo)


@mcp.tool()
def meta_ads_analisar_lucratividade(
    periodo: str = "last_30d",
    ad_account_id: Optional[str] = None,
    cogs_pct: float = 0.35,
    custos_fixos: float = 4500.0,
    funnel_type: str = "b2c_ecommerce",
    usar_mock_se_falhar: bool = True,
    access_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Pipeline Completo de Inteligência: Conecta as campanhas de Meta Ads ao motor matemático JAX (Capvi SEO).
    Calcula:
      1. Métricas de Tráfego: Investimento Real, Cliques, Pedidos, Receita e ROAS.
      2. DRE Pro Vetorial: Margem de Contribuição, COGS (Custo de Produto), Impostos, Frete, EBITDA Final e Ponto de Equilíbrio (Breakeven).
      3. Diagnóstico & Health Score: Identifica se a operação está no Lucro ou Prejuízo com alertas acionáveis.
      4. Engenharia Reversa: Calcula o investimento exato em tráfego necessário para atingir o breakeven ou meta de lucro.
    - ad_account_id: opcional. Se não informado, busca do .env (META_AD_ACCOUNT_ID).
    - funnel_type: 'b2c_ecommerce', 'b2c_servico_agendamento', 'b2b_servico', 'b2c_infoproduto'
    """
    codigo = f"""
from services.meta_ads_service import MetaAdsService
from connectors.meta_to_finance_connector import MetaToFinanceConnector
from engines.finance_engine import FinanceEngine

token_arg = {repr(access_token)}
svc = MetaAdsService(access_token=token_arg)
raw_acc = {repr(ad_account_id)} or os.getenv('META_AD_ACCOUNT_ID', '317590331118373')
ad_acc = str(raw_acc).replace('act_', '').strip()
metrics_res = svc.get_campaign_metrics(ad_acc, date_preset={json.dumps(periodo)})

modo_execucao = 'api_live'
if not metrics_res.get('success'):
    if {str(usar_mock_se_falhar)}:
        metrics_res = svc.get_mock_data('demo')
        modo_execucao = 'contingencia_mock'
    else:
        print('JSON_START' + json.dumps(metrics_res) + 'JSON_END')
        sys.exit(0)

campanhas_raw = metrics_res['data']['campanhas_raw']
connector = MetaToFinanceConnector()
traffic = connector.build_traffic_data(
    campanhas_raw,
    cogs_pct={cogs_pct},
    fixed_costs={custos_fixos},
    funnel_type={json.dumps(funnel_type)}
)

engine = FinanceEngine()
analysis = engine.analyze_from_raw(traffic)
analysis['modo_origem_dados'] = modo_execucao
analysis['periodo_consultado'] = {json.dumps(periodo)}
analysis['resumo_trafego'] = metrics_res['data']['resumo']

print('JSON_START' + json.dumps(analysis) + 'JSON_END')
"""
    return _executar_capvi_jax_script(codigo)


@mcp.tool()
def meta_ads_diagnostico_otimizacao(
    periodo: str = "last_30d",
    ad_account_id: Optional[str] = None,
    usar_mock_se_falhar: bool = True,
    access_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Diagnóstico puro de Gestor de Tráfego / Media Buyer (SEM necessidade de motor financeiro DRE).
    Analisa métricas operacionais de mídia paga:
      - CTR e CPC (eficiência de anúncio e criativo)
      - Frequência (fadiga de anúncio / saturação de público)
      - ROAS por campanha e custo por compra (CAC direto de tráfego)
      - Classificação acionável de cada campanha: 'ESCALAR', 'OTIMIZAR_CRIATIVO', 'TESTAR_NOVOS_CRIATIVOS', 'PAUSAR_OU_REVER'
    """
    codigo = f"""
from services.meta_ads_service import MetaAdsService
token_arg = {repr(access_token)}
svc = MetaAdsService(access_token=token_arg)
raw_acc = {repr(ad_account_id)} or os.getenv('META_AD_ACCOUNT_ID', '317590331118373')
ad_acc = str(raw_acc).replace('act_', '').strip()
metrics_res = svc.get_campaign_metrics(ad_acc, date_preset={json.dumps(periodo)})

if not metrics_res.get('success'):
    if {str(usar_mock_se_falhar)}:
        metrics_res = svc.get_mock_data('demo')
    else:
        print('JSON_START' + json.dumps(metrics_res) + 'JSON_END')
        sys.exit(0)

campanhas = metrics_res['data']['campanhas']
resumo = metrics_res['data']['resumo']

classificacoes = []
for c in campanhas:
    nome = c.get('nome', '')
    roas = c.get('roas', 0.0)
    ctr = c.get('ctr', 0.0)
    cpc = c.get('cpc', 0.0)
    freq = c.get('frequencia', 1.0)
    pedidos = c.get('pedidos', 0)
    invest = c.get('investimento', 0.0)
    
    if roas >= 4.0 and ctr >= 1.8:
        acao = "ESCALAR"
        motivo = f"Campanha de alta performance (ROAS {{roas}}x e CTR {{ctr}}%). Recomendado aumentar orçamento diário em 15-20%."
    elif freq >= 2.5:
        acao = "OTIMIZAR_CRIATIVO"
        motivo = f"Frequência elevada ({{freq}}x). Público saturado; necessário renovar criativos e ganchos visuais."
    elif pedidos == 0 and invest > 100.0:
        acao = "PAUSAR_OU_REVER"
        motivo = f"Investimento de R$ {{invest}} sem conversões diretas. Checar página de destino ou oferta."
    elif ctr < 1.0:
        acao = "TESTAR_NOVOS_CRIATIVOS"
        motivo = f"CTR abaixo de 1.0% ({{ctr}}%). Gancho fraco ou criativo pouco atrativo no feed."
    else:
        acao = "MONITORAR"
        motivo = f"Desempenho estável com ROAS {{roas}}x e CPC R$ {{cpc}}."
        
    classificacoes.append({{
        "campaign_id": c.get('campaign_id'),
        "campanha": nome,
        "investimento": invest,
        "receita": c.get('receita', 0.0),
        "roas": roas,
        "ctr": ctr,
        "cpc": cpc,
        "frequencia": freq,
        "pedidos": pedidos,
        "recomendacao": acao,
        "justificativa": motivo
    }})

diagnostico = {{
    "periodo": {json.dumps(periodo)},
    "investimento_total": resumo.get('investimento_total'),
    "receita_total": resumo.get('receita_total'),
    "roas_geral": resumo.get('roas_geral'),
    "cpc_medio": resumo.get('cpc_geral'),
    "ctr_medio": resumo.get('ctr_geral'),
    "campanhas_analisadas": classificacoes,
    "resumo_tatico": {{
        "campanhas_para_escalar": len([c for c in classificacoes if c['recomendacao'] == 'ESCALAR']),
        "campanhas_para_renovar_criativo": len([c for c in classificacoes if 'CRIATIVO' in c['recomendacao']]),
        "campanhas_em_alerta": len([c for c in classificacoes if c['recomendacao'] == 'PAUSAR_OU_REVER'])
    }}
}}
print('JSON_START' + json.dumps(diagnostico) + 'JSON_END')
"""
    return _executar_capvi_jax_script(codigo)


@mcp.tool()
def meta_ads_gerar_sugestoes_criativos(
    nicho_ou_produto: str,
    objetivo: str = "vendas",
    tom_de_voz: str = "direto_e_persuasivo"
) -> Dict[str, Any]:
    """
    Gera ideias práticas de criativos e anúncios para o Meta Ads (Instagram/Facebook):
    Retorna 3 formatos de anúncios prontos:
      1. Gancho Visual (3 primeiros segundos)
      2. Texto Principal (Copy no modelo AIDA - Atenção, Interesse, Desejo, Ação)
      3. Título do Botão e Chamada para Ação (CTA)
      4. Sugestão de Roteiro de Vídeo Vertical (pronto para renderizar no video_bot ou gravar)
    """
    return {
        "produto_ou_nicho": nicho_ou_produto,
        "objetivo": objetivo,
        "tom": tom_de_voz,
        "variacoes_de_anuncio": [
            {
                "angulo": "Dor / Problema Imediato",
                "gancho_visual_3s": f"Você ainda perde tempo tentando resolver {nicho_ou_produto} do jeito antigo?",
                "copy_principal": f"Se você sente que está gastando dinheiro sem ver o retorno que merece em {nicho_ou_produto}, o problema não é o seu esforço — é a estratégia. Descubra como mudar o jogo com quem realmente entrega resultado comprovado.",
                "titulo_anuncio": "Pare de Perder Dinheiro Hoje",
                "cta": "Saiba Mais",
                "sugestao_video_bot": f"Vídeo vertical 9:16 com ritmo dinâmico, takes rápidos mostrando o contraste entre 'antes' e 'depois' de {nicho_ou_produto}."
            },
            {
                "angulo": "Prova Social / Curiosidade",
                "gancho_visual_3s": f"O segredo que ninguém te conta sobre ter resultado com {nicho_ou_produto}...",
                "copy_principal": f"Mais de dezenas de clientes já destravaram seus resultados aplicando esse método simples. Em menos de 5 minutos você entende exatamente o que fazer.",
                "titulo_anuncio": "Descubra o Método na Prática",
                "cta": "Comprar Agora",
                "sugestao_video_bot": "Vídeo estilo tutorial de tela com tipografia neon moderna e áudio ambiente instigante."
            },
            {
                "angulo": "Oferta Direta / Escassez",
                "gancho_visual_3s": f"Última chamada para quem busca o melhor custo-benefício em {nicho_ou_produto}!",
                "copy_principal": f"Condição especial por tempo limitado para você garantir {nicho_ou_produto} com a máxima qualidade e suporte direto. Clique abaixo e aproveite antes que encerre.",
                "titulo_anuncio": "Condição Exclusiva Liberada",
                "cta": "Aproveitar Oferta",
                "sugestao_video_bot": "Vídeo minimalista com corte acelerado, texto dinâmico central e transições suaves."
            }
        ]
    }


# ==========================================
# PONTO DE ENTRADA DO SERVIDOR MCP
# ==========================================

if __name__ == "__main__":
    mcp.run()


