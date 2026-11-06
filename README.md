# Manage_Expenses_Wisely 💰

A full-featured personal expense and financial management web application built with **Django** and **Chart.js**.

## 🌟 Features

- **Interactive Dashboard:** Real-time summary cards displaying today's spending, this month's total, overall expenses, monthly salary, and estimated savings.
- **Visual Analytics:** Interactive line charts, bar charts, and doughnut charts powered by Chart.js for monthly trends and category breakdowns.
- **Expense Tracking:** Add, edit, delete, and view expenses with categories, payment methods, dates, and amounts.
- **Search & Filtering:** Easily search expenses by title and filter records by category.
- **Salary & Budget Management:** Set and update monthly salary to calculate real-time savings rate.
- **Savings Goals Tracker:** Define target savings goals, monitor progress percentages, and estimate months required to reach each goal.
- **Dark Mode Support:** Seamless toggle between light and dark modes with persistent local storage.
- **Responsive & Accessible UI:** Reflow-safe layouts, fluid typography, and accessible touch targets across desktop, tablet, and mobile devices.

## 🛠️ Tech Stack

- **Backend:** Python, Django 5.2
- **Database:** SQLite (default)
- **Frontend:** HTML5, CSS3 (Custom Responsive Ocean Teal Theme), Vanilla JavaScript
- **Visualizations:** Chart.js

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/devagiri308-hue/Manage_Expenses_Wisely.git
   cd Manage_Expenses_Wisely
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📁 Project Structure

```text
Manage_Expenses_Wisely/
├── Make_expenses/          # Project configuration (settings, URLs, WSGI)
├── expenses/               # Core application (models, views, templates, static)
│   ├── migrations/         # Database migrations
│   ├── static/             # CSS styling and JavaScript
│   └── templates/          # HTML templates
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```
