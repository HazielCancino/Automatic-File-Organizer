import os
import shutil
import logging
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# Ensure the "logs" folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure the logging system
logging.basicConfig(
    filename=os.path.join("logs", "organizer.log"),  # Path to the log file
    level=logging.INFO,  # Logging level (INFO, ERROR, etc.)
    format="%(asctime)s - %(message)s"  # Log message format
)

# Define categories and their corresponding file extensions
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Compressed": [".zip", ".rar", ".7z"],
    "Executables": [".exe", ".msi"],
    "Others": []  # For files that don't match any category
}

# Function to create folders if they don't exist
def create_folders(base_path, categories):
    for category in categories:
        folder_path = os.path.join(base_path, category)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            message = f"Folder created: {folder_path}"
            log_message(message)

# Function to organize files
def organize_files(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        
        # Skip if it's a folder
        if os.path.isdir(file_path):
            continue
        
        # Get the file extension
        name, extension = os.path.splitext(file)
        extension = extension.lower()

        # Find the corresponding category
        found_category = "Others"
        for category, extensions in CATEGORIES.items():
            if extension in extensions:
                found_category = category
                break

        # Move the file to the corresponding folder
        destination_path = os.path.join(folder_path, found_category, file)
        shutil.move(file_path, destination_path)
        message = f"Moved: {file} -> {found_category}"
        log_message(message)

# Function to log messages and display them in the GUI
def log_message(message):
    logging.info(message)  # Log the message to the file
    log_area.insert(tk.END, message + "\n")  # Display the message in the GUI
    log_area.see(tk.END)  # Auto-scroll to the latest message

# Function to handle the "Organize" button click
def organize_button_click():
    folder_path = folder_path_var.get()
    
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder first.")
        return
    
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "The selected folder does not exist.")
        return
    
    log_message(f"Starting organization of: {folder_path}")
    create_folders(folder_path, CATEGORIES.keys())
    organize_files(folder_path)
    log_message("Organization completed.")
    messagebox.showinfo("Success", "Folder organization completed!")

# Function to handle the "Browse" button click
def browse_button_click():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_var.set(folder_selected)

# Create the main application window
root = tk.Tk()
root.title("Automatic File Organizer")
root.geometry("800x500")
root.configure(bg="#0d0d1a")  # Dark background for cyberpunk theme

# Cyberpunk color scheme
bg_color = "#0d0d1a"  # Dark blue
fg_color = "#ffffff"  # White
accent_color = "#8a2be2"  # Purple
button_color = "#4b0082"  # Dark purple
log_bg_color = "#1a1a2e"  # Darker blue for log area

# Variable to store the selected folder path
folder_path_var = tk.StringVar()

# Create and place GUI elements
tk.Label(root, text="Automatic File Organizer", font=("Helvetica", 20, "bold"), bg=bg_color, fg=accent_color).grid(row=0, column=0, columnspan=3, pady=10)

tk.Label(root, text="Select Folder to Organize:", font=("Helvetica", 12), bg=bg_color, fg=fg_color).grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=folder_path_var, width=50, font=("Helvetica", 12), bg=log_bg_color, fg=fg_color, insertbackground=fg_color).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_button_click, font=("Helvetica", 12), bg=button_color, fg=fg_color, activebackground=accent_color, activeforeground=fg_color).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Organize", command=organize_button_click, font=("Helvetica", 14, "bold"), bg=button_color, fg=fg_color, activebackground=accent_color, activeforeground=fg_color).grid(row=2, column=1, pady=20)

# Create a scrollable text area for logs
log_area = scrolledtext.ScrolledText(root, width=80, height=15, font=("Courier", 10), bg=log_bg_color, fg=fg_color, insertbackground=fg_color)
log_area.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()