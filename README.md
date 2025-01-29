# my-devops-project

Создание простого веб-приложения (на Python/Flask).

Контейнеризацию приложения с помощью Docker.

Настройку CI/CD с использованием GitHub Actions.

Оркестрацию контейнеров с помощью Docker Compose.

Мониторинг и логирование (опционально, если есть время).

Шаг 1: Создание простого веб-приложения
Установи Python и Flask, если они еще не установлены:

bash
Copy
sudo apt-get update
sudo apt-get install python3 python3-pip
pip3 install Flask
Создай директорию для проекта:

bash
Copy
mkdir my-devops-project
cd my-devops-project
Создай файл app.py с простым веб-приложением на Flask:

python
Copy
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, DevOps World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
Запусти приложение:

bash
Copy
python3 app.py
Перейди в браузере по адресу http://localhost:5000, чтобы убедиться, что приложение работает.

Шаг 2: Контейнеризация приложения с помощью Docker
Создай файл Dockerfile в корневой директории проекта:

Dockerfile
Copy
# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
Создай файл requirements.txt:

Copy
Flask==2.0.1
Собери Docker-образ:

bash
Copy
docker build -t my-devops-app .
Запусти контейнер:

bash
Copy
docker run -d -p 5000:5000 my-devops-app
Проверь, что приложение работает по адресу http://localhost:5000.

Шаг 3: Настройка CI/CD с использованием GitHub Actions
Создай репозиторий на GitHub и загрузи туда свой проект.

Создай директорию .github/workflows в корне проекта:

bash
Copy
mkdir -p .github/workflows
Создай файл ci-cd.yml в директории .github/workflows:

yaml
Copy
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python -m unittest discover

    - name: Build Docker image
      run: docker build -t my-devops-app .

    - name: Login to Docker Hub
      run: echo "${{ secrets.DOCKER_HUB_TOKEN }}" | docker login -u "${{ secrets.DOCKER_HUB_USERNAME }}" --password-stdin

    - name: Push Docker image
      run: |
        docker tag my-devops-app ${{ secrets.DOCKER_HUB_USERNAME }}/my-devops-app:latest
        docker push ${{ secrets.DOCKER_HUB_USERNAME }}/my-devops-app:latest
Добавь секреты DOCKER_HUB_USERNAME и DOCKER_HUB_TOKEN в настройках репозитория на GitHub.

Шаг 4: Оркестрация контейнеров с помощью Docker Compose
Создай файл docker-compose.yml:

yaml
Copy
version: '3'
services:
  web:
    image: my-devops-app
    build: .
    ports:
      - "5000:5000"
Запусти приложение с помощью Docker Compose:

bash
Copy
docker-compose up -d
Проверь, что приложение работает по адресу http://localhost:5000.

Шаг 5: Мониторинг и логирование (опционально)
Добавь сервис для мониторинга, например, Prometheus и Grafana.

Настрой сбор логов с помощью ELK-стека (Elasticsearch, Logstash, Kibana) или Fluentd.
