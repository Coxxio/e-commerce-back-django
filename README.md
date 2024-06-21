## Installation

Poetry provides a custom installer that will install `poetry` isolated
from the rest of your system.

### osx / linux / bashonwindows install instructions
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
### windows powershell install instructions
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Clone the repository 
Clone with SSH
```bash
git clone git@gitlab.com:Coxxio/ecommerce-back-django.git
```
Or Clone with HTTPS
```bash
https://gitlab.com/Coxxio/ecommerce-back-django.git
```

### Install dependencies
```bash
cd ecommerce-back-django
```
```bash
poetry install
```

### Create the database
- Instalar MongoDB
- Crear su usuario

### Configure the .env file

copiar el archivo .env.example como .env en la ruta raiz del sistema y configurar las siguiente variables.

```bash
DB_NAME=
DB_TEST=
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=27017

JWT=5
JWT_REFRESH=30

DJANGO_SETTINGS_MODULE=src.settings.dev
SECRET_KEY=django-insecure-_l67gkupnfr_79_tmq&wro_s*o0kyzrhh%g+^vv@
```
### Getting started
```bash
poetry shell
```
```bash
py manage.py migrate
```
```bash
py manage.py LoadSeeds
```
### Initializing project
```bash
poetry shell
```
```bash
py manage.py runserver
```
### Run Tests
```bash
py manage.py test
```
