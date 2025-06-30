# Sistema de Protección de Rutas - Peluquería

## Descripción General

El sistema de protección de rutas permite controlar el acceso a diferentes páginas según el estado de autenticación y rol del usuario. Esto reemplaza el componente anterior `protect_auth_login` con un sistema más flexible y reutilizable.

## Tipos de Protección Disponibles

### 1. `anonymous_only_guard`
**Uso**: Para páginas que solo deben ser accesibles a usuarios NO autenticados (login, registro)
```python
from peluqueria.components.route_guard import anonymous_only_guard

def login() -> rx.Component:
    content = rx.vstack(
        navbar(),
        login_form(),
        footer(),
    )
    return anonymous_only_guard(content)
```

### 2. `authenticated_only_guard`
**Uso**: Para páginas que requieren que el usuario esté autenticado (citas)
```python
from peluqueria.components.route_guard import authenticated_only_guard

def appointments_table() -> rx.Component:
    content = rx.flex(
        # Contenido de la tabla de citas
    )
    return authenticated_only_guard(content)
```

### 3. `employee_only_guard`
**Uso**: Para páginas que solo pueden acceder empleados (dashboard, gestión)
```python
from peluqueria.components.route_guard import employee_only_guard

def users_manage() -> rx.Component:
    content = rx.hstack(sidebar(), users_table())
    return employee_only_guard(content)
```

### 4. `customer_restricted_guard`
**Uso**: Para páginas a las que los clientes NO pueden acceder
```python
from peluqueria.components.route_guard import customer_restricted_guard

def admin_panel() -> rx.Component:
    content = rx.div("Panel de administración")
    return customer_restricted_guard(content)
```

## Personalización de Mensajes

Todos los guards permiten personalizar los mensajes y rutas de redirección:

```python
def my_protected_page() -> rx.Component:
    content = rx.div("Contenido protegido")
    return authenticated_only_guard(
        content,
        redirect_path="/ingreso",
        title="Acceso Denegado",
        message="Necesitas iniciar sesión para ver esta página",
        button_text="Ir al Login"
    )
```

## Matriz de Protección por Tipo de Usuario

| Ruta | Usuario Anónimo | Customer | Employee |
|------|----------------|----------|----------|
| `/` (inicio) | ✅ | ✅ | ✅ |
| `/ingreso` | ✅ | ❌ | ❌ |
| `/registro` | ✅ | ❌ | ❌ |
| `/citas` | ❌ | ✅ | ✅ |
| `/dashboard` | ❌ | ❌ | ✅ |

## Implementación Actual

### Páginas ya Protegidas:
- ✅ `/ingreso` - `anonymous_only_guard`
- ✅ `/registro` - `anonymous_only_guard`
- ✅ `/citas` - `authenticated_only_guard`
- ✅ `/dashboard/usuarios` - `employee_only_guard`
- ✅ `/dashboard/servicios` - `employee_only_guard`

### Características del Sistema:
- **Flexible**: Fácil personalización de mensajes y rutas
- **Reutilizable**: Un solo componente para múltiples tipos de protección
- **Consistente**: UI unificada para mensajes de acceso denegado
- **Type-safe**: Utiliza las propiedades computadas del AuthState

### Estado de Autenticación (AuthState):
El sistema utiliza las siguientes propiedades del estado global:
- `is_authenticated`: Boolean que indica si el usuario está autenticado
- `user_role`: String con el rol del usuario ("customer" o "employee")
- `is_customer`: Propiedad computada para verificar si es cliente
- `is_employee`: Propiedad computada para verificar si es empleado
