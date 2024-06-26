---

# Инструкция по развертыванию Flask приложения с PostgreSQL через Docker Compose

Этот проект демонстрирует развертывание Flask приложения с использованием PostgreSQL базы данных через Docker Compose. Ниже приведены инструкции по инициализации и запуску проекта.

## Требования

Убедитесь, что у вас установлены следующие компоненты:

- Docker
- Docker Compose

## Шаги инициализации

### Клонирование репозитория

```
git clone https://github.com/madiyar9802/task_manager.git
cd task_manager
```

### Создание .env файла

Создайте файл `.env` в корне проекта и добавьте следующие переменные окружения:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres
POSTGRES_DATABASE_URL=postgresql://postgres:password@db:5432/postgres
```

Эти переменные будут использоваться в настройках Docker Compose для подключения к PostgreSQL.

### Запуск Docker Compose

Запустите Docker Compose для сборки и запуска контейнеров:

```
docker-compose up --build
```

Эта команда соберет и запустит контейнеры для Flask приложения и PostgreSQL базы данных. Вы увидите вывод, отображающий процесс запуска.

### Проверка работоспособности

Откройте веб-браузер и перейдите на [http://localhost:5002](http://localhost:5002), чтобы убедиться, что Flask приложение работает корректно.

### Остановка контейнеров

Чтобы остановить контейнеры, используйте сочетание клавиш `Ctrl + C`, затем выполните:

```
docker-compose down
```

Эта команда остановит и удалит контейнеры.

## Дополнительные настройки

### Настройки Flask приложения

При необходимости внесите изменения в файлы Flask приложения в соответствии с вашими требованиями. Обратитесь к документации Flask для более подробной информации о настройках.

### Настройки PostgreSQL

Вы можете изменить переменные окружения в `.env` файле для PostgreSQL под свои требования. Убедитесь, что настройки соответствуют конфигурации PostgreSQL, которую вы хотите использовать.

---

