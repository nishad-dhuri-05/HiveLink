# HiveLink
A full stack web app featuring discussion rooms on various topics ,built using the Django framework. The default sqlite database was used for storing data. It can be used for discussions on various topics. Features complete CRUD functionality for rooms and reviews.
## Features
* Sort rooms by topics
* View recent activity from the home page
* Users can edit their profiles.
* CRUD functionality allowing owners to modify rooms or reviews.
* Images:

![Alt text](<Screenshot (59).png>)
<p align="center"> Home Page </p>

![Alt text](<Screenshot (62).png>)
<p align="center"> User Profile </p>

![Alt text](<Screenshot (63).png>)
<p align="center"> Room </p>

![Alt text](<Screenshot (60).png>)
<p align="center"> Create/Update Study Room </p>

![Alt text](<Screenshot (61).png>)
<p align="center"> Edit User </p>

## Installation
1. Download the zip file from github and extract it.
2. Set up a virtual environment and activate it
    ```bash
    virtualenv env
    ./env/Scripts/activate
3. Install the required dependecies:
    ```bash
    pip install -r requirements.txt
4. Run the app
    ```bash
    python manage.py runserver
5. Open your web browser and navigate to http://localhost:8000 to access HiveLink
