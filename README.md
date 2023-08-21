Project Scope
---

**Web Application: A food vendor recommendation service for university lecturers, to address the challenges they face in selecting and ordering food on campus.**

* To implement a recommendation system that generates personalized recommendations for lecturers based on their preferences.
* To create a booking and order tracking system that allows lecturers to schedule orders in advance, specifying the desired date, estimated time, and location for delivery.
* To incorporate a nutrition information about the food items offered by vendors.


### Project Installation

**Requirements**

- Python 3

_Follow the steps below to get the program working on your system locally. These steps are tailored for users developing on Windows OS._

1. Clone the repo
   ```sh
   git clone https://github.com/Pythonian/food_recommendation.git
   ```
2. Change into the directory of the cloned repo
   ```sh
   cd food_recommendation
   ```
3. Setup a Python virtual environment
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment
   ```sh
   .\venv\Scripts\activate
   ```
5. Install project requirements
   ```sh
   pip install -r requirements.txt
   ```
6. Run database migrations
   ```sh
   python manage.py migrate
   ```
7. Create an admin superuser
   ```sh
   python manage.py createsuperuser
   ```
   _Note: Use `admin` for both the `username` and `password`, and skip entering the `email`. Also type `y` to bypass Password validation._
8. Run the development server
   ```sh
   python manage.py runserver
   ```
9. Visit the URL in your browser
   ```sh
   127.0.0.1:8000
   ```
10. You can also visit the admin dashboard in a new tab and login with the credentials used in step 7.
   ```sh
   127.0.0.1:8000/admin/
   ```