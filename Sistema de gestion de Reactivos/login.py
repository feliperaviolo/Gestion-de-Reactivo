import tkinter as tk
from tkinter import messagebox
import db


COLOR_FONDO = "#f6f8fb"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"


class Login(tk.Frame):
    def __init__(self, root, on_login_ok):
        super().__init__(root, bg=COLOR_FONDO)
        self.root = root
        self.on_login_ok = on_login_ok

        self.pack(fill="both", expand=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = tk.Frame(self, bg="white", padx=45, pady=40)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            contenedor,
            text="🧪 Gestión de Reactivos",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(0, 8))

        tk.Label(
            contenedor,
            text="Inicio de sesión",
            bg="white",
            fg="#64748b",
            font=("Segoe UI", 11)
        ).pack(pady=(0, 25))

        tk.Label(
            contenedor,
            text="Usuario",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.entry_usuario = tk.Entry(
            contenedor,
            width=35,
            font=("Segoe UI", 11)
        )
        self.entry_usuario.pack(ipady=7, pady=(4, 15))
        self.entry_usuario.insert(0, "admin")

        tk.Label(
            contenedor,
            text="Contraseña",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.entry_password = tk.Entry(
            contenedor,
            width=35,
            font=("Segoe UI", 11),
            show="*"
        )
        self.entry_password.pack(ipady=7, pady=(4, 20))
        self.entry_password.insert(0, "admin")

        tk.Button(
            contenedor,
            text="Ingresar",
            command=self.login,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            width=30,
            pady=8,
            cursor="hand2"
        ).pack()

        self.entry_password.bind("<Return>", lambda e: self.login())

    def login(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning(
                "Datos faltantes",
                "Ingresá usuario y contraseña."
            )
            return

        usuario_validado = db.validar_login(usuario, password)

        if usuario_validado:
            self.destroy()
            self.on_login_ok(usuario_validado)
        else:
            messagebox.showerror(
                "Acceso denegado",
                "Usuario o contraseña incorrectos."
            )