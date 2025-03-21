import socket
import threading
import tkinter as tk
from tkinter import scrolledtext


host = '127.0.0.1'
port = 4343  


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


clients = []
usuarios = []


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(f"{sender} envió un mensaje: {message.decode('utf-8')}".encode('utf-8'))
            except:
                
                disconnected_client(client)

def disconnected_client(client):
    if client in clients:
        index = clients.index(client)
        usuario = usuarios[index]
        broadcast(f"ChatBot: [{usuario}] ha abandonado el chat".encode('utf-8'), client)
        clients.remove(client)
        usuarios.remove(usuario)
        client.close()
        log_message(f"El usuario [{usuario}] se ha desconectado")


def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)  
            if message:
                index = clients.index(client)
                sender = usuarios[index]
                log_message(f"Remitente [{sender}]: {message.decode('utf-8')}")
                broadcast(message, sender)
            else:
                disconnected_client(client)
                break
        except:
            disconnected_client(client)
            break

def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        usuario = client.recv(1024).decode('utf-8')  

        clients.append(client)
        usuarios.append(usuario)

        log_message(f"[{usuario}] se acaba de conectar al servidor {str(address)}")
        
        message = f"ChatBot: {usuario} ingresó al chat!".encode("utf-8")
        broadcast(message, usuario)
        client.send("Conectado al servidor del grupo 26LF371".encode("utf-8"))
       
        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()


def start_server():
    server.bind((host, port))
    server.listen()
    log_message(f"El servidor del grupo de Octavo iniciado en {host}:{port}")
    threading.Thread(target=receive_connections).start()


def log_message(message):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, message + "\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)
root = tk.Tk()
root.title("Servidor del grupo de Octavo")
frame = tk.Frame(root)
scroll_bar = tk.Scrollbar(frame)
text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.DISABLED)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame.pack(expand=True, fill=tk.BOTH)

start_button = tk.Button(root, text="Iniciar Servidor", command=start_server)
start_button.pack(pady=10)

root.mainloop()
