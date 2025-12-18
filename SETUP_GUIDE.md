# Quick Setup Guide
## Computer Networks Chat Application

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Verify Python Installation

```bash
python --version
```

You should see Python 3.6 or higher. If not, install Python from [python.org](https://www.python.org/).

### Step 2: Clone the Repository

```bash
git clone https://github.com/BitR1ft/semprojectcn.git
cd semprojectcn
```

### Step 3: Test Python Libraries

```bash
python -c "import socket, threading, json, tkinter, base64; print('All libraries available!')"
```

If you see "All libraries available!" you're ready!

### Step 4: Start the Server

Open a terminal/command prompt:

```bash
cd src
python server.py
```

You should see:
```
============================================================
COMPUTER NETWORKS CHAT SERVER
Semester Project - OSI Model Implementation
============================================================
[SERVER] Initializing on 0.0.0.0:5555
[SERVER] Server started on 0.0.0.0:5555
[SERVER] Waiting for connections...
```

✅ **Server is running!**

### Step 5: Start a Client

Open a **NEW** terminal/command prompt:

```bash
cd src
python client.py
```

A login window appears. Enter:
- **Server Address**: `127.0.0.1`
- **Port**: `5555`
- **Username**: `Alice`

Click **Connect**.

✅ **You're connected!**

### Step 6: Test with Multiple Clients

Open more terminals and run:

```bash
python client.py
```

Login with different usernames (`Bob`, `Charlie`, etc.)

---

## 🎯 Testing Features

### Private Message
1. In Alice's window, select "Bob" from the users list
2. Type a message
3. Press Enter or click Send
4. Bob receives it!

### Broadcast
1. Select "All Users"
2. Type a message
3. Everyone receives it!

### Group Chat
1. Click "Create Group"
2. Enter group name
3. Select members
4. Send group messages

### File Transfer
1. Select a user
2. Click "Send File"
3. Choose a file
4. Recipient saves it

---

## 🐛 Troubleshooting

### "Connection failed"
- Check if server is running
- Verify server address and port
- Check firewall settings

### "No module named 'tkinter'"

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

### Window not appearing
- Check if it's minimized
- Try Alt+Tab (Windows/Linux) or Cmd+Tab (Mac)

---

## 🌐 Network Setup

### Local Testing (Same Computer)
Use `127.0.0.1` as server address. ✅ Easy!

### LAN Setup (Different Computers)

**Step 1:** Find server's IP address

**Windows:**
```cmd
ipconfig
```

**Mac/Linux:**
```bash
ifconfig
# or
ip addr show
```

Look for an address like `192.168.x.x`

**Step 2:** On client computers, use that IP address

Example: `192.168.1.100`

**Step 3:** Ensure firewall allows port 5555

**Windows:**
```
Control Panel → Windows Firewall → Allow an app → Add Python
```

**Linux:**
```bash
sudo ufw allow 5555
```

---

## 📁 Project Structure

```
semprojectcn/
├── src/
│   ├── server.py          ← Start this first
│   └── client.py          ← Then start this (multiple times)
├── docs/                  ← Documentation
├── presentation/          ← Presentation materials
├── reports/               ← Project report
├── README.md             ← Overview
└── SETUP_GUIDE.md        ← This file
```

---

## ✅ Success Checklist

- [ ] Python 3.6+ installed
- [ ] Repository cloned
- [ ] Server starts without errors
- [ ] Client connects successfully
- [ ] Can send private messages
- [ ] Can send broadcast messages
- [ ] Can create groups
- [ ] Can transfer files

If all checked, you're ready to go! 🎉

---

## 📚 Next Steps

1. **Read the User Manual**: `docs/USER_MANUAL.md`
2. **Explore Technical Docs**: `docs/TECHNICAL_DOC.md`
3. **Study OSI Mapping**: `docs/OSI_MODEL_MAPPING.md`
4. **Review Project Report**: `reports/PROJECT_REPORT.md`

---

## 🤝 Getting Help

If you encounter issues:

1. Check the **USER_MANUAL.md** troubleshooting section
2. Review error messages carefully
3. Verify network connectivity
4. Ensure correct IP addresses and ports

---

**Happy Chatting!** 💬
