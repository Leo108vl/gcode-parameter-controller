import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

# Variables globales para almacenar selección
archivos_seleccionados = []
carpeta_destino = None

# Cambios a realizar
REEMPLAZOS = [
    ("M140 S95", "; Cambiado de 95°C a 110°C para mejor adherencia\nM140 S110"),
    ("M190 S95", "; Cambiado de 95°C a 110°C para mejor adherencia\nM190 S110"),
]

def procesar_archivo(origen, destino):
    with open(origen, 'r', encoding='utf-8', errors='ignore') as f:
        lineas = f.readlines()
    modificado = False
    nuevas_lineas = []
    for linea in lineas:
        reemplazada = False
        for buscar, reemplazo in REEMPLAZOS:
            if linea.strip().startswith(buscar):
                nuevas_lineas.append(reemplazo + '\n')
                modificado = True
                reemplazada = True
                break
        if not reemplazada:
            nuevas_lineas.append(linea)
    if modificado:
        with open(destino, 'w', encoding='utf-8') as f:
            f.writelines(nuevas_lineas)
    return modificado

def ejecutar_proceso():
    global archivos_seleccionados, carpeta_destino
    if not archivos_seleccionados or not carpeta_destino:
        messagebox.showwarning("Faltan datos", "Debes seleccionar archivos y carpeta destino primero.")
        return
    modificados = []
    for archivo in archivos_seleccionados:
        nombre = os.path.basename(archivo)
        backup = os.path.join(carpeta_destino, nombre + ".bak")
        destino = os.path.join(carpeta_destino, nombre)
        shutil.copy2(archivo, backup)
        if procesar_archivo(archivo, destino):
            modificados.append(nombre)
    if modificados:
        messagebox.showinfo("Proceso terminado", f"Archivos modificados y respaldados:\n" + "\n".join(modificados))
    else:
        messagebox.showinfo("Sin cambios", "No se detectaron líneas para modificar en los archivos seleccionados.")

def seleccionar_archivos():
    global archivos_seleccionados, carpeta_destino
    archivos = filedialog.askopenfilenames(title="Selecciona archivos G-code", filetypes=[("G-code","*.gcode *.nc *.cnc *.tap"), ("Todos","*.*")])
    if not archivos:
        return
    carpeta = filedialog.askdirectory(title="Selecciona carpeta destino para archivos modificados")
    if not carpeta:
        return
    archivos_seleccionados = archivos
    carpeta_destino = carpeta
    messagebox.showinfo("Listo", f"Archivos y carpeta destino seleccionados. Ahora puedes ejecutar el proceso.")

root = tk.Tk()
root.title("Editor de G-code: Temperatura de cama")
root.geometry("400x200")

label = tk.Label(root, text="Selecciona archivos G-code para modificar la temperatura de cama a 110°C.\nSe hará backup en la carpeta destino.", wraplength=380)
label.pack(pady=20)

btn = tk.Button(root, text="Seleccionar archivos y carpeta destino", command=seleccionar_archivos)
btn.pack(pady=20)

btn_ejecutar = tk.Button(root, text="Ejecutar", command=ejecutar_proceso)
btn_ejecutar.pack(pady=10)

root.mainloop()
