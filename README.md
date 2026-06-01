<div align="center">

# 🏛️ Sistema de Atención Ciudadana
## Alcaldía del Municipio Guanta

<img src="static/img/logo.webp" alt="Logo Alcaldía de Guanta" width="120"/>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-Demo-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)

</div>

---

> ## ⚠️ AVISO IMPORTANTE — VERSIÓN DEMO
>
> **Este repositorio contiene una versión de demostración** del sistema de gestión de atención ciudadana de la Alcaldía de Guanta.
>
> | Característica | Versión Demo (este repo) | Sistema Original (producción) |
> |---|---|---|
> | **Base de datos** | 🗄️ SQLite (archivo local) | 🐬 MySQL / MariaDB |
> | **Backend** | 🐍 Python + Flask | 🐍 Python + Flask |
> | **Propósito** | Evaluación y pruebas | Operación institucional |
> | **Datos** | Datos de muestra | Datos reales ciudadanos |
> | **Autenticación** | Sesiones básicas | Autenticación robusta |
>
> El sistema en producción opera sobre **Python + MySQL**, con mayor seguridad, manejo de concurrencia y capacidad para múltiples usuarios simultáneos. Esta demo usa **SQLite** para facilitar su instalación y evaluación sin necesidad de un servidor de base de datos.

---

## 🎯 ¿Qué es este sistema?

El **Sistema de Atención Ciudadana** es una plataforma web diseñada para que la Alcaldía del Municipio Guanta gestione eficientemente la atención a los ciudadanos, el registro de casos sociales y el seguimiento de las ayudas otorgadas.

### ✨ Funcionalidades principales

| Módulo | Descripción |
|--------|-------------|
| 📊 **Dashboard** | Panel de control con estadísticas en tiempo real y gráficos interactivos |
| 👥 **Ciudadanos** | Registro, búsqueda y administración de datos de ciudadanos |
| 📋 **Casos** | Gestión completa de casos: creación, seguimiento, aprobación y cierre |
| 🔀 **Remisiones** | Derivación de casos a entidades externas (Salud, Educación, FONDEGUNATA, etc.) |
| 📈 **Reportes** | Estadísticas por comuna, motivo de caso y entidad de remisión |

---

## 🛠️ Stack Tecnológico (Demo)

```
┌─────────────────────────────────────────────────────┐
│                   FRONTEND                          │
│  Bootstrap 5.3 · Chart.js · DataTables · SweetAlert2│
│  Font Awesome · jQuery                              │
├─────────────────────────────────────────────────────┤
│                   BACKEND                           │
│  Python 3.8+ · Flask 2.0 · Flask-Session           │
├─────────────────────────────────────────────────────┤
│               BASE DE DATOS (DEMO)                  │
│  SQLite 3 — archivo local: alc.db                  │
│                                                     │
│  ⚠️ En producción: MySQL / MariaDB                 │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Instalación Rápida (Demo)

### Opción 1: Script automático (Windows)

```bat
# Simplemente ejecuta:
start.bat
```

### Opción 2: Instalación manual

```bash
# 1. Clonar o descargar el repositorio
git clone https://github.com/Adrianmbt/AtencionAlcaldiaGuanta.git
cd AtencionAlcaldiaGuanta

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Inicializar base de datos SQLite
python init_db.py

# 6. (Opcional) Importar datos de muestra
python import_data.py

# 7. Iniciar la aplicación
python app.py
```

> 🌐 Accede a: **http://localhost:5000**

---

## 🔐 Credenciales de Acceso (Demo)

```
Usuario:    Adrianmbt
Contraseña: adrianmbt1
```

> ⚠️ Estas credenciales son solo para la demo. El sistema de producción cuenta con gestión de usuarios y roles más robusta.

---

## 📁 Estructura del Proyecto

```
AtencionAlcaldiaGuanta/
│
├── 📄 app.py                  # Aplicación principal Flask + rutas
├── ⚙️  config.py               # Configuración de la aplicación
├── 📋 requirements.txt        # Dependencias Python
├── 🗄️  alc.db                  # Base de datos SQLite (demo)
├── 🔧 init_db.py              # Inicializar esquema de base de datos
├── 📥 import_data.py          # Importar datos de respaldo
├── 🚀 start.bat               # Script de inicio rápido (Windows)
│
├── 📂 models/                 # Modelos de datos
│   ├── usuario.py
│   ├── persona.py
│   └── ayuda.py
│
├── 📂 templates/              # Plantillas HTML (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── ciudadano.html
│   ├── casos.html
│   └── proteccion.html
│
├── 📂 static/
│   ├── css/                   # Estilos personalizados
│   ├── js/                    # Scripts JavaScript
│   └── img/                   # Imágenes y logos
│
└── 📂 logs/                   # Registros de errores
```

---

## 🗄️ Esquema de Base de Datos

```sql
-- Tabla de usuarios del sistema
usuarios (id, usuario, clave, nombre, rol)

-- Tabla de ciudadanos registrados
persona (id, nombre, cedula, direccion, telefono, comuna)

-- Tabla de casos y ayudas
ayudas (
  id, idP, idUs,
  motivo_caso, especificacion_caso,
  valor_inversion_social,
  FechaSolicitud, FechaEntrega,
  descayuda, estado,
  remitido, entidad_remision, fecha_remision
)
```

---

## 🐛 Solución de Problemas

### `ModuleNotFoundError: No module named 'flask'`
```bash
pip install -r requirements.txt
```

### `Database is locked`
- Cierra todas las instancias del sistema
- Si el problema persiste, elimina `alc.db` y ejecuta `python init_db.py`

### `Permission denied`
- Ejecuta la terminal como **Administrador**
- Verifica que `alc.db` no esté siendo usado por otro proceso

---

## 🔄 Diferencias Demo vs Producción

```
DEMO (SQLite)                    PRODUCCIÓN (MySQL)
─────────────────────────────    ─────────────────────────────
✅ Instalación sin servidor DB   ✅ Alta concurrencia
✅ Archivo único (alc.db)        ✅ Backup automatizado
✅ Ideal para evaluación         ✅ Múltiples usuarios simultáneos
⚠️  Un usuario a la vez         ✅ Transacciones ACID completas
⚠️  Sin replicación             ✅ Replicación y alta disponibilidad
⚠️  Limitada en producción      ✅ Escalable para producción
```

---

## 📞 Contacto y Soporte

Para información sobre el sistema de producción o soporte técnico, contactar al equipo de desarrollo de la Alcaldía del Municipio Guanta.

---

## 📄 Licencia

Este sistema es de uso institucional de la **Alcaldía del Municipio Guanta**, Estado Anzoátegui, Venezuela.

---

<div align="center">

**Sistema de Atención Ciudadana** — Alcaldía de Guanta  
Versión Demo `1.0.0` · Junio 2026  
*Sistema original desarrollado en Python + MySQL*

</div>
