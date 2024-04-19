import subprocess
import threading
import os
import tkinter as tk
from tkinter import scrolledtext

def worker(script, textbox, output_file):
    with open(output_file, 'w') as file:
        proc = subprocess.Popen(['python', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in iter(proc.stdout.readline, b''):
            line = f"{line.strip()}\n"  # Strip whitespace
            textbox.insert(tk.END, line)
            textbox.see(tk.END)
            file.write(line)
            file.flush()

        for line in iter(proc.stderr.readline, b''):
            line = f"{line.strip()}\n"  # Strip whitespace
            textbox.insert(tk.END, line)
            textbox.see(tk.END)
            file.write(line)
            file.flush()

if __name__ == "__main__":
    scripts = [r"C:\Users\14374\Downloads\internal camera.py",
               r"C:\Users\14374\Downloads\Front Camera.py",
               r"C:\Users\14374\Downloads\AD1.py",
               r"C:\Users\14374\Downloads\tracking checker.py"]

    output_files = [f"output_{i}.txt" for i in range(len(scripts))]

    root = tk.Tk()

    textboxes = []
    for _ in range(4):
        textbox = scrolledtext.ScrolledText(root)
        textboxes.append(textbox)

    for i, (textbox, output_file) in enumerate(zip(textboxes, output_files)):
        textbox.grid(row=i//2, column=i%2, sticky="nsew")
        thread = threading.Thread(target=worker, args=(scripts[i], textbox, output_file))
        thread.start()

    root.mainloop()

    print("All scripts finished.")
