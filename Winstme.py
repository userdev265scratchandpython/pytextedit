import customtkinter as ctk
import hashlib
import os
import time
import winreg
import sys
import platform

#api keys can be handmade too, but generating them is more than a good option

# Function to compute SHA-256 hash
def compute_sha256(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

file_content = "example" #replace "example with api key"
sha256_hash = hashlib.sha256(file_content.encode('utf-8')).hexdigest()
# Function to save credentials to the Windows Registry
def save_to_registry(username, password_hash, theme):
    try:
        registry_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Winst\\login\\v1\\{sha256_hash}")
        winreg.SetValueEx(registry_key, "Username", 0, winreg.REG_SZ, username)
        winreg.SetValueEx(registry_key, "PasswordHash", 0, winreg.REG_SZ, password_hash)
        winreg.CloseKey(registry_key)
    except Exception as e:
        print(f"Error saving to registry: {e}")

# Function to load credentials from the Windows Registry
def load_from_registry():
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Winst\\login\\v1\\{sha256_hash}")
        username = winreg.QueryValueEx(registry_key, "Username")[0]
        password_hash = winreg.QueryValueEx(registry_key, "PasswordHash")[0]
        winreg.CloseKey(registry_key)
        return username, password_hash
    except FileNotFoundError:
        return None, None

# Load usernames and password hashes from files
def load_data():
    usernames = []
    hashes = []

    # Load usernames
    if os.path.exists("unames.json"):
        with open("unames.json", "r") as f:
            usernames = [line.strip() for line in f.readlines()]
    else:
        if not "@" in f"{os.getlogin()}":
            usernames.append(f"{os.getlogin()}")  # Add default username
            with open("unames.json", "w") as f:
                f.write(f"{os.getlogin()}")  # Write default username
            with open("defaultdreds.txt", "w") as f:
                f.write(f"username : {os.getlogin()}\npassword : login")
        else:
            usernames.append("user")  # Add default username
            with open("unames.json", "w") as f:
                f.write("user")  # Write default username
            with open("defaultdreds.txt", "w") as f:
                f.write(f"username : user\npassword : login")
            

    # Load password hashes
    if os.path.exists("pwds.json"):
        with open("pwds.json", "r") as f:
            hashes = [line.strip() for line in f.readlines()]
    else:
        hashes.append(compute_sha256("login"))  # Add default password hash
        with open("pwds.json", "w") as f:
            f.write(compute_sha256("login") + "\n")  # Write default password hash

    return usernames, hashes

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Compute the SHA-256 hash of the entered password
    password_hash = compute_sha256(password)
    
    # Check username and password hash
    if username in usernames:
        index = usernames.index(username)
        if password_hash == hashes[index]:
            if remember_var.get():
                save_to_registry(username, password_hash)
            app.destroy()
            open_text_editor()
            os.system(f"taskkill /pid {os.getpid()} /f")

    # Show error message
    error_label.configure(text="Invalid username or password!", text_color="red")
    time.sleep(2)
    error_label.configure(text="Winst login", text_color="white")

# Function to handle signup
def signup():
    username = entry_username.get()
    password = entry_password.get()
    
    # Check if username already exists
    if username in usernames:
        error_label.configure(text="Username already taken!", text_color="red")
        time.sleep(2)
        error_label.configure(text="Winst login", text_color="white")
        return
    
    # Hash the password and save the new user
    password_hash = compute_sha256(password)
    usernames.append(username)
    hashes.append(password_hash)

    # Save the new username and password hash to files
    with open("unames.json", "a") as f:
        f.write(username + "\n")
    with open("pwds.json", "a") as f:
        f.write(password_hash + "\n")

    error_label.configure(text="Signup successful! You can now log in.", text_color="green")
    time.sleep(2)
    error_label.configure(text="Winst login", text_color="white")

# Function to open the text editor

def open_text_editor():
    editor_window = ctk.CTk()

    global loctheme
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Winst\\login\\v1\\{sha256_hash}")
    except:
        registry_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, f"Software\\Winst\\login\\v1\\{sha256_hash}")
    else:
        pass
    loctheme = "light"
    try:
        loctheme = winreg.QueryValueEx(registry_key, "Theme")[0]
    except:
        winreg.SetValueEx(registry_key, "Theme", 0, winreg.REG_SZ, loctheme)
    else:
        pass
    if loctheme == "dark":
        ctk.set_appearance_mode("dark")
    elif loctheme == "light":
        ctk.set_appearance_mode("light")
    else:
        os.system(f"taskkill /pid {os.getpid()} /f")
    
    releaseos = platform.release()
    if os.name == "nt":
        if sys.getwindowsversion().build >= 22000:
            editor_window.title(f"Text Editor - Winst v1.0 (using PID : {os.getpid()}) on Windows 11 build {sys.getwindowsversion().build}")
        elif releaseos == "10":
            editor_window.title(f"Text Editor - Winst v1.0 (using PID : {os.getpid()}) on Windows 10 build {sys.getwindowsversion().build}")
        else:
            editor_window.title(f"Text Editor - Winst v1.0 (using PID : {os.getpid()}) on older Windows ({releaseos}) build {sys.getwindowsversion().build}")
    else:
        editor_window.title(f"Text Editor - Winst v1.0 on other OS")
    editor_window.geometry("650x450")

    # Create buttons for file operations
    button_frame = ctk.CTkFrame(editor_window)
    button_frame.pack(fill='x')

    open_file_button = ctk.CTkButton(button_frame, text="Open", command=lambda: open_file(text_area))
    open_file_button.pack(side='left', padx=5, pady=5)

    save_file_button = ctk.CTkButton(button_frame, text="Save", command=lambda: save_file(text_area))
    save_file_button.pack(side='left', padx=5, pady=5)

    thme_button = ctk.CTkButton(button_frame, text="Theme", command=thme)
    thme_button.pack(side='left', padx=5, pady=5)
    
    exit_button = ctk.CTkButton(button_frame, text="Exit", command=stop)
    exit_button.pack(side='left', padx=5, pady=5)

    # Create a text area
    text_area = ctk.CTkTextbox(editor_window, wrap='word')
    text_area.pack(expand=True, fill='both')

    

    editor_window.mainloop()

# Function to open a file in the text editor
def thme():
    global loctheme
    if loctheme == "dark":
        ctk.set_appearance_mode("light")
        loctheme = "light"
    elif loctheme == "light":
        ctk.set_appearance_mode("dark")
        loctheme = "dark"
    else:
        os.system(f"taskkill /pid {os.getpid()} /f")
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, f"Software\\Winst\\login\\v1\\{sha256_hash}")
    winreg.SetValueEx(registry_key, "Theme", 0, winreg.REG_SZ, loctheme)

def stop():
    os.system(f"taskkill /pid {os.getpid()} /f")

def open_file(text_area):
    file_path = ctk.filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"),
                                                           ("All Files", "*.*"),
                                                           ("JSON configuration files", "*.json")])
    if file_path:
        text_area.delete(1.0, ctk.END)  # Clear the text area
        with open(file_path, 'r') as file:
            text_area.insert(ctk.END, file.read())  # Insert file content

# Function to save the text editor content
def save_file(text_area):
    file_path = ctk.filedialog.asksaveasfilename(defaultextension=".txt",
                                                  filetypes=[("Text Files", "*.txt"),
                                                             ("All Files", "*.*"),
                                                             ("JSON configuration files", "*.json")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_area.get(1.0, ctk.END))  # Save the content of the text area

# Check for saved credentials on startup
saved_username, saved_password_hash = load_from_registry()
usernames, hashes = load_data()

mainvar = "err"

if saved_username and saved_password_hash:
    if saved_username in usernames and saved_password_hash in hashes:
        open_text_editor()
        os.system(f"taskkill /pid {os.getpid()} /f")
    else:
        usernames, hashes = load_data()

# Create the main application window
app = ctk.CTk()
app.title("Winst Login")
app.geometry("250x225")

# Username and password entry fields
entry_username = ctk.CTkEntry(app, placeholder_text="Username")
entry_username.pack(pady=10)

entry_password = ctk.CTkEntry(app, placeholder_text="Password", show='⚫')
entry_password.pack(pady=10)

# Remember me checkbox
remember_var = ctk.BooleanVar()
remember_checkbox = ctk.CTkCheckBox(app, text="Remember Me", variable=remember_var)
remember_checkbox.pack(pady=10)

# Login and signup buttons
login_button = ctk.CTkButton(app, text="Login", command=login)
login_button.pack(pady=5)

signup_button = ctk.CTkButton(app, text="Sign Up", command=signup)
signup_button.pack(pady=5)

# Error label
error_label = ctk.CTkLabel(app, text="", text_color="white")
error_label.pack(pady=10)

app.mainloop()
