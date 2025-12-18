"""
Chat Client Application with GUI
Computer Networks Semester Project

This client implements a GUI-based chat application demonstrating OSI Model layers.
"""

import socket
import threading
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import datetime
import base64
import os

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        """
        Initialize the chat client
        
        OSI Model Mapping:
        - Transport Layer: TCP socket creation
        - Network Layer: IP address configuration
        """
        self.host = host
        self.port = port
        self.socket = None
        self.username = None
        self.connected = False
        self.online_users = []
        
        # GUI components
        self.root = None
        self.chat_display = None
        self.message_entry = None
        self.users_listbox = None
        self.selected_recipient = "all"
        
    def connect(self, username):
        """
        Connect to the chat server
        
        OSI Model Mapping:
        - Transport Layer: TCP connection establishment (3-way handshake)
        - Session Layer: Establishing a session with the server
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.username = username
            self.connected = True
            
            # Send login message
            login_msg = {
                'type': 'login',
                'username': username
            }
            self.send_message(login_msg)
            
            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            return False
            
    def send_message(self, message):
        """
        Send message to server
        
        OSI Model Mapping:
        - Presentation Layer: JSON encoding
        - Transport Layer: TCP transmission
        """
        try:
            data = json.dumps(message).encode('utf-8')
            self.socket.send(data)
        except Exception as e:
            print(f"[CLIENT ERROR] Error sending message: {e}")
            
    def receive_messages(self):
        """
        Receive messages from server
        
        OSI Model Mapping:
        - Transport Layer: TCP reception
        - Presentation Layer: JSON decoding
        - Application Layer: Message processing
        """
        while self.connected:
            try:
                data = self.socket.recv(4096)
                
                if not data:
                    break
                
                message = json.loads(data.decode('utf-8'))
                self.handle_message(message)
                
            except Exception as e:
                if self.connected:
                    print(f"[CLIENT ERROR] Error receiving message: {e}")
                break
                
        self.connected = False
        
    def handle_message(self, message):
        """
        Handle different types of messages from server
        
        OSI Model Mapping:
        - Application Layer: Message interpretation and action
        """
        msg_type = message.get('type')
        
        if msg_type == 'login_response':
            status = message.get('status')
            msg = message.get('message')
            self.online_users = message.get('online_users', [])
            
            if status == 'success':
                self.display_system_message(msg)
                self.update_users_list()
                
        elif msg_type == 'message':
            sender = message.get('sender')
            content = message.get('content')
            timestamp = message.get('timestamp')
            self.display_message(f"[{timestamp}] {sender}: {content}")
            
        elif msg_type == 'group_message':
            sender = message.get('sender')
            group_name = message.get('group_name')
            content = message.get('content')
            timestamp = message.get('timestamp')
            self.display_message(f"[{timestamp}] [{group_name}] {sender}: {content}")
            
        elif msg_type == 'user_joined':
            username = message.get('username')
            self.online_users = message.get('online_users', [])
            self.display_system_message(f"{username} joined the chat")
            self.update_users_list()
            
        elif msg_type == 'user_left':
            username = message.get('username')
            self.online_users = message.get('online_users', [])
            self.display_system_message(f"{username} left the chat")
            self.update_users_list()
            
        elif msg_type == 'group_created':
            group_name = message.get('group_name')
            self.display_system_message(f"Group '{group_name}' created")
            
        elif msg_type == 'file_transfer':
            sender = message.get('sender')
            filename = message.get('filename')
            filedata = message.get('filedata')
            
            # Ask user where to save
            save_path = filedialog.asksaveasfilename(
                defaultextension=".*",
                initialfile=filename,
                title=f"Save file from {sender}"
            )
            
            if save_path:
                try:
                    with open(save_path, 'wb') as f:
                        f.write(base64.b64decode(filedata))
                    self.display_system_message(f"File '{filename}' received from {sender}")
                except Exception as e:
                    self.display_system_message(f"Error saving file: {e}")
                    
        elif msg_type == 'users_list':
            self.online_users = message.get('users', [])
            self.update_users_list()
            
    def display_message(self, message):
        """Display a chat message in the GUI"""
        if self.chat_display:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, message + '\n')
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
    def display_system_message(self, message):
        """Display a system message in the GUI"""
        if self.chat_display:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"*** {message} ***\n", 'system')
            self.chat_display.tag_config('system', foreground='blue', font=('Arial', 9, 'italic'))
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
    def update_users_list(self):
        """Update the online users list"""
        if self.users_listbox:
            self.users_listbox.delete(0, tk.END)
            self.users_listbox.insert(tk.END, "All Users")
            for user in self.online_users:
                if user != self.username:
                    self.users_listbox.insert(tk.END, user)
                    
    def send_chat_message(self):
        """Send a chat message"""
        message_text = self.message_entry.get()
        
        if message_text.strip():
            msg = {
                'type': 'message',
                'recipient': self.selected_recipient,
                'content': message_text
            }
            self.send_message(msg)
            
            # Display in own chat
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            recipient_display = self.selected_recipient if self.selected_recipient != "all" else "Everyone"
            self.display_message(f"[{timestamp}] You -> {recipient_display}: {message_text}")
            
            self.message_entry.delete(0, tk.END)
            
    def send_file(self):
        """Send a file to selected user"""
        if self.selected_recipient == "all":
            messagebox.showwarning("File Transfer", "Please select a specific user to send a file")
            return
            
        file_path = filedialog.askopenfilename(title="Select file to send")
        
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    filedata = base64.b64encode(f.read()).decode('utf-8')
                
                filename = os.path.basename(file_path)
                
                msg = {
                    'type': 'file_transfer',
                    'recipient': self.selected_recipient,
                    'filename': filename,
                    'filedata': filedata
                }
                self.send_message(msg)
                
                self.display_system_message(f"File '{filename}' sent to {self.selected_recipient}")
                
            except Exception as e:
                messagebox.showerror("File Transfer Error", f"Error sending file: {e}")
                
    def create_group(self):
        """Create a group chat"""
        group_name = simpledialog.askstring("Create Group", "Enter group name:")
        
        if group_name:
            # Select members
            member_dialog = tk.Toplevel(self.root)
            member_dialog.title("Select Members")
            member_dialog.geometry("300x400")
            
            tk.Label(member_dialog, text="Select group members:", font=('Arial', 10, 'bold')).pack(pady=10)
            
            listbox = tk.Listbox(member_dialog, selectmode=tk.MULTIPLE, width=40, height=15)
            listbox.pack(pady=10)
            
            for user in self.online_users:
                if user != self.username:
                    listbox.insert(tk.END, user)
            
            def confirm_group():
                selected_indices = listbox.curselection()
                members = [listbox.get(i) for i in selected_indices]
                members.append(self.username)  # Add self to group
                
                if members:
                    msg = {
                        'type': 'group_create',
                        'group_name': group_name,
                        'members': members
                    }
                    self.send_message(msg)
                    self.display_system_message(f"Group '{group_name}' created with {len(members)} members")
                    member_dialog.destroy()
                else:
                    messagebox.showwarning("Group Creation", "Please select at least one member")
            
            tk.Button(member_dialog, text="Create Group", command=confirm_group, bg='#4CAF50', fg='white').pack(pady=10)
            
    def on_user_select(self, event):
        """Handle user selection from list"""
        selection = self.users_listbox.curselection()
        if selection:
            selected = self.users_listbox.get(selection[0])
            self.selected_recipient = "all" if selected == "All Users" else selected
            
    def create_gui(self):
        """
        Create the GUI interface
        
        OSI Model Mapping:
        - Application Layer: User interface for chat application
        """
        self.root = tk.Tk()
        self.root.title(f"Chat Application - {self.username}")
        self.root.geometry("900x600")
        self.root.configure(bg='#2C3E50')
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame - Title
        top_frame = tk.Frame(main_frame, bg='#34495E', relief=tk.RAISED, borderwidth=2)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            top_frame,
            text="Computer Networks Chat Application",
            font=('Arial', 16, 'bold'),
            bg='#34495E',
            fg='white'
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            top_frame,
            text=f"Logged in as: {self.username}",
            font=('Arial', 10),
            bg='#34495E',
            fg='#ECF0F1'
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Middle frame - Chat and users
        middle_frame = tk.Frame(main_frame, bg='#2C3E50')
        middle_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Chat area
        chat_frame = tk.Frame(middle_frame, bg='#34495E', relief=tk.RAISED, borderwidth=2)
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        chat_label = tk.Label(
            chat_frame,
            text="Chat Messages",
            font=('Arial', 12, 'bold'),
            bg='#34495E',
            fg='white'
        )
        chat_label.pack(pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=('Arial', 10),
            bg='#ECF0F1',
            fg='#2C3E50',
            state=tk.DISABLED
        )
        self.chat_display.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Right side - Users list
        users_frame = tk.Frame(middle_frame, bg='#34495E', relief=tk.RAISED, borderwidth=2)
        users_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        users_label = tk.Label(
            users_frame,
            text="Online Users",
            font=('Arial', 12, 'bold'),
            bg='#34495E',
            fg='white'
        )
        users_label.pack(pady=5)
        
        self.users_listbox = tk.Listbox(
            users_frame,
            width=25,
            height=20,
            font=('Arial', 10),
            bg='#ECF0F1',
            fg='#2C3E50',
            selectmode=tk.SINGLE
        )
        self.users_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.users_listbox.bind('<<ListboxSelect>>', self.on_user_select)
        
        # Buttons frame
        buttons_frame = tk.Frame(users_frame, bg='#34495E')
        buttons_frame.pack(pady=5)
        
        group_btn = tk.Button(
            buttons_frame,
            text="Create Group",
            command=self.create_group,
            bg='#3498DB',
            fg='white',
            font=('Arial', 9, 'bold'),
            width=15
        )
        group_btn.pack(pady=2)
        
        file_btn = tk.Button(
            buttons_frame,
            text="Send File",
            command=self.send_file,
            bg='#9B59B6',
            fg='white',
            font=('Arial', 9, 'bold'),
            width=15
        )
        file_btn.pack(pady=2)
        
        # Bottom frame - Message input
        bottom_frame = tk.Frame(main_frame, bg='#34495E', relief=tk.RAISED, borderwidth=2)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        input_label = tk.Label(
            bottom_frame,
            text="Type your message:",
            font=('Arial', 10, 'bold'),
            bg='#34495E',
            fg='white'
        )
        input_label.pack(pady=(10, 5))
        
        input_frame = tk.Frame(bottom_frame, bg='#34495E')
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.message_entry = tk.Entry(
            input_frame,
            font=('Arial', 11),
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', lambda e: self.send_chat_message())
        
        send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.send_chat_message,
            bg='#27AE60',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=10
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Initialize users list
        self.update_users_list()
        
        # Display welcome message
        self.display_system_message("Welcome to the chat! Select a user to chat privately or 'All Users' to broadcast.")
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing"""
        if self.connected:
            self.connected = False
            if self.socket:
                self.socket.close()
        self.root.destroy()

def main():
    """Main function to start the chat client"""
    # Login dialog
    root = tk.Tk()
    root.withdraw()
    
    # Show splash screen
    splash = tk.Toplevel()
    splash.title("Computer Networks Chat Application")
    splash.geometry("500x400")
    splash.configure(bg='#2C3E50')
    splash.resizable(False, False)
    
    # Center the splash screen
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (splash.winfo_width() // 2)
    y = (splash.winfo_screenheight() // 2) - (splash.winfo_height() // 2)
    splash.geometry(f"+{x}+{y}")
    
    # Title
    title_frame = tk.Frame(splash, bg='#34495E', relief=tk.RAISED, borderwidth=3)
    title_frame.pack(fill=tk.X, pady=20, padx=20)
    
    tk.Label(
        title_frame,
        text="Computer Networks",
        font=('Arial', 20, 'bold'),
        bg='#34495E',
        fg='white'
    ).pack(pady=(10, 5))
    
    tk.Label(
        title_frame,
        text="Chat Application",
        font=('Arial', 18, 'bold'),
        bg='#34495E',
        fg='#3498DB'
    ).pack(pady=(0, 5))
    
    tk.Label(
        title_frame,
        text="Semester Project - OSI Model Implementation",
        font=('Arial', 10),
        bg='#34495E',
        fg='#ECF0F1'
    ).pack(pady=(0, 10))
    
    # Login form
    login_frame = tk.Frame(splash, bg='#2C3E50')
    login_frame.pack(pady=30)
    
    tk.Label(
        login_frame,
        text="Server Address:",
        font=('Arial', 11, 'bold'),
        bg='#2C3E50',
        fg='white'
    ).grid(row=0, column=0, sticky='e', padx=10, pady=10)
    
    server_entry = tk.Entry(login_frame, font=('Arial', 11), width=25)
    server_entry.insert(0, "127.0.0.1")
    server_entry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(
        login_frame,
        text="Port:",
        font=('Arial', 11, 'bold'),
        bg='#2C3E50',
        fg='white'
    ).grid(row=1, column=0, sticky='e', padx=10, pady=10)
    
    port_entry = tk.Entry(login_frame, font=('Arial', 11), width=25)
    port_entry.insert(0, "5555")
    port_entry.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Label(
        login_frame,
        text="Username:",
        font=('Arial', 11, 'bold'),
        bg='#2C3E50',
        fg='white'
    ).grid(row=2, column=0, sticky='e', padx=10, pady=10)
    
    username_entry = tk.Entry(login_frame, font=('Arial', 11), width=25)
    username_entry.grid(row=2, column=1, padx=10, pady=10)
    username_entry.focus()
    
    status_label = tk.Label(
        splash,
        text="",
        font=('Arial', 9),
        bg='#2C3E50',
        fg='#E74C3C'
    )
    status_label.pack()
    
    def connect_to_server():
        server = server_entry.get().strip()
        port = port_entry.get().strip()
        username = username_entry.get().strip()
        
        if not server or not port or not username:
            status_label.config(text="Please fill all fields!")
            return
        
        try:
            port = int(port)
        except ValueError:
            status_label.config(text="Port must be a number!")
            return
        
        # Create client and connect
        client = ChatClient(host=server, port=port)
        
        if client.connect(username):
            splash.destroy()
            root.destroy()
            client.create_gui()
        else:
            status_label.config(text="Connection failed! Check server address and port.")
    
    # Connect button
    connect_btn = tk.Button(
        splash,
        text="Connect",
        command=connect_to_server,
        bg='#27AE60',
        fg='white',
        font=('Arial', 12, 'bold'),
        width=20,
        height=2
    )
    connect_btn.pack(pady=20)
    
    # Bind Enter key
    username_entry.bind('<Return>', lambda e: connect_to_server())
    
    splash.mainloop()

if __name__ == "__main__":
    main()
