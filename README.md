# API Favoritos Spotify 

API desarrollada con Django para gestionar usuarios y sus favoritos en Spotify: artistas, discos y canciones.

## Estructura del proyecto

```
API_Spotify_Django/
│
├─ api_server/             # Configuración del proyecto Django
├─ viewset_spotify/        # Aplicación principal
├─ .env                    # Variables de entorno
├─ db.sqlite3              # Base de datos SQLite
├─ manage.py               # Script de gestión de Django
├─ requirements.txt        # Dependencias
├─ usuarios.json           # Datos iniciales de usuarios y favoritos
└─ README.md               # Documentación
```

## Requisitos

- Python 3.14+
- Virtualenv (recomendado)

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

1. Activar el entorno virtual:

```bash
.venv/Scripts/activate  # Windows PowerShell
```

2. Introducir las credenciales de Spotify en archivo `.env`:

```
SPOTIFY_CLIENT_ID=tu_client_id
SPOTIFY_CLIENT_SECRET=tu_client_secret
```

3. Migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Cargar datos iniciales (usuarios y favoritos) desde `usuarios.json`:

```bash
python manage.py loaddata usuarios.json
```

## Ejecutar servidor

```bash
python manage.py runserver
```

Accede a la API en `http://127.0.0.1:8000/viewset-spotify/`

## Endpoints principales

- **Agregar favorito** (POST, enviar JSON en el body):
  - `/viewset-spotify/usuarios/{id}/add_artista/`  → Añadir artista
  - `/viewset-spotify/usuarios/{id}/add_disco/`    → Añadir disco
  - `/viewset-spotify/usuarios/{id}/add_cancion/`  → Añadir canción

- **Listar favoritos** (GET):
  - `/viewset-spotify/usuarios/{id}/ver_artistas/`
  - `/viewset-spotify/usuarios/{id}/ver_discos/`
  - `/viewset-spotify/usuarios/{id}/ver_canciones/`

- **Borrar favorito** (DELETE, enviar JSON en el body con `favorito_id`):
  - `/viewset-spotify/usuarios/{id}/borrar_artista/`
  - `/viewset-spotify/usuarios/{id}/borrar_disco/`
  - `/viewset-spotify/usuarios/{id}/borrar_cancion/`

## Documentación Swagger / OpenAPI

Documentación disponible en:

```
http://127.0.0.1:8000/swagger/
```

Aquí se pueden ver y probar todos los endpoints.

## Notas

- Los datos iniciales en `usuarios.json` permiten probar la API sin necesidad de crear manualmente usuarios y favoritos.
- Los datos musicales se obtienen desde la API de Spotify
- Solo se almacenan favoritos validados
- No se permiten duplicados por usuario

