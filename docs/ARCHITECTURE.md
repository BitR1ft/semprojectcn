# System Architecture Documentation
## Computer Networks Chat Application

---

## Table of Contents
1. [Overview](#overview)
2. [Architectural Style](#architectural-style)
3. [Component Diagram](#component-diagram)
4. [Deployment Architecture](#deployment-architecture)
5. [Data Flow](#data-flow)
6. [Threading Model](#threading-model)
7. [Network Topology](#network-topology)
8. [Protocol Stack](#protocol-stack)

---

## 1. Overview

The Chat Application follows a **Client-Server Architecture** pattern where multiple clients communicate through a central server. This architecture provides centralized control, easier maintenance, and consistent message routing.

### Key Characteristics
- **Centralized Communication**: All messages route through server
- **Stateful Server**: Server maintains active connection state
- **Stateless Protocol**: Messages are independent
- **Multi-threaded**: Concurrent client handling
- **Event-driven**: Asynchronous message processing

---

## 2. Architectural Style

### 2.1 Client-Server Pattern

```
┌─────────────────────────────────────────────────────────┐
│                  Client-Server Model                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Multiple Clients          Central Server              │
│  ┌──────────┐                                          │
│  │ Client 1 │────┐                                     │
│  └──────────┘    │                                     │
│                  │        ┌────────────┐               │
│  ┌──────────┐    ├───────►│            │               │
│  │ Client 2 │────┤        │   SERVER   │               │
│  └──────────┘    │        │  (Central  │               │
│                  │        │    Hub)    │               │
│  ┌──────────┐    │        │            │               │
│  │ Client 3 │────┘        └────────────┘               │
│  └──────────┘                                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Advantages:**
- Centralized control and management
- Easy to implement security at one point
- Simple client implementation
- Consistent message delivery

**Disadvantages:**
- Single point of failure
- Server can become bottleneck
- Network dependency

### 2.2 Layered Architecture

The application is organized in layers corresponding to the OSI Model:

```
┌──────────────────────────────────────┐
│     Application Layer (Layer 7)      │
│   Chat GUI, Message Processing       │
├──────────────────────────────────────┤
│    Presentation Layer (Layer 6)      │
│   JSON Serialization, Base64         │
├──────────────────────────────────────┤
│      Session Layer (Layer 5)         │
│   Connection Management              │
├──────────────────────────────────────┤
│     Transport Layer (Layer 4)        │
│   TCP Sockets, Port 5555             │
├──────────────────────────────────────┤
│      Network Layer (Layer 3)         │
│   IP Addressing, Routing             │
├──────────────────────────────────────┤
│    Data Link Layer (Layer 2)         │
│   Ethernet/WiFi (OS Managed)         │
├──────────────────────────────────────┤
│     Physical Layer (Layer 1)         │
│   Hardware (NIC, Cables, WiFi)       │
└──────────────────────────────────────┘
```

---

## 3. Component Diagram

### 3.1 Server Components

```
┌─────────────────────────────────────────────────┐
│              Server Application                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │      Main Server Thread                │    │
│  │  - Initialize server socket            │    │
│  │  - Bind to address and port            │    │
│  │  - Listen for connections              │    │
│  │  - Accept client connections           │    │
│  └──────────┬─────────────────────────────┘    │
│             │                                    │
│             │ creates                            │
│             ▼                                    │
│  ┌────────────────────────────────────────┐    │
│  │   Client Handler Threads (N threads)   │    │
│  │  - One thread per client               │    │
│  │  - Receive messages                    │    │
│  │  - Parse JSON                          │    │
│  │  - Process commands                    │    │
│  └──────────┬─────────────────────────────┘    │
│             │                                    │
│             │ uses                               │
│             ▼                                    │
│  ┌────────────────────────────────────────┐    │
│  │       Shared Data Structures            │    │
│  │  - clients: dict (socket -> username)  │    │
│  │  - groups: dict (name -> [members])    │    │
│  │  - chat_history: list                  │    │
│  │  - thread_lock: Lock                   │    │
│  └────────────────────────────────────────┘    │
│             │                                    │
│             │ protected by                       │
│             ▼                                    │
│  ┌────────────────────────────────────────┐    │
│  │     Synchronization Mechanisms          │    │
│  │  - Threading locks                     │    │
│  │  - Atomic operations                   │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└─────────────────────────────────────────────────┘
```

### 3.2 Client Components

```
┌─────────────────────────────────────────────────┐
│              Client Application                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │         Main GUI Thread                │    │
│  │  - Create and manage GUI               │    │
│  │  - Handle user input                   │    │
│  │  - Display messages                    │    │
│  │  - Update UI elements                  │    │
│  └──────────┬─────────────────────────────┘    │
│             │                                    │
│             │ sends to                           │
│             ▼                                    │
│  ┌────────────────────────────────────────┐    │
│  │        Network Layer                   │    │
│  │  - TCP socket connection               │    │
│  │  - Send messages                       │    │
│  │  - JSON encoding                       │    │
│  └────────────────────────────────────────┘    │
│             │                                    │
│             │ receives from                      │
│             ▼                                    │
│  ┌────────────────────────────────────────┐    │
│  │      Receiver Thread                   │    │
│  │  - Continuously receive data           │    │
│  │  - Parse JSON messages                 │    │
│  │  - Update GUI (thread-safe)            │    │
│  └────────────────────────────────────────┘    │
│             │                                    │
│             │ updates                            │
│             ▼                                    │
│  ┌────────────────────────────────────────┐    │
│  │       Message Queue/Handler            │    │
│  │  - Process incoming messages           │    │
│  │  - Route to appropriate handler        │    │
│  │  - Update application state            │    │
│  └────────────────────────────────────────┘    │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 4. Deployment Architecture

### 4.1 Local Network Deployment

```
┌──────────────────────────────────────────────────┐
│           Local Area Network (LAN)               │
│                                                   │
│  ┌──────────────┐                                │
│  │   Router     │                                │
│  │  (Gateway)   │                                │
│  └──────┬───────┘                                │
│         │                                         │
│    ┌────┴────┐                                   │
│    │ Switch  │                                   │
│    └────┬────┘                                   │
│         │                                         │
│    ╔════╪════════════════════════════════╗       │
│    ║    │      Server Computer           ║       │
│    ║    └─► IP: 192.168.1.100           ║       │
│    ║        Port: 5555                   ║       │
│    ║        Running: server.py           ║       │
│    ╚════════════════════════════════════╝       │
│         │                                         │
│         ├──────────────────┬────────────────┐   │
│         │                  │                │   │
│   ╔═════▼═════╗     ╔═════▼═════╗   ╔═════▼═════╗
│   ║  Client 1 ║     ║  Client 2 ║   ║  Client 3 ║
│   ║ 192.168.  ║     ║ 192.168.  ║   ║ 192.168.  ║
│   ║   1.101   ║     ║   1.102   ║   ║   1.103   ║
│   ╚═══════════╝     ╚═══════════╝   ╚═══════════╝
│                                                   │
└──────────────────────────────────────────────────┘
```

### 4.2 Internet Deployment (with Port Forwarding)

```
┌────────────────────────────────────────────────────┐
│                    Internet                         │
└──────────────────────┬─────────────────────────────┘
                       │
              Public IP: X.X.X.X:5555
                       │
┌──────────────────────▼─────────────────────────────┐
│              Home/Office Router                     │
│        Port Forwarding: 5555 → 192.168.1.100:5555  │
└──────────────────────┬─────────────────────────────┘
                       │
              ┌────────┴────────┐
              │  Local Network  │
              └────────┬────────┘
                       │
              ╔════════▼═════════╗
              ║  Server Computer ║
              ║  192.168.1.100   ║
              ║  Port: 5555      ║
              ╚══════════════════╝
```

---

## 5. Data Flow

### 5.1 Message Send Flow

```
┌──────────────┐                                    ┌──────────────┐
│  Client A    │                                    │  Client B    │
│  (Alice)     │                                    │  (Bob)       │
└──────┬───────┘                                    └──────▲───────┘
       │                                                   │
       │ 1. User types message                           │
       │    "Hello Bob"                                   │
       │                                                   │
       │ 2. Create message object                        │
       │    {type: "message",                            │
       │     content: "Hello Bob",                       │
       │     recipient: "Bob"}                           │
       │                                                   │
       │ 3. JSON encode + UTF-8                          │
       │                                                   │
       │ 4. TCP send                                     │
       ▼                                                   │
┌──────────────────┐                                     │
│     SERVER       │                                     │
├──────────────────┤                                     │
│ 5. Receive data  │                                     │
│ 6. Parse JSON    │                                     │
│ 7. Identify      │                                     │
│    recipient     │                                     │
│ 8. Route message │                                     │
│                  │                                     │
│ 9. TCP send ─────────────────────────────────────────►│
└──────────────────┘                                     │
                                          10. Receive    │
                                          11. Parse JSON │
                                          12. Display    │
                                              "Alice:    │
                                               Hello Bob"│
```

### 5.2 Login Flow

```
Client                          Server
  │                               │
  │────── TCP Connect ───────────►│
  │                               │
  │◄────── TCP Accept ────────────│
  │                               │
  │────── Login Message ─────────►│
  │  {type: "login",              │
  │   username: "Alice"}          │
  │                               │
  │                         [Validate]
  │                         [Store session]
  │                               │
  │◄────── Login Response ────────│
  │  {type: "login_response",     │
  │   status: "success",          │
  │   online_users: [...]}        │
  │                               │
  │◄────── Broadcast ─────────────┤───► Other Clients
  │  {type: "user_joined",        │
  │   username: "Alice"}          │
  │                               │
```

### 5.3 Group Message Flow

```
Alice                Server                Bob & Charlie
  │                    │                        │
  │── Group Message ──►│                        │
  │                    │                        │
  │              [Lookup group]                 │
  │              [Get members]                  │
  │                    │                        │
  │◄── Confirmation ───│                        │
  │                    │                        │
  │                    ├──── Forward ──────────►│
  │                    │      to Bob            │
  │                    │                        │
  │                    ├──── Forward ──────────►│
  │                    │      to Charlie        │
  │                    │                        │
```

---

## 6. Threading Model

### 6.1 Server Threading

```
┌─────────────────────────────────────────────────┐
│              Main Process                        │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────┐                 │
│  │    Main Thread             │                 │
│  │  - Start server socket     │                 │
│  │  - Accept connections      │                 │
│  │  - Create client threads   │                 │
│  └──────────┬─────────────────┘                 │
│             │                                     │
│             │ spawns                              │
│             │                                     │
│      ┌──────┴──────┬──────────┬──────────┐      │
│      │             │          │          │      │
│  ┌───▼───┐    ┌───▼───┐  ┌───▼───┐  ┌───▼───┐ │
│  │Thread │    │Thread │  │Thread │  │Thread │ │
│  │   1   │    │   2   │  │   3   │  │  ...  │ │
│  │       │    │       │  │       │  │       │ │
│  │Client │    │Client │  │Client │  │Client │ │
│  │ Alice │    │  Bob  │  │Charlie│  │   N   │ │
│  └───────┘    └───────┘  └───────┘  └───────┘ │
│      │             │          │          │      │
│      └─────────────┴──────────┴──────────┘      │
│                    │                             │
│         access (with locks)                      │
│                    │                             │
│          ┌─────────▼──────────┐                 │
│          │   Shared Resources │                 │
│          │  - clients dict    │                 │
│          │  - groups dict     │                 │
│          │  - thread lock     │                 │
│          └────────────────────┘                 │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Key Points:**
- One thread per client for concurrent handling
- Daemon threads (die when main thread exits)
- Shared data protected by locks
- Non-blocking for new connections

### 6.2 Client Threading

```
┌─────────────────────────────────────────────────┐
│           Client Process                         │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────┐                 │
│  │    Main Thread (GUI)       │                 │
│  │  - Event loop              │                 │
│  │  - User input              │                 │
│  │  - Display updates         │                 │
│  │  - Button clicks           │                 │
│  └──────────┬─────────────────┘                 │
│             │                                     │
│             │ spawns                              │
│             │                                     │
│      ┌──────▼──────────┐                         │
│      │                 │                         │
│  ┌───▼────────────┐    │                         │
│  │ Receiver Thread│    │                         │
│  │  - Continuous  │    │                         │
│  │    receive     │    │                         │
│  │  - Parse JSON  │    │                         │
│  │  - Update GUI  │    │                         │
│  └────────────────┘    │                         │
│                         │                         │
│        both access      │                         │
│             │           │                         │
│      ┌──────▼───────────▼───┐                    │
│      │  TCP Socket          │                    │
│      │  - send()            │                    │
│      │  - recv()            │                    │
│      └──────────────────────┘                    │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Key Points:**
- Main thread handles GUI (must not block)
- Receiver thread handles network I/O
- Thread-safe GUI updates
- Socket shared between threads

---

## 7. Network Topology

### 7.1 Star Topology

```
           ┌─────────────┐
           │   Server    │
           │  (Central)  │
           └──────┬──────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
   ┌────▼───┐ ┌──▼────┐ ┌──▼────┐
   │Client 1│ │Client2│ │Client3│
   └────────┘ └───────┘ └───────┘
```

**Characteristics:**
- All clients connect to central server
- Server is hub for all communication
- Clients don't communicate directly
- Adding/removing clients doesn't affect others

### 7.2 Physical Network Layout

```
┌────────────────────────────────────────┐
│           Subnet: 192.168.1.0/24       │
├────────────────────────────────────────┤
│                                         │
│  ┌──────────┐                          │
│  │  Router  │ 192.168.1.1              │
│  └────┬─────┘                          │
│       │                                 │
│  ┌────▼─────┐                          │
│  │  Switch  │                          │
│  └────┬─────┘                          │
│       │                                 │
│  ╔════╪══════════════════════╗         │
│  ║    │    Server            ║         │
│  ║    │    192.168.1.100     ║         │
│  ║    │    Port: 5555        ║         │
│  ╚═════════════════════════╝         │
│       │                                 │
│       ├───────┬───────┬───────┐        │
│       │       │       │       │        │
│   ┌───▼──┐ ┌─▼───┐ ┌─▼───┐ ┌─▼───┐   │
│   │PC 1  │ │PC 2 │ │PC 3 │ │PC N │   │
│   │.101  │ │.102 │ │.103 │ │.xxx │   │
│   └──────┘ └─────┘ └─────┘ └─────┘   │
│                                         │
└────────────────────────────────────────┘
```

---

## 8. Protocol Stack

### 8.1 Complete Stack View

```
┌───────────────────────────────────────────┐
│         Application Layer                 │
│  - Chat Protocol (Custom)                 │
│  - Commands: login, message, group, file  │
│  - User Interface (Tkinter GUI)           │
├───────────────────────────────────────────┤
│        Presentation Layer                 │
│  - JSON (JavaScript Object Notation)      │
│  - UTF-8 Text Encoding                    │
│  - Base64 File Encoding                   │
├───────────────────────────────────────────┤
│          Session Layer                    │
│  - Socket Sessions                        │
│  - Connection Management                  │
│  - State Tracking                         │
├───────────────────────────────────────────┤
│         Transport Layer                   │
│  - TCP (Transmission Control Protocol)    │
│  - Port: 5555                             │
│  - Reliable, Ordered, Error-checked       │
├───────────────────────────────────────────┤
│          Network Layer                    │
│  - IP (Internet Protocol v4)              │
│  - Addressing: 192.168.x.x               │
│  - Routing (OS Managed)                   │
├───────────────────────────────────────────┤
│         Data Link Layer                   │
│  - Ethernet (IEEE 802.3)                  │
│  - WiFi (IEEE 802.11)                     │
│  - MAC Addressing                         │
│  - Frame Formatting                       │
├───────────────────────────────────────────┤
│         Physical Layer                    │
│  - Ethernet Cables (Cat5/6)               │
│  - WiFi Radio (2.4/5 GHz)                 │
│  - Network Interface Card (NIC)           │
│  - Electrical/Radio Signals               │
└───────────────────────────────────────────┘
```

### 8.2 Message Encapsulation

```
┌────────────────────────────────────────────────┐
│  Application Data: "Hello Bob"                 │
└────────────────────────────────────────────────┘
                    │ JSON encode
                    ▼
┌────────────────────────────────────────────────┐
│  JSON: {"type":"message","content":"Hello"}    │
└────────────────────────────────────────────────┘
                    │ UTF-8 encode
                    ▼
┌────────────────────────────────────────────────┐
│  Bytes: [bytes representation]                 │
└────────────────────────────────────────────────┘
                    │ TCP segment
                    ▼
┌────────────────────────────────────────────────┐
│ TCP Header │ Data                               │
│ Src:54321  │                                    │
│ Dst:5555   │                                    │
└────────────────────────────────────────────────┘
                    │ IP packet
                    ▼
┌────────────────────────────────────────────────┐
│ IP Header    │ TCP Segment                      │
│ Src:192.168. │                                  │
│     1.101    │                                  │
│ Dst:192.168. │                                  │
│     1.100    │                                  │
└────────────────────────────────────────────────┘
                    │ Ethernet frame
                    ▼
┌────────────────────────────────────────────────┐
│ Eth Header  │ IP Packet           │ CRC        │
│ Dst MAC     │                     │ Checksum   │
│ Src MAC     │                     │            │
│ Type:IP     │                     │            │
└────────────────────────────────────────────────┘
                    │ Physical transmission
                    ▼
          [Electrical/Radio Signals]
```

---

## Conclusion

This architecture successfully demonstrates:
- Clear separation of concerns (layers)
- Concurrent client handling (threading)
- Reliable communication (TCP)
- Extensible design (easy to add features)
- Educational value (clear OSI mapping)

The modular design allows for future enhancements without major restructuring, making it both a functional application and an excellent learning platform.
