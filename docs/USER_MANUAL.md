# User Manual
## Computer Networks Chat Application

---

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using the Application](#using-the-application)
4. [Features Guide](#features-guide)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

---

## 1. Introduction

Welcome to the Computer Networks Chat Application! This application allows you to communicate with other users in real-time over a network. It's similar to popular messaging apps like WhatsApp but built as an educational project to demonstrate computer networking concepts.

### What Can You Do?
- Send instant messages to other users
- Create and participate in group chats
- Transfer files to other users
- See who's online
- Chat in real-time with multiple users

---

## 2. Getting Started

### 2.1 System Requirements

Before you begin, ensure your system meets these requirements:

**Operating System:**
- Windows 7 or later
- macOS 10.12 or later
- Linux (any recent distribution)

**Software:**
- Python 3.6 or higher installed
- Network connection (WiFi or Ethernet)

**Hardware:**
- Any modern computer with at least 512 MB RAM
- Network adapter (WiFi or Ethernet card)

### 2.2 Installation

**Step 1: Download the Application**
```bash
git clone https://github.com/BitR1ft/semprojectcn.git
cd semprojectcn
```

**Step 2: Verify Python Installation**
```bash
python --version
```
You should see version 3.6 or higher.

**Step 3: Install Tkinter (if needed)**

Most Python installations include Tkinter. If you get an error about Tkinter:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
brew install python-tk
```

### 2.3 First-Time Setup

**For Server (One person needs to do this):**

1. Open Terminal/Command Prompt
2. Navigate to the project folder
3. Run:
   ```bash
   cd src
   python server.py
   ```
4. Note the IP address displayed (you'll need to share this with others)

**For Clients (Everyone who wants to chat):**

1. Open Terminal/Command Prompt
2. Navigate to the project folder
3. Run:
   ```bash
   cd src
   python client.py
   ```

---

## 3. Using the Application

### 3.1 Logging In

When you start the client application, you'll see a login screen:

**Fields to Fill:**
1. **Server Address**: 
   - For local testing: `127.0.0.1`
   - For network: The IP address of the server computer
   
2. **Port**: 
   - Default: `5555`
   - Use the same port that the server is using
   
3. **Username**: 
   - Choose any username you like
   - Make it unique so others can identify you

**Steps:**
1. Enter the server address
2. Enter the port (usually 5555)
3. Type your desired username
4. Click "Connect" or press Enter

**Success:** You'll see the chat window open.

**Failure:** If connection fails:
- Check if the server is running
- Verify the server address and port
- Check your network connection

### 3.2 Main Chat Interface

After logging in, you'll see the main chat window with three main areas:

**1. Chat Messages Area (Left Side)**
- Displays all messages
- Shows timestamps
- Shows sender names
- System messages appear in blue italic text

**2. Online Users List (Right Side)**
- Shows all connected users
- "All Users" option for broadcasting
- Click a username to chat privately

**3. Message Input Area (Bottom)**
- Type your messages here
- Press Enter or click "Send" to send

### 3.3 Navigation

**Selecting Chat Recipients:**
1. Look at the "Online Users" list on the right
2. Click "All Users" to send messages to everyone
3. Click a specific username to chat privately

**Sending Messages:**
1. Select a recipient from the users list
2. Type your message in the input box
3. Press Enter or click "Send"

---

## 4. Features Guide

### 4.1 Private Messaging

**To send a private message:**
1. Click on a username in the "Online Users" list
2. Type your message
3. Press Enter or click "Send"

**Your message will appear as:**
```
[2024-01-01 12:00:00] You -> Username: Hello!
```

**Received messages appear as:**
```
[2024-01-01 12:00:00] Username: Hi there!
```

### 4.2 Broadcast Messages

**To send to everyone:**
1. Click "All Users" in the users list
2. Type your message
3. Press Enter or click "Send"

**Your message will appear as:**
```
[2024-01-01 12:00:00] You -> Everyone: Hello everyone!
```

### 4.3 Group Chat

**To create a group:**
1. Click the "Create Group" button
2. Enter a group name
3. A member selection window appears
4. Select members by clicking on their names
   - Hold Ctrl (Windows/Linux) or Cmd (Mac) to select multiple
5. Click "Create Group"

**To send group messages:**
- Group messages are automatically delivered to all members
- They appear with the group name:
```
[2024-01-01 12:00:00] [GroupName] Username: Hello group!
```

### 4.4 File Transfer

**To send a file:**
1. Select a specific user (not "All Users")
2. Click the "Send File" button
3. Browse and select the file you want to send
4. The file will be transferred

**To receive a file:**
1. When someone sends you a file, a dialog appears
2. Choose where to save the file
3. Click "Save"
4. The file is saved to your chosen location

**Supported Files:**
- Documents (PDF, DOCX, TXT, etc.)
- Images (JPG, PNG, GIF, etc.)
- Archives (ZIP, RAR, etc.)
- Any file type!

**File Size Limit:**
- Recommended: Under 10 MB for best performance
- Larger files may take longer to transfer

### 4.5 Online Status

**Online Users List:**
- Shows all currently connected users
- Updates in real-time
- Displays join/leave notifications

**System Notifications:**
- User joined: `*** Alice joined the chat ***`
- User left: `*** Bob left the chat ***`
- Group created: `*** Group 'Friends' created ***`

### 4.6 Chat History

**During Your Session:**
- All messages remain visible in the chat area
- Scroll up to see previous messages

**After Closing:**
- Chat history is not saved (current version)
- You'll start with a fresh chat window on next login

---

## 5. Troubleshooting

### 5.1 Connection Issues

**Problem: "Connection failed! Check server address and port."**

**Solutions:**
1. Verify the server is running
2. Check the server address:
   - Local: Use `127.0.0.1`
   - Network: Use the correct IP address
3. Confirm the port number (default: 5555)
4. Check firewall settings
5. Ensure you're on the same network (for LAN)

**Finding the Server IP Address:**

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address"

**Mac/Linux:**
```bash
ifconfig
```
or
```bash
ip addr show
```
Look for "inet" address

### 5.2 Application Issues

**Problem: Application won't start**

**Solutions:**
1. Verify Python installation:
   ```bash
   python --version
   ```
2. Check Tkinter:
   ```bash
   python -m tkinter
   ```
   A small window should appear
3. Reinstall Tkinter if needed

**Problem: Can't see the window**

**Solutions:**
1. Check if it's minimized
2. Try Alt+Tab (Windows/Linux) or Cmd+Tab (Mac)
3. Close and restart the application

**Problem: Messages not sending**

**Solutions:**
1. Check your internet/network connection
2. Verify the server is still running
3. Try disconnecting and reconnecting

### 5.3 File Transfer Issues

**Problem: Can't send files**

**Solutions:**
1. Make sure you selected a specific user (not "All Users")
2. Check file size (keep under 10 MB)
3. Verify you have permission to read the file
4. Check network bandwidth

**Problem: Can't receive files**

**Solutions:**
1. Make sure you have write permission in the save location
2. Check available disk space
3. Ensure your antivirus isn't blocking it

### 5.4 Performance Issues

**Problem: Application running slowly**

**Solutions:**
1. Close other applications
2. Check network connection speed
3. Reduce number of connected clients
4. Restart the application

**Problem: High network usage**

**Solutions:**
1. Avoid sending large files
2. Limit broadcast messages
3. Check for other network-heavy applications

---

## 6. FAQ

### General Questions

**Q: Do I need internet to use this?**
A: No! You can use it on a local network (LAN) without internet. However, you do need to be on the same network as the server.

**Q: How many people can use it at once?**
A: The application can handle many users simultaneously, limited only by your server's resources and network bandwidth.

**Q: Is my data encrypted?**
A: No, the current version doesn't include encryption. Use it only on trusted networks. Don't share sensitive information.

**Q: Can I use this over the internet?**
A: Yes, but you'll need to:
1. Configure port forwarding on your router
2. Use your public IP address
3. Consider security implications

### Usage Questions

**Q: Can I change my username?**
A: You need to disconnect and reconnect with a new username.

**Q: Can I send messages to multiple specific users?**
A: Currently, you can send to one user or all users. For multiple specific users, create a group.

**Q: How do I know if my message was delivered?**
A: If you don't see an error message, it was delivered successfully.

**Q: Can I send emojis?**
A: Yes! Your system's emoji keyboard works. On:
- Windows: Win + .
- Mac: Cmd + Ctrl + Space
- Linux: Depends on distribution

### Technical Questions

**Q: What protocol does it use?**
A: TCP/IP protocol for reliable message delivery.

**Q: What port does it use?**
A: Default is 5555, but it's configurable.

**Q: Can I run multiple servers?**
A: Yes, use different ports for each server.

**Q: Does it work on Raspberry Pi?**
A: Yes! Python runs on Raspberry Pi.

### Troubleshooting Questions

**Q: What if I lose connection?**
A: Close the application and reconnect. You'll lose your current session.

**Q: What if the server crashes?**
A: All clients will be disconnected. Restart the server and have everyone reconnect.

**Q: Can I recover lost messages?**
A: No, messages aren't saved in the current version.

---

## Best Practices

### For Server Operators

1. **Keep the server running** - Closing it disconnects everyone
2. **Note the IP address** - Share it with users who want to connect
3. **Monitor the console** - Watch for connection issues
4. **Use a stable computer** - Don't run server on a laptop that might sleep

### For Users

1. **Choose unique usernames** - Avoid confusion
2. **Be respectful** - Follow good chat etiquette
3. **Don't share sensitive info** - Messages aren't encrypted
4. **Keep files small** - Under 10 MB for best performance
5. **Stay connected** - Closing the window disconnects you

---

## Getting Help

If you encounter issues not covered in this manual:

1. Check the technical documentation in `/docs/TECHNICAL_DOC.md`
2. Review the project report in `/reports/PROJECT_REPORT.md`
3. Check the code comments in `server.py` and `client.py`

---

## Conclusion

Enjoy using the Computer Networks Chat Application! This tool demonstrates fundamental networking concepts while providing a practical communication platform.

Remember: This is an educational project. For production use, consider adding:
- Encryption (SSL/TLS)
- User authentication
- Database for persistence
- Enhanced security features

**Happy Chatting!** 💬
