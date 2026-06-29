import tkinter as tk
from tkinter import ttk, messagebox
import db


COLOR_FONDO = "#f6f8fb"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"
COLOR_BORDE = "#e5e7eb"


def mostrar_modulo_configuracion(parent, usuario=None):
    modulo = ModuloConfiguracion(parent)
    modulo.pack(fill="both", expand=True)


class ModuloConfiguracion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.crear_interfaz()

    def crear_interfaz(self):
        card = tk.Frame(
            self,
            bg="white",
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        card.pack(fill="both", expand=True)

        top = tk.Frame(card, bg="white")
        top.pack(fill="x", padx=18, pady=15)

        tk.Label(
            top,
            text="Configuración - Usuarios",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nuevo Usuario",
            command=self.abrir_formulario_usuario,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        self.crear_tabla(card)
        self.cargar_usuarios()

    def crear_tabla(self, parent):
        columnas = ("id", "nombre", "email", "rol", "estado")

        self.tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=14)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 15))

        encabezados = {
            "id": "ID",
            "nombre": "Nombre",
            "email": "Email",
            "rol": "Rol",
            "estado": "Estado"
        }

        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=180)

        self.tabla.column("id", width=60)

    def cargar_usuarios(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for fila in db.obtener_usuarios():
            self.tabla.insert("", "end", values=fila)

    def abrir_formulario_usuario(self):
        ventana = tk.Toplevel(self)
        ventana.title("Nuevo Usuario")
        ventana.geometry("500x430")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Nuevo Usuario",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(ventana, bg="white")
        frame.pack(fill="both", expand=True, padx=30)

        campos = {}

        def crear_campo(label, nombre, show=None):
            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(frame, font=("Segoe UI", 10), show=show)
            entry.pack(fill="x", ipady=6)
            campos[nombre] = entry

        crear_campo("Nombre *", "nombre")
        crear_campo("Email *", "email")

        tk.Label(
            frame,
            text="Rol *",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_rol = ttk.Combobox(
            frame,
            values=["Administrador", "Operario", "Responsable"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_rol.pack(fill="x", ipady=6)
        combo_rol.set("Operario")

        crear_campo("Contraseña *", "password", show="*")

        def guardar():
            nombre = campos["nombre"].get().strip()
            email = campos["email"].get().strip()
            password = campos["password"].get().strip()
            rol = combo_rol.get()

            if not nombre or not email or not password or not rol:
                messagebox.showwarning("Campos obligatorios", "Completá todos los campos obligatorios.")
                return

            try:
                db.crear_usuario(nombre, email, rol, password)
                self.cargar_usuarios()
                ventana.destroy()
                messagebox.showinfo("Correcto", "Usuario creado correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el usuario.\n\n{e}")

        botones = tk.Frame(ventana, bg="white")
        botones.pack(fill="x", padx=30, pady=20)

        tk.Button(
            botones,
            text="Cancelar",
            command=ventana.destroy,
            bg="#e5e7eb",
            fg=COLOR_TEXTO,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        ).pack(side="left")

        tk.Button(
            botones,
            text="Guardar Usuario",
            command=guardar,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        ).pack(side="right")