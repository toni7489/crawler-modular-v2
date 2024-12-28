import tkinter as tk
from tkinter import messagebox

def show_config(root, max_depth, request_timeout, excluded_domains):
    config_window=tk.Toplevel(root) 
    config_window.title("Configuración") 
    config_window.geometry("500x250") 
    config_window.resizable(True, True)

    frame=tk.Frame(config_window,padx=20,pady=20) 
    frame.pack(fill=tk.BOTH,expand=True)

    tk.Label(frame,text="Profundidad máxima de escaneo:").grid(row=0,column=0,padx=10,pady=5,sticky="e")
    depth_entry=tk.Entry(frame) 
    depth_entry.insert(0,str(max_depth)) 
    depth_entry.grid(row=0,column=1,padx=10,pady=5)

    tk.Label(frame,text="Tiempo de espera (segundos):").grid(row=1,column=0,padx=10,pady=5,sticky="e")
    timeout_entry=tk.Entry(frame) 
    timeout_entry.insert(0,str(request_timeout)) 
    timeout_entry.grid(row=1,column=1,padx=10,pady=5)

    tk.Label(frame,text="Dominios excluidos\n(separados por coma):").grid(row=2,column=0,padx=10,pady=5,sticky="ne")
    excluded_entry=tk.Text(frame,height=3,width=30) 
    excluded_entry.insert(tk.END,", ".join(excluded_domains)) 
    excluded_entry.grid(row=2,column=1,padx=10,pady=5)

    def save_config():
        nonlocal max_depth, request_timeout, excluded_domains
        max_depth=int(depth_entry.get())
        request_timeout=int(timeout_entry.get())
        excluded_domains=[domain.strip() for domain in excluded_entry.get("1.0",tk.END).split(',') if domain.strip()]
        config_window.destroy()
        messagebox.showinfo("Configuración","Configuración guardada correctamente.")

    save_button=tk.Button(frame,text="Guardar",command=save_config) 
    save_button.grid(row=3,column=0,columnspan=2,pady=(10))