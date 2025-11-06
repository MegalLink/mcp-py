FROM python:3.14-slim
RUN pip install uv
WORKDIR /app
COPY pyproject.toml .
RUN uv pip install --system --no-cache .

# Copiar toda la carpeta mcp_server con todos los módulos
COPY mcp_server/ ./mcp_server/

EXPOSE 8000
# Mantiene el contenedor vivo y esperando comandos
CMD ["sleep", "infinity"]