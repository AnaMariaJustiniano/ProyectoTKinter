#importación de librerías
import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime
#crear ventana principal
ventana_principal = tk.Tk()
#titutlo de la ventana
ventana_principal.title("Libro de Pacientes y Doctores")
#tamaño de la ventana
ventana_principal.geometry("400x600")

#Crear pestaña Notebook
pestaña = ttk.Notebook(ventana_principal)

#Crear frames para opciones de menú
frame_pacientes = ttk.Frame(pestaña)

#declarar variables
nombreP=tk.StringVar()
genero=tk.StringVar()
edadP=tk.StringVar()
tipo_seguro=tk.StringVar()
centro_medico=tk.StringVar()
grupo_sanguineo=tk.StringVar()

def enmascar_fecha(texto):
    limpio = ''.join(filter(str.isdigit, texto))
    formato_final=""
    
    if len(limpio) >8:
        limpio = limpio[:8]
    if len(limpio) > 4:
        formato_final = f"{limpio[:2]}-{limpio[2:4]}-{limpio[4:]}"
    elif len(limpio) > 2:
        formato_final = f"{limpio[:2]}-{limpio[2:]}"
    else:
        formato_final = limpio  
    
    if entry_fecha.get() != formato_final:
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, formato_final)
        
    if len(entry_fecha.get()) == 10:
        fecha_actual = datetime.now().date()
        fecha_nacimiento = datetime.strptime(entry_fecha.get(), "%d-%m-%Y").date()
        edad=fecha_actual.year - fecha_nacimiento.year 
        edadP.set(edad)
    return True
def cargar_lista_centros(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea_limpia = linea.strip()
                if linea_limpia: # Verifica que la línea no esté vacía
                    datos.append(linea_limpia)
    except FileNotFoundError:
        messagebox.showerror("Error", f"El archivo: '{nombre_archivo}'")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrio un error al leer el archivo: {e}")
    return datos
def registrar():
    print("Nombre Paciente:", nombreP.get()+"\nFecha de Nacimiento:" + entry_fecha.get() +"\nEdad:"+ edadP.get() + "Años"+"\nGénero:"+ genero.get()+ "\nGrupo Sanguineo: "+grupo_sanguineo.get()+"\nTipo de seguro"+tipo_seguro.get()+"\nCentro de salud: "+centro_medico.get()) #cargar centros de salud desde un txt
ruta_archivo = "centros.txt"
centros_combobox=cargar_lista_centros(ruta_archivo)
def registrar_paciente():
    try:
        with open("registro_paciente.txt", "a") as archivo:
            archivo.write(nombreP.get().title()+"\n")
            archivo.write(entry_fecha.get()+"\n")
            archivo.write(edadP.get()+"\n")
            archivo.write(genero.get()+"\n")
            archivo.write(grupo_sanguineo.get()+"\n")
            archivo.write(tipo_seguro.get()+"\n")
            archivo.write(centro_medico.get()+"\n")
        cargar_treeview()
        print("Datos registrados exitosamente.")
    except IOError as e:
        print(f"error al escribir en el archivo: {e}")

def lista_pacientes(nombre_archivo):   
    list_paciente=[] 
    try:
        with open(nombre_archivo, 'r', encoding="utf-8") as archivo:
            lines = archivo.readlines() 
            for i in range(0, len(lines), 7):
                if i+6 < len(lines):
                    paciente = {
                        "Nombre": lines[i].strip(),
                        "Fecha Nacimiento": lines[i+1].strip(),
                        "Edad": lines[i+2].strip(),
                        "Genero": lines[i+3].strip(),
                        "Tipo sangre":lines[i+4].strip(),
                        "Seguro":lines[i+5].strip(),
                        "Hospital":lines[i+6].strip()
                    }
                    list_paciente.append(paciente)
    except FileNotFoundError:
        print(f"Error: El archivo '{lista_pacientes}' no fue encontrado")   
    return list_paciente
def cargar_treeview():
    lista = lista_pacientes("registro_paciente.txt")
    for paciente in treeview.get_children():
        treeview.delete(paciente)
        
    for item in lista:
        treeview.insert("","end",values=(
        item["Nombre"],item["Fecha Nacimiento"],item["Edad"], item["Genero"],
        item["Tipo sangre"],item["Seguro"],item["Hospital"]
    ))
#asignar valores a variables
genero.set("M")  # Valor por defecto para género
tipo_seguro.set("Seleccionar una opcion")  # Valor por defecto para tipo de seguro
centro_medico.set("Seleccionar un centro de salud")  # Valor por defecto para centro médico
#asignar los frame a la pestaña
pestaña.add(frame_pacientes, text="Pacientes")
pestaña.pack(expand=True, fill="both")


#crear contenido dentro de la pestaña de pacientes

tk.Label(frame_pacientes, text="Nombre Completo:").pack(anchor="w", pady=10)
tk.Entry(frame_pacientes, textvariable=nombreP).pack(anchor="w")

tk.Label(frame_pacientes, text="Fecha de Nacimiento:").pack(anchor="w")
vcmd=ventana_principal.register(enmascar_fecha)

entry_fecha = ttk.Entry(frame_pacientes,validate="key",validatecommand=(vcmd, '%P'))
entry_fecha.pack(anchor="w")

tk.Label(frame_pacientes, text="Edad:").pack(anchor="w")
tk.Entry(frame_pacientes, textvariable=edadP, state="readonly").pack(anchor="w")


tk.Label(frame_pacientes, text="Género:").pack(anchor="w")
contenedorGenero=tk.Frame(frame_pacientes)
contenedorGenero.pack(anchor="w")
ttk.Radiobutton(contenedorGenero, text="Masculino", variable=genero, value="M").pack(side="left")
ttk.Radiobutton(contenedorGenero, text="Femenino", variable=genero, value="F").pack(side="left")

tk.Label(frame_pacientes, text="Grupo Sanguineo:").pack(anchor="w")
tk.Entry(frame_pacientes, textvariable=grupo_sanguineo).pack(anchor="w")

tk.Label(frame_pacientes, text="Tipo de Seguro:").pack(anchor="w")
ttk.Combobox(frame_pacientes, textvariable=tipo_seguro, values=["Público", "Privado", "Ninguno"]).pack(anchor="w")

tk.Label(frame_pacientes, text="Centro de salud:").pack(anchor="w")
ttk.Combobox(frame_pacientes, values=centros_combobox, textvariable=centro_medico).pack(anchor="w") 

tk.Button(frame_pacientes, text="Registrar", command=registrar_paciente).pack(pady=10)  

#Crear Treeview
global treeview
#Crear TreeView para mostrar pacientes
treeview=ttk.Treeview(frame_pacientes, columns=("Nombre", "FechaN", "Edad", "Genero", "GrupoS", "TipoS", "CentroM"), show="headings")
treeview.heading("Nombre", text="Nombre Completo")
treeview.heading("FechaN", text="Fecha Nacimiento")
treeview.heading("Edad", text="Edad")
treeview.heading("Genero", text="Genero")
treeview.heading("GrupoS", text="Grupo Sanguineo")
treeview.heading("TipoS", text="Tipo sangre")
treeview.heading("CentroM", text="Centro Médico")
cargar_treeview()


#para una posición dentro de la ventana_principal


# Crear Scrollbar para el TreeView o barra lateral
scrollbarV = ttk.Scrollbar(frame_pacientes, orient="vertical", command=treeview.yview)
scrollbarV.pack(side="right", fill="y")
treeview.configure(yscrollcommand=scrollbarV.set)
treeview.pack(side="top", fill="both", expand=True)
ventana_principal.mainloop()
