# Divine Peluquería - Aplicación Web

Un sistema completo de gestión para peluquerías construido con Reflex, FastAPI y MongoDB. Esta aplicación permite a los usuarios registrarse, iniciar sesión, ver servicios y gestionar citas. Los administradores pueden gestionar usuarios y servicios a través de un panel de control.

## Tecnologías Utilizadas

- **Frontend y Backend**: [Reflex](https://reflex.dev/) v0.7.14 (Python full-stack)
- **API**: FastAPI
- **Base de Datos**: MongoDB
- **Autenticación**: JWT
- **Otros paquetes**: bcrypt, pydantic, pymongo, pendulum, etc.

## Estructura del Proyecto

```
peluqueria/
├── .env                 # Variables de entorno
├── requirements.txt     # Dependencias del proyecto
├── rxconfig.py          # Configuración de Reflex
├── assets/              # Recursos estáticos (imágenes, CSS)
└── peluqueria/
    ├── __init__.py
    ├── constants.py     # Constantes del proyecto
    ├── peluqueria.py    # Punto de entrada principal
    ├── settings.py      # Configuración del proyecto
    ├── utils.py         # Utilidades generales
    ├── api/             # API Backend (FastAPI)
    ├── components/      # Componentes reutilizables
    ├── pages/           # Páginas principales
    ├── state/           # Estado global
    ├── styles/          # Estilos de la aplicación
    └── views/           # Vistas y componentes específicos
```

## Requisitos Previos

- Python 3.9 o superior
- MongoDB instalado y en ejecución
- pip (gestor de paquetes de Python)

## Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone <repositorio>
   cd peluqueria
   ```

2. **Crear y activar un entorno virtual**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   
   Crea o modifica el archivo `.env` en la raíz del proyecto:
   ```
   MONGO_DB_URI="mongodb://localhost:27017/"
   MONGO_DB_NAME="peluqueria"
   API_BACKEND_URL="http://localhost:8000"
   ```

5. **Inicializar la base de datos MongoDB**:
   - Asegúrate de que MongoDB esté en ejecución en tu sistema
   - La aplicación creará automáticamente las colecciones y los índices necesarios

## Ejecución del Proyecto

1. **Iniciar la aplicación en modo desarrollo**:
   ```bash
   reflex run
   ```

2. **Acceder a la aplicación**:
   - Abre tu navegador en `http://localhost:3000`
   - La API estará disponible en `http://localhost:8000`

## Despliegue en Producción

### Opción 1: Servidor dedicado

1. **Construir la aplicación**:
   ```bash
   reflex build
   ```

2. **Ejecutar en modo producción**:
   ```bash
   reflex run --env prod
   ```

3. **Configurar un servidor web** (Nginx recomendado):
   - Configura Nginx como proxy inverso para tu aplicación
   - Asegura las conexiones con SSL/TLS (usar Certbot para Let's Encrypt)

## Características Principales

- **Autenticación de usuarios**: Registro e inicio de sesión
- **Visualización de servicios**: Información detallada sobre servicios de peluquería
- **Gestión de citas**: Agendamiento y administración de citas
- **Panel administrativo**: Gestión de usuarios y servicios
- **Diseño responsive**: Adaptable a dispositivos móviles y de escritorio

## Seguridad

- Las contraseñas se almacenan con hash seguro usando bcrypt
- Autenticación basada en tokens JWT
- Validación de datos con Pydantic
- HTTPS recomendado para producción

## Mantenimiento

- **Backups**: Realizar copias de seguridad periódicas de la base de datos MongoDB
- **Actualizaciones**: Mantener actualizadas las dependencias con pip

## Solución de Problemas Comunes

- **Error de conexión a MongoDB**: Verificar que MongoDB esté en ejecución y que la URI en `.env` sea correcta
- **Problemas con las rutas**: Asegurarse de que todos los archivos `__init__.py` estén presentes en los directorios
- **Error al ejecutar reflex**: Verificar la versión de Python y que todas las dependencias estén instaladas

## Documentación de API (FastAPI)

La API del backend está construida con FastAPI y proporciona documentación interactiva automáticamente generada.

### Acceso a la Documentación API

Cuando la aplicación está en ejecución, puedes acceder a la documentación interactiva de la API en:

- **Swagger UI**: `http://localhost:8000/docs`
  - Interfaz interactiva completa para explorar y probar los endpoints
  - Permite enviar solicitudes directamente desde el navegador
  - Muestra todos los modelos de datos y esquemas

- **ReDoc**: `http://localhost:8000/redoc`
  - Documentación alternativa más limpia y orientada a la lectura
  - Ideal para consulta de referencia

### Endpoints Principales

La API incluye los siguientes grupos de endpoints:

#### Autenticación (`/auth`)
- `POST /auth/login` - Inicio de sesión y generación de token JWT
- `GET /auth/me` - Obtener información del usuario autenticado

#### Usuarios (`/users`)
- `GET /users/` - Listar usuarios (solo admin)
- `GET /users/{user_id}` - Obtener detalles de un usuario
- `POST /users` - Registrar un usuario
- `PATCH /users/{user_id}` - Actualizar información de usuario
- `DELETE /users/{user_id}` - Eliminar usuario

#### Servicios (`/services`)
- `GET /services/` - Listar todos los servicios disponibles
- `POST /services/` - Crear un nuevo servicio (solo admin)
- `PATCH /services/{service_id}` - Actualizar un servicio
- `DELETE /services/{service_id}` - Eliminar un servicio

### Uso de la API

Para usar la API directamente:

1. Obtén un token de autenticación a través del endpoint de login
2. Incluye el token en el encabezado de autorización de tus solicitudes:
   ```
   Authorization: Bearer {tu_token_jwt}
   ```


---