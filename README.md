# DRF Blog API

A RESTful API for a blog application built with Django REST Framework.

## How to Run

1. Create and activate virtual environment:
```bash
python -m venv venv
 On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create superuser (optional):
```bash
python manage.py createsuperuser
```

5. Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`
