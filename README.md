# Computer Networks Chat Application
## Semester Project - OSI Model Implementation

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![Network](https://img.shields.io/badge/Network-TCP%2FIP-green)
![OSI](https://img.shields.io/badge/OSI-7%20Layers-orange)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [OSI Model Implementation](#osi-model-implementation)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Documentation](#technical-documentation)
- [Screenshots](#screenshots)
- [Contributors](#contributors)

---

## 🎯 Overview

This is a comprehensive **Computer Networks Semester Project** that implements a full-featured chat application similar to WhatsApp. The project demonstrates practical implementation of the **OSI (Open Systems Interconnection) Model** and various networking concepts including:

- Client-Server Architecture
- Socket Programming
- TCP/IP Protocol
- Multi-threading
- Data Serialization
- Network Security Concepts

The application provides real-time messaging capabilities with support for:
- ✅ One-to-one chat
- ✅ Group chat
- ✅ File transfer
- ✅ User authentication
- ✅ Online user tracking
- ✅ Beautiful GUI interface

---

## ✨ Features

### Core Features
1. **User Authentication**: Secure login system with username validation
2. **Real-time Messaging**: Instant message delivery using TCP sockets
3. **Private Chat**: One-to-one messaging between users
4. **Group Chat**: Create and manage group conversations
5. **File Transfer**: Send and receive files between users
6. **Online Users**: Real-time list of connected users
7. **Timestamps**: All messages include date and time
8. **User Notifications**: Join/leave notifications

### Technical Features
- Multi-client support using threading
- JSON-based message protocol
- Base64 file encoding
- Thread-safe operations
- Graceful connection handling
- Error handling and recovery

---

## 🌐 OSI Model Implementation

This project demonstrates all 7 layers of the OSI Model:

### Layer 7: Application Layer
- **Implementation**: Chat protocol, user interface, message formatting
- **Components**: Client GUI, server message handlers, command processing
- **Code Reference**: `client.py` - GUI implementation, `server.py` - message routing

### Layer 6: Presentation Layer
- **Implementation**: Data encoding/decoding, JSON serialization, Base64 file encoding
- **Components**: Message serialization, file data encoding
- **Code Reference**: `json.dumps()`, `json.loads()`, `base64.b64encode()`

### Layer 5: Session Layer
- **Implementation**: Connection management, session establishment and termination
- **Components**: Login/logout handling, session tracking
- **Code Reference**: `handle_client()` function, client connection management

### Layer 4: Transport Layer
- **Implementation**: TCP sockets, reliable data transmission, port management
- **Components**: Socket creation, data streaming, connection-oriented communication
- **Code Reference**: `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
- **Port**: 5555 (configurable)

### Layer 3: Network Layer
- **Implementation**: IP addressing, packet routing
- **Components**: IP address configuration, client-server addressing
- **Code Reference**: `socket.bind((host, port))`, `socket.connect((host, port))`
- **Default IP**: 127.0.0.1 (localhost) or LAN IP for network communication

### Layer 2: Data Link Layer
- **Implementation**: Frame handling (managed by operating system)
- **Components**: MAC addressing, error detection at hardware level
- **Note**: Handled automatically by OS network stack

### Layer 1: Physical Layer
- **Implementation**: Physical network interface (Ethernet/WiFi)
- **Components**: Hardware communication, signal transmission
- **Note**: Handled by network interface card (NIC) and OS drivers

---

## 💻 System Requirements

### Hardware Requirements
- **Processor**: Any modern CPU (Pentium 4 or higher)
- **RAM**: Minimum 512 MB (1 GB recommended)
- **Storage**: 50 MB free space
- **Network**: Ethernet or WiFi adapter

### Software Requirements
- **Operating System**: 
  - Windows 7/8/10/11
  - Linux (Ubuntu, Fedora, etc.)
  - macOS 10.12+
- **Python**: Version 3.6 or higher
- **Tkinter**: Usually included with Python
- **Network**: Local network or Internet connection

---

## 📦 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/BitR1ft/semprojectcn.git
cd semprojectcn
```

### Step 2: Verify Python Installation
```bash
python --version
# or
python3 --version
```

### Step 3: Install Dependencies (if needed)
```bash
# On Ubuntu/Debian, if tkinter is not installed:
sudo apt-get install python3-tk

# On Fedora:
sudo dnf install python3-tkinter

# On macOS (using Homebrew):
brew install python-tk
```

### Step 4: No Additional Package Installation Required
This project uses only Python standard library modules!

---

## 🚀 Usage

### Running the Server

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the server:

```bash
cd src
python server.py
```

**Output:**
```
============================================================
COMPUTER NETWORKS CHAT SERVER
Semester Project - OSI Model Implementation
============================================================
[SERVER] Initializing on 0.0.0.0:5555
[SERVER] Server started on 0.0.0.0:5555
[SERVER] Waiting for connections...
```

### Running the Client

1. Open a **new** terminal/command prompt
2. Navigate to the project directory
3. Run the client:

```bash
cd src
python client.py
```

4. Enter connection details:
   - **Server Address**: `127.0.0.1` (for localhost) or server IP
   - **Port**: `5555`
   - **Username**: Your desired username

5. Click "Connect" to join the chat!

### Running Multiple Clients

To test the chat application, run multiple client instances:

```bash
# Terminal 1 - Server
python server.py

# Terminal 2 - Client 1
python client.py

# Terminal 3 - Client 2
python client.py

# Terminal 4 - Client 3
python client.py
```

---

## 📁 Project Structure

```
semprojectcn/
│
├── src/                          # Source code
│   ├── server.py                 # Chat server implementation
│   └── client.py                 # Chat client with GUI
│
├── docs/                         # Documentation
│   ├── USER_MANUAL.md           # User manual
│   ├── TECHNICAL_DOC.md         # Technical documentation
│   ├── OSI_MODEL_MAPPING.md     # OSI model detailed mapping
│   └── ARCHITECTURE.md          # System architecture
│
├── presentation/                 # Presentation materials
│   ├── PRESENTATION.md          # Presentation slides
│   └── SCRIPT.md                # Presentation script
│
├── reports/                      # Project reports
│   └── PROJECT_REPORT.md        # Complete project report
│
├── screenshots/                  # Application screenshots
│
├── tests/                        # Test files
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore file
```

---

## 📚 Technical Documentation

### Network Configuration

**Server Configuration:**
- **IP Address**: `0.0.0.0` (listens on all interfaces)
- **Port**: `5555` (TCP)
- **Protocol**: TCP/IP
- **Max Connections**: Unlimited (limited by system resources)

**Client Configuration:**
- **Connection Type**: TCP
- **Timeout**: 30 seconds
- **Buffer Size**: 4096 bytes
- **Encoding**: UTF-8

### Message Protocol

All messages use JSON format:

```json
{
    "type": "message_type",
    "sender": "username",
    "recipient": "recipient_username",
    "content": "message content",
    "timestamp": "2024-01-01 12:00:00"
}
```

**Message Types:**
- `login`: User authentication
- `message`: Private or broadcast message
- `group_message`: Group chat message
- `group_create`: Create a group
- `file_transfer`: Send a file
- `user_joined`: User join notification
- `user_left`: User leave notification

### Security Considerations

1. **No Encryption**: Messages are sent in plain text (can be enhanced with SSL/TLS)
2. **No Authentication**: Simple username-based login (can be enhanced with passwords)
3. **No Authorization**: All users have equal privileges
4. **Local Network**: Best used in trusted local networks

**Future Enhancements:**
- SSL/TLS encryption
- User authentication with passwords
- Message encryption (end-to-end)
- Role-based access control

---

## 📸 Screenshots

Screenshots are available in the `screenshots/` directory:
- Login screen
- Chat interface
- Group chat creation
- File transfer
- Multiple users

---

## 🤝 Contributors

**Project Type**: Computer Networks Semester Project

**Academic Institution**: [Your Institution Name]

**Course**: Computer Networks

**Semester**: [Your Semester]

**Year**: 2024

---

## 📝 License

This is an academic project for educational purposes.

---

## 📞 Support

For questions or issues:
1. Check the documentation in `/docs` folder
2. Review the presentation materials in `/presentation` folder
3. Read the technical documentation

---

## 🎓 Learning Objectives

This project demonstrates understanding of:

1. **Network Programming**: Socket programming, client-server architecture
2. **OSI Model**: Practical implementation of all 7 layers
3. **TCP/IP Protocol**: Reliable data transmission
4. **Multi-threading**: Concurrent client handling
5. **GUI Development**: User interface design
6. **Data Serialization**: JSON encoding/decoding
7. **File Handling**: Base64 encoding for file transfer
8. **Software Engineering**: Project structure, documentation, testing

---

## 🔜 Future Enhancements

1. **Security**: Add SSL/TLS encryption
2. **Database**: Persist chat history
3. **Mobile App**: Android/iOS clients
4. **Video/Audio**: Voice and video calls
5. **Emojis**: Enhanced emoji support
6. **Read Receipts**: Message delivery confirmation
7. **Typing Indicators**: Show when users are typing
8. **Push Notifications**: Desktop notifications

---

**Happy Chatting! 💬**
