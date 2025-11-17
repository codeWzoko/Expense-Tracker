# auth.py
import os

AUTH_FILE = "users.txt"

def register(username, password):
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            for line in f:
                u, p = line.strip().split(" ", 1)
                if u == username:
                    return False  # Username taken
    with open(AUTH_FILE, "a") as f:
        f.write(f"{username} {password}\n")
    return True

def login(username, password):
    if not os.path.exists(AUTH_FILE):
        return None
    with open(AUTH_FILE, "r") as f:
        for line in f:
            u, p = line.strip().split(" ", 1)
            if u == username and p == password:
                return username  # Return username on success
    return None