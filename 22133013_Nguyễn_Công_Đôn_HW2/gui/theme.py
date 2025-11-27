import tkinter as tk
from tkinter import ttk

# Color Palette
COLOR_BG = "#f5f5f7"        # Light gray background
COLOR_FG = "#1d1d1f"        # Dark text
COLOR_ACCENT = "#0066cc"    # Blue accent
COLOR_ACCENT_HOVER = "#0052a3"
COLOR_WHITE = "#ffffff"
COLOR_BORDER = "#d1d1d6"
COLOR_PANEL_BG = "#ffffff"

FONT_MAIN = ("Segoe UI", 10)
FONT_HEADER = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 14, "bold")

def setup_theme(root: tk.Tk):
    style = ttk.Style(root)
    
    # Try to use 'clam' theme as base for consistent cross-platform styling
    # If not available, fallback to default
    if "clam" in style.theme_names():
        style.theme_use("clam")
    
    # Configure Colors and Fonts
    style.configure(".", 
        background=COLOR_BG, 
        foreground=COLOR_FG, 
        font=FONT_MAIN
    )
    
    # TFrame
    style.configure("TFrame", background=COLOR_BG)
    style.configure("Card.TFrame", background=COLOR_PANEL_BG, relief="flat")
    
    # TLabel
    style.configure("TLabel", background=COLOR_BG, foreground=COLOR_FG)
    style.configure("Title.TLabel", font=FONT_TITLE, foreground=COLOR_ACCENT)
    style.configure("Header.TLabel", font=FONT_HEADER, foreground=COLOR_FG)
    style.configure("Card.TLabel", background=COLOR_PANEL_BG)
    
    # TButton
    style.configure("TButton",
        padding=(10, 6),
        relief="flat",
        background=COLOR_ACCENT,
        foreground=COLOR_WHITE,
        font=("Segoe UI", 10, "bold"),
        borderwidth=0
    )
    style.map("TButton",
        background=[("active", COLOR_ACCENT_HOVER), ("pressed", COLOR_ACCENT_HOVER)],
        foreground=[("disabled", "#a0a0a0")]
    )
    
    # Secondary Button (e.g. Close, Restore)
    style.configure("Secondary.TButton",
        background="#e0e0e0",
        foreground="#333333"
    )
    style.map("Secondary.TButton",
        background=[("active", "#d0d0d0"), ("pressed", "#c0c0c0")]
    )

    # TLabelframe
    style.configure("TLabelframe", 
        background=COLOR_PANEL_BG, 
        relief="solid", 
        borderwidth=1,
        bordercolor=COLOR_BORDER
    )
    style.configure("TLabelframe.Label", 
        background=COLOR_PANEL_BG, 
        foreground=COLOR_ACCENT,
        font=FONT_HEADER
    )
    
    # TScale
    style.configure("Horizontal.TScale", 
        background=COLOR_PANEL_BG,
        troughcolor="#e0e0e0",
        sliderthickness=16
    )
    
    # TRadiobutton & TCheckbutton
    style.configure("TRadiobutton", background=COLOR_PANEL_BG, font=FONT_MAIN)
    style.configure("TCheckbutton", background=COLOR_PANEL_BG, font=FONT_MAIN)
    
    # TPanedwindow
    style.configure("TPanedwindow", background=COLOR_BG)
    
    # Scrollbar
    style.configure("Vertical.TScrollbar", 
        background="#f0f0f0",
        troughcolor=COLOR_BG,
        relief="flat",
        arrowsize=12
    )

    # Configure root background
    root.configure(bg=COLOR_BG)

