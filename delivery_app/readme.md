# Delivery App

Proyecto para encontrar el camino mínimo

## Requisitos

- Python 3.8
- Docker

## Instalación

    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate

o

    docker-compose up -d

## Configuración

Generar Llave ApiKey Google Maps y agregarlo a settings.py

GOOGLE_MAPS_API_KEY = "Google ApiKey"

