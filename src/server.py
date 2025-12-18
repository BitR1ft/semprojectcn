"""
Chat Server Application
Computer Networks Semester Project

This server implements a multi-client chat system demonstrating OSI Model layers:
- Application Layer: Chat protocol
- Presentation Layer: Message encoding/decoding
- Session Layer: Connection management
- Transport Layer: TCP sockets
- Network Layer: IP addressing
- Data Link Layer: Frame handling (managed by OS)
- Physical Layer: Hardware communication (managed by OS)
"""

import socket
import threading
import json
import datetime
import os
import base64

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        """
        Initialize the chat server
        
        OSI Model Mapping:
        - Transport Layer: TCP socket creation
        - Network Layer: IP address binding
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Client management
        self.clients = {}  # {socket: username}
        self.client_addresses = {}  # {socket: address}
        self.groups = {}  # {group_name: [usernames]}
        
        # Lock for thread safety
        self.lock = threading.Lock()
        
        # Chat history
        self.chat_history = []
        
        print(f"[SERVER] Initializing on {host}:{port}")
        
    def start(self):
        """
        Start the server and listen for connections
        
        OSI Model Mapping:
        - Transport Layer: TCP listening and accepting connections
        - Session Layer: Establishing sessions with clients
        """
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"[SERVER] Server started on {self.host}:{self.port}")
            print(f"[SERVER] Waiting for connections...")
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"[SERVER] New connection from {address}")
                
                # Create a new thread for each client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            print(f"[SERVER ERROR] {e}")
        finally:
            self.server_socket.close()
            
    def handle_client(self, client_socket, address):
        """
        Handle individual client connections
        
        OSI Model Mapping:
        - Application Layer: Processing chat commands and messages
        - Presentation Layer: JSON encoding/decoding
        - Session Layer: Managing client session lifecycle
        """
        username = None
        
        try:
            while True:
                # Receive data from client
                data = client_socket.recv(4096)
                
                if not data:
                    break
                
                # Presentation Layer: Decode received data
                try:
                    message = json.loads(data.decode('utf-8'))
                except json.JSONDecodeError:
                    continue
                
                # Application Layer: Process different message types
                msg_type = message.get('type')
                
                if msg_type == 'login':
                    username = message.get('username')
                    with self.lock:
                        self.clients[client_socket] = username
                        self.client_addresses[client_socket] = address
                    
                    response = {
                        'type': 'login_response',
                        'status': 'success',
                        'message': f'Welcome {username}!',
                        'online_users': list(self.clients.values())
                    }
                    self.send_message(client_socket, response)
                    
                    # Notify all clients about new user
                    self.broadcast({
                        'type': 'user_joined',
                        'username': username,
                        'online_users': list(self.clients.values())
                    }, exclude=client_socket)
                    
                    print(f"[SERVER] {username} logged in from {address}")
                    
                elif msg_type == 'message':
                    if username:
                        recipient = message.get('recipient')
                        content = message.get('content')
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        chat_message = {
                            'type': 'message',
                            'sender': username,
                            'recipient': recipient,
                            'content': content,
                            'timestamp': timestamp
                        }
                        
                        # Store in history
                        self.chat_history.append(chat_message)
                        
                        # Send to recipient
                        if recipient == 'all':
                            self.broadcast(chat_message, exclude=client_socket)
                        else:
                            self.send_to_user(recipient, chat_message)
                        
                        # Send confirmation to sender
                        self.send_message(client_socket, {
                            'type': 'message_sent',
                            'status': 'success'
                        })
                        
                        print(f"[SERVER] Message from {username} to {recipient}")
                        
                elif msg_type == 'group_create':
                    if username:
                        group_name = message.get('group_name')
                        members = message.get('members', [])
                        
                        with self.lock:
                            self.groups[group_name] = members
                        
                        response = {
                            'type': 'group_created',
                            'group_name': group_name,
                            'members': members
                        }
                        
                        # Notify all group members
                        for member in members:
                            self.send_to_user(member, response)
                        
                        print(f"[SERVER] Group '{group_name}' created by {username}")
                        
                elif msg_type == 'group_message':
                    if username:
                        group_name = message.get('group_name')
                        content = message.get('content')
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        if group_name in self.groups:
                            group_msg = {
                                'type': 'group_message',
                                'sender': username,
                                'group_name': group_name,
                                'content': content,
                                'timestamp': timestamp
                            }
                            
                            # Send to all group members
                            for member in self.groups[group_name]:
                                if member != username:
                                    self.send_to_user(member, group_msg)
                            
                            print(f"[SERVER] Group message in '{group_name}' from {username}")
                            
                elif msg_type == 'file_transfer':
                    if username:
                        recipient = message.get('recipient')
                        filename = message.get('filename')
                        filedata = message.get('filedata')
                        
                        file_msg = {
                            'type': 'file_transfer',
                            'sender': username,
                            'filename': filename,
                            'filedata': filedata,
                            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        self.send_to_user(recipient, file_msg)
                        print(f"[SERVER] File '{filename}' transferred from {username} to {recipient}")
                        
                elif msg_type == 'get_users':
                    if username:
                        response = {
                            'type': 'users_list',
                            'users': list(self.clients.values())
                        }
                        self.send_message(client_socket, response)
                        
        except Exception as e:
            print(f"[SERVER ERROR] Error handling client {address}: {e}")
        finally:
            # Client disconnected
            if username:
                with self.lock:
                    if client_socket in self.clients:
                        del self.clients[client_socket]
                    if client_socket in self.client_addresses:
                        del self.client_addresses[client_socket]
                
                # Notify all clients
                self.broadcast({
                    'type': 'user_left',
                    'username': username,
                    'online_users': list(self.clients.values())
                })
                
                print(f"[SERVER] {username} disconnected")
            
            client_socket.close()
            
    def send_message(self, client_socket, message):
        """
        Send message to a specific client
        
        OSI Model Mapping:
        - Presentation Layer: JSON encoding
        - Transport Layer: TCP transmission
        """
        try:
            data = json.dumps(message).encode('utf-8')
            client_socket.send(data)
        except Exception as e:
            print(f"[SERVER ERROR] Error sending message: {e}")
            
    def send_to_user(self, username, message):
        """Send message to a specific user by username"""
        with self.lock:
            for client_socket, user in self.clients.items():
                if user == username:
                    self.send_message(client_socket, message)
                    break
                    
    def broadcast(self, message, exclude=None):
        """
        Broadcast message to all connected clients
        
        OSI Model Mapping:
        - Application Layer: Message routing to multiple recipients
        """
        with self.lock:
            for client_socket in list(self.clients.keys()):
                if client_socket != exclude:
                    self.send_message(client_socket, message)

def main():
    """
    Main function to start the chat server
    
    Network Configuration:
    - Default Host: 0.0.0.0 (listens on all network interfaces)
    - Default Port: 5555 (Application Layer port number)
    """
    print("=" * 60)
    print("COMPUTER NETWORKS CHAT SERVER")
    print("Semester Project - OSI Model Implementation")
    print("=" * 60)
    
    # Create and start server
    server = ChatServer(host='0.0.0.0', port=5555)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")

if __name__ == "__main__":
    main()
