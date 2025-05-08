# English Project

**EnglishProject** is a Django-based web application designed for managing vocabulary and educational user roles. The app simulates a lightweight platform for language learning environments, where access is controlled by administrators and users are assigned roles.

## 🔧 Features

- 🔐 User authentication (no public registration)
- 📚 Personal vocabulary management (add/edit/delete words)
- 📖 Dictionary view shown when word count exceeds 10
- 👥 Role-based access (Admin, Teacher, Student)
- 🧑‍🏫 Admins can:
  - Create teacher and student accounts via the Django admin panel
- 🧑‍🎓 Teachers can:
  - View a list of their students
  - Access and edit student profiles
  - Switch between students using a dropdown menu

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Frontend:** HTML, Bootstrap
- **Tools:** Git, GitHub, Django Admin

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/ArtemAlabuzhyn/english_project.git
cd english_project
```


## Create a virtual environment and activate it

```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```



## Install the dependencies:
```bash
pip install -r requirements.txt
```

## Set up your PostgreSQL database and update settings.py with your credentials.

## Apply migrations and run the development server:
```bash
python manage.py migrate
python manage.py runserver
```

## Access the app at:
http://127.0.0.1:8000/

## 🧪 Usage
1. Log in using teacher or student credentials created in the admin panel
2. Teachers can manage assigned students and their vocabulary
3. Students can manage their personal word list

## 🔐 Test Access (for local development)

```bash
python manage.py createsuperuser
```

## 📩 Contact
Created by [Artem Alabuzhyn](mailto:artem.alabuzhyn.dev@gmail.com) — feel free to reach out!

