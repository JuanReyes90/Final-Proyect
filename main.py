import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os

archivo = "estudiantes.txt"



def cargar_estudiantes():
    estudiantes = {}
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    matricula, nombre, notas = linea.split(":")
                    estudiantes[matricula] = {"nombre": nombre, "notas": list(map(float, notas.split(",")))}
    return estudiantes

def guardar_estudiantes(estudiantes):
    with open(archivo, "w") as f:
        for matricula, info in estudiantes.items():
            f.write(f"{matricula}:{info['nombre']}:{','.join(map(str, info['notas']))}\n")



def agregar_estudiante_gui():
    matricula = simpledialog.askstring("Matrícula", "Ingrese matrícula (4 dígitos):", parent=root)
    if matricula is None: return
    if not matricula.isdigit() or len(matricula) != 4:
        messagebox.showerror("Error", "La matrícula debe ser un número entero de 4 dígitos.", parent=root)
        return
    if matricula in estudiantes:
        messagebox.showerror("Error", f"La matrícula {matricula} ya está registrada.", parent=root)
        return

    nombre = simpledialog.askstring("Nombre", "Ingrese el nombre del estudiante:", parent=root)
    if nombre is None: return
    if not nombre.replace(" ", "").isalpha():
        messagebox.showerror("Error", "El nombre solo puede contener letras.", parent=root)
        return
    if len(nombre) > 50:
        messagebox.showerror("Error", "El nombre no puede tener más de 50 caracteres.", parent=root)
        return

  
    notas_ventana = tk.Toplevel(root)
    notas_ventana.title("Ingresar Notas")
    notas_ventana.geometry("300x200")
    notas_ventana.resizable(False, False)

    tk.Label(notas_ventana, text="Nota 1 (1er Periodo):").pack(pady=5)
    entry_nota1 = tk.Entry(notas_ventana)
    entry_nota1.pack()

    tk.Label(notas_ventana, text="Nota 2 (2do Periodo):").pack(pady=5)
    entry_nota2 = tk.Entry(notas_ventana)
    entry_nota2.pack()

    tk.Label(notas_ventana, text="Nota 3 (3er Periodo):").pack(pady=5)
    entry_nota3 = tk.Entry(notas_ventana)
    entry_nota3.pack()

    def guardar_notas():
        lista_notas = []
        for e in [entry_nota1, entry_nota2, entry_nota3]:
            n = e.get()
            try:
                n_float = float(n)
            except ValueError:
                messagebox.showerror("Error", f"'{n}' no es un número válido.", parent=notas_ventana)
                return
            if not (1 <= n_float <= 100):
                messagebox.showerror("Error", "Las notas deben estar entre 1 y 100.", parent=notas_ventana)
                return
            lista_notas.append(n_float)

        estudiantes[matricula] = {"nombre": nombre, "notas": lista_notas}
        guardar_estudiantes(estudiantes)
        promedio = int(round(sum(lista_notas) / len(lista_notas)))
        messagebox.showinfo("Estudiante agregado", f"{nombre} agregado con éxito.\nPromedio = {promedio}", parent=root)
        notas_ventana.destroy()

    tk.Button(notas_ventana, text="Aceptar", command=guardar_notas).pack(pady=15)

def mostrar_estudiantes_gui():
    if not estudiantes:
        messagebox.showinfo("Estudiantes", "No hay estudiantes registrados.", parent=root)
        return

    ventana = tk.Toplevel(root)
    ventana.title("GADE - Lista de Estudiantes")
    ventana.geometry("800x450")
    ventana.resizable(False, False)
    ventana.configure(bg="#ffffff")

    frame = ttk.LabelFrame(ventana, text="Lista de Estudiantes", padding=10)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("Matrícula", "Nombre", "Notas", "Promedio")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=15)
    tabla.pack(fill="both", expand=True)

    tabla.heading("Matrícula", text="Matrícula")
    tabla.column("Matrícula", width=120, anchor="center")
    tabla.heading("Nombre", text="Nombre")
    tabla.column("Nombre", width=220, anchor="center")
    tabla.heading("Notas", text="Notas")
    tabla.column("Notas", width=300, anchor="center")
    tabla.heading("Promedio", text="Promedio")
    tabla.column("Promedio", width=120, anchor="center")

    for matricula, info in estudiantes.items():
        notas_str = ", ".join(str(int(n)) for n in info['notas'])
        promedio = int(round(sum(info['notas']) / len(info['notas'])))
        tabla.insert("", "end", values=(matricula, info['nombre'], notas_str, promedio))

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

def borrar_estudiante_gui():
    if not estudiantes:
        messagebox.showinfo("Estudiantes", "No hay estudiantes registrados.", parent=root)
        return
    ventana = tk.Toplevel(root)
    ventana.title("GADE - Borrar Estudiante")
    ventana.geometry("600x400")
    ventana.resizable(False, False)

    frame = ttk.LabelFrame(ventana, text="Estudiantes Registrados", padding=10)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    texto = tk.Text(frame, width=70, height=15, font=("Helvetica", 11))
    texto.pack(fill="both", expand=True)
    for matricula, info in estudiantes.items():
        texto.insert(tk.END, f"{matricula} - {info['nombre']}\n")
    texto.config(state="disabled")

    matricula_borrar = simpledialog.askstring("Borrar", "Ingrese la matrícula del estudiante a borrar:", parent=ventana)
    if matricula_borrar is None: return
    if matricula_borrar in estudiantes:
        nombre_borrar = estudiantes[matricula_borrar]['nombre']
        del estudiantes[matricula_borrar]
        guardar_estudiantes(estudiantes)
        messagebox.showinfo("Eliminado", f"Estudiante {nombre_borrar} eliminado con éxito.", parent=ventana)
    else:
        messagebox.showerror("Error", f"No se encontró la matrícula {matricula_borrar}.", parent=ventana)

def editar_estudiante_gui():
    if not estudiantes:
        messagebox.showinfo("Estudiantes", "No hay estudiantes registrados.", parent=root)
        return

    matricula = simpledialog.askstring("Editar Estudiante", "Ingrese la matrícula del estudiante:", parent=root)
    if matricula is None: return
    if matricula not in estudiantes:
        messagebox.showerror("Error", f"No se encontró la matrícula {matricula}.", parent=root)
        return

    estudiante = estudiantes[matricula]

   
    nuevo_nombre = simpledialog.askstring("Editar Nombre",
                                          f"Nombre actual: {estudiante['nombre']}\nIngrese nuevo nombre (o deje vacío para no cambiar):",
                                          parent=root)
    if nuevo_nombre:
        if not nuevo_nombre.replace(" ", "").isalpha():
            messagebox.showerror("Error", "El nombre solo puede contener letras.", parent=root)
            return
        if len(nuevo_nombre) > 50:
            messagebox.showerror("Error", "El nombre no puede tener más de 50 caracteres.", parent=root)
            return
        estudiante['nombre'] = nuevo_nombre


    notas_actuales = estudiante['notas']
    notas_ventana = tk.Toplevel(root)
    notas_ventana.title("Editar Notas")
    notas_ventana.geometry("300x200")
    notas_ventana.resizable(False, False)

    tk.Label(notas_ventana, text="Nota 1 (1-100):").pack(pady=5)
    entry_nota1 = tk.Entry(notas_ventana)
    entry_nota1.insert(0, str(int(notas_actuales[0])))
    entry_nota1.pack()

    tk.Label(notas_ventana, text="Nota 2 (1-100):").pack(pady=5)
    entry_nota2 = tk.Entry(notas_ventana)
    entry_nota2.insert(0, str(int(notas_actuales[1])))
    entry_nota2.pack()

    tk.Label(notas_ventana, text="Nota 3 (1-100):").pack(pady=5)
    entry_nota3 = tk.Entry(notas_ventana)
    entry_nota3.insert(0, str(int(notas_actuales[2])))
    entry_nota3.pack()

    def guardar_notas_edit():
        nueva_notas = []
        for e in [entry_nota1, entry_nota2, entry_nota3]:
            n = e.get()
            try:
                n_float = float(n)
            except ValueError:
                messagebox.showerror("Error", f"'{n}' no es un número válido.", parent=notas_ventana)
                return
            if not (1 <= n_float <= 100):
                messagebox.showerror("Error", "Las notas deben estar entre 1 y 100.", parent=notas_ventana)
                return
            nueva_notas.append(n_float)
        estudiante['notas'] = nueva_notas
        guardar_estudiantes(estudiantes)
        promedio = int(round(sum(estudiante['notas']) / len(estudiante['notas'])))
        messagebox.showinfo("Estudiante actualizado",
                            f"Estudiante {estudiante['nombre']} actualizado.\nPromedio = {promedio}",
                            parent=root)
        notas_ventana.destroy()

    tk.Button(notas_ventana, text="Aceptar", command=guardar_notas_edit).pack(pady=15)



root = tk.Tk()
root.title("GADE - Gestión Académica de Estudiantes")
root.geometry("600x550")
root.resizable(False, False)
root.configure(bg="#ffffff")


estudiantes = cargar_estudiantes()


frame_logo = tk.Frame(root, bg="#ffffff")
frame_logo.pack(pady=(20,10))

logo_sombra = tk.Label(frame_logo, text="GADE", font=("Helvetica", 34, "bold"), bg="#ffffff", fg="#aaaaaa")
logo_sombra.pack()

logo = tk.Label(frame_logo, text="GADE", font=("Helvetica", 32, "bold"), bg="#ffffff", fg="#4db6ac")
logo.place(x=0, y=-2)

subtitulo = tk.Label(root, text="Gestión Académica de Estudiantes", font=("Helvetica", 16), bg="#ffffff", fg="#333333")
subtitulo.pack(pady=(10,30))


def on_enter(e, color):
    e.widget['background'] = color

def on_leave(e, color):
    e.widget['background'] = color


botones_info = [
    ("Agregar estudiante", agregar_estudiante_gui, "#4db6ac", "#26a69a"),
    ("Ver estudiantes", mostrar_estudiantes_gui, "#81c784", "#43a047"),
    ("Editar estudiante", editar_estudiante_gui, "#64b5f6", "#1976d2"),
    ("Borrar estudiante", borrar_estudiante_gui, "#e57373", "#d32f2f"),
    ("Salir", root.quit, "#90a4ae", "#607d8b")
]

for texto, comando, color_base, color_hover in botones_info:
    btn = tk.Button(root, text=texto, command=comando, font=("Helvetica", 13, "bold"),
                    bg=color_base, fg="white", activebackground=color_hover, bd=0, relief="raised", height=2)
    btn.pack(fill="x", padx=80, pady=10)
    btn.bind("<Enter>", lambda e, c=color_hover: on_enter(e, c))
    btn.bind("<Leave>", lambda e, c=color_base: on_leave(e, c))

root.mainloop()
