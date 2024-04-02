import secrets
import string
import time
import os
import sys
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import threading
import requests
import random


def status(text):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[1;34m" + text + "\033[0m")

# Config
Accounts = 40  # how many accounts
MaxWindows = 3
ActualWindows = 0

# URLs
first_names_url = "https://raw.githubusercontent.com/tomdevw/neww/main/firstt.txt"
roblox_url = "https://www.roblox.com/"

# File paths
files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
text_files_folder = os.path.join(files_path, "Accounts")
text_file = os.path.join(text_files_folder, f"Accounts_{date.today()}.txt")
text_file2 = os.path.join(text_files_folder, f"AltManagerLogin_{date.today()}.txt")

# Create folder if it does not exist
if not os.path.exists(text_files_folder):
    os.makedirs(text_files_folder)

# Lists of days, months and years
days = [str(i + 1) for i in range(10, 28)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [str(i + 1) for i in range(1980, 2004)]

# Lists of days, months and years
days = [str(i + 1) for i in range(10, 28)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [str(i + 1) for i in range(1980, 2004)]

class UsernamesGenerator:
    def __init__(self, url, used_usernames_file):
        self.url = url
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

    def get_username(self):
        if not self.available_usernames:
            print("No usernames available. Fetching from URL...")
            self.fetch_usernames()

        while self.available_usernames:
            username = self.available_usernames.pop()
            if username not in self.used_usernames:
                self.used_usernames.append(username)
                self.save_used_usernames()  # Save used usernames to file
                return username
        print("No available usernames found.")
        return None

# Config
Accounts = 40  # how many accounts
MaxWindows = 3
ActualWindows = 0

# URLs
first_names_url = "https://raw.githubusercontent.com/tomdevw/neww/main/firstt.txt"
roblox_url = "https://www.roblox.com/"

# File paths
files_path = os.path.dirname(os.path.abspath(sys.argv[0]))
text_files_folder = os.path.join(files_path, "Accounts")
text_file = os.path.join(text_files_folder, f"Accounts_{date.today()}.txt")
text_file2 = os.path.join(text_files_folder, f"AltManagerLogin_{date.today()}.txt")

# Create folder if it does not exist
if not os.path.exists(text_files_folder):
    os.makedirs(text_files_folder)

# Initialize the usernames generator
used_usernames_file = os.path.join(text_files_folder, "used_usernames.txt")
usernames_generator = UsernamesGenerator(first_names_url, used_usernames_file)

# Password generator
def gen_password(length):
    return "tomdevwonTopBud234"

# Function to create an account
def create_account(url, usernames_generator):
    global ActualWindows
    try:
        status("Starting to create an account...")
        cookie_found = False
        elapsed_time = 0

        # Initialize webdriver
        driver = webdriver.Chrome()  # Use Chrome WebDriver
        driver.set_window_size(1200, 800)
        driver.set_window_position(0, 0)
        driver.get(url)
        time.sleep(2)

        # HTML elements
        username_input = driver.find_element("id", "signup-username")
        username_error = driver.find_element("id", "signup-usernameInputValidation")
        password_input = driver.find_element("id", "signup-password")
        day_dropdown = driver.find_element("id", "DayDropdown")
        month_dropdown = driver.find_element("id", "MonthDropdown")
        year_dropdown = driver.find_element("id", "YearDropdown")
        male_button = driver.find_element("id", "MaleButton")
        female_button = driver.find_element("id", "FemaleButton")
        register_button = driver.find_element("id", "signup-button")

        # Select random date of birth
        Selection = Select(day_dropdown)
        Selection.select_by_value(str(random.randint(10, 28)))
        time.sleep(0.3)

        Selection = Select(month_dropdown)
        Selection.select_by_value(random.choice(months))
        time.sleep(0.3)

        Selection = Select(year_dropdown)
        Selection.select_by_value(str(random.randint(1980, 2004)))
        time.sleep(0.3)

        # Generate unique username
        username = usernames_generator.get_username()
        if not username:
            print("Failed to generate a username.")
            return

        # Enter username and password
        username_input.send_keys(username)
        time.sleep(0.3)
        password_input.send_keys("tomdevwonTopBud234")
        time.sleep(0.3)

        # Select gender
        gender = secrets.choice([male_button, female_button])
        gender.click()
        time.sleep(0.5)

        # Register account
        register_button.click()
        time.sleep(3)

        # Wait for cookie
        while not cookie_found and elapsed_time < 180:
            time.sleep(3)
            elapsed_time += 3
            for cookie in driver.get_cookies():
                if cookie.get('name') == '.ROBLOSECURITY':
                    cookie_found = True
                    break

        if cookie_found:
            # Save account info
            result = [cookie.get('value'), username, "tomdevwonTopBud234"]
            save_account_info(result)
            save_altmanager_login(result)
            status("Successfully created!")
            time.sleep(3)
            ActualWindows -= 1
            status(f"Pestanas abiertas: {ActualWindows}")

    except Exception as e:
        print(f"Exception occurred: {e}")
        status(f"Pestanas abiertas: {ActualWindows}")
        ActualWindows -= 1
    finally:
        driver.quit()

# Save account information to text file
def save_account_info(account_info):
    status("Saving account info...")
    try:
        with open(text_file, 'a') as file:
            file.write(f"Username: {account_info[1]}\nPassword: {account_info[2]}\nCookie: {account_info[0]}\n\n\n")
        print("Account information saved successfully.")
    except Exception as e:
        print(f"Error saving account information: {e}")
        print("Text file path:", text_file)  # Debug print to check file path

# Save login information for AltManager
def save_altmanager_login(account_info):
    try:
        with open(text_file2, 'a') as file:
            status("Saving account login (for alt manager)...")
            file.write(f"{account_info[1]}:{account_info[2]}\n")
        print("AltManager login information saved successfully.")
    except Exception as e:
        print(f"Error saving AltManager login information: {e}")
        print("Text file path:", text_file2)  # Debug print to check file path

# Create accounts
for _ in range(Accounts):
    while ActualWindows >= MaxWindows:
        status(f"Esperando... {ActualWindows}/{MaxWindows}")
        time.sleep(1)
    ActualWindows += 1
    account_thread = threading.Thread(target=create_account, args=(roblox_url, usernames_generator))
    account_thread.start()
    time.sleep(1)
