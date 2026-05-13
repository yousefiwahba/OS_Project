import tkinter as tk
from tkinter import font as tkfont
from client import NetworkClient

# ─────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────
BG_DARK = "#0f1117"
BG_PANEL = "#1a1d27"
BG_INPUT = "#22253a"
BG_BUBBLE_YOU = "#2f6feb"
BG_BUBBLE_FRI = "#252836"
BG_SYS = "#1e2030"
ACCENT = "#4f8eff"
TEXT_PRIMARY = "#e8eaf6"
TEXT_SECONDARY = "#8b8fa8"
TEXT_BUBBLE = "#ffffff"
BORDER = "#2a2d3e"


# ─────────────────────────────────────────────
#  UI <--> NETWORK INTEGRATION
# ─────────────────────────────────────────────
def handle_incoming_message(text):
    display_message("friend", text)


net_client = NetworkClient(host='127.0.0.1', port=9999, on_receive_callback=handle_incoming_message)


def connect_to_server():
    success = net_client.connect()
    if success:
        display_message("system", "Connected to server.")
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


def display_message(kind, text):
    root.after(0, _insert_bubble, kind, text)


# ─────────────────────────────────────────────
#  BUBBLE RENDERER
# ─────────────────────────────────────────────
def _insert_bubble(kind, text):
    chat_area.config(state=tk.NORMAL)
    if kind == "you":
        tag, prefix, label, label_tag = ("bubble_you", "", "  You", "label_you")
    elif kind == "friend":
        tag, prefix, label, label_tag = ("bubble_friend", "", "  Friend", "label_friend")
    else:
        tag, prefix, label, label_tag = ("bubble_sys", "⚙  ", None, None)

    if label:
        chat_area.insert(tk.END, f"\n{label}\n", label_tag)
    else:
        chat_area.insert(tk.END, "\n")

    chat_area.insert(tk.END, f"  {prefix}{text}\n", tag)
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)


# ─────────────────────────────────────────────
#  WINDOW & LAYOUT (FIXED PACKING ORDER)
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("OS Project Chat")
root.geometry("460x640")
root.minsize(360, 480)
root.configure(bg=BG_DARK)

font_body = tkfont.Font(family="Segoe UI", size=11)
font_label = tkfont.Font(family="Segoe UI", size=9, weight="bold")
font_title = tkfont.Font(family="Segoe UI", size=13, weight="bold")
font_subtitle = tkfont.Font(family="Segoe UI", size=9)
font_input = tkfont.Font(family="Segoe UI", size=11)
font_btn = tkfont.Font(family="Segoe UI", size=10, weight="bold")

# 1. HEADER (Packed TOP)
header = tk.Frame(root, bg=BG_PANEL, height=64)
header.pack(fill=tk.X, side=tk.TOP)
header.pack_propagate(False)

avatar_canvas = tk.Canvas(header, width=40, height=40, bg=BG_PANEL, highlightthickness=0)
avatar_canvas.place(x=16, y=12)
avatar_canvas.create_oval(0, 0, 40, 40, fill=ACCENT, outline="")
avatar_canvas.create_text(20, 20, text="F", fill="white", font=tkfont.Font(family="Segoe UI", size=14, weight="bold"))
avatar_canvas.create_oval(27, 27, 38, 38, fill=BG_PANEL, outline="")
avatar_canvas.create_oval(29, 29, 37, 37, fill="#3ddc84", outline="")

header_text_frame = tk.Frame(header, bg=BG_PANEL)
header_text_frame.place(x=66, y=10)
tk.Label(header_text_frame, text="Network Chat", font=font_title, bg=BG_PANEL, fg=TEXT_PRIMARY).pack(anchor="w")
tk.Label(header_text_frame, text="● Online", font=font_subtitle, bg=BG_PANEL, fg="#3ddc84").pack(anchor="w")
tk.Frame(root, bg=BORDER, height=1).pack(fill=tk.X)

# 2. INPUT BAR (Packed BOTTOM first, so it claims its space!)
input_bar = tk.Frame(root, bg=BG_INPUT, height=64)
input_bar.pack(fill=tk.X, side=tk.BOTTOM)
input_bar.pack_propagate(False)

input_inner = tk.Frame(input_bar, bg=BG_INPUT)
input_inner.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

message_entry = tk.Entry(input_inner, font=font_input, bg="#2e3150", fg=TEXT_PRIMARY, relief=tk.FLAT, bd=0,
                         insertbackground=ACCENT, selectbackground=ACCENT, highlightthickness=1, highlightcolor=ACCENT,
                         highlightbackground=BORDER)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=7, padx=(0, 10))
message_entry.bind("<Return>", send_message)

send_button = tk.Button(input_inner, text="Send ↑", command=send_message, bg=ACCENT, fg="white",
                        activebackground="#3d7be8", activeforeground="white", relief=tk.FLAT, bd=0, font=font_btn,
                        padx=18, pady=6, cursor="hand2")
send_button.pack(side=tk.RIGHT)


def on_btn_enter(e):  send_button.config(bg="#3d7be8")


def on_btn_leave(e):  send_button.config(bg=ACCENT)


send_button.bind("<Enter>", on_btn_enter)
send_button.bind("<Leave>", on_btn_leave)

# 3. CHAT AREA (Packed BOTH expand=True last, so it strictly takes the remaining middle space)
chat_frame = tk.Frame(root, bg=BG_PANEL)
chat_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(chat_frame, width=6, troughcolor=BG_PANEL, bg=BG_INPUT, activebackground=ACCENT,
                         relief=tk.FLAT, bd=0, highlightthickness=0)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 4), pady=8)

chat_area = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=font_body, bg=BG_PANEL, fg=TEXT_PRIMARY,
                    relief=tk.FLAT, bd=0, padx=12, pady=12, spacing1=2, spacing3=4, cursor="arrow",
                    selectbackground=ACCENT, yscrollcommand=scrollbar.set, insertbackground=ACCENT,
                    highlightthickness=0)
chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=chat_area.yview)

chat_area.tag_configure("bubble_you", background=BG_BUBBLE_YOU, foreground=TEXT_BUBBLE, font=font_body, lmargin1=80,
                        lmargin2=80, rmargin=12, spacing1=4, spacing3=8, relief=tk.FLAT)
chat_area.tag_configure("bubble_friend", background=BG_BUBBLE_FRI, foreground=TEXT_PRIMARY, font=font_body, lmargin1=12,
                        lmargin2=12, rmargin=80, spacing1=4, spacing3=8)
chat_area.tag_configure("bubble_sys", background=BG_SYS, foreground=TEXT_SECONDARY,
                        font=tkfont.Font(family="Segoe UI", size=9, slant="italic"), lmargin1=20, lmargin2=20,
                        rmargin=20, spacing1=2, spacing3=6, justify=tk.CENTER)
chat_area.tag_configure("label_you", foreground=TEXT_SECONDARY, font=font_label, lmargin1=80, lmargin2=80, spacing1=10,
                        spacing3=0, justify=tk.RIGHT)
chat_area.tag_configure("label_friend", foreground=TEXT_SECONDARY, font=font_label, lmargin1=12, lmargin2=12,
                        spacing1=10, spacing3=0)

tk.Frame(root, bg=BORDER, height=1).pack(fill=tk.X)

root.protocol("WM_DELETE_WINDOW", on_close)

# Start App
connect_to_server()
root.mainloop()