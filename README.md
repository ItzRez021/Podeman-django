# Podeman - Django Online Shop

This is a **fully-featured Django-based online shopping platform** with a modern and clean architecture. The project is built with **Persian (Farsi)** support, including a fully translated admin panel and front-end content.

---

# Features

- Fully translated **Persian admin panel**
- Front-end in **Persian (Farsi)**
- **Shopping Cart** system
- **Wishlist** functionality
- **Product search**
- **Product rating system**
- Clean and modular Django structure

---

# Security Notice

For security reasons:

- The `SECRET_KEY` and **database credentials** are not shared in the public repository.
- However, **default database connection structure** is included in `settings.py` as a placeholder so you can easily configure your local or production database.

---

# Media Uploads

To upload images (e.g., product photos), place your files inside the 'media/(path)/ directory:


Creating Virtual Environment
It is recommended to create a Python virtual environment before running the project to isolate dependencies.

Steps to create and activate a virtual environment:

1.Open your terminal or command prompt.
2. Navigate to your project directory:
 cd /path/to/your/project
 
3. Create a virtual environment named venv (you can name it anything):
  python -m venv venv

4. Activate the virtual environment:
  On Windows: venv\Scripts\activate
  On macOS/Linux: source venv/bin/activate

5. Install the required packages (usually listed in requirements.txt):
6.   pip install -r requirements.txt

6. Now you can run your Django project commands inside this isolated environment.



