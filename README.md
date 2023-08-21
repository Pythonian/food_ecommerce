Project Scope
---

**Web Application: A food vendor recommendation service for university lecturers, to address the challenges they face in selecting and ordering food on campus.**

### Project Installation

**Requirements**

- Python 3

_Follow the steps below to get the program working on your system locally._

1. Clone the repo
   ```sh
   git clone https://github.com/Pythonian/food_ecommerce.git
   ```
2. Change into the directory of the cloned repo
   ```sh
   cd food_ecommerce
   ```
3. Setup a Python virtual environment
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment
   ```sh
   . venv/bin/activate
   ```
5. Install project requirements
   ```sh
   pip install -r requirements.txt
   ```
6. Run the development server
   ```sh
   python manage.py runserver
   ```
7. Visit the URL in your browser
   ```sh
   127.0.0.1:8000
   ```
8. You can also visit the admin dashboard in a new tab and login with the credentials used in step 7.
   ```sh
   127.0.0.1:8000/admin/
   ```
   _Note: Use `admin` for both the `username` and `password`_
