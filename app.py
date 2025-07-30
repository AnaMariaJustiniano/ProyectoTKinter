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
#variables para la función editar
entry_editor = None
item_actual=None
id_columna_actual=None
paciente_data=[]
global treeview
treeview_columna_key={
    "Nombre": "Nombre",
    "FechaN":"Fecha de Nacimiento",
    "Edad":"Edad",
    "Genero":"Genero",
    "GrupoS":"Tipo de Sangre",
    "TipoS":"Seguro",
    "CentroM":"Hospital"
    
}

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

def registrar_paciente():
    try:
        with open("registro_pacientes.txt", "a", encoding="utf-8") as archivo:
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
                        "Fecha de Nacimiento": lines[i+1].strip(),
                        "Edad": lines[i+2].strip(),
                        "Genero": lines[i+3].strip(),
                        "Tipo de Sangre":lines[i+4].strip(),
                        "Seguro":lines[i+5].strip(),
                        "Hospital":lines[i+6].strip()
                    }
                    list_paciente.append(paciente)
    except FileNotFoundError:
        print(f"Error: El archivo '{lista_pacientes}' no fue encontrado")   
    return list_paciente
def cargar_treeview():
    global paciente_data
    paciente_data = lista_pacientes("registro_pacientes.txt")
    for paciente in treeview.get_children():
        treeview.delete(paciente)
        
    for i,item in enumerate(paciente_data):
        treeview.insert("","end",iid=str(i),values=(
        item["Nombre"],item["Fecha de Nacimiento"],item["Edad"], item["Genero"],
        item["Tipo de Sangre"],item["Seguro"],item["Hospital"]
    ))
#asignar valores a variables
def clic_izquierdo(event):
    global entry_editor
    item=treeview.identify_row(event.y)
    id_columna=treeview.identify_column(event.x)
    
    if item and id_columna:
        if entry_editor:
            guardar_destruir_entry_editar()
        editar_celda(item, id_columna)

def doble_click_izquierdo(event):
    clic_izquierdo(event)
    
def editar_celda(id_item, id_columna):
    
    global entry_editor, item_actual, id_columna_actual, treeview_columna_key
    x,y,width, height=treeview.bbox(id_item, id_columna)
    
    treeview_nombre_columna=treeview.column(id_columna,option="id")
    diccionario_key=treeview_columna_key.get(treeview_nombre_columna)
    
    if not diccionario_key:
        return 
    if diccionario_key=="Edad":
        messagebox.showinfo("Informacion","La edad se calcula automaticamente. Edite la fecha de nacimiento para cambiarla.")
        return
    #obtener el valor actual de la celda
    valor_actual=treeview.set(id_item,treeview_nombre_columna)
    item_actual=id_item
    id_columna_actual=diccionario_key
    
    entry_editor=ttk.Entry(treeview)
    entry_editor.place(x=x, y=y, width=width, height=height)
    entry_editor.insert(0,valor_actual)
    entry_editor.focus_set()
    
    entry_editor.bind("<FocusOut>",entry_foco)
    entry_editor.bind("<Return>",presionar_enter)

def entry_foco(event=None):
    guardar_destruir_entry_editar()
    
def presionar_enter(event=None):
    guardar_destruir_entry_editar()
        
def guardar_destruir_entry_editar():
    global entry_editor, item_actual, id_columna_actual, paciente_data, treeview
    if entry_editor and item_actual is not None and id_columna_actual:
        nuevo_valor=entry_editor.get()
        
        if id_columna_actual=="Fecha de Nacimiento":
            try:
                datetime.strptime(nuevo_valor, '%d-%m-%Y')
            except ValueError:
                messagebox.showerror("Error de Edicion","Formato de fecha invalido. Use DD-MM-AAAA.")
                entry_editor.destroy()
                entry_editor=None
                item_actual=None
                id_columna_actual=None
                return
        paciente_index = int(item_actual)
        if 0 <=paciente_index<len(paciente_data):
            paciente_data[paciente_index][id_columna_actual]=nuevo_valor
            
            if id_columna_actual=="Fecha de Nacimiento":
                try:
                    fecha_actual=datetime.now().date()
                    fecha_nacimiento=datetime.strptime(nuevo_valor,'%d-%m-%Y').date()
                    edad=fecha_actual.year-fecha_nacimiento.year
                    if fecha_actual<datetime(fecha_actual.year, fecha_nacimiento.month, fecha_nacimiento.day).date():
                        edad-=1
                    paciente_data[paciente_index]["Edad"]=str(edad)
                except ValueError:
                    paciente_data[paciente_index]["Edad"]="Fecha Inválida"
                    messagebox.showerror("Error de Edicion","La fecha de nacimiento editada no es válida")
            actualizar_valor =tuple(paciente_data[paciente_index].values())
            treeview.item(item_actual, values=actualizar_valor)
            actualizar_lista_archivo()
        
        
        entry_editor.destroy()
        entry_editor=None
        item_actual=None
        id_columna_actual=None
        
def actualizar_lista_archivo():
    global paciente_data
    try:
        with open("registro_pacientes.txt", "w", encoding="utf-8") as archivo:
            for paciente in paciente_data:
                archivo.write(paciente["Nombre"]+"\n")   
                archivo.write(paciente["Fecha de Nacimiento"]+"\n")
                archivo.write(paciente["Edad"]+"\n") 
                archivo.write(paciente["Genero"]+"\n")
                archivo.write(paciente["Tipo de Sangre"]+"\n")
                archivo.write(paciente["Seguro"]+"\n")
                archivo.write(paciente["Hospital"]+"\n")
    except IOError as e:
        messagebox.showerror("Error de Archivo", f"Error al actualizar el archivo de pacientes: {e}")
def eliminar_paciente():
    global paciente_data, treeview
    seleccionr_items = treeview.selection()
    if not seleccionr_items:
        messagebox.showwarning("Eliminar Paciente","Por favor seleccionar un registro de paciente a eliminar")
        return
    id_item_eliminado=seleccionr_items[0]
    paciente_index=int(id_item_eliminado)
    
    if messagebox.askyesno("Confirmar Eliminacion",f"?Está segurode eliminar el registro seleccionado?\n"
                           f"Paciente: {paciente_data[paciente_index]["Nombre"]}"):
        del paciente_data[paciente_index]
        actualizar_lista_archivo()
        cargar_treeview()
        messagebox.showinfo("Eliminar Paciente","Registro eliminado exitosamente.")
    else:
        messagebox.showinfo("Eliminar Paciente","Eliminacion cancelada")                    
ruta_archivo = "centros.txt"
centros_combobox=cargar_lista_centros(ruta_archivo)                
                
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
tk.Button(frame_pacientes, text="Eliminar", command=eliminar_paciente).pack(pady=10)  

#Crear Treeview

#Crear TreeView para mostrar pacientes
treeview=ttk.Treeview(frame_pacientes, columns=("Nombre", "FechaN", "Edad", "Genero", "GrupoS", "TipoS", "CentroM"), show="headings")
treeview.heading("Nombre", text="Nombre Completo")
treeview.heading("FechaN", text="Fecha Nacimiento")
treeview.heading("Edad", text="Edad")
treeview.heading("Genero", text="Genero")
treeview.heading("GrupoS", text="Grupo Sanguineo")
treeview.heading("TipoS", text="Tipo sangre")
treeview.heading("CentroM", text="Centro Médico")

treeview.column("Nombre", width=120)
treeview.column("FechaN", width=190)
treeview.column("Edad", width=50)
treeview.column("Genero", width=60)
treeview.column("GrupoS", width=80)
treeview.column("TipoS", width=80)
treeview.column("CentroM", width=100)

treeview.bind("<Double-1>", doble_click_izquierdo)
cargar_treeview()


#para una posición dentro de la ventana_principal


# Crear Scrollbar para el TreeView o barra lateral
scrollbarV = ttk.Scrollbar(frame_pacientes, orient="vertical", command=treeview.yview)
scrollbarV.pack(side="right", fill="y")
treeview.configure(yscrollcommand=scrollbarV.set)
treeview.pack(side="top", fill="both", expand=True)
ventana_principal.mainloop()
