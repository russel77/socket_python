import tkinter as tk
from tkinter import messagebox
import socket
import json
from threading import Thread


def create_player():
    first_name = entry_first_name.get().capitalize()
    last_name = entry_last_name.get().capitalize()

    if not first_name.isalpha() or not last_name.isalpha():
        messagebox.showerror("Error", "Invalid characters in first or last name. Use only alphabets.")
        return

    try:
        age = int(entry_age.get())
        if age > 50 or age < 15:
            raise ValueError("Age should be between 15 and 50.")
    except ValueError:
        messagebox.showerror("Error", "Invalid age. Please enter a valid number between 15 and 50.")
        return

    scored_try = var_scored_try.get()

    player_data = {
        "First name": first_name,
        "Last name": last_name,
        "Age": age,
        "Scored Try": scored_try
    }

    return player_data


def clear_form():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    var_scored_try.set(False)


def start_socket_thread():
    host = socket.gethostbyname(socket.gethostname())  # Server IP, at the moment we assume the setup is local
    port = 5000  # Port on the server

    s = socket.socket()  # Create a new socket
    try:
        s.connect((host, port))  # Connect to the server
        print("You are connected to the server.")
        return s
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        messagebox.showerror("Error", "Error connecting to the server.")
        return None


def send_data(s, player):
    try:
        player_json = json.dumps(player)
        s.send(player_json.encode('utf-8'))
        print("Sending data completed.")
    except Exception as e:
        print(f"Error sending data: {e}")
        messagebox.showerror("Error", "Error sending data.")


def submit_player_data():
    player = create_player()
    send_data(socket_connection, player)
    clear_form()


# Start the socket connection in a separate thread
socket_connection = start_socket_thread()

# GUI setup
root = tk.Tk()
root.title("Player Information")

# Set background color to slick dark grey
root.configure(bg='#333333')

# Set font
font_style = ('Helvetica', 12)

# Set text color to white
text_color = 'white'
Tick_color = 'Black'

# Labels
label_first_name = tk.Label(root, text="First Name:", font=font_style, bg='#333333', fg=text_color)
label_last_name = tk.Label(root, text="Last Name:", font=font_style, bg='#333333', fg=text_color)
label_age = tk.Label(root, text="Age:", font=font_style, bg='#333333', fg=text_color)
label_scored_try = tk.Label(root, text="Scored Try:", font=font_style, bg='#333333', fg=text_color)

# Entry widgets
entry_first_name = tk.Entry(root, font=font_style)
entry_last_name = tk.Entry(root, font=font_style)
entry_age = tk.Entry(root, font=font_style)

# Checkbutton for Scored Try
var_scored_try = tk.BooleanVar()
checkbutton_scored_try = tk.Checkbutton(root, text="Yes", variable=var_scored_try, font=font_style, bg='#333333',
                                        fg=Tick_color)

# Button to submit
submit_button = tk.Button(root, text="Submit", command=submit_player_data, font=font_style, bg='#333333', fg=text_color)

# Grid layout with padding
label_first_name.grid(row=0, column=0, sticky="e", padx=10, pady=5)
label_last_name.grid(row=1, column=0, sticky="e", padx=10, pady=5)
label_age.grid(row=2, column=0, sticky="e", padx=10, pady=5)
label_scored_try.grid(row=3, column=0, sticky="e", padx=10, pady=5)

entry_first_name.grid(row=0, column=1, padx=10, pady=5)
entry_last_name.grid(row=1, column=1, padx=10, pady=5)
entry_age.grid(row=2, column=1, padx=10, pady=5)
checkbutton_scored_try.grid(row=3, column=1, sticky="w", padx=10, pady=5)

submit_button.grid(row=4, column=1, pady=10)

root.protocol("WM_DELETE_WINDOW", lambda: close_socket(socket_connection))
root.mainloop()


# Function to close the socket
def close_socket(s):
    if s:
        s.close()
