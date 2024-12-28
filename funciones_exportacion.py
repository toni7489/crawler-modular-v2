import pandas as pd
from tkinter import filedialog, messagebox

def export_to_excel(collected_data):
    if not collected_data:
        messagebox.showerror("Error", "No hay datos para exportar.")
        return
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Archivos de Excel", "*.xlsx")],
        title="Guardar como"
    )
    
    if not file_path:
        return
    
    df = pd.DataFrame(collected_data)
    
    try:
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Éxito", "Resultados exportados a Excel correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a Excel: {e}")

def save_results(collected_data):
    if not collected_data: 
        messagebox.showerror("Error", "No hay datos para guardar.") 
        return
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")],
        title="Guardar análisis"
    )
    
    if not file_path: 
        return
    
    try: 
        with open(file_path,'w',encoding='utf-8') as file: 
            json.dump(collected_data,file,ensure_ascii=False,indent=4) 
            messagebox.showinfo("Éxito","Análisis guardado correctamente.")
    
    except Exception as e: 
        messagebox.showerror("Error",f"No se pudo guardar el análisis: {e}")

def open_results(result_tree, collected_data, link_count_label, status_label):
    file_path = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")],
        title="Abrir análisis guardado"
    )
    
    if not file_path:
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)

        result_tree.delete(*result_tree.get_children())
        
        collected_data.clear()
        
        for item in loaded_data:
            result_tree.insert("", "end", values=(
                item['Código de Respuesta'],
                item['URL'],
                item['Tipo'],
                item['Título'],
                item['Etiqueta H1'],
                item['Meta Descripción'],
                item['Profundidad']
            ))
            
            collected_data.append(item)

        link_count_label.config(text=f"Enlaces encontrados: {len(collected_data)}")
        
        status_label.config(text="Resultados cargados correctamente.")
        
        messagebox.showinfo("Éxito", "Análisis cargado correctamente.")
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el análisis: {e}")