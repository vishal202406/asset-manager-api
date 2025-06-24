# Asset Management REST API

A Flask REST API to manage assets with service and expiration timings.  
✅ Sends reminders 15 minutes before service/expiration time.  
✅ Logs notifications and violations in the database.  
✅ No frontend — purely backend API.

---

## 🚀 Features

- Create, update, delete, list assets
- Track service time and expiration time
- Generate notifications (reminders) when service/expiration is near
- Generate violations if service/expiration overdue
- Simulate background tasks via `/run-checks` API
- Uses **SQLite** database

---

## ⚙️ Technologies

- Python 3.x
- Flask + Flask-RESTful
- Flask-SQLAlchemy
- Flasgger (Swagger API docs)

---

## 📌 Setup Instructions

### 1️⃣ Clone the repo and set up the environment

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt

python app.py

pip install -r requirements.txt

python app.py
