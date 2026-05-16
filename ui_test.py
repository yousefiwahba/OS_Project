import tkinter as tk
from tkinter import font as tkfont
from client import NetworkClient
from datetime import datetime

# ─────────────────────────────────────────────
#  COLOUR PALETTE (WhatsApp Light Theme)
# ─────────────────────────────────────────────
BG_DARK = "#e6ded4"
BG_PANEL = "#eee8e1"
BG_INPUT = "#f0f2f5"
BG_BUBBLE_YOU = "#d9fdd3"
BG_BUBBLE_FRI = "#ffffff"
BG_SYS = "#fff3c4"
ACCENT = "#25d366"
TEXT_PRIMARY = "#111b21"
TEXT_SECONDARY = "#667781"
TEXT_BUBBLE = "#111b21"
BORDER = "#d1d7db"


# ─────────────────────────────────────────────
#  UI <--> NETWORK INTEGRATION
# ─────────────────────────────────────────────
def handle_incoming_message(sender_name, text):
    display_message("friend", text, sender_name)


net_client = NetworkClient(host='127.0.0.1', port=9999, on_receive_callback=handle_incoming_message)


def enter_chat(event=None):
    username = username_entry.get().strip()
    if not username:
        return

    login_frame.pack_forget()
    header.pack(fill=tk.X, side=tk.TOP)
    input_bar.pack(fill=tk.X, side=tk.BOTTOM)
    chat_frame.pack(fill=tk.BOTH, expand=True)

    success = net_client.connect(username)
    if success:
        display_message("system", f"Connected as '{username}'")
    else:
        display_message("system", "Could not connect. Is the server running?")


def send_message(event=None):
    message = message_entry.get()
    if not message:
        return

    display_message("you", message)
    message_entry.delete(0, tk.END)
    net_client.send_message(message)


def on_close():
    net_client.disconnect()
    root.destroy()


def display_message(kind, text, sender_name="Friend"):
    root.after(0, _insert_bubble, kind, text, sender_name)


# ─────────────────────────────────────────────
#  REFINED BUBBLE RENDERER
# ─────────────────────────────────────────────
def _insert_bubble(kind, text, sender_name):
    chat_area.config(state=tk.NORMAL)
    current_time = datetime.now().strftime("%I:%M %p")

    # 1. Insert a transparent spacer to separate chat bubbles visually
    chat_area.insert(tk.END, "\n", "spacer")

    # 2. Insert the components piece by piece with distinct tags
    if kind == "you":
        # Sender (Right Side)
        chat_area.insert(tk.END, "You\n", ("col_you", "bg_you", "name_you"))
        chat_area.insert(tk.END, f"{text}\n", ("col_you", "bg_you", "msg_text"))
        chat_area.insert(tk.END, f"{current_time}", ("col_you", "bg_you", "time_you"))

    elif kind == "friend":
        # Receiver (Left Side)
        chat_area.insert(tk.END, f"{sender_name}\n", ("col_friend", "bg_friend", "name_friend"))
        chat_area.insert(tk.END, f"{text}\n", ("col_friend", "bg_friend", "msg_text"))
        chat_area.insert(tk.END, f"{current_time}", ("col_friend", "bg_friend", "time_friend"))

    else:
        # System Messages (Centered)
        chat_area.insert(tk.END, f"⚙ {text}", ("col_sys", "bg_sys"))

    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)


# ─────────────────────────────────────────────
#  WINDOW & LAYOUT SETUP
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("OS Project Chat")
root.geometry("460x640")
root.minsize(360, 480)
root.configure(bg=BG_DARK)

# Global Fonts
font_body = tkfont.Font(family="Segoe UI", size=11)
font_label = tkfont.Font(family="Segoe UI", size=9, weight="bold")
font_title = tkfont.Font(family="Segoe UI", size=13, weight="bold")
font_subtitle = tkfont.Font(family="Segoe UI", size=9)
font_input = tkfont.Font(family="Segoe UI", size=11)
font_btn = tkfont.Font(family="Segoe UI", size=10, weight="bold")

# ─────────────────────────────────────────────
#  LOGIN SCREEN
# ─────────────────────────────────────────────
login_frame = tk.Frame(root, bg=BG_DARK)
login_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(login_frame, text="Welcome to Network Chat", font=font_title, bg=BG_DARK, fg=TEXT_PRIMARY).pack(pady=(150, 20))
tk.Label(login_frame, text="Enter a display name:", font=font_body, bg=BG_DARK, fg=TEXT_SECONDARY).pack(pady=(0, 10))

username_entry = tk.Entry(login_frame, font=font_input, bg=BG_BUBBLE_FRI, fg=TEXT_PRIMARY,
                          insertbackground=TEXT_PRIMARY, relief=tk.FLAT, justify=tk.CENTER)
username_entry.pack(ipady=8, ipadx=10)
username_entry.bind("<Return>", enter_chat)

join_btn = tk.Button(login_frame, text="Join Chat", command=enter_chat, bg=ACCENT, fg="white", font=font_btn,
                     relief=tk.FLAT, cursor="hand2", padx=20, pady=8)
join_btn.pack(pady=20)

# ─────────────────────────────────────────────
#  CHAT INTERFACE
# ─────────────────────────────────────────────

# 1. HEADER
header = tk.Frame(root, bg=BG_PANEL, height=64)
header.pack_propagate(False)

avatar_canvas = tk.Canvas(header, width=40, height=40, bg=BG_PANEL, highlightthickness=0)
avatar_canvas.place(x=16, y=12)
avatar_canvas.create_oval(0, 0, 40, 40, fill=ACCENT, outline="")
avatar_canvas.create_text(20, 20, text="#", fill="white", font=tkfont.Font(family="Segoe UI", size=14, weight="bold"))
avatar_canvas.create_oval(27, 27, 38, 38, fill=BG_PANEL, outline="")
avatar_canvas.create_oval(29, 29, 37, 37, fill="#3ddc84", outline="")

header_text_frame = tk.Frame(header, bg=BG_PANEL)
header_text_frame.place(x=66, y=10)
tk.Label(header_text_frame, text="Global Chat Room", font=font_title, bg=BG_PANEL, fg=TEXT_PRIMARY).pack(anchor="w")
tk.Label(header_text_frame, text="● Online", font=font_subtitle, bg=BG_PANEL, fg="#3ddc84").pack(anchor="w")

# 2. INPUT BAR
input_bar = tk.Frame(root, bg="#f0f2f5", height=64)
input_bar.pack_propagate(False)

input_inner = tk.Frame(input_bar, bg="#f0f2f5")
input_inner.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

message_entry = tk.Entry(
    input_inner, font=font_input, bg="#ffffff", fg=TEXT_PRIMARY, relief=tk.FLAT, bd=0,
    insertbackground=TEXT_PRIMARY, selectbackground="#cce8ff", highlightthickness=1,
    highlightcolor=BORDER, highlightbackground=BORDER)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=7, padx=(0, 10))
message_entry.bind("<Return>", send_message)

send_button = tk.Canvas(input_inner, width=44, height=44, bg="#f0f2f5", highlightthickness=0, bd=0, cursor="hand2")
send_button.pack(side=tk.RIGHT)
send_button.create_oval(2, 2, 42, 42, fill=ACCENT, outline=ACCENT)
send_button.create_text(22, 22, text="➤", fill="white", font=("Segoe UI", 14, "bold"))
send_button.bind("<Button-1>", lambda e: send_message())

# 3. CHAT AREA
chat_frame = tk.Frame(root, bg=BG_PANEL)

scrollbar = tk.Scrollbar(chat_frame, width=6, troughcolor=BG_PANEL, bg=BG_INPUT, activebackground=ACCENT,
                         relief=tk.FLAT, bd=0, highlightthickness=0)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 4), pady=8)

chat_area = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED, bg=BG_PANEL, fg=TEXT_PRIMARY,
                    relief=tk.FLAT, bd=0, padx=12, pady=12, cursor="arrow",
                    selectbackground=ACCENT, yscrollcommand=scrollbar.set, highlightthickness=0)
chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=chat_area.yview)

# ─────────────────────────────────────────────────────────────
#  TAG CONFIGURATIONS (THE FIX)
# ─────────────────────────────────────────────────────────────

# 1. Alignment & Margins (Creates the Left/Right columns)
chat_area.tag_configure("col_you", justify=tk.RIGHT, lmargin1=80, lmargin2=80, rmargin=20)
chat_area.tag_configure("col_friend", justify=tk.LEFT, lmargin1=20, lmargin2=20, rmargin=80)
chat_area.tag_configure("col_sys", justify=tk.CENTER, lmargin1=20, lmargin2=20, rmargin=20)

# 2. Bubble Background Colors
chat_area.tag_configure("bg_you", background=BG_BUBBLE_YOU)
chat_area.tag_configure("bg_friend", background=BG_BUBBLE_FRI)
chat_area.tag_configure("bg_sys", background=BG_SYS, font=tkfont.Font(family="Segoe UI", size=9, slant="italic"))

# 3. Fonts & Colors for specific text lines
font_msg = tkfont.Font(family="Segoe UI", size=11)
font_name = tkfont.Font(family="Segoe UI", size=10, weight="bold")
font_time = tkfont.Font(family="Segoe UI", size=8)

chat_area.tag_configure("msg_text", font=font_msg, foreground=TEXT_PRIMARY)
chat_area.tag_configure("name_you", font=font_name, foreground="#075E54")  # Dark green name
chat_area.tag_configure("name_friend", font=font_name, foreground="#128C7E")  # Teal name
chat_area.tag_configure("time_you", font=font_time, foreground=TEXT_SECONDARY)
chat_area.tag_configure("time_friend", font=font_time, foreground=TEXT_SECONDARY)

# 4. Transparent Spacer to separate bubbles
chat_area.tag_configure("spacer", font=("Segoe UI", 4))

root.protocol("WM_DELETE_WINDOW", on_close)

# Start App
root.mainloop()