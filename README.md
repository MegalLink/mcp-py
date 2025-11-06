# 📁 MCP Google Drive Server

<div align="center">

**Servidor MCP (Model Context Protocol) para interactuar con Google Drive**

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com)

</div>

---

## � Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Herramientas Disponibles](#-herramientas-disponibles)
- [Integración con IDEs](#-integración-con-ides)
- [Arquitectura](#-arquitectura)
- [Solución de Problemas](#-solución-de-problemas)

---

## 🎯 Descripción

Este servidor MCP proporciona una interfaz para interactuar con Google Drive a través del Model Context Protocol. Permite a las aplicaciones de IA leer y actualizar archivos de Google Drive de manera sencilla y eficiente.

### ¿Qué es MCP?

Model Context Protocol (MCP) es un protocolo estándar que permite a las aplicaciones de IA interactuar con fuentes de datos externas de manera estructurada y segura.

---

## ✨ Características

- � **Lectura inteligente de archivos**: Soporta Google Docs, Sheets, Slides y archivos de texto
- 📝 **Actualización de contenido**: Modifica archivos de Google Drive directamente
- 🔗 **URLs amigables**: Acepta URLs completas de Google Drive (no necesitas extraer el ID manualmente)
- 🐳 **Docker-ready**: Despliega fácilmente con Docker y Docker Compose
- 🔄 **Auto-detección de tipos**: Detecta automáticamente el tipo de archivo y usa el método apropiado
- 🛡️ **Manejo de errores robusto**: Mensajes de error claros y descriptivos

---

## 📋 Requisitos Previos

- **Python 3.14+**
- **uv** (gestor de paquetes Python)
- **Cuenta de Google Cloud** con API de Drive habilitada
- **Docker** (opcional, para deployment)

---

## 🚀 Instalación

### Opción 1: Instalación Local

1. **Clona el repositorio**
   ```bash
   git clone <repository-url>
   cd mcp-py
   ```

2. **Instala las dependencias**
   ```bash
   uv sync
   ```

3. **Configura las credenciales** (ver sección [Configuración](#-configuración))

### Opción 2: Usando Docker

1. **Clona el repositorio**
   ```bash
   git clone <repository-url>
   cd mcp-py
   ```

2. **Configura las credenciales** (ver sección [Configuración](#-configuración))

3. **Levanta el contenedor**
   ```bash
   docker-compose up --build -d
   ```

---

## 🔧 Configuración

### 1. Obtener Credenciales de Google Cloud

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **Google Drive API**
4. Ve a **Credenciales** > **Crear credenciales** > **Cuenta de servicio**
5. Descarga el archivo JSON de credenciales
6. Guarda el archivo como `credentials.json` en la raíz del proyecto

### 2. Configurar Permisos de Archivos

Para que el servidor pueda acceder a tus archivos de Google Drive:

1. Abre el archivo `credentials.json`
2. Copia el valor del campo `client_email` (ej: `my-service@project.iam.gserviceaccount.com`)
3. En Google Drive:
   - Haz clic derecho en el archivo que deseas compartir
   - Selecciona **Compartir**
   - Pega el email de la cuenta de servicio
   - Dale permisos de **Editor**
   - Haz clic en **Enviar**

> ⚠️ **Importante**: Sin compartir el archivo con la cuenta de servicio, obtendrás errores de "Permiso denegado".

### 3. Variables de Entorno

El servidor detecta automáticamente el entorno:

- **Desarrollo** (local): Lee `credentials.json` de la raíz del proyecto
- **Producción** (Docker): Lee credenciales desde `/run/secrets/google_creds`

Para forzar modo producción:
```bash
export APP_ENV=production
```

---

## 🎮 Uso

### Ejecutar Localmente

```bash
uv run mcp dev mcp_server/main.py:mcp
```

Esto iniciará el servidor MCP en modo desarrollo con inspector en `http://localhost:6274`

### Ejecutar con Docker

```bash
# Iniciar el servidor
docker-compose up --build -d

# Ver logs
docker-compose logs -f

# Detener el servidor
docker-compose down
```

---

## Herramientas Disponibles

### 1. `get_drive_file_tool`

Obtiene el contenido de un archivo de Google Drive.

**Parámetros:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `url` | `string` | URL completa de Google Drive o file_id |

**Tipos de archivos soportados:**
- ✅ **Google Docs** → Exportado como texto plano
- ✅ **Google Sheets** → Exportado como CSV
- ✅ **Google Slides** → Exportado como texto plano
- ✅ **Archivos de texto** → `.txt`, `.md`, `.json`, etc.
- ✅ **Otros archivos binarios** → Con contenido de texto

**Ejemplos de uso:**

```python
# Con URL completa de Google Docs
url = "https://docs.google.com/document/d/1h9sRNgBe.../edit?usp=sharing"
content = await get_drive_file_tool(url)

# Con URL de Google Sheets
url = "https://docs.google.com/spreadsheets/d/1h9sRNgBe.../edit"
csv_content = await get_drive_file_tool(url)

# Con file_id directo
file_id = "1h9sRNgBeEpC3aa3aXqjVaWTUrbjqKAWtvcoIBXdVdss"
content = await get_drive_file_tool(file_id)
```

**Respuesta:**
```
Contenido del archivo como string
```

---

### 2. `update_drive_file_tool`

Actualiza el contenido de un archivo en Google Drive.

**Parámetros:**
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `file_id` | `string` | ID del archivo a actualizar |
| `content` | `string` | Nuevo contenido del archivo |

**Ejemplo de uso:**

```python
file_id = "1h9sRNgBeEpC3aa3aXqjVaWTUrbjqKAWtvcoIBXdVdss"
new_content = "Este es el nuevo contenido del archivo"

result = await update_drive_file_tool(file_id, new_content)
```

**Respuesta:**
```json
{
  "status": "success",
  "file_name": "Mi Documento.txt"
}
```

---

### 3. `test_server_tool`

Verifica que el servidor está funcionando correctamente.

**Parámetros:** Ninguno

**Ejemplo de uso:**

```python
response = await test_server_tool()
```

**Respuesta:**
```
"Test de mcp py exitosa"
```

---

## 🔌 Integración con IDEs

> ⚠️ **Importante**: Todas las configuraciones a continuación usan Docker. Asegúrate de que el contenedor esté corriendo:
> ```bash
> docker-compose up -d
> ```

### Warp Terminal

Agrega esta configuración a tu archivo de configuración MCP:

```json
{
  "mcp-py-drive-server": {
    "command": "docker",
    "args": [
      "exec",
      "-i",
      "mcp-py",
      "uv",
      "run",
      "mcp",
      "run",
      "mcp_server/main.py:mcp"
    ],
    "env": {},
    "working_directory": null
  }
}
```

### VS Code

Agrega a tu `settings.json`:

```json
{
  "mcp.servers": {
    "google-drive": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-py",
        "uv",
        "run",
        "mcp",
        "run",
        "mcp_server/main.py:mcp"
      ],
      "env": {}
    }
  }
}
```

### Claude Desktop

Edita `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-py",
        "uv",
        "run",
        "mcp",
        "run",
        "mcp_server/main.py:mcp"
      ]
    }
  }
}
```

### Cursor

Agrega a tu configuración de MCP en Cursor:

```json
{
  "mcp.servers": {
    "google-drive": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-py",
        "uv",
        "run",
        "mcp",
        "run",
        "mcp_server/main.py:mcp"
      ]
    }
  }
}
```

### Windsurf

Configura el servidor MCP en Windsurf:

```json
{
  "mcp.servers": {
    "google-drive": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-py",
        "uv",
        "run",
        "mcp",
        "run",
        "mcp_server/main.py:mcp"
      ]
    }
  }
}
```

### Configuración Alternativa (Sin Docker)

Si prefieres ejecutar el servidor localmente sin Docker:

```json
{
  "command": "uv",
  "args": ["run", "mcp", "run", "mcp_server/main.py:mcp"],
  "cwd": "/ruta/absoluta/a/mcp-py"
}
```

> 💡 **Tip**: La configuración con Docker es recomendada para ambientes de producción y asegura consistencia entre diferentes máquinas.

---

## 🏗️ Arquitectura

Este proyecto sigue una arquitectura en capas clara y modular:

```
mcp-py/
├── mcp_server/            # Servidor MCP
│   ├── main.py           # Punto de entrada del servidor MCP
│   ├── gateway/          # Integraciones con servicios externos
│   │   └── google_drive_client.py
│   ├── services/         # Lógica de negocio
│   │   └── drive_service.py
│   └── tools/            # Herramientas MCP
│       ├── get_drive_file.py
│       ├── update_drive_file.py
│       └── test_server.py
├── credentials.json       # Credenciales de Google Cloud
├── pyproject.toml        # Dependencias del proyecto
└── docker-compose.yml    # Configuración de Docker
```

**Flujo de datos:**
```
Cliente MCP → Docker → mcp_server/main.py → tools/ → services/ → gateway/ → Google Drive API
```

Para más detalles sobre la arquitectura, consulta [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## 🐛 Solución de Problemas

### Error: "Servicio de Drive no inicializado"

**Causa:** El archivo `credentials.json` no se encuentra o tiene errores.

**Solución:**
1. Verifica que `credentials.json` existe en la raíz del proyecto
2. Verifica que el JSON es válido
3. Verifica que las credenciales no han expirado

---

### Error: "Permiso denegado" (403)

**Causa:** El archivo no está compartido con la cuenta de servicio.

**Solución:**
1. Abre `credentials.json` y copia el `client_email`
2. Comparte el archivo de Google Drive con ese email
3. Dale permisos de **Editor**

---

### El servidor no responde

**Solución:**
1. Verifica que el servidor está corriendo: `docker ps` o revisa logs
2. Verifica que el puerto no esté en uso
3. Reinicia el servidor: `docker-compose restart`

---

### Error al extraer file_id de la URL

**Causa:** El formato de la URL no es reconocido.

**Solución:**
El servidor acepta estos formatos:
- `https://docs.google.com/document/d/FILE_ID/edit`
- `https://drive.google.com/file/d/FILE_ID/view`
- `FILE_ID` (directo)

Si tu URL es diferente, usa el file_id directamente.

---

## 📚 Recursos Adicionales

- [Model Context Protocol Docs](https://modelcontextprotocol.io)
- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/about-sdk)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📧 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la sección [Solución de Problemas](#-solución-de-problemas)
2. Busca en los [Issues](https://github.com/tu-usuario/mcp-py/issues) existentes
3. Crea un nuevo Issue si es necesario

---

<div align="center">

**Hecho con ❤️ usando MCP**

</div>

