import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedTk
import threading
import webbrowser
import json
from funciones_analisis import extract_info_from_url
from funciones_exportacion import export_to_excel, save_results, open_results
from funciones_configuracion import show_config

# Colores
COLOR_FONDO_PRINCIPAL = "#2E3440"
COLOR_TEXTO_PRINCIPAL = "#D8DEE9"
COLOR_BOTONES = "#5E81AC"
COLOR_TEXTO_BOTONES = "#ECEFF4"
COLOR_BORDES = "#4C566A"
COLOR_FONDO_TABLA = "#3B4252"
COLOR_ENCABEZADOS_TABLA = "#387abc"
COLOR_TEXTO_TABLA = "#ECEFF4"

# Variables globales de configuración
max_depth = 3
request_timeout = 10
excluded_domains = []

# Variables globales
collected_data = []
processed_urls = set()

def analyze_url():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Debes ingresar una URL.")
        return
    
    result_tree.delete(*result_tree.get_children())
    collected_data.clear()
    processed_urls.clear()
    
    result_tree.insert("", "end", text="Iniciando análisis...")

    def run_analysis():
        try:
            processed_urls.add(url)
            extract_info_from_url(url, update_treeview, processed_urls, 1, max_depth, request_timeout, excluded_domains)
            status_label.config(text=f"Análisis completado.")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al procesar la URL: {e}")
            status_label.config(text="Error en el análisis.")

    threading.Thread(target=run_analysis, daemon=True).start()

def update_treeview(result):
    if result == "FIN":
        return
    
    result_tree.insert("", "end", values=(result['Código de Respuesta'], result['URL'], result['Tipo'], result['Título'], result['Etiqueta H1'], result['Meta Descripción'], result['Profundidad']))
    
    collected_data.append(result)
    total_links_label.config(text=f"Enlaces encontrados: {len(result_tree.get_children())}")

def open_url(event):
    selected_item = result_tree.selection()
    
    if selected_item:
        url = result_tree.item(selected_item[0])['values'][1]
        webbrowser.open(url)

def new_analysis():
    url_entry.delete(0, tk.END)
    result_tree.delete(*result_tree.get_children())
    
    collected_data.clear()
    processed_urls.clear()
    
    status_label.config(text="Esperando para iniciar el análisis...")
    total_links_label.config(text="Enlaces encontrados: 0")

def filter_results():
    # Implementa la lógica para filtrar resultados
    pass

def show_manual():
    # Implementa la lógica para mostrar el manual de usuario
    pass

def show_about():
    messagebox.showinfo("Acerca de", "Analizador de Enlaces SEO\nVersión 1.0\n© 2024 Tu Nombre")

# Crear la ventana principal con un tema moderno
root = ThemedTk(theme="arc")
root.title("Analizador de Enlaces SEO")
root.configure(bg=COLOR_FONDO_PRINCIPAL)

# Crear la barra de menú
menu_bar = tk.Menu(root, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL)
menu_bar.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Nuevo análisis", command=new_analysis)
file_menu.add_command(label="Abrir resultados", command=lambda: open_results(result_tree, collected_data, total_links_label, status_label))
file_menu.add_command(label="Guardar resultados", command=lambda: save_results(collected_data))
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)

tools_menu = tk.Menu(menu_bar, tearoff=0, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL)
menu_bar.add_cascade(label="Herramientas", menu=tools_menu)
tools_menu.add_command(label="Configuración", command=lambda: show_config(root, max_depth, request_timeout, excluded_domains))
tools_menu.add_command(label="Filtrar resultados", command=filter_results)

help_menu = tk.Menu(menu_bar, tearoff=0, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO_PRINCIPAL)
menu_bar.add_cascade(label="Ayuda", menu=help_menu)
help_menu.add_command(label="Manual de usuario", command=show_manual)
help_menu.add_command(label="Acerca de", command=show_about)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

root.resizable(True, True)

# Estilo para Treeview
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    font=("Verdana", 13),
    rowheight=25,
    background=COLOR_FONDO_TABLA,
    fieldbackground=COLOR_FONDO_TABLA,
    foreground=COLOR_TEXTO_TABLA,
)

style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background=COLOR_ENCABEZADOS_TABLA, foreground=COLOR_TEXTO_TABLA)

style.map("Treeview", background=[("selected", "#666666")], foreground=[("selected", "white")])

# Frame para la entrada de URL y botón de análisis
input_frame = ttk.Frame(root, padding="10 10 10 10", style="Custom.TFrame")
input_frame.pack(pady=(10))

url_label = ttk.Label(input_frame, text="Ingresa la URL:", background=COLOR_FONDO_PRINCIPAL, foreground=COLOR_TEXTO_PRINCIPAL)
url_label.pack(side="left", padx=(5))

url_entry = ttk.Entry(input_frame, width=50)
url_entry.pack(side="left", padx=(5))

analyze_button = ttk.Button(input_frame, text="Iniciar Análisis", command=analyze_url, style="Custom.TButton")
analyze_button.pack(side="left", padx=(5))

status_label = ttk.Label(root, text="Esperando para iniciar el análisis...", background=COLOR_FONDO_PRINCIPAL, foreground=COLOR_TEXTO_PRINCIPAL)
status_label.pack(pady=(5))

total_links_label = ttk.Label(root, text="Enlaces encontrados: 0", background=COLOR_FONDO_PRINCIPAL, foreground=COLOR_TEXTO_PRINCIPAL)
total_links_label.pack(pady=(5))

# Frame para la tabla de resultados
result_frame = ttk.Frame(root, padding="10 10 10 10")
result_frame.pack(fill=tk.BOTH, expand=True)

columns = ("Respuesta", "URL", "Tipo", "Título", "Etiqueta H1", "Meta Descripción", "Profundidad")

result_tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=20)

for col in columns:
    result_tree.heading(col, text=col)

result_tree.pack(expand=True, fill=tk.BOTH, padx=(10), pady=(10))

scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_tree.yview)
result_tree.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill='y')

result_tree.bind("<Double-1>", open_url)

# Frame para el botón de exportación
bottom_frame = ttk.Frame(root, padding="10 10 10 10")
bottom_frame.pack(side='bottom', fill='x', pady=(10))

export_button = ttk.Button(bottom_frame, text='Exportar a Excel', command=lambda: export_to_excel(collected_data), style="Custom.TButton")
export_button.pack(side='left', padx=(10))

# Definir estilos personalizados
style.configure("Custom.TFrame", background=COLOR_FONDO_PRINCIPAL)
style.configure("Custom.TButton", background=COLOR_BOTONES, foreground=COLOR_TEXTO_BOTONES)
style.map("Custom.TButton", background=[("active", COLOR_ENCABEZADOS_TABLA)])

root.mainloop()