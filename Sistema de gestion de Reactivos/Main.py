import tkinter as tk
import db

from login import Login

from reactivos import mostrar_modulo_reactivos
from proveedores import mostrar_modulo_proveedores
from ingresos import mostrar_modulo_ingresos
from uso import mostrar_modulo_uso
from alertas import mostrar_modulo_alertas
from reportes import mostrar_modulo_reportes
from configuracion import mostrar_modulo_configuracion


COLOR_FONDO = "#f6f8fb"
COLOR_SIDEBAR = "#081a33"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"


class AppReactivos:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario

        self.root.title("Gestión de Reactivos")
        self.root.geometry("1400x780")
        self.root.configure(bg=COLOR_FONDO)

        self.crear_layout()

    def crear_layout(self):
        self.sidebar = tk.Frame(self.root, bg=COLOR_SIDEBAR, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main = tk.Frame(self.root, bg=COLOR_FONDO)
        self.main.pack(side="right", fill="both", expand=True)

        self.crear_sidebar()
        self.crear_header()

        self.main_container = tk.Frame(self.main, bg=COLOR_FONDO)
        self.main_container.pack(fill="both", expand=True, padx=18, pady=18)

        rol = self.usuario[2]

        if rol == "Operario":
            self.cargar_modulo(mostrar_modulo_uso)
        else:
            self.cargar_modulo(mostrar_modulo_reactivos)

    def crear_sidebar(self):
        tk.Label(
            self.sidebar,
            text="🧪 GESTIÓN DE REACTIVOS\nLABORATORIO",
            bg=COLOR_SIDEBAR,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            justify="left"
        ).pack(pady=30, padx=20, anchor="w")

        rol = self.usuario[2]

        if rol == "Administrador":
            self.boton_menu("🧪 Reactivos", lambda: self.cargar_modulo(mostrar_modulo_reactivos))
            self.boton_menu("🏢 Proveedores", lambda: self.cargar_modulo(mostrar_modulo_proveedores))
            self.boton_menu("📥 Ingresos", lambda: self.cargar_modulo(mostrar_modulo_ingresos))
            self.boton_menu("🧬 Uso", lambda: self.cargar_modulo(mostrar_modulo_uso))
            self.boton_menu("🔔 Alertas", lambda: self.cargar_modulo(mostrar_modulo_alertas))
            self.boton_menu("📊 Reportes", lambda: self.cargar_modulo(mostrar_modulo_reportes))

            tk.Frame(self.sidebar, bg=COLOR_SIDEBAR).pack(expand=True, fill="both")

            self.boton_menu("⚙️ Configuración", lambda: self.cargar_modulo(mostrar_modulo_configuracion))

        elif rol == "Responsable":
            self.boton_menu("🧪 Reactivos", lambda: self.cargar_modulo(mostrar_modulo_reactivos))
            self.boton_menu("🏢 Proveedores", lambda: self.cargar_modulo(mostrar_modulo_proveedores))
            self.boton_menu("📥 Ingresos", lambda: self.cargar_modulo(mostrar_modulo_ingresos))
            self.boton_menu("🧬 Uso", lambda: self.cargar_modulo(mostrar_modulo_uso))
            self.boton_menu("🔔 Alertas", lambda: self.cargar_modulo(mostrar_modulo_alertas))
            self.boton_menu("📊 Reportes", lambda: self.cargar_modulo(mostrar_modulo_reportes))

        elif rol == "Operario":
            self.boton_menu("🧬 Uso", lambda: self.cargar_modulo(mostrar_modulo_uso))

        else:
            tk.Label(
                self.sidebar,
                text=f"Rol sin permisos:\n{rol}",
                bg=COLOR_SIDEBAR,
                fg="white",
                font=("Segoe UI", 10)
            ).pack(padx=20, pady=20)

    def boton_menu(self, texto, comando):
        tk.Button(
            self.sidebar,
            text=texto,
            command=comando,
            bg=COLOR_SIDEBAR,
            fg="white",
            activebackground=COLOR_AZUL,
            activeforeground="white",
            relief="flat",
            anchor="w",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            height=2,
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=4)

    def crear_header(self):
        header = tk.Frame(self.main, bg="white", height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="☰",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 22)
        ).pack(side="left", padx=25)

        tk.Label(
            header,
            text="Sistema de Gestión de Reactivos",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")

        nombre_usuario = self.usuario[1]
        rol_usuario = self.usuario[2]

        tk.Label(
            header,
            text=f"👤 {nombre_usuario} - {rol_usuario}",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 11)
        ).pack(side="right", padx=30)

    def limpiar_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def cargar_modulo(self, modulo_funcion):
        self.limpiar_main_container()
        modulo_funcion(self.main_container, self.usuario)


def iniciar_app():
    db.inicializar_bd()

    root = tk.Tk()
    root.geometry("1400x780")
    root.title("Gestión de Reactivos")
    root.configure(bg=COLOR_FONDO)

    def iniciar_sistema(usuario):
        for widget in root.winfo_children():
            widget.destroy()

        AppReactivos(root, usuario)

    Login(root, iniciar_sistema)

    root.mainloop()


if __name__ == "__main__":
    iniciar_app()

