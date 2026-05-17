#  Socket-Based Messaging App

> A real-time, multi-client chat application built with Python, demonstrating core Operating Systems concepts including **TCP sockets**, **POSIX system calls**, **multi-threading**, and **inter-process communication**.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [OS & Networking Concepts Demonstrated](#os--networking-concepts-demonstrated)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the App](#running-the-app)
  - [Same Machine (Two Terminals)](#option-1-same-machine-two-terminals)
  - [Two Devices on the Same Network](#option-2-two-devices-on-the-same-network)
  - [Using Virtual Machines](#option-3-using-virtual-machines)
  - [Using WSL (Windows Subsystem for Linux)](#option-4-using-wsl-windows-subsystem-for-linux)
- [Message Protocol](#message-protocol)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)

---

## Overview

PyChat is a client-server messaging application developed as an Operating Systems course project. It demonstrates how two (or more) users can exchange real-time messages over a **TCP network** using **POSIX-compliant socket system calls**.

The application is split into three components:

| File | Role |
|------|------|
| `server.py` | Central relay server — accepts connections and routes messages |
| `client.py` | Network layer — manages the socket connection and message protocol |
| `ui.py` | Graphical interface — WhatsApp-style light-theme chat window |

---

## Features

- ✅ Real-time messaging between multiple clients
- ✅ Username-based identification (login screen on startup)
- ✅ WhatsApp-inspired light UI with left/right chat bubbles
- ✅ Timestamps on every message
- ✅ System messages for connection/disconnection events
- ✅ Multi-threaded server — handles multiple clients simultaneously
- ✅ Graceful disconnect on window close
- ✅ Works across physical devices, virtual machines, and WSL instances

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        SERVER (server.py)                    │
│                                                              │
│   socket() → bind() → listen() → accept() [loops forever]   │
│                                                              │
│   Per client: threading.Thread → handle_client()            │
│               recv() → broadcast() → send() to all others   │
└──────────────────┬──────────────────────┬───────────────────┘
                   │  TCP Port 9999        │
         ┌─────────▼──────────┐  ┌────────▼──────────┐
         │   CLIENT A          │  │   CLIENT B         │
         │   (ui.py)           │  │   (ui.py)          │
         │   (client.py)       │  │   (client.py)      │
         │                     │  │                    │
         │  connect()          │  │  connect()         │
         │  send_message()     │  │  send_message()    │
         │  _receive_messages()│  │  _receive_messages()│
         └─────────────────────┘  └────────────────────┘
```

**Message flow:**

```
Client A types "Hello"
       │
       ▼
client.py formats: "Alice|Hello"
       │
       ▼  socket.send()
SERVER receives: "Alice|Hello"
       │
       ▼  broadcast() to all except sender
Client B receives: "Alice|Hello"
       │
       ▼
client.py parses → sender_name="Alice", text="Hello"
       │
       ▼
ui.py renders bubble on the left side
```

---

## OS & Networking Concepts Demonstrated

### System Calls Used

| System Call | Python Equivalent | Description |
|-------------|-------------------|-------------|
| `socket(2)` | `socket.socket(AF_INET, SOCK_STREAM)` | Creates a TCP socket file descriptor |
| `bind(2)` | `server.bind((HOST, PORT))` | Assigns an IP address and port to the socket |
| `listen(2)` | `server.listen()` | Marks socket as passive, ready to accept |
| `accept(2)` | `conn, addr = server.accept()` | Blocks until a client connects; returns a new socket |
| `connect(2)` | `client_socket.connect((HOST, PORT))` | Initiates a TCP connection to the server |
| `send(2)` | `client_socket.send(data)` | Writes bytes to the TCP stream |
| `recv(2)` | `conn.recv(1024)` | Reads up to 1024 bytes (blocks until data arrives) |
| `shutdown(2)` | `client_socket.shutdown(SHUT_RDWR)` | Gracefully terminates a connection |
| `close(2)` | `client_socket.close()` | Releases the socket file descriptor |

### Threading & Concurrency

- **Server**: Each accepted connection spawns a `threading.Thread`. Threads run `handle_client()` concurrently — the server can handle many clients at once without blocking.
- **Client**: A dedicated daemon thread runs `_receive_messages()` in the background. This prevents `recv()` (a **blocking** call) from freezing the Tkinter GUI event loop.
- **Thread safety**: Tkinter is single-threaded. The `root.after(0, fn)` pattern safely schedules UI updates from the background thread onto the main GUI thread.

### Protocol Design

A simple pipe-delimited framing protocol carries sender identity with each message:

```
FORMAT:   <username>|<message text>
EXAMPLE:  Alice|Hey, how are you?
```

The server is protocol-agnostic — it relays raw bytes. The client parses the `|` separator to split sender name from message body.

---

## Project Structure

```
pychat/
│
├── server.py          # TCP server — handles connections, threading, broadcast
├── client.py          # NetworkClient class — socket logic and protocol parsing
├── ui.py              # Tkinter GUI — login screen + chat window
├── paper-plane.png    # App icon (place in the same directory)
└── README.md
```

---

## Requirements

- **Python 3.8+**
- **Tkinter** (bundled with standard Python on Windows and macOS)

### Installing Tkinter on Linux/Ubuntu

```bash
sudo apt update
sudo apt install python3-tk
```

No other external libraries are needed — only Python's standard library (`socket`, `threading`, `tkinter`).

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/yousefiwahba/OS_Project.git

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. No pip install needed — standard library only
```

---

## Running the App

> **Always start the server before any clients.**

---

### Option 1: Same Machine (Two Terminals)

Best for quick local testing. Both clients connect to `127.0.0.1` (localhost).

**Terminal 1 — Start the server:**
```bash
python server.py
```
Expected output:
```
[STARTING] Server is listening on 0.0.0.0:9999...
```

**Terminal 2 — Start Client A:**
```bash
python ui.py
```

**Terminal 3 — Start Client B:**
```bash
python ui.py
```

Enter different usernames in each login screen, then type and send messages between the two windows.

---

### Option 2: Two Devices on the Same Network

Both devices must be connected to the **same Wi-Fi or LAN**.

**Step 1 — Find the server machine's local IP address**

On the machine that will run the server:

```bash
# Windows
ipconfig
# Look for "IPv4 Address" under your active adapter, e.g. 192.168.1.105

# Linux / macOS
ip a
# or
ifconfig
# Look for "inet" under your active interface, e.g. 192.168.1.105
```

**Step 2 — Start the server on Machine A:**
```bash
python server.py
```
The server binds to `0.0.0.0`, meaning it accepts connections on all interfaces automatically.

**Step 3 — Edit `client.py` on Machine B**

Open `client.py` and change the default host:
```python
# Before
def __init__(self, host='127.0.0.1', port=9999, ...):

# After — replace with Machine A's IP
def __init__(self, host='192.168.1.105', port=9999, ...):
```

**Step 4 — Start the client on Machine B:**
```bash
python ui.py
```

> **Firewall note:** If the connection is refused, allow port `9999` through the firewall on the server machine.
>
> Windows: `Control Panel → Windows Defender Firewall → Advanced Settings → Inbound Rules → New Rule → Port 9999 TCP`
>
> Linux: `sudo ufw allow 9999/tcp`

---

### Option 3: Using Virtual Machines

Works with VirtualBox, VMware, or any hypervisor.

**Recommended network mode: Bridged Adapter**

In this mode the VM gets its own IP address on your physical network, and the host and VM can communicate directly.

**VirtualBox setup:**
1. Open VM Settings → **Network**
2. Change "Attached to" from **NAT** to **Bridged Adapter**
3. Select your physical network card from the dropdown
4. Boot the VM

**Find the VM's IP:**
```bash
# Inside the VM
ip a
# Note the inet address, e.g. 192.168.1.110
```

**Scenario A — Server on host, client on VM:**
- Run `python server.py` on the host
- Find the host's LAN IP (`ipconfig` / `ifconfig`)
- In the VM, update `client.py` with the host's IP, then run `python ui.py`

**Scenario B — Server on VM, client on host:**
- Run `python server.py` inside the VM
- Find the VM's LAN IP (`ip a` inside VM)
- On the host, update `client.py` with the VM's IP, then run `python ui.py`

**Scenario C — Server on host, clients on two VMs:**
- Run `python server.py` on the host
- Point both VMs' `client.py` to the host's LAN IP
- Run `python ui.py` on each VM — they will chat through the host server

> **NAT mode alternative:** If you cannot use Bridged mode, use NAT with port forwarding. In VirtualBox: Settings → Network → Advanced → Port Forwarding → add a rule: `Host Port 9999 → Guest Port 9999`. Then use `127.0.0.1` as the server IP from the host side.

---

### Option 4: Using WSL (Windows Subsystem for Linux)

You can run the server inside WSL and the client on Windows (or vice versa).

**Find the WSL IP from inside WSL:**
```bash
ip addr show eth0 | grep inet
# e.g. inet 172.22.144.1
```

**Find the Windows host IP from inside WSL:**
```bash
cat /etc/resolv.conf | grep nameserver
# e.g. nameserver 172.22.144.1
```

**Scenario — Server in WSL, client on Windows:**
1. Inside WSL: `python server.py`
2. Note the WSL IP (e.g. `172.22.144.5`)
3. On Windows, update `client.py` → `host='172.22.144.5'`
4. On Windows: `python ui.py`

> **Note:** WSL 2 uses a virtual network adapter. The IP can change on each restart. Always re-check with `ip a` before connecting.

---

## Message Protocol

The app uses a lightweight plain-text framing protocol over TCP:

```
┌────────────────────────────────────────┐
│  <sender_name> | <message_body>        │
│  e.g.  "Alice|Hello everyone!"         │
└────────────────────────────────────────┘
```

**Encoding/Decoding** (`client.py`):

```python
# Sending
formatted_message = f"{self.username}|{text}"
self.client_socket.send(formatted_message.encode("utf-8"))

# Receiving
sender_name, actual_message = data.split("|", 1)
```

The `split("|", 1)` uses `maxsplit=1` so that a `|` character inside the message body is preserved correctly.

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `ConnectionRefusedError` | Server not running, or wrong IP/port | Start `server.py` first; verify IP and port match |
| App opens but messages don't appear on the other side | Clients not connected to the same server | Double-check `host` in `client.py` on both machines |
| `Address already in use` on server restart | OS hasn't released the port yet | Wait ~30 seconds, or the `SO_REUSEADDR` option handles this automatically |
| Window icon not found error | `paper-plane.png` missing | Place the icon file in the same directory as `ui.py`, or comment out the `root.iconphoto()` line |
| Tkinter not found (Linux) | Not installed by default | `sudo apt install python3-tk` |
| Can't connect across Wi-Fi | Firewall blocking port 9999 | Allow TCP port 9999 in the server machine's firewall settings |
| WSL IP keeps changing | WSL 2 assigns dynamic IPs | Re-run `ip a` in WSL after each reboot to get the current IP |

---

## Academic Context

This project was developed as part of an **Operating Systems** course assignment. The core learning objectives demonstrated are:

- Creating and managing **TCP sockets** using POSIX system calls
- Implementing a **multi-threaded server** with concurrent client handling
- Designing a simple **application-layer protocol** for structured messaging
- Integrating **non-blocking UI** with blocking I/O using threads
- Managing **thread safety** between the network layer and the GUI
