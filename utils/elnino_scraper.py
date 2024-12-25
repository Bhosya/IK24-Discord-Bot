import requests
from bs4 import BeautifulSoup
import json

LOGIN_URL = "https://elnino20212.polines.ac.id/login/index.php"

def login_to_moodle(username, password):
    session = requests.Session()
    try:
        login_page = session.get(LOGIN_URL)
        soup = BeautifulSoup(login_page.text, "html.parser")
        token = soup.find("input", {"name": "logintoken"})["value"]

        payload = {
            "logintoken": token,
            "username": username,
            "password": password,
        }
        response = session.post(LOGIN_URL, data=payload)
        if "Dasbor" in response.text:
            return session
        else:
            print(f"[ERROR] Login gagal untuk username: {username}.")
            return None
    except Exception as e:
        print(f"[ERROR] Kesalahan saat login: {e}")
        return None

def check_new_tasks(session, course_url, course_name, file_path):
    new_tasks = []
    try:
        response = session.get(course_url)
        soup = BeautifulSoup(response.text, "html.parser")
        tasks = soup.find_all("li", class_="activity assign modtype_assign")

        existing_tasks = load_logged_tasks(file_path)

        for task in tasks:
            task_name = task.find("span", class_="instancename").text.strip()
            task_url = task.find("a")["href"] if task.find("a") else None

            if task_url and task_url not in existing_tasks:
                new_tasks.append({"name": task_name, "url": task_url, "course": course_name})
                existing_tasks.append(task_url)

        save_logged_tasks(file_path, existing_tasks)
    except Exception as e:
        print(f"[ERROR] Gagal memeriksa tugas untuk {course_name}: {e}")

    return new_tasks

def load_logged_tasks(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_logged_tasks(file_path, tasks):
    with open(file_path, "w") as f:
        json.dump(tasks, f)
