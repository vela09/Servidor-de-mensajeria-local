import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog


host = '127.0.0.1'
port = 4343


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                display_message(message)
        except:
            print("Algo salió mal")
            client.close()
            break


def send_message():
    message = f"{username}: {message_entry.get()}"
    client.send(message.encode('utf-8'))
    display_message(message)
    message_entry.delete(0, tk.END)


def display_message(message):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, message + "\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

root = tk.Tk()
root.title("Chat del grupo de Octavo")


frame = tk.Frame(root)
scroll_bar = tk.Scrollbar(frame)
text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame.pack(expand=True, fill=tk.BOTH)

message_entry = tk.Entry(root)
message_entry.pack(fill=tk.X, padx=10, pady=10)
send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack(pady=5)


username_prompt = tk.Tk()
username_prompt.withdraw()
username = simpledialog.askstring("Nombre de usuario", "Ingrese su nombre de usuario:", parent=username_prompt)


def display_welcome_message():
    display_message("\n*                              *\n*Bienvenido al servidor de 8vo *\n*                              *\n")
    root.after(2000, clear_welcome_message_1)

def clear_welcome_message_1():
    text_area.delete("1.0", tk.END)
    display_message("\n*                              *\n*Aqui podras chatear con todos *\n*                              *\n")
    root.after(2000, clear_welcome_message_2)

def clear_welcome_message_2():
    text_area.delete("1.0", tk.END)
    display_message("*\n*                               *\n*      puedes comenzar          *\n*                               *\n*\n")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


display_message(f"Estás interactuando como: {username}")

display_welcome_message()

root.mainloop()
