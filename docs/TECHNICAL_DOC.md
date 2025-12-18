# Technical Documentation
## Computer Networks Chat Application

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [OSI Model Implementation](#osi-model-implementation)
3. [Network Components](#network-components)
4. [Protocol Specification](#protocol-specification)
5. [Implementation Details](#implementation-details)
6. [Security Analysis](#security-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Code Structure](#code-structure)

---

## 1. Architecture Overview

### 1.1 System Architecture

The application follows a **Client-Server Architecture**:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Client 1  │◄───────►│             │◄───────►│   Client 2  │
│   (GUI)     │  TCP/IP │   Server    │  TCP/IP │   (GUI)     │
└─────────────┘         │  (Central)  │         └─────────────┘
                        │             │
┌─────────────┐         │   Port:     │         ┌─────────────┐
│   Client 3  │◄───────►│   5555      │◄───────►│   Client N  │
│   (GUI)     │  TCP/IP │             │  TCP/IP │   (GUI)     │
└─────────────┘         └─────────────┘         └─────────────┘
```

**Components:**
- **Server**: Central hub managing all connections and message routing
- **Clients**: User interfaces connecting to the server
- **Network**: TCP/IP protocol for communication

### 1.2 Design Pattern

**Pattern Used**: Multi-threaded Server Model

**Advantages:**
- Handles multiple clients simultaneously
- Non-blocking operations
- Scalable architecture
- Independent client sessions

---

## 2. OSI Model Implementation

### Layer 7: Application Layer

**Purpose**: User interaction and application-specific protocols

**Implementation:**
- **Chat Protocol**: Custom JSON-based messaging protocol
- **User Interface**: Tkinter GUI for user interaction
- **Message Types**: login, message, group_message, file_transfer, etc.
- **Commands**: User commands and server responses

**Code Components:**
```python
# Message structure
{
    "type": "message",
    "sender": "username",
    "recipient": "recipient",
    "content": "message text",
    "timestamp": "2024-01-01 12:00:00"
}
```

**Key Functions:**
- `handle_client()` - Process client requests
- `send_chat_message()` - Send user messages
- `create_group()` - Group management

### Layer 6: Presentation Layer

**Purpose**: Data formatting, encoding, and encryption

**Implementation:**
- **Serialization**: JSON encoding/decoding
- **File Encoding**: Base64 encoding for binary files
- **Character Encoding**: UTF-8 for text messages

**Code Components:**
```python
# JSON encoding
data = json.dumps(message).encode('utf-8')

# JSON decoding
message = json.loads(data.decode('utf-8'))

# File encoding
filedata = base64.b64encode(file_content).decode('utf-8')

# File decoding
file_content = base64.b64decode(filedata)
```

**Key Functions:**
- `json.dumps()` - Serialize Python objects
- `json.loads()` - Deserialize JSON data
- `base64.b64encode()` - Encode binary data
- `base64.b64decode()` - Decode binary data

### Layer 5: Session Layer

**Purpose**: Connection management and session control

**Implementation:**
- **Session Establishment**: Login process
- **Session Maintenance**: Keep-alive through active connection
- **Session Termination**: Graceful disconnect handling

**Code Components:**
```python
# Session management
self.clients = {}  # Active client sessions
self.client_addresses = {}  # Client address mapping

# Session establishment
def handle_client(self, client_socket, address):
    # Manage client session lifecycle

# Session termination
finally:
    if client_socket in self.clients:
        del self.clients[client_socket]
```

**Key Features:**
- Session tracking with unique socket identifiers
- Automatic cleanup on disconnect
- Thread-per-session model

### Layer 4: Transport Layer

**Purpose**: Reliable end-to-end communication

**Implementation:**
- **Protocol**: TCP (Transmission Control Protocol)
- **Socket Type**: SOCK_STREAM (connection-oriented)
- **Port**: 5555 (application-defined)
- **Features**: 
  - Reliable delivery
  - Flow control
  - Error checking
  - Ordered delivery

**Code Components:**
```python
# TCP socket creation
self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server binding
self.server_socket.bind((self.host, self.port))

# Server listening
self.server_socket.listen(5)

# Client connection
client_socket, address = self.server_socket.accept()

# Data transmission
client_socket.send(data)

# Data reception
data = client_socket.recv(4096)
```

**TCP Features Utilized:**
- **3-Way Handshake**: Connection establishment (SYN, SYN-ACK, ACK)
- **Sequence Numbers**: Ordered delivery
- **Acknowledgments**: Reliable delivery
- **Flow Control**: Window mechanism
- **4-Way Termination**: Clean connection closure (FIN, ACK, FIN, ACK)

### Layer 3: Network Layer

**Purpose**: Logical addressing and routing

**Implementation:**
- **Protocol**: IP (Internet Protocol)
- **Addressing**: IPv4 addresses
- **Routing**: Handled by OS network stack

**Code Components:**
```python
# IP address configuration
host = '0.0.0.0'  # Server: listen on all interfaces
host = '127.0.0.1'  # Client: localhost
host = '192.168.x.x'  # Client: specific network IP

# Address family
socket.AF_INET  # IPv4 addressing
```

**IP Addressing:**
- **Server**: Typically binds to `0.0.0.0` (all interfaces)
- **Client**: Connects to server's IP address
- **Localhost**: `127.0.0.1` for local testing
- **LAN**: `192.168.x.x` or `10.x.x.x` for network

**Packet Routing:**
- Handled by operating system
- Uses routing tables
- Supports both LAN and WAN

### Layer 2: Data Link Layer

**Purpose**: Physical addressing and frame handling

**Implementation:**
- **Handled by**: Operating system and network drivers
- **MAC Addressing**: Automatic hardware address resolution
- **Framing**: Ethernet frames (managed by OS)
- **Error Detection**: CRC checksums (managed by hardware)

**Components:**
- Network Interface Card (NIC)
- Ethernet/WiFi drivers
- ARP (Address Resolution Protocol) for IP-to-MAC mapping

### Layer 1: Physical Layer

**Purpose**: Physical transmission of bits

**Implementation:**
- **Handled by**: Network hardware (NIC, cables, switches)
- **Medium**: 
  - Ethernet: Copper cables (Cat5/Cat6)
  - WiFi: Radio waves (2.4GHz/5GHz)
- **Signals**: Electrical or electromagnetic waves

**Components:**
- Network cables
- WiFi adapters
- Switches and routers
- Physical connectors (RJ45, etc.)

---

## 3. Network Components

### 3.1 Server Component

**File**: `src/server.py`

**Responsibilities:**
1. Accept client connections
2. Manage client sessions
3. Route messages between clients
4. Manage groups
5. Handle file transfers
6. Maintain online user list

**Key Classes:**
```python
class ChatServer:
    def __init__(self, host='0.0.0.0', port=5555)
    def start(self)
    def handle_client(self, client_socket, address)
    def send_message(self, client_socket, message)
    def broadcast(self, message, exclude=None)
```

**Threading Model:**
- Main thread: Accept new connections
- Worker threads: One per client connection
- Thread-safe operations using locks

**Data Structures:**
```python
self.clients = {}  # {socket: username}
self.client_addresses = {}  # {socket: address}
self.groups = {}  # {group_name: [usernames]}
self.chat_history = []  # Message history
```

### 3.2 Client Component

**File**: `src/client.py`

**Responsibilities:**
1. Connect to server
2. Send messages
3. Receive messages
4. Display GUI
5. Handle user input
6. Manage file transfers

**Key Classes:**
```python
class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555)
    def connect(self, username)
    def send_message(self, message)
    def receive_messages(self)
    def create_gui(self)
```

**Threading Model:**
- Main thread: GUI event loop
- Receiver thread: Continuously receive messages

---

## 4. Protocol Specification

### 4.1 Message Format

**Base Structure:**
```json
{
    "type": "message_type",
    "sender": "username",
    "additional_fields": "..."
}
```

### 4.2 Message Types

**1. Login Message**
```json
{
    "type": "login",
    "username": "alice"
}
```

**2. Login Response**
```json
{
    "type": "login_response",
    "status": "success",
    "message": "Welcome alice!",
    "online_users": ["alice", "bob", "charlie"]
}
```

**3. Private/Broadcast Message**
```json
{
    "type": "message",
    "recipient": "bob",  // or "all" for broadcast
    "content": "Hello, Bob!",
    "sender": "alice",
    "timestamp": "2024-01-01 12:00:00"
}
```

**4. Group Creation**
```json
{
    "type": "group_create",
    "group_name": "Project Team",
    "members": ["alice", "bob", "charlie"]
}
```

**5. Group Message**
```json
{
    "type": "group_message",
    "group_name": "Project Team",
    "content": "Meeting at 3 PM",
    "sender": "alice",
    "timestamp": "2024-01-01 12:00:00"
}
```

**6. File Transfer**
```json
{
    "type": "file_transfer",
    "recipient": "bob",
    "filename": "document.pdf",
    "filedata": "base64_encoded_data...",
    "sender": "alice",
    "timestamp": "2024-01-01 12:00:00"
}
```

**7. User Status**
```json
{
    "type": "user_joined",  // or "user_left"
    "username": "charlie",
    "online_users": ["alice", "bob", "charlie"]
}
```

### 4.3 Protocol Flow

**Connection Establishment:**
```
Client                          Server
  |                               |
  |-------- TCP Connect --------->|
  |<------ TCP Accept ------------|
  |                               |
  |-------- Login Msg ----------->|
  |<------ Login Response --------|
  |<------ User List -------------|
  |                               |
```

**Message Exchange:**
```
Client A                  Server                  Client B
  |                         |                         |
  |---- Message Msg ------->|                         |
  |<--- Msg Sent Ack -------|                         |
  |                         |---- Forward Msg ------->|
  |                         |                         |
```

**Disconnection:**
```
Client                          Server
  |                               |
  |---- Close Connection -------->|
  |                               |
  |                         [Cleanup Session]
  |                         [Notify Other Clients]
  |                               |
```

---

## 5. Implementation Details

### 5.1 Socket Programming

**Server Socket Setup:**
```python
# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow address reuse
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to address
server_socket.bind((host, port))

# Listen for connections
server_socket.listen(5)  # Backlog of 5

# Accept connections
client_socket, address = server_socket.accept()
```

**Client Socket Setup:**
```python
# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((host, port))

# Send data
client_socket.send(data)

# Receive data
data = client_socket.recv(buffer_size)
```

### 5.2 Threading

**Server Threading:**
```python
# Create thread for each client
client_thread = threading.Thread(
    target=self.handle_client,
    args=(client_socket, address)
)
client_thread.daemon = True  # Daemon thread
client_thread.start()
```

**Thread Safety:**
```python
# Use locks for shared data
self.lock = threading.Lock()

# Protect critical sections
with self.lock:
    self.clients[client_socket] = username
```

### 5.3 Error Handling

**Connection Errors:**
```python
try:
    client_socket.connect((host, port))
except socket.error as e:
    print(f"Connection failed: {e}")
```

**Data Transmission Errors:**
```python
try:
    client_socket.send(data)
except socket.error:
    # Handle disconnection
    pass
```

**JSON Parsing Errors:**
```python
try:
    message = json.loads(data.decode('utf-8'))
except json.JSONDecodeError:
    # Handle invalid data
    continue
```

### 5.4 File Transfer

**Encoding Process:**
```python
# Read file
with open(file_path, 'rb') as f:
    file_content = f.read()

# Encode to base64
encoded_data = base64.b64encode(file_content).decode('utf-8')

# Send in message
message = {
    'type': 'file_transfer',
    'filename': filename,
    'filedata': encoded_data
}
```

**Decoding Process:**
```python
# Receive message
filedata = message.get('filedata')

# Decode from base64
file_content = base64.b64decode(filedata)

# Write to file
with open(save_path, 'wb') as f:
    f.write(file_content)
```

---

## 6. Security Analysis

### 6.1 Current Security Features

**✓ Implemented:**
- Basic username authentication
- Connection management
- Input validation (JSON parsing)

**✗ Not Implemented:**
- No encryption (plain text transmission)
- No password authentication
- No message integrity checks
- No access control
- No rate limiting

### 6.2 Vulnerabilities

**1. Eavesdropping**
- **Issue**: Messages sent in plain text
- **Risk**: Anyone on the network can read messages
- **Mitigation**: Use only on trusted networks

**2. Man-in-the-Middle**
- **Issue**: No authentication of server identity
- **Risk**: Attacker could impersonate server
- **Mitigation**: Implement SSL/TLS

**3. Denial of Service**
- **Issue**: No rate limiting
- **Risk**: Attacker could flood server with connections
- **Mitigation**: Implement connection limits

**4. Username Spoofing**
- **Issue**: No password verification
- **Risk**: Users can impersonate others
- **Mitigation**: Add password authentication

### 6.3 Security Recommendations

**For Production Use:**

1. **Add SSL/TLS Encryption:**
```python
import ssl

# Wrap socket with SSL
secure_socket = ssl.wrap_socket(
    socket,
    certfile="server.crt",
    keyfile="server.key",
    ssl_version=ssl.PROTOCOL_TLSv1_2
)
```

2. **Implement Password Authentication:**
```python
import hashlib

# Hash password
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

3. **Add Message Integrity:**
```python
import hmac

# Create message authentication code
mac = hmac.new(key, message.encode(), hashlib.sha256).hexdigest()
```

4. **Implement Rate Limiting:**
```python
# Limit connections per IP
connection_count = {}
if connection_count.get(ip, 0) > MAX_CONNECTIONS:
    reject_connection()
```

---

## 7. Performance Considerations

### 7.1 Scalability

**Current Capacity:**
- **Concurrent Users**: Limited by system resources
- **Messages/Second**: Dependent on network bandwidth
- **File Size**: Recommended < 10 MB

**Bottlenecks:**
1. Single-threaded message routing
2. In-memory data storage
3. No message queuing
4. Synchronous I/O operations

**Improvements:**
- Implement message queuing
- Use async I/O (asyncio)
- Add load balancing
- Implement connection pooling

### 7.2 Network Performance

**Buffer Size:**
```python
BUFFER_SIZE = 4096  # 4 KB
```

**Optimal Settings:**
- Keep-alive: Enabled by default in TCP
- Nagle's algorithm: Enabled (can disable for real-time)
- TCP window size: OS managed

**Latency Factors:**
- Network distance
- Router hops
- Bandwidth limitations
- Server processing time

### 7.3 Memory Usage

**Per Client:**
- Socket: ~1 KB
- Thread: ~1 MB
- Message buffers: Variable

**Total Estimate:**
- 100 clients: ~100 MB
- 1000 clients: ~1 GB

---

## 8. Code Structure

### 8.1 Server Code Organization

```
server.py
│
├── ChatServer Class
│   ├── __init__(): Initialize server
│   ├── start(): Start listening
│   ├── handle_client(): Per-client handler
│   ├── send_message(): Send to single client
│   ├── send_to_user(): Send by username
│   └── broadcast(): Send to all clients
│
└── main(): Entry point
```

### 8.2 Client Code Organization

```
client.py
│
├── ChatClient Class
│   ├── __init__(): Initialize client
│   ├── connect(): Connect to server
│   ├── send_message(): Send data
│   ├── receive_messages(): Receive thread
│   ├── handle_message(): Process received messages
│   ├── create_gui(): Build GUI
│   ├── send_chat_message(): User message handler
│   ├── send_file(): File transfer
│   └── create_group(): Group management
│
└── main(): Entry point with login dialog
```

### 8.3 Key Algorithms

**Message Routing:**
```
1. Receive message from client
2. Parse JSON
3. Determine message type
4. If private: send to specific user
5. If broadcast: send to all except sender
6. If group: send to group members
7. Send confirmation to sender
```

**Group Management:**
```
1. Receive group creation request
2. Validate group name
3. Store members list
4. Notify all members
5. Add to groups dictionary
```

**File Transfer:**
```
1. Read file as binary
2. Encode with base64
3. Create file transfer message
4. Send to recipient
5. Recipient decodes base64
6. Save to disk
```

---

## Conclusion

This technical documentation provides a comprehensive view of the chat application's implementation. The application successfully demonstrates fundamental networking concepts including:

- Socket programming
- TCP/IP protocol
- Client-server architecture
- Multi-threading
- Data serialization
- OSI model layers

For educational purposes, this implementation is complete. For production use, additional features like encryption, authentication, and database integration would be necessary.
