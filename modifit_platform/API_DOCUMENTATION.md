# Modifit Platform - API Documentation

## Base URL
```
http://localhost:8000/api
```

## Autenticación

Esta API utiliza JWT (JSON Web Tokens) para autenticación. Los endpoints protegidos requieren incluir el token en el header:

```
Authorization: Bearer <access_token>
```

---

## Endpoints de Autenticación

### 1. Registro de Usuario
**POST** `/api/auth/register/`

Crea un nuevo usuario en el sistema.

**Request Body:**
```json
{
    "username": "string",
    "email": "email@example.com",
    "password": "string",
    "password_confirm": "string",
    "first_name": "string (opcional)",
    "last_name": "string (opcional)"
}
```

**Response (201 Created):**
```json
{
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "email@example.com",
        "first_name": "",
        "last_name": "",
        "date_joined": "2025-10-22T12:00:00Z"
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "Usuario creado exitosamente"
}
```

---

### 2. Login
**POST** `/api/auth/login/`

Autentica un usuario existente.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "email@example.com",
        "first_name": "",
        "last_name": "",
        "date_joined": "2025-10-22T12:00:00Z"
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "message": "Login exitoso"
}
```

**Error Response (400 Bad Request):**
```json
{
    "non_field_errors": ["Credenciales inválidas."]
}
```

---

### 3. Obtener Perfil de Usuario
**GET** `/api/auth/profile/`

Obtiene la información del usuario autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "usuario",
    "email": "email@example.com",
    "first_name": "",
    "last_name": "",
    "date_joined": "2025-10-22T12:00:00Z"
}
```

---

### 4. Refrescar Token
**POST** `/api/auth/token/refresh/`

Obtiene un nuevo access token usando el refresh token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## Endpoints de Fitness

### 5. Home
**GET** `/api/fitness/home/`

Vista principal de la aplicación fitness (requiere autenticación).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "message": "Bienvenido a Modifit, usuario!",
    "user": {
        "id": 1,
        "username": "usuario",
        "email": "email@example.com"
    }
}
```

---

## Configuración JWT

- **Access Token Lifetime**: 5 horas
- **Refresh Token Lifetime**: 1 día
- **Token Type**: Bearer

---

## Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Error en los datos enviados
- `401 Unauthorized` - Token inválido o no proporcionado
- `403 Forbidden` - Sin permisos para acceder al recurso
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## Ejemplos de Uso con JavaScript (Fetch API)

### Registro
```javascript
const response = await fetch('http://localhost:8000/api/auth/register/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'usuario',
        email: 'email@example.com',
        password: 'mipassword123',
        password_confirm: 'mipassword123'
    })
});

const data = await response.json();
console.log(data);
```

### Login y guardar token
```javascript
const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'usuario',
        password: 'mipassword123'
    })
});

const data = await response.json();
// Guardar tokens en localStorage
localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);
```

### Hacer petición autenticada
```javascript
const token = localStorage.getItem('access_token');

const response = await fetch('http://localhost:8000/api/fitness/home/', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    }
});

const data = await response.json();
console.log(data);
```

### Refrescar token
```javascript
const refreshToken = localStorage.getItem('refresh_token');

const response = await fetch('http://localhost:8000/api/auth/token/refresh/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        refresh: refreshToken
    })
});

const data = await response.json();
localStorage.setItem('access_token', data.access);
```
