"""
Inicia o servidor MCP em modo Web (Streamable HTTP) usando mcp.run()
e gera a URL pública HTTPS via Cloudflare Tunnel para o Google Gemini Spark.
"""

import sys
import time
import re
import threading
import subprocess
from pathlib import Path

# Suporte a UTF-8 no Windows Console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from mcp.server.transport_security import TransportSecuritySettings

# Importa o MCPServer configurado
from hub_server import mcp

PORT = 8000
HOST = "127.0.0.1"

# Desativa a proteção de DNS rebinding para aceitar o domínio dinâmico do túnel
security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
    allowed_hosts=["*"],
    allowed_origins=["*"]
)

def start_mcp_server():
    """Inicia o servidor MCP através do método oficial mcp.run()"""
    try:
        mcp.run(
            transport="streamable-http",
            host=HOST,
            port=PORT,
            streamable_http_path="/mcp",
            transport_security=security
        )
    except Exception as e:
        print(f"[ERRO NO SERVIDOR MCP]: {e}")

def start_tunnel_and_extract_url():
    dir_central = Path(__file__).resolve().parent
    cloudflared_bin = dir_central / "cloudflared.exe"
    
    if not cloudflared_bin.exists():
        print("[ERRO] cloudflared.exe nao encontrado em central_mcp.")
        return

    # Inicia o servidor MCP oficial em thread separada
    server_thread = threading.Thread(target=start_mcp_server, daemon=True)
    server_thread.start()
    time.sleep(2)

    print("\n" + "="*60)
    print("Iniciando tunel HTTPS seguro para o Spark...")
    print("="*60)

    process = subprocess.Popen(
        [str(cloudflared_bin), "tunnel", "--url", f"http://{HOST}:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace"
    )

    tunnel_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    for line in iter(process.stdout.readline, ""):
        match = url_pattern.search(line)
        if match:
            tunnel_url = match.group(0)
            break

    if tunnel_url:
        mcp_link = f"{tunnel_url}/mcp"
        
        # Salva o link no arquivo spark_link.txt
        (dir_central / "spark_link.txt").write_text(
            f"LINK_MCP={mcp_link}\n",
            encoding="utf-8"
        )

        print("\n" + "*"*60)
        print("LINK OFICIAL GERADO PARA O SPARK:")
        print(f"👉 LINK DO SERVIDOR: {mcp_link}")
        print("*"*60 + "\n")
        print("Mantenha este processo em execucao enquanto usa o Spark.")
        sys.stdout.flush()
        
        # Mantém processo ativo
        process.wait()
    else:
        print("[AVISO] Nao foi possivel obter o link do tunel.")

if __name__ == "__main__":
    start_tunnel_and_extract_url()
