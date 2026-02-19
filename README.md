<div align="center">

<img src="https://img.shields.io/badge/King%20Shopping-E--Commerce%20Platform-gold?style=for-the-badge&logo=shopping-cart&logoColor=white" alt="King Shopping Banner"/>

# 👑 King Shopping

### A Full-Featured E-Commerce Web Application Built with Django & Python

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-Latest-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

</div>

---

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Admin Panel](#-admin-panel)
- [Contact](#-contact)

---

## 🛍️ About

**King Shopping** is a modern, full-featured e-commerce web application that delivers a seamless online shopping experience. Built on the robust Django framework, it provides both a customer-facing storefront and a powerful admin panel for complete store management — from product listings to order tracking.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Authentication** | User Registration, Login & Secure Session Management |
| 🛒 **Shopping Cart** | Add, update, and remove items with real-time cart updates |
| 📦 **Product Catalog** | Browse products by category with detailed product pages |
| 🔍 **Product Search** | Fast and relevant search across the entire catalog |
| 📋 **Order Tracking** | Real-time order status and history for users |
| 👤 **User Profile** | Manage personal info, addresses, and preferences |
| 🏷️ **Banners & Promos** | Dynamic banner management via the admin panel |
| ⚙️ **Admin Panel** | Full CRUD for categories, products, orders, and more |

---

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Database:** MySQL (via XAMPP / WAMP / LAMP)
- **Frontend:** HTML, CSS, JavaScript
- **ORM:** Django ORM with MySQL connector

---

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- A local server stack — [XAMPP](https://www.apachefriends.org/), [WAMP](https://www.wampserver.com/), or [LAMP](https://bitnami.com/stack/lamp)

---

## 🚀 Installation & Setup

Follow these steps to get King Shopping running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/dhadukparth/King-Shopping-Project.git
cd king-shopping
```

### 2. Create & Activate Virtual Environment

```bash
# Create virtual environment
python -m venv env

# Activate on Windows
env\Scripts\activate.bat

# Activate on macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

1. Start your local server (XAMPP / WAMP / LAMP)
2. Open **phpMyAdmin** → [http://localhost/phpmyadmin/](http://localhost/phpmyadmin/)
3. Create a new database named:

```
kingshopdb
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

---

## 🌐 Usage

Once the server is running, open your browser:

| Interface | URL |
|---|---|
| 🛍️ **Customer Storefront** | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| ⚙️ **Admin Panel** | [http://127.0.0.1:8000/adminsideproweb/](http://127.0.0.1:8000/adminsideproweb/) *(use incognito mode)* |

> 💡 **Tip:** Open the admin panel in an **incognito/private window** to avoid session conflicts with the customer storefront.

---

## 🗂️ Project Structure

```
king-shopping/
├── manage.py
├── requirements.txt
├── kingshopdb/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                   # Main app (products, cart, orders)
├── users/                   # Authentication & user profiles
├── adminsideproweb/         # Custom admin panel
├── static/                  # CSS, JS, images
└── templates/               # HTML templates
```

---

## 🔑 Admin Panel

Access the admin dashboard to manage your entire store.

| Field | Value |
|---|---|
| **URL** | `http://127.0.0.1:8000/adminsideproweb/` |
| **Username** | `parthpatel` |
| **Password** | `Parth@123` |

> ⚠️ **Security Notice:** Change the default admin credentials before deploying to any public-facing environment.

---

## 📬 Contact

Have questions, found a bug, or want to contribute? Feel free to reach out!

<div align="center">

**Parth Dhaduk**

[![Email](https://img.shields.io/badge/Email-ps359511%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ps359511@gmail.com)

</div>

---

<div align="center">

Made with ❤️ by **Parth Dhaduk**

⭐ If you found this project helpful, please give it a star!

</div>
