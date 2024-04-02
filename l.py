import requests
import random

class UsernamesGenerator:
    def __init__(self, url, available_usernames_file, used_usernames_file):
        self.url = url
        self.available_usernames_file = available_usernames_file
        self.used_usernames_file = used_usernames_file
        self.used_usernames = []
        self.available_usernames = []

    def fetch_usernames(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.available_usernames = response.text.splitlines()
                random.shuffle(self.available_usernames)
                self.load_used_usernames()
            else:
                print("Failed to fetch usernames from the provided URL.")
        except Exception as e:
            print(f"An error occurred while fetching usernames: {e}")

    def load_used_usernames(self):
        try:
            with open(self.used_usernames_file, 'r') as file:
                self.used_usernames = file.read().splitlines()
        except FileNotFoundError:
            print("Used usernames file not found. Creating a new one.")

    def save_used_usernames(self):
        with open(self.used_usernames_file, 'w') as file:
            file.write("\n".join(self.used_usernames))

    def load_available_usernames(self):
        try:
            with open(self.available_usernames_file, 'r') as file:
                self.available_usernames = file.read().splitlines()
        except FileNotFoundError:
            print("Available usernames file not found. Creating a new one.")

    def save_available_usernames(self):
        with open(self.available_usernames_file, 'w') as file:
            file.write("\n".join(self.available_usernames))

    def get_username(self):
        if not self.available_usernames:
            print("No usernames available. Fetching from URL...")
            self.fetch_usernames()
        self.load_available_usernames()
        
        while self.available_usernames:
            username = self.available_usernames.pop()
            if username not in self.used_usernames:
                self.used_usernames.append(username)
                self.save_used_usernames()  # Save used usernames to file
                self.save_available_usernames()  # Save updated available usernames to file
                return username
        print("No available usernames found.")
        return None

# Usage
url = "https://raw.githubusercontent.com/tomdevw/neww/main/firstt.txt"
available_usernames_file = "available_usernames.txt"
used_usernames_file = "used_usernames.txt"
usernames_generator = UsernamesGenerator(url, available_usernames_file, used_usernames_file)

# Get usernames one by one
for _ in range(10):  # Generate 10 usernames
    username = usernames_generator.get_username()
    if username:
        print(f"Generated username: {username}")
    else:
        print("Failed to generate username.")
