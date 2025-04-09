Запуск сервиса

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