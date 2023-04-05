### Тестовой задание для Python Backend Developer

**Запуск проекта:**

`python main.py`

**Запуск тестов:**

`pytest test.py`

**Задание**
* Напишите скрипт, асинхронно, в 3 одновременных задачи, скачивающий содержимое HEAD репозитория https://gitea.radium.group/radium/project-configuration во временную папку.
* После выполнения всех асинхронных задач скрипт должен посчитать sha256 хэши от каждого файла.
* Код должен проходить без замечаний проверку линтером wemake-python-styleguide. Конфигурация nitpick - https://gitea.radium.group/radium/project-configuration
* Обязательно 100% покрытие тестами
