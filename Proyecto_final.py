import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date, datetime
import urllib.request
import io
from PIL import Image, ImageTk

# Diccionario de configuración de la base de datos
# Aquí se guardan las credenciales para conectarse a tu base de datos MySQL.
# Recuerda reemplazar 'localhost', 'root' y '' con tu host, usuario y contraseña reales.
# 'recursos_humanos' es el nombre de tu base de datos.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "recursos_humanos"
}

# URL para la imagen del logo de la aplicación
# Esta URL apunta a una imagen alojada en línea que se utilizará como logo de la aplicación.
IMAGE_URL = "https://i.postimg.cc/HWFwDC49/logo-124x124.png"

def obtener_conexion():#Establece y devuelve una conexión a la base de datos MySQL.
    #Si la conexión falla, imprime un error y muestra un cuadro de mensaje.
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al obtener la conexión: {err}")
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}\n"
                                                    "Asegúrate de que MySQL esté corriendo y las credenciales sean correctas.")
        return None

class LoginApp:#Gestiona la interfaz de inicio de sesión del usuario y la autenticación.
    def __init__(self, master):#Inicializa la aplicación de inicio de sesión (LoginApp).

        #Args:
            #master (tk.Tk): La ventana raíz de Tkinter para la pantalla de inicio de sesión.
        self.master = master
        master.title("Gestionamientos")  # Establece el título de la ventana
        master.geometry("400x500")       # Establece el tamaño de la ventana
        master.resizable(False, False)   # Hace que la ventana no sea redimensionable

        self.center_window(master)  # Centra la ventana en la pantalla

        # Marco principal para contener los widgets de inicio de sesión
        main_frame = tk.Frame(master, padx=20, pady=20)
        main_frame.pack(expand=True)

        self.tk_logo_image = None
        # Intenta cargar la imagen del logo desde la URL
        try:
            with urllib.request.urlopen(IMAGE_URL) as u:
                raw_data = u.read()

            original_image = Image.open(io.BytesIO(raw_data))

            width = 150
            height = int(original_image.height * (width / original_image.width))
            resized_image = original_image.resize((width, height), Image.Resampling.LANCZOS)

            self.tk_logo_image = ImageTk.PhotoImage(resized_image)

            self.logo_label = tk.Label(main_frame, image=self.tk_logo_image)
            self.logo_label.pack(pady=(0, 10))

        except urllib.error.URLError as e:
            # Maneja errores de red o URLs inválidas al obtener la imagen
            messagebox.showwarning("Error de Conexión", f"No se pudo cargar la imagen desde la URL. Problema de red o URL inválida: {e.reason}\nSe usará texto en su lugar.")
            self.logo_label = tk.Label(main_frame, text="RRHH Corporation", font=("Segoe UI", 18, "bold"), fg="#000000")
            self.logo_label.pack(pady=(0, 10))
        except IOError as e:
            # Maneja errores durante el procesamiento de la imagen (por ejemplo, datos de imagen corruptos)
            messagebox.showwarning("Error de Imagen", f"No se pudo procesar la imagen de la URL: {e}\nSe usará texto en su lugar.")
            self.logo_label = tk.Label(main_frame, text="RRHH Corporation", font=("Segoe UI", 18, "bold"), fg="#000000")
            self.logo_label.pack(pady=(0, 10))
        except Exception as e:
            # Captura cualquier otro error inesperado durante la carga de la imagen
            messagebox.showerror("Error Inesperado", f"Ocurrió un error inesperado al cargar la imagen: {e}\nSe usará texto en su lugar.")
            self.logo_label = tk.Label(main_frame, text="RRHH Corporation", font=("Segoe UI", 18, "bold"), fg="#000000")
            self.logo_label.pack(pady=(0, 10))

        # Etiqueta de título para la pantalla de inicio de sesión
        self.title_label = tk.Label(main_frame, text="Bienvenido", font=("Segoe UI", 20, "bold"))
        self.title_label.pack(pady=(0, 15))

        # Entrada de nombre de usuario
        self.password_label = tk.Label(main_frame, text="Usuario:", font=("Segoe UI", 15))
        self.password_label.pack(pady=(10, 0), anchor="w")

        self.username_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=35, fg='grey')
        self.username_entry.insert(0, "Ingrese su usuario") # Texto de marcador de posición
        # Vincula eventos de enfoque para borrar/añadir texto de marcador de posición
        self.username_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, self.username_entry, "Ingrese su usuario"))
        self.username_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.username_entry, "Ingrese su usuario"))
        self.username_entry.pack(pady=5)

        # Entrada de contraseña
        self.password_label = tk.Label(main_frame, text="Contraseña:", font=("Segoe UI", 15))
        self.password_label.pack(pady=(10, 0), anchor="w")

        self.password_entry = tk.Entry(main_frame, font=("Segoe UI", 12), show='', width=35, fg='grey')
        self.password_entry.insert(0, "Ingrese su contraseña") # Texto de marcador de posición
        # Vincula eventos de enfoque para borrar/añadir texto de marcador de posición y manejar el enmascaramiento de contraseña
        self.password_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, self.password_entry, "Ingrese su contraseña", is_password=True))
        self.password_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.password_entry, "Ingrese su contraseña", is_password=True))
        self.password_entry.pack(pady=(0, 20))

        # Botón de inicio de sesión
        self.login_button = tk.Button(main_frame, text="Iniciar Sesión", font=("Segoe UI", 12, "bold"), bg="#3D3D3D", fg="white", width=18, command=self.attempt_login)
        self.login_button.pack(pady=10)

        # Vincula la tecla Enter al intento de inicio de sesión
        master.bind('<Return>', lambda event=None: self.attempt_login())

    def center_window(self, window):#Centra la ventana de Tkinter dada en la pantalla.

        #Args:
            #window (tk.Tk o tk.Toplevel): La ventana a centrar.
        window.update_idletasks() # Asegura que las dimensiones de la ventana se calculen
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def clear_placeholder(self, event, entry_widget, default_text, is_password=False):#Borra el texto de marcador de posición de un widget Entry cuando este obtiene el foco.
        #Si es un campo de contraseña, también habilita el enmascaramiento de caracteres.

        #Args:
            #event: El evento que activó la función (por ejemplo, FocusIn).
            #entry_widget (tk.Entry): El widget Entry a borrar.
            #default_text (str): El texto del marcador de posición.
            #is_password (bool): True si la entrada es para una contraseña, False en caso contrario.
        if entry_widget.get() == default_text:
            entry_widget.delete(0, tk.END)
            entry_widget.config(fg='black') # Cambia el color del texto a negro
            if is_password:
                entry_widget.config(show='*') # Enmascara los caracteres para la contraseña

    def add_placeholder(self, event, entry_widget, default_text, is_password=False):#Añade texto de marcador de posición a un widget Entry si está vacío cuando pierde el foco.
        #Si es un campo de contraseña, elimina el enmascaramiento de caracteres.
        #Args:
            #event: El evento que activó la función (por ejemplo, FocusOut).
            #entry_widget (tk.Entry): El widget Entry al que se le añadirá el marcador de posición.
            #default_text (str): El texto del marcador de posición.
            #is_password (bool): True si la entrada es para una contraseña, False en caso contrario.
        if not entry_widget.get():
            entry_widget.insert(0, default_text)
            entry_widget.config(fg='grey') # Cambia el color del texto a gris
            if is_password:
                entry_widget.config(show='') # Elimina el enmascaramiento para la contraseña
            else:
                entry_widget.config(show='') # Asegura que no haya enmascaramiento para campos que no son de contraseña


    def attempt_login(self):
        username = self.username_entry.get() # Esto es el 'username' que el usuario ingresa
        password = self.password_entry.get()

        # Validación de entrada para campos vacíos
        if username == "Ingrese su usuario" or not username:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese su nombre de usuario.")
            return
        if password == "Ingrese su contraseña" or not password:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese su contraseña.")
            return

        conexion = obtener_conexion()
        if conexion is None:
            return # Sale si la conexión a la base de datos falló

        cursor = None
        user_info = None
        try:
            cursor = conexion.cursor(dictionary=True) # El cursor devuelve filas como diccionarios
            sql = "SELECT id, nombre, apellido, puesto, salario, fecha_ingreso, username, password FROM empleados WHERE username = %s"
            cursor.execute(sql, (username,)) # Ahora pasamos 'username' al execute
            user_info = cursor.fetchone() # Obtiene una sola fila

            # Comprueba si el usuario existe y si la contraseña coincide
            if user_info and user_info['password'] == password: # Usa la columna 'password' de la DB
                full_name_for_welcome = f"{user_info['nombre']} {user_info['apellido']}" if 'apellido' in user_info else user_info['nombre']
                messagebox.showinfo("Bienvenido", f"¡Bienvenido, {full_name_for_welcome}!")
                self.master.destroy()  # Cierra la ventana de inicio de sesión
                root_main = tk.Tk()    # Crea una nueva raíz de Tkinter para la aplicación principal
                MainApp(root_main, full_name_for_welcome) # Inicializa MainApp con el nombre adecuado
                root_main.mainloop()   # Inicia el bucle de eventos de la aplicación principal
            else:
                messagebox.showerror("Error de Credenciales", "Nombre de usuario o contraseña incorrectos.")

        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error al verificar credenciales: {e}")
        finally:
            # Cierra el cursor y la conexión
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()


class MainApp:#Representa la aplicación principal para la gestión de Recursos Humanos.
    #Permite a los usuarios ver, añadir, actualizar y eliminar registros de empleados.
    def __init__(self, master, user_full_name):
        """
        Inicializa la aplicación principal (MainApp).

        Args:
            master (tk.Tk): La ventana raíz de Tkinter para la aplicación principal.
            user_full_name (str): El nombre completo del usuario que ha iniciado sesión.
        """
        self.master = master
        master.title("Sistema de Gestión de Recursos Humanos")
        master.geometry("900x700")
        self.user_full_name = user_full_name
        self.selected_empleado_id = None  # Almacena el ID del empleado actualmente seleccionado

        # Mensaje de bienvenida para el usuario que ha iniciado sesión
        self.welcome_label = tk.Label(master, text=f"Bienvenido, {self.user_full_name}", font=("Arial", 14, "bold"), fg="#0078D4")
        self.welcome_label.pack(pady=(10, 5))

        # Marco para mostrar la lista de empleados
        frame_lista = tk.LabelFrame(master, text="Lista de Empleados", font=("Arial", 12, "bold"))
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Listbox para mostrar los registros de empleados
        self.lista = tk.Listbox(frame_lista, font=("Consolas", 10))
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Barra de desplazamiento para el Listbox
        self.scrollbar_lista = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista.yview)
        self.scrollbar_lista.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista.config(yscrollcommand=self.scrollbar_lista.set)

        # Vincula el evento de selección del Listbox al método seleccionar_empleado
        self.lista.bind('<<ListboxSelect>>', self.seleccionar_empleado)

        # Marco para los campos de entrada de datos del empleado
        frame_datos = tk.LabelFrame(master, text="Datos del Empleado", font=("Arial", 12, "bold"))
        frame_datos.pack(fill=tk.X, padx=10, pady=5)

        input_frame = tk.Frame(frame_datos)
        input_frame.pack(pady=5)

        # Etiquetas y widgets Entry para los datos del empleado
        labels = ["ID:", "Nombre:", "Apellido:", "Puesto:", "Salario:", "Fecha Ingreso (YYYY-MM-DD):"]
        self.entries = {} # Diccionario para almacenar los widgets Entry para un fácil acceso
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text, font=("Arial", 10)).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            if text == "ID:":
                # La entrada de ID es de solo lectura ya que es autogenerada por la base de datos
                self.entry_id = tk.Entry(input_frame, font=("Arial", 10), width=30, state='readonly')
                self.entry_id.grid(row=i, column=1, padx=5, pady=2)
                self.entries['id'] = self.entry_id
            else:
                entry = tk.Entry(input_frame, font=("Arial", 10), width=30)
                entry.grid(row=i, column=1, padx=5, pady=2)
                # Almacena los widgets de entrada con claves estandarizadas (por ejemplo, 'nombre', 'salario')
                # La clave para "Fecha Ingreso (YYYY-MM-DD):" será 'fecha_ingreso_yyyy-mm-dd'
                self.entries[text.replace(":", "").replace(" ", "_").replace("(", "").replace(")", "").lower()] = entry

        # Marco para los botones de acción
        frame_botones = tk.Frame(master)
        frame_botones.pack(pady=10)

        # Botones para gestionar empleados
        self.btn_cargar = tk.Button(frame_botones, text="Cargar Empleados", font=("Arial", 10), command=self.cargar_empleados)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        self.btn_agregar = tk.Button(frame_botones, text="Registrar Empleado", font=("Arial", 10), command=self.agregar_empleado)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_actualizar = tk.Button(frame_botones, text="Editar Empleado", font=("Arial", 10), command=self.actualizar_empleado)
        self.btn_actualizar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = tk.Button(frame_botones, text="Borrar Empleado", font=("Arial", 10), command=self.eliminar_empleado)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        self.btn_limpiar = tk.Button(frame_botones, text="Limpiar Campos", font=("Arial", 10), command=self.limpiar_campos)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Carga los empleados cuando se inicia la aplicación principal
        self.cargar_empleados()

    def cargar_empleados(self):
        """
        Obtiene todos los registros de empleados de la base de datos y los muestra en el Listbox.
        """
        conexion = obtener_conexion()
        if conexion is None:
            return

        cursor = None
        try:
            cursor = conexion.cursor(dictionary=True) # Obtener filas como diccionarios
            cursor.execute("SELECT id, nombre, apellido, puesto, salario, fecha_ingreso FROM empleados ORDER BY id ASC")
            registros = cursor.fetchall()

            self.lista.delete(0, tk.END) # Borra las entradas existentes del listbox

            # Inserta cada registro de empleado en el Listbox
            for emp in registros:
                # Formatea la fecha a cadena para la visualización
                fecha_str = emp['fecha_ingreso'].strftime("%Y-%m-%d") if isinstance(emp['fecha_ingreso'], date) else str(emp['fecha_ingreso'])
                self.lista.insert(tk.END,
                                  f"ID: {emp['id']:<4} | {emp['nombre']:<15} | {emp['apellido']:<15} | {emp['puesto']:<15} | ${emp['salario']:.2f} | {fecha_str}")

        except Exception as e:
            messagebox.showerror("Error al cargar empleados", f"Ocurrió un error al cargar los datos: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    def seleccionar_empleado(self, event):
        """
        Maneja la selección de un empleado del Listbox.
        Rellena los campos de entrada con los datos del empleado seleccionado.

        Args:
            event: El evento que activó la función (ListboxSelect).
        """
        try:
            selected_index = self.lista.curselection()[0] # Obtiene el índice del elemento seleccionado
            selected_item_text = self.lista.get(selected_index) # Obtiene el texto del elemento seleccionado

            # Extrae el ID del empleado de la cadena formateada
            id_start_idx = selected_item_text.find("ID: ") + 4
            id_end_idx = selected_item_text.find(" |", id_start_idx)
            empleado_id = int(selected_item_text[id_start_idx:id_end_idx])

            conexion = obtener_conexion()
            if conexion is None:
                return

            cursor = None
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT id, nombre, apellido, puesto, salario, fecha_ingreso FROM empleados WHERE id = %s", (empleado_id,))
                empleado_data = cursor.fetchone()

                if empleado_data:
                    # Habilita y rellena la entrada de ID
                    self.entries['id'].config(state='normal')
                    self.entries['id'].delete(0, tk.END)
                    self.entries['id'].insert(0, str(empleado_data['id']))
                    self.entries['id'].config(state='readonly') # Vuelve a dejarlo como solo lectura

                    # Rellena otros campos de entrada
                    self.entries['nombre'].delete(0, tk.END)
                    self.entries['nombre'].insert(0, empleado_data['nombre'])

                    self.entries['apellido'].delete(0, tk.END)
                    self.entries['apellido'].insert(0, empleado_data['apellido'])

                    self.entries['puesto'].delete(0, tk.END)
                    self.entries['puesto'].insert(0, empleado_data['puesto'])

                    self.entries['salario'].delete(0, tk.END)
                    self.entries['salario'].insert(0, str(empleado_data['salario']))

                    # *** CORRECCIÓN AQUÍ: Usar la clave correcta para fecha_ingreso ***
                    self.entries['fecha_ingreso_yyyy-mm-dd'].delete(0, tk.END)
                    fecha_str = empleado_data['fecha_ingreso'].strftime("%Y-%m-%d") if isinstance(empleado_data['fecha_ingreso'], date) else str(empleado_data['fecha_ingreso'])
                    self.entries['fecha_ingreso_yyyy-mm-dd'].insert(0, fecha_str)

                    self.selected_empleado_id = empleado_data['id'] # Almacena el ID del empleado seleccionado
                else:
                    self.selected_empleado_id = None

            except Exception as e:
                messagebox.showerror("Error al seleccionar empleado", f"Ocurrió un error: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conexion and conexion.is_connected():
                    conexion.close()

        except IndexError:
            # Maneja el caso en que no se selecciona ningún elemento (por ejemplo, al hacer clic en un espacio vacío)
            self.selected_empleado_id = None
            self.limpiar_campos() # Limpia los campos si no hay nada seleccionado

    def agregar_empleado(self):#Añade un nuevo registro de empleado a la base de datos utilizando los datos de los campos de entrada.
        #Realiza la validación de entrada y maneja las operaciones de la base de datos.
        nombre = self.entries['nombre'].get()
        apellido = self.entries['apellido'].get()
        puesto = self.entries['puesto'].get()
        salario_str = self.entries['salario'].get()
        # *** CORRECCIÓN AQUÍ: Usar la clave correcta para fecha_ingreso ***
        fecha_ingreso_str = self.entries['fecha_ingreso_yyyy-mm-dd'].get()

        # Validación de entrada para campos vacíos
        if not (nombre and apellido and puesto and salario_str and fecha_ingreso_str):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        # Validación del tipo de datos
        try:
            salario = float(salario_str)
            fecha_ingreso = datetime.strptime(fecha_ingreso_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error de Formato", "Salario debe ser un número y Fecha de Ingreso debe tener formato YYYY-MM-DD.")
            return

        conexion = obtener_conexion()
        if conexion is None:
            return

        cursor = None
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO empleados (nombre, apellido, puesto, salario, fecha_ingreso) VALUES (%s, %s, %s, %s, %s)"
            values = (nombre, apellido, puesto, salario, fecha_ingreso)
            cursor.execute(sql, values)
            conexion.commit() # Confirma los cambios en la base de datos
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
            self.limpiar_campos()    # Limpia los campos de entrada
            self.cargar_empleados()  # Vuelve a cargar la lista de empleados
        except Exception as e:
            messagebox.showerror("Error al agregar empleado", f"Ocurrió un error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    def actualizar_empleado(self):#Actualiza un registro de empleado existente en la base de datos utilizando los datos de los campos de entrada.
        #Requiere que un empleado esté seleccionado de la lista.
        if self.selected_empleado_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un empleado de la lista para actualizar.")
            return

        id_empleado = self.selected_empleado_id
        nombre = self.entries['nombre'].get()
        apellido = self.entries['apellido'].get()
        puesto = self.entries['puesto'].get()
        salario_str = self.entries['salario'].get()
        # *** CORRECCIÓN AQUÍ: Usar la clave correcta para fecha_ingreso ***
        fecha_ingreso_str = self.entries['fecha_ingreso_yyyy-mm-dd'].get()

        # Validación de entrada para campos vacíos
        if not (nombre and apellido and puesto and salario_str and fecha_ingreso_str):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        # Validación del tipo de datos
        try:
            salario = float(salario_str)
            fecha_ingreso = datetime.strptime(fecha_ingreso_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error de Formato", "Salario debe ser un número y Fecha de Ingreso debe tener formato YYYY-MM-DD.")
            return

        conexion = obtener_conexion()
        if conexion is None:
            return

        cursor = None
        try:
            cursor = conexion.cursor()
            sql = """
            UPDATE empleados
            SET nombre = %s, apellido = %s, puesto = %s, salario = %s, fecha_ingreso = %s
            WHERE id = %s
            """
            values = (nombre, apellido, puesto, salario, fecha_ingreso, id_empleado)
            cursor.execute(sql, values)
            conexion.commit()
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")
            self.limpiar_campos()    # Limpia los campos de entrada
            self.cargar_empleados()  # Vuelve a cargar la lista de empleados
            self.selected_empleado_id = None # Deselecciona el empleado después de la actualización
        except Exception as e:
            messagebox.showerror("Error al actualizar empleado", f"Ocurrió un error: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()


    def eliminar_empleado(self): #Elimina un registro de empleado seleccionado de la base de datos.
        #Requiere confirmación del usuario antes de la eliminación.
        if self.selected_empleado_id is None:
            messagebox.showwarning("Advertencia", "Seleccione un empleado de la lista para eliminar.")
            return

        id_empleado = self.selected_empleado_id

        # Pide confirmación antes de eliminar
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar al empleado con ID {id_empleado}?"):
            conexion = obtener_conexion()
            if conexion is None:
                return

            cursor = None
            try:
                cursor = conexion.cursor()
                sql = "DELETE FROM empleados WHERE id = %s"
                cursor.execute(sql, (id_empleado,))
                conexion.commit()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
                self.limpiar_campos()    # Limpia los campos de entrada
                self.cargar_empleados()  # Vuelve a cargar la lista de empleados
                self.selected_empleado_id = None # Deselecciona el empleado después de la eliminación
            except Exception as e:
                messagebox.showerror("Error al eliminar empleado", f"Ocurrió un error: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conexion and conexion.is_connected():
                    conexion.close()

    def limpiar_campos(self):#Limpia todos los campos de entrada en la sección de datos del empleado y deselecciona cualquier empleado
        # Habilita la entrada de ID temporalmente para borrar, luego vuelve a establecerla como solo lectura
        self.entries['id'].config(state='normal')
        self.entries['id'].delete(0, tk.END)
        self.entries['id'].config(state='readonly')

        self.entries['nombre'].delete(0, tk.END)
        self.entries['apellido'].delete(0, tk.END)
        self.entries['puesto'].delete(0, tk.END)
        self.entries['salario'].delete(0, tk.END)
        # *** CORRECCIÓN AQUÍ: Usar la clave correcta para fecha_ingreso ***
        self.entries['fecha_ingreso_yyyy-mm-dd'].delete(0, tk.END)
        self.selected_empleado_id = None # Reinicia el ID del empleado seleccionado

# Bloque de ejecución principal
if __name__ == "__main__":
    # Crea la ventana raíz de Tkinter para la aplicación de inicio de sesión
    root_login = tk.Tk()
    # Inicializa la aplicación de inicio de sesión
    login_app = LoginApp(root_login)
    # Inicia el bucle de eventos de Tkinter para la ventana de inicio de sesión
    root_login.mainloop()