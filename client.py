import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Import ttk for Combobox

def select_file():
    """Opens a file dialog to select the input file."""
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=(("All files", "*.*"),))
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def convert_file():
    """Handles the file conversion process after user inputs."""
    filename = file_entry.get().strip()
    target_format = format_combobox.get().strip()

    if not filename or not target_format:
        messagebox.showerror("Input Error", "Please select a file and specify a target format.")
        return

    if not os.path.exists(filename):
        messagebox.showerror("File Error", "The selected file does not exist.")
        return

    try:
        base_filename = os.path.basename(filename)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 9999))

        # Send filename and target format
        client.send(f"{base_filename},{target_format}".encode())
        client.recv(1024)  # Wait for ACK

        with open(filename, "rb") as f:
            client.sendall(f.read())
        client.shutdown(socket.SHUT_WR)

        output_filename = f"converted_{base_filename.split('.')[0]}.{target_format}"
        with open(output_filename, "wb") as f:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                f.write(data)

        messagebox.showinfo("Success", f"File converted successfully and saved as: {output_filename}")
        client.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# GUI setup
root = tk.Tk()
root.title("File Conversion Tool")
root.geometry("800x500")  # Increased the size of the window
root.resizable(False, False)

# Set the background color for the window
root.configure(bg="#f7f7f7")

# Title Label
title_label = tk.Label(root, text="File Converter", font=("Helvetica", 18, "bold"), fg="#0f5769", bg="#f7f7f7")
title_label.pack(pady=20)

# Frame for file selection
frame = tk.Frame(root, bg="#f7f7f7")
frame.pack(padx=30, pady=10)

file_label = tk.Label(frame, text="Select File:", font=("Helvetica", 12), fg="#333", bg="#f7f7f7")
file_label.grid(row=0, column=0, padx=10, pady=10)

file_entry = tk.Entry(frame, width=35, font=("Helvetica", 12), bd=2, relief="solid", bg="#4c5557")
file_entry.grid(row=0, column=1, padx=10, pady=10)

browse_button = tk.Button(frame, text="Browse", command=select_file, font=("Helvetica", 12), bg="#FF6347", fg="#214852", relief="raised", width=12)  # Changed color to Coral
browse_button.grid(row=0, column=2, padx=10, pady=10)

# Frame for target format input (Dropdown list)
format_label = tk.Label(frame, text="Target Format:", font=("Helvetica", 12), fg="#333", bg="#f7f7f7")
format_label.grid(row=1, column=0, padx=10, pady=10)

# Dropdown list for target format
formats = ["pdf", "png", "jpg", "docx", "txt"]  # Add any other formats here
format_combobox = ttk.Combobox(frame, values=formats, state="readonly", width=33, font=("Helvetica", 12))
format_combobox.grid(row=1, column=1, padx=10, pady=10)
format_combobox.set("pdf")  # Default to "pdf"

# Convert button
convert_button = tk.Button(root, text="Convert File", command=convert_file, font=("Helvetica", 14, "bold"), bg="#4A90E2", fg="#214852", relief="raised", width=20)  # Changed color to Blue
convert_button.pack(pady=20)


# Run the GUI
root.mainloop()