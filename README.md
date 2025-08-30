# Recipe App API

A fully featured **Recipe API** built with **Django** and **Django REST Framework (DRF)**.  
This project was developed while learning advanced backend development techniques such as **Test Driven Development (TDD)**, **Docker containerization**, **unit testing**, **linting**, and **CI/CD with GitHub Actions**.

---

## 🚀 Features

- **User Authentication**
  - Custom user model with email & password login.
  - Secure token authentication.

- **Recipe Management**
  - Create, update, delete, and view recipes.
  - Upload and manage recipe images.
  - Associate recipes with tags and ingredients.

- **Tags & Ingredients**
  - Full CRUD support for tags and ingredients.
  - Tags & ingredients can be reused across multiple recipes.
  - Safe deletion (removes associations without breaking recipes).

- **Filtering**
  - Filter recipes by `tag_ids` and `ingredient_ids`.
  - Display all tags & ingredients, even if not linked to any recipe.

- **API Documentation**
  - Auto-generated schema using **drf-spectacular**.
  - Interactive **Swagger UI** for browsable API testing.
  - Manual documentation examples for filtering and usage.

---

## 🛠️ Development Practices

- **Test Driven Development (TDD)**
  - Wrote tests first, implemented functionality later.
  - Ensured reliable and maintainable code.
  
- **Mocking & Patching**
  - Used mocking techniques for external dependencies.
  - Patched services to test in isolation.

- **Docker & Docker Compose**
  - Fully containerized application.
  - Development, testing, and deployment run in isolated environments.

- **Linting & CI/CD**
  - Code style enforced using **flake8**.
  - Automated tests and linting via **GitHub Actions**.

---

## 🧑‍💻 Tech Stack

- **Language:** Python
- **Framework:** Django, Django REST Framework
- **Database:** PostgreSQL (via Docker)
- **Containerization:** Docker & Docker Compose
- **Testing:** Unit tests with `unittest` and `pytest`
- **API Docs:** drf-spectacular & Swagger UI

## 📚 Learning Outcomes

Through this project, I learned:
- How to build REST APIs with **Django REST Framework**.
- How to structure and containerize applications using **Docker**.
- The importance and workflow of **Test Driven Development**.
- Advanced concepts like **mocking**, **patching**, and **automated testing**.
- How to generate and customize **API documentation** using **drf-spectacular** and **Swagger UI**.

---

## ⚡ Getting Started

1. Clone the repository  
   ```bash
   git clone https://github.com/your-username/recipe-app-api.git
   cd recipe-app-api
