"""
Inicia o servidor MCP local na porta 8000 pronto para receber conexões
do túnel permanente Cloudflare (mcp.promptpulse.com.br).
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from mcp.server.transport_security import TransportSecuritySettings
from hub_server import mcp

PORT = 8000
HOST = "127.0.0.1"

# Permite acesso via Cloudflare Tunnel sem bloqueio de DNS rebinding
security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
    allowed_hosts=["*"],
    allowed_origins=["*"]
)

if __name__ == "__main__":
    print(f"[*] Iniciando Servidor MCP Antigravity Central Hub...")
    print(f"[*] Porta local: {HOST}:{PORT}")
    print(f"[*] Conexão pública permanente: https://mcp.promptpulse.com.br/mcp")
    mcp.run(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        streamable_http_path="/mcp",
        transport_security=security
    )
