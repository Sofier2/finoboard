# FinoBoard

## Опис
FinoBoard — це веб-застосунок для управління фінансовими даними громадян з авторизацією користувачів та інтеграцією Arduino для ідентифікації.

## Технології
Python (Django), MySQL, HTML, CSS, JavaScript, Arduino (Serial communication)

## Функціонал
Реєстрація та авторизація користувачів. Профіль громадянина. Збереження даних у MySQL. Веб-інтерфейс для роботи з системою. Отримання даних з Arduino через Serial порт.

## Запуск проєкту
Клонувати репозиторій:
git clone https://github.com/Sofier2/finoboard.git
cd finoboard

Створити та активувати віртуальне середовище:
python -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Linux/Mac)

Встановити залежності:
pip install -r requirements.txt

Налаштувати базу даних MySQL та прописати дані в settings.py

Виконати міграції:
python manage.py makemigrations
python manage.py migrate

Запустити сервер:
python manage.py runserver