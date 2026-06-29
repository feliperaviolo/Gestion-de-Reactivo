import tkinter as tk
from tkinter import ttk, messagebox
import db


COLOR_FONDO = "#f6f8fb"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"
COLOR_BORDE = "#e5e7eb"


def mostrar_modulo_uso(parent, usuario=None):
    modulo = ModuloUso(parent)
    modulo.pack(fill="both", expand=True)


class ModuloUso(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.combo_lotes = []
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
            text="Uso de Reactivos",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Registrar Uso",
            command=self.abrir_formulario_uso,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        self.crear_tabla(card)
        self.cargar_tabla()

    def crear_tabla(self, parent):
        columnas = (
            "id",
            "codigo",
            "reactivo",
            "lote",
            "cantidad",
            "unidad",
            "fecha",
            "observaciones"
        )

        self.tabla = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            height=14
        )
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 15))

        encabezados = {
            "id": "ID",
            "codigo": "Código",
            "reactivo": "Reactivo",
            "lote": "Lote",
            "cantidad": "Cantidad usada",
            "unidad": "Unidad",
            "fecha": "Fecha",
            "observaciones": "Observaciones"
        }

        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=130)

        self.tabla.column("id", width=50)
        self.tabla.column("observaciones", width=250)

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        datos = db.obtener_usos()

        for fila in datos:
            self.tabla.insert("", "end", values=fila)

    def abrir_formulario_uso(self):
        self.combo_lotes = db.obtener_lotes_disponibles_combo()

        if not self.combo_lotes:
            messagebox.showwarning(
                "Sin lotes disponibles",
                "No hay lotes disponibles para registrar uso."
            )
            return

        ventana = tk.Toplevel(self)
        ventana.title("Registrar Uso")
        ventana.geometry("580x620")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Registrar Uso de Reactivo",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(ventana, bg="white")
        frame.pack(fill="both", expand=True, padx=30)

        tk.Label(
            frame,
            text="Buscar por código interno, reactivo o lote",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        entry_buscar = tk.Entry(
            frame,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )
        entry_buscar.pack(fill="x", ipady=6)

        tk.Label(
            frame,
            text="Lote disponible *",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        valores_combo = [str(x[1]) for x in self.combo_lotes]

        combo_lote = ttk.Combobox(
            frame,
            values=valores_combo,
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_lote.pack(fill="x", ipady=6)

        def filtrar_lotes(event=None):
            texto = entry_buscar.get().strip().lower()
            filtrados = []

            for item in self.combo_lotes:
                texto_item = str(item[1])

                if texto in texto_item.lower():
                    filtrados.append(texto_item)

            combo_lote["values"] = filtrados

            if filtrados:
                combo_lote.set(filtrados[0])
            else:
                combo_lote.set("")

        entry_buscar.bind("<KeyRelease>", filtrar_lotes)

        # ==========================
        # MOTIVO / OBSERVACIÓN RÁPIDA
        # ==========================

        tk.Label(
            frame,
            text="Motivo del movimiento *",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(12, 2))

        motivo_var = tk.StringVar(value="Uso normal")

        frame_motivos = tk.Frame(frame, bg="white")
        frame_motivos.pack(fill="x", pady=(0, 5))

        tk.Radiobutton(
            frame_motivos,
            text="Uso normal",
            variable=motivo_var,
            value="Uso normal",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Radiobutton(
            frame_motivos,
            text="Descarte por vencimiento",
            variable=motivo_var,
            value="Descarte por vencimiento",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Radiobutton(
            frame_motivos,
            text="Merma",
            variable=motivo_var,
            value="Merma",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Radiobutton(
            frame_motivos,
            text="Derrame",
            variable=motivo_var,
            value="Derrame",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        campos = {}

        def crear_campo(label, nombre):
            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(
                frame,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )
            entry.pack(fill="x", ipady=6)
            campos[nombre] = entry

        crear_campo("Cantidad usada *", "cantidad")
        crear_campo("Detalle / Observaciones", "observaciones")

        def guardar():
            seleccionado = combo_lote.get()
            cantidad = campos["cantidad"].get().strip()
            observacion_libre = campos["observaciones"].get().strip()
            motivo = motivo_var.get()

            if not seleccionado or not cantidad:
                messagebox.showwarning(
                    "Campos obligatorios",
                    "Seleccioná un lote e ingresá la cantidad usada."
                )
                return

            id_lote = None

            for item in self.combo_lotes:
                if str(item[1]).strip() == seleccionado.strip():
                    id_lote = item[0]
                    break

            if id_lote is None:
                messagebox.showerror(
                    "Error",
                    "No se encontró el lote seleccionado."
                )
                return

            try:
                cantidad = float(cantidad.replace(",", "."))
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "La cantidad usada debe ser un número."
                )
                return

            if observacion_libre:
                observaciones = f"[{motivo}] - {observacion_libre}"
            else:
                observaciones = f"[{motivo}]"

            try:
                db.registrar_uso_lote(
                    id_lote,
                    cantidad,
                    observaciones,
                    1
                )

                self.cargar_tabla()
                ventana.destroy()

                messagebox.showinfo(
                    "Correcto",
                    "Uso registrado correctamente."
                )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo registrar el uso.\n\n{e}"
                )

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
            pady=8,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            botones,
            text="Guardar Uso",
            command=guardar,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="right")