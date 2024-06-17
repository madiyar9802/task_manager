import requests

pref_url = "http://127.0.0.1:5002"


# Authorization requests
def sign_up():
    url = f"{pref_url}/sign_up"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "name": "test_name",
        "surname": "test_surname",
        "email": "test@example.com",
        "login": "test123",
        "password": "testingmyproject1"
    }

    response = requests.post(url, json=data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


def change_password():
    url = f"{pref_url}/change_password"
    auth = ("test123", "testingmyproject1")
    data = {
        "old_password": "testingmyproject1",
        "new_password": "testingmyproject"
    }

    response = requests.put(url, json=data, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


# Project requests
def create_project():
    url = f"{pref_url}/create_project"
    auth = ("test123", "testingmyproject")
    data = {
        'name': 'Project for my app',
        'description': 'Just a short description of the Project',
        'start_time': '2024-06-10T15:00:00',
        'end_time': '2024-06-30T12:00:00'
    }

    response = requests.post(url, json=data, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


def get_projects():
    url = f"{pref_url}/get_projects"
    auth = ("test123", "testingmyproject")

    response = requests.get(url, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


def get_project_id():
    url = f"{pref_url}/get_project/1"
    auth = ("test123", "testingmyproject")

    response = requests.get(url, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


def update_project():
    project_id = 1
    auth = ("test123", "testingmyproject")
    url = f"{pref_url}/update_project/{project_id}"

    data = {
        'name': 'New Project name',
        'description': 'New Project description',
        'start_time': '2024-06-05T12:00:00',
        'end_time': '2024-07-05T12:00:00'
    }

    response = requests.put(url, json=data, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


# Task requests
def create_task():
    url = f"{pref_url}/create_task"
    auth = ("test123", "testingmyproject")
    data = {
        'project_id': 1,
        'description': 'Task description',
        'start_time': '2024-06-02T12:00:00',
        'end_time': '2024-06-30T12:00:00',
        'status_id': 1
    }

    response = requests.post(url, json=data, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)


def get_tasks():
    url = f"{pref_url}/get_tasks"
    auth = ("test123", "testingmyproject")

    response = requests.get(url, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


def get_task_id():
    url = f"{pref_url}/get_task/1"
    auth = ("test123", "testingmyproject")

    response = requests.get(url, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


def update_task():
    task_id = 1
    url = f"{pref_url}/update_task/{task_id}"
    auth = ("test123", "testingmyproject")
    data = {
        'project_id': 1,
        'description': 'New description of the task',
        'start_time': '2024-05-02T12:00:00',
        'end_time': '2024-07-31T12:00:00',
        'status_id': 2
    }

    response = requests.put(url, json=data, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


# Comment requests
def create_comment():
    url = f"{pref_url}/task/1/create_comment"
    auth = ("test123", "testingmyproject")
    data = {
        'comment_text': 'Comment for task #1'
    }

    response = requests.post(url, json=data, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


def update_comment():
    url = f"{pref_url}/task/1/update_comment/1"
    auth = ("test123", "testingmyproject")
    data = {
        'comment_text': 'New comment for task #1'
    }

    response = requests.put(url, json=data, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


def delete_comment():
    url = f"{pref_url}/task/1/delete_comment/1"
    auth = ("test123", "testingmyproject")

    response = requests.delete(url, auth=auth)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print("Response JSON:", response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


# Вызываем функции
sign_up()
change_password()

create_project()
create_task()
get_projects()
get_project_id()
update_project()

get_tasks()
get_task_id()
update_task()

create_comment()
create_comment()
create_comment()
create_comment()
update_comment()
delete_comment()
