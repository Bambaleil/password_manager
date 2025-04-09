# Локальная разработка (Без Docker)

Инструкция по установке зависимостей, настройке окружения и запуску проекта с использованием **Python 3.12**, **Poetry** и **PostgreSQL**.

---

## Требования

- Python **3.12**
- pip (обновлённый)
- [Poetry](https://python-poetry.org/)
- PostgreSQL

---

## Установка зависимостей

### 1. Обновите pip

```bash
python.exe -m pip install --upgrade pip
```

### 2. Установите Poetry

```bash
pip install poetry
```

### 3. Установите зависимости проекта

Перейдите в директорию проекта (например, `backend`) и выполните:

```bash
cd backend
poetry install --no-root
```

---

## Виртуальное окружение

### 4. Явно укажите версию Python

```bash
poetry env use 3.12
```

Также можно:

```bash
poetry env use python
```

### 5. Посмотреть путь к окружению

```bash
poetry env info --path
```

### 6. Активация окружения

Автоматически:

```bash
poetry env activate
```

Или вручную (для PowerShell):

```powershell
& "C:\Users\Профиль\AppData\Local\pypoetry\Cache\virtualenvs\Ваша_вертуалка\Scripts\activate.ps1"
```

---

## Настройка в PyCharm

1. Открой **Settings → Python Interpreter**
2. Нажми **Add Interpreter → Add Local Interpreter**
3. Выбери **Poetry Environment → Existing Environment**
4. Укажи путь до `python.exe` из виртуального окружения

---

## Обновление зависимостей

Если нужно обновить зависимости:

```bash
poetry update
```

---

## Настройка переменных окружения

Создай `.env` файл на основе шаблона:

```bash
cp .env.template .env
```

Заполни все необходимые переменные в `.env`.

---

## Установка и настройка PostgreSQL

1. Установи PostgreSQL
2. Создай базу данных:

```sql
CREATE DATABASE data_base;
```

---

## Миграции с Alembic

Примените миграции:

```bash
poetry run alembic upgrade head
```

---

## Запуск приложения

Запусти основной модуль приложения:

```bash
python -m app.main
```

---


настройка pre-commit

установка и запуск гит-хуков

```bash
pre-commit install
pre-commit run
```
# Локальная разработка (С Docker)

1) Скачать docker
2) Создай `.env` файл на основе шаблона: Заполни все необходимые переменные в `.env`.

```bash
cp .env.template .env
```


3) Запустить команду
вручную
```bash
docker-compose up -d --build
```
через скрипт
```bash
scripts.\build.sh
```
