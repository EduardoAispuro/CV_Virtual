# CV Project - Desarrollador Full Stack

Un proyecto interactivo de CV que combina un backend Flask con un frontend React, incluyendo funcionalidades de escaneo de puertos con nmap y sistema de donaciones con Stripe.

## 📂 Estructura del Proyecto

```
📂 cv-project/
├─ backend/ (Flask API)
│   ├─ app.py                    # Servidor Flask principal
│   ├─ scan_utils.py            # Utilidades para escaneo nmap
│   ├─ requirements.txt         # Dependencias Python
│   └─ .env                     # Variables de entorno (no subir a git)
└─ frontend/ (React + Vite)
    ├─ package.json             # Dependencias Node.js
    ├─ vite.config.js          # Configuración Vite
    ├─ index.html              # HTML principal
    └─ src/
        ├─ main.jsx            # Punto de entrada React
        ├─ App.jsx             # Componente principal
        ├─ index.css           # Estilos globales
        └─ components/
            ├─ NmapScanner.jsx # Componente escáner de puertos
            └─ DonateButton.jsx # Componente de donaciones
```

## 🚀 Características

### Backend (Flask)
- **API REST** con endpoints para CV, escaneo de puertos y pagos
- **Seguridad**: Solo permite escaneo en localhost/127.0.0.1
- **Integración Stripe** para procesamiento de pagos en modo test
- **Validación robusta** de entrada de datos
- **CORS habilitado** para desarrollo frontend

### Frontend (React + Vite)
- **Interfaz moderna** y responsive con diseño profesional
- **Componentes reutilizables** para funcionalidades específicas
- **Integración API** con axios para comunicación backend
- **UX optimizada** con estados de carga y manejo de errores
- **Puerto personalizado** 5173 como solicitado

### Funcionalidades Principales
1. **Visualización de CV** - Muestra perfil, experiencia, educación y habilidades
2. **Escáner de Puertos** - Herramienta de seguridad usando nmap
3. **Sistema de Donaciones** - Integración con Stripe Checkout

## 📋 Requisitos Previos

### Sistema
- **Python 3.8+** instalado
- **Node.js 16+** y npm instalados
- **nmap** instalado en el sistema

### Instalación de nmap

#### Windows
1. Descargar desde: https://nmap.org/download.html
2. Instalar el ejecutable
3. Agregar nmap al PATH del sistema

#### macOS
```bash
brew install nmap
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install nmap
```

### Verificar instalación de nmap
```bash
nmap --version
```

## ⚙️ Configuración e Instalación

### Opción 1: Instalación con Docker (Recomendada) 🐳

#### Requisitos previos
- Docker Desktop instalado
- Docker Compose instalado

#### Configuración rápida
1. **Clonar/Descargar el proyecto**
```bash
# Si usas git
git clone <repository-url>
cd cv-project

# O descargar y extraer el ZIP
```

2. **Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example backend/.env

# Editar backend/.env con tus claves de Stripe
```

3. **Ejecutar con Docker Compose**
```bash
# Producción (Frontend en puerto 80, Backend en puerto 5000)
docker-compose up -d

# O para desarrollo con hot reload (Frontend en puerto 5173)
docker-compose -f docker-compose.dev.yml up -d
```

#### Acceso a la aplicación
- **Producción**: http://localhost (puerto 80)
- **Desarrollo**: http://localhost:5173
- **API Backend**: http://localhost:5000

#### Comandos útiles Docker
```bash
# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Ver estado de contenedores
docker-compose ps

# Ejecutar comando en contenedor
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Opción 2: Instalación Manual (Sin Docker)

#### 1. Clonar/Descargar el Proyecto
```bash
# Si usas git
git clone <repository-url>
cd cv-project

# O descargar y extraer el ZIP
```

#### 2. Configurar Backend

##### Navegar al directorio backend
```bash
cd backend
```

##### Crear entorno virtual
```bash
python -m venv venv
```

##### Activar entorno virtual
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

##### Instalar dependencias
```bash
pip install -r requirements.txt
```

##### Configurar variables de entorno
1. Abrir el archivo `.env`
2. Reemplazar las claves de Stripe con tus claves de prueba:

```env
# Obtener estas claves desde https://dashboard.stripe.com/test/apikeys
STRIPE_SECRET_KEY=sk_test_tu_clave_secreta_aqui
STRIPE_PUBLISHABLE_KEY=pk_test_tu_clave_publica_aqui

FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta_cambiar_en_produccion
```

##### Ejecutar servidor backend
```bash
python app.py
```

El servidor estará disponible en: http://localhost:5000

#### 3. Configurar Frontend

##### Abrir nueva terminal y navegar al directorio frontend
```bash
cd frontend
```

##### Instalar dependencias
```bash
npm install
```

##### Ejecutar servidor de desarrollo
```bash
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## 🔧 Uso de la Aplicación

### 1. Visualizar CV
- La página principal muestra automáticamente el CV completo
- Incluye perfil, experiencia profesional, educación y habilidades técnicas

### 2. Escáner de Puertos
- Ubicado en la sección "Herramientas"
- Ingresa un rango de puertos (ej: "22-443", "80-8080")
- Solo funciona con localhost por seguridad
- Muestra puertos abiertos, cerrados y filtrados
- Incluye información detallada de servicios detectados

### 3. Sistema de Donaciones
- Selecciona un monto predefinido o ingresa uno personalizado
- Usa tarjetas de prueba de Stripe para testing
- Se abre Stripe Checkout en nueva pestaña

## 💳 Tarjetas de Prueba Stripe

Para probar el sistema de pagos, usa estas tarjetas de prueba:

| Tarjeta | Número | Resultado |
|---------|--------|-----------|
| Visa | 4242 4242 4242 4242 | Pago exitoso |
| Visa (débito) | 4000 0566 5566 5556 | Pago exitoso |
| Mastercard | 5555 5555 5555 4444 | Pago exitoso |
| American Express | 3782 822463 10005 | Pago exitoso |
| Visa (declinada) | 4000 0000 0000 0002 | Pago declinado |

**Datos adicionales para pruebas:**
- **Fecha de expiración:** Cualquier fecha futura (ej: 12/25)
- **CVC:** Cualquier número de 3-4 dígitos (ej: 123)
- **Código postal:** Cualquier código válido (ej: 12345)

## 🛠️ API Endpoints

### Backend (http://localhost:5000)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/cv` | Obtiene datos del CV en JSON |
| POST | `/api/scan` | Escanea puertos con nmap |
| POST | `/api/create-checkout-session` | Crea sesión de pago Stripe |
| GET | `/api/health` | Verifica estado del servidor |

#### Ejemplo de uso del endpoint de escaneo:
```bash
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"port_range": "80-443", "target": "localhost"}'
```

## 🔒 Consideraciones de Seguridad

### Escaneo de Puertos
- **Restricción de objetivo**: Solo localhost/127.0.0.1 permitidos
- **Límite de rango**: Máximo 1000 puertos por escaneo
- **Validación de entrada**: Formato y rangos validados
- **Timeout configurado**: Evita escaneos indefinidos

### Stripe Integration
- **Modo test**: Solo para desarrollo y pruebas
- **Claves seguras**: Variables de entorno para credenciales
- **Validación de montos**: Monto mínimo $0.50 USD
- **URLs de retorno**: Configuradas para localhost

## 🐛 Solución de Problemas

### Backend no inicia
1. Verificar que Python 3.8+ esté instalado
2. Confirmar que el entorno virtual esté activado
3. Instalar dependencias: `pip install -r requirements.txt`
4. Verificar que el puerto 5000 esté libre

### Frontend no carga
1. Verificar que Node.js 16+ esté instalado
2. Instalar dependencias: `npm install`
3. Verificar que el puerto 5173 esté libre
4. Confirmar que el backend esté ejecutándose

### Escaneo nmap falla
1. Verificar instalación de nmap: `nmap --version`
2. En Windows, confirmar que nmap esté en el PATH
3. Ejecutar como administrador si es necesario
4. Verificar permisos de firewall

### Stripe no funciona
1. Verificar claves de API en `.env`
2. Confirmar que sean claves de **test** (empiezan con `sk_test_` y `pk_test_`)
3. Verificar conexión a internet
4. Revisar logs del backend para errores específicos

### Error de CORS
1. Verificar que flask-cors esté instalado
2. Confirmar que el backend esté en puerto 5000
3. Verificar que el frontend esté en puerto 5173

## 📝 Scripts Disponibles

### Backend
```bash
# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (macOS/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py

# Desactivar entorno virtual
deactivate
```

### Frontend
```bash
# Instalar dependencias
npm install

# Ejecutar en desarrollo (puerto 5173)
npm run dev

# Construir para producción
npm run build

# Vista previa de build
npm run preview

# Linting
npm run lint
```

## 🐳 Arquitectura Docker

### Estructura de Contenedores

```
📦 Docker Setup
├─ backend/
│   ├─ Dockerfile              # Imagen Python con Flask + nmap
│   └─ .dockerignore          # Exclusiones para build
├─ frontend/
│   ├─ Dockerfile             # Build multi-stage con nginx
│   ├─ Dockerfile.dev         # Imagen de desarrollo con hot reload
│   ├─ nginx.conf            # Configuración nginx para producción
│   └─ .dockerignore         # Exclusiones para build
├─ docker-compose.yml         # Orquestación para producción
├─ docker-compose.dev.yml     # Orquestación para desarrollo
└─ .env.example              # Template de variables de entorno
```

### Características Docker

#### Backend Container
- **Base**: Python 3.11 slim
- **Incluye**: nmap preinstalado
- **Puerto**: 5000
- **Healthcheck**: Endpoint `/api/health`
- **Seguridad**: Usuario no-root
- **Volúmenes**: `.env` montado como read-only

#### Frontend Container (Producción)
- **Build multi-stage**: Node.js para build + nginx para serving
- **Puerto**: 80
- **Proxy**: API calls redirigidas al backend
- **Optimizaciones**: Gzip, cache headers, seguridad headers
- **Healthcheck**: Verificación HTTP

#### Frontend Container (Desarrollo)
- **Base**: Node.js Alpine
- **Puerto**: 5173
- **Hot reload**: Cambios en tiempo real
- **Volúmenes**: Código fuente montado

### Redes Docker
- **Producción**: `cv-project-network`
- **Desarrollo**: `cv-project-dev-network`
- **Comunicación**: Backend accesible como `backend:5000`

## 🚀 Despliegue en Producción

### Opción 1: Docker (Recomendada)
```bash
# 1. Configurar variables de entorno
cp .env.example backend/.env
# Editar backend/.env con claves reales de Stripe

# 2. Ejecutar en producción
docker-compose up -d

# 3. Verificar estado
docker-compose ps
docker-compose logs -f
```

### Opción 2: Despliegue Manual

#### Backend
1. Cambiar `FLASK_ENV=production` en `.env`
2. Usar claves reales de Stripe (no test)
3. Configurar servidor web (nginx + gunicorn)
4. Habilitar HTTPS
5. Configurar firewall apropiadamente

#### Frontend
1. Ejecutar `npm run build`
2. Servir archivos estáticos desde `dist/`
3. Configurar proxy para API calls
4. Habilitar HTTPS

### Consideraciones de Producción
- **SSL/TLS**: Habilitar HTTPS con certificados válidos
- **Firewall**: Restringir acceso a puertos necesarios
- **Monitoreo**: Logs centralizados y métricas
- **Backup**: Estrategia de respaldo para datos
- **Escalabilidad**: Load balancer para múltiples instancias

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear rama para feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Juan Pérez**
- Email: juan.perez@email.com
- LinkedIn: [linkedin.com/in/juanperez](https://linkedin.com/in/juanperez)
- GitHub: [github.com/juanperez](https://github.com/juanperez)

## 🙏 Agradecimientos

- **Flask** - Framework web para Python
- **React** - Biblioteca para interfaces de usuario
- **Vite** - Build tool rápido para desarrollo
- **Stripe** - Plataforma de pagos
- **nmap** - Herramienta de escaneo de red
- **Lucide React** - Iconos para React

---

**¡Gracias por usar CV Project! 🎉**

Si tienes preguntas o encuentras algún problema, no dudes en crear un issue o contactarme directamente.
