import tkinter as tk
from tkinter import ttk, messagebox
import db


COLOR_FONDO = "#f6f8fb"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"
COLOR_BORDE = "#e5e7eb"


def mostrar_modulo_proveedores(parent, usuario=None):
    modulo = ModuloProveedores(parent)
    modulo.pack(fill="both", expand=True)


class ModuloProveedores(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.id_proveedor_seleccionado = None
        self.reactivos_combo = []
        self.crear_interfaz()

    def crear_interfaz(self):
        card_proveedores = tk.Frame(
            self,
            bg="white",
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        card_proveedores.pack(fill="x", pady=(0, 12))

        top = tk.Frame(card_proveedores, bg="white")
        top.pack(fill="x", padx=18, pady=12)

        tk.Label(
            top,
            text="Proveedores",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nuevo Proveedor",
            command=self.abrir_formulario_proveedor,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        tk.Button(
            top,
            text="Editar Proveedor",
            command=self.abrir_formulario_editar_proveedor,
            bg="#64748b",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right", padx=(0, 10))

        self.crear_tabla_proveedores(card_proveedores)

        card_reactivos = tk.Frame(
            self,
            bg="white",
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        card_reactivos.pack(fill="both", expand=True)

        top_reactivos = tk.Frame(card_reactivos, bg="white")
        top_reactivos.pack(fill="x", padx=18, pady=12)

        tk.Label(
            top_reactivos,
            text="Reactivos asociados al proveedor",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        tk.Button(
            top_reactivos,
            text="+ Asociar Reactivo",
            command=self.abrir_formulario_reactivo_proveedor,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        tk.Button(
            top_reactivos,
            text="Editar Asociación",
            command=self.abrir_formulario_editar_reactivo_proveedor,
            bg="#64748b",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right", padx=(0, 10))

        self.crear_tabla_reactivos_proveedor(card_reactivos)

        self.cargar_tabla_proveedores()

    def crear_tabla_proveedores(self, parent):
        columnas = (
            "id",
            "codigo_sap",
            "nombre",
            "cufe",
            "tipo",
            "email",
            "telefono",
            "estado"
        )

        self.tabla_proveedores = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            height=5
        )
        self.tabla_proveedores.pack(fill="x", padx=18, pady=(0, 12))

        encabezados = {
            "id": "ID",
            "codigo_sap": "Código SAP",
            "nombre": "Nombre",
            "cufe": "CUFE",
            "tipo": "Tipo",
            "email": "Email",
            "telefono": "Teléfono",
            "estado": "Estado",
        }

        for col in columnas:
            self.tabla_proveedores.heading(col, text=encabezados[col])
            self.tabla_proveedores.column(col, width=130)

        self.tabla_proveedores.column("id", width=50)
        self.tabla_proveedores.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

    def crear_tabla_reactivos_proveedor(self, parent):
        columnas = (
            "id",
            "codigo_interno",
            "reactivo",
            "codigo_proveedor",
            "cantidad_inicial",
            "estado"
        )

        self.tabla_reactivos = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            height=10
        )
        self.tabla_reactivos.pack(fill="both", expand=True, padx=18, pady=(0, 12))

        encabezados = {
            "id": "ID",
            "codigo_interno": "Código interno",
            "reactivo": "Reactivo",
            "codigo_proveedor": "Código proveedor",
            "cantidad_inicial": "Cantidad inicial",
            "estado": "Estado",
        }

        for col in columnas:
            self.tabla_reactivos.heading(col, text=encabezados[col])
            self.tabla_reactivos.column(col, width=140)

        self.tabla_reactivos.column("id", width=50)

    def cargar_tabla_proveedores(self):
        for item in self.tabla_proveedores.get_children():
            self.tabla_proveedores.delete(item)

        datos = db.obtener_proveedores()

        for fila in datos:
            self.tabla_proveedores.insert("", "end", values=fila)

    def seleccionar_proveedor(self, event=None):
        seleccionado = self.tabla_proveedores.selection()

        if not seleccionado:
            return

        valores = self.tabla_proveedores.item(seleccionado[0], "values")
        self.id_proveedor_seleccionado = valores[0]

        self.cargar_reactivos_del_proveedor()

    def cargar_reactivos_del_proveedor(self):
        for item in self.tabla_reactivos.get_children():
            self.tabla_reactivos.delete(item)

        if not self.id_proveedor_seleccionado:
            return

        datos = db.obtener_reactivos_por_proveedor(self.id_proveedor_seleccionado)

        for fila in datos:
            self.tabla_reactivos.insert("", "end", values=fila)

    def abrir_formulario_proveedor(self):
        ventana = tk.Toplevel(self)
        ventana.title("Nuevo Proveedor")
        ventana.geometry("540x620")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        canvas = tk.Canvas(
            ventana,
            bg="white",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            ventana,
            orient="vertical",
            command=canvas.yview
        )

        contenido = tk.Frame(
            canvas,
            bg="white"
        )

        contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        window_canvas = canvas.create_window(
            (0, 0),
            window=contenido,
            anchor="nw"
        )

        def ajustar_ancho(event):
            canvas.itemconfig(window_canvas, width=event.width)

        canvas.bind("<Configure>", ajustar_ancho)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(
            contenido,
            text="Nuevo Proveedor",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(
            contenido,
            bg="white"
        )

        frame.pack(fill="both", expand=True, padx=30)

        campos = {}

        def crear_campo(label, nombre):
            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(frame, font=("Segoe UI", 10), relief="solid", bd=1)
            entry.pack(fill="x", ipady=6)
            campos[nombre] = entry

        crear_campo("Código SAP", "codigo_sap")
        crear_campo("CUFE", "cufe")
        crear_campo("Nombre *", "nombre")
        tk.Label(
            frame,
            text="Tipo proveedor",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_tipo = ttk.Combobox(
            frame,
            values=["Fisico Quimico", "Microbiologico", "Ambos"],
            state="readonly",
            font=("Segoe UI", 10)
            )
        combo_tipo.pack(fill="x", ipady=6)
        combo_tipo.set("Ambos")
        
        crear_campo("Email", "email")
        crear_campo("Teléfono", "telefono")

        def guardar():
            nombre = campos["nombre"].get().strip()

            if not nombre:
                messagebox.showwarning("Campo obligatorio", "El nombre es obligatorio.")
                return

            try:
                db.insertar_proveedor(
                    campos["codigo_sap"].get().strip(),
                    nombre,
                    campos["cufe"].get().strip(),
                    combo_tipo.get(),
                    campos["email"].get().strip(),
                    campos["telefono"].get().strip()
                )

                self.cargar_tabla_proveedores()
                cerrar()
                messagebox.showinfo("Correcto", "Proveedor creado correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar.\n\n{e}")

        botones = tk.Frame(ventana, bg="white")
        botones.pack(fill="x", padx=30, pady=20)

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        ventana.bind("<MouseWheel>", _on_mousewheel)

        def cerrar():
            ventana.unbind("<MouseWheel>")
            ventana.destroy()

        botones = tk.Frame(contenido, bg="white")
        botones.pack(fill="x", padx=30, pady=25)

        tk.Button(
            botones,
            text="Cancelar",
            command=cerrar,
            bg="#e5e7eb",
            fg=COLOR_TEXTO,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        ).pack(side="left")

        tk.Button(
            botones,
            text="Guardar Proveedor",
            command=guardar,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        ).pack(side="right")

    def abrir_formulario_reactivo_proveedor(self):
        if not self.id_proveedor_seleccionado:
            messagebox.showwarning(
                "Proveedor no seleccionado",
                "Primero seleccioná un proveedor de la tabla superior."
            )
            return

        self.reactivos_combo = db.obtener_reactivos_combo()

        if not self.reactivos_combo:
            messagebox.showwarning(
                "Sin reactivos",
                "Primero tenés que cargar reactivos en el módulo Reactivos."
            )
            return

        ventana = tk.Toplevel(self)
        ventana.title("Asociar Reactivo al Proveedor")
        ventana.geometry("620x520")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Asociar Reactivo al Proveedor",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(ventana, bg="white")
        frame.pack(fill="both", expand=True, padx=30)

        tk.Label(
            frame,
            text="Buscar reactivo",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        entry_buscar = tk.Entry(frame, font=("Segoe UI", 10), relief="solid", bd=1)
        entry_buscar.pack(fill="x", ipady=6)

        tk.Label(
            frame,
            text="Reactivo *",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        valores_combo = [x[1] for x in self.reactivos_combo]

        combo_reactivo = ttk.Combobox(
            frame,
            values=valores_combo,
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_reactivo.pack(fill="x", ipady=6)

        def filtrar_reactivos(event=None):
            texto = entry_buscar.get().strip().lower()

            filtrados = [
                item[1] for item in self.reactivos_combo
                if texto in item[1].lower()
            ]

            combo_reactivo["values"] = filtrados

            if filtrados:
                combo_reactivo.set(filtrados[0])
            else:
                combo_reactivo.set("")

        entry_buscar.bind("<KeyRelease>", filtrar_reactivos)

        campos = {}

        def crear_campo(label, nombre):
            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(frame, font=("Segoe UI", 10), relief="solid", bd=1)
            entry.pack(fill="x", ipady=6)
            campos[nombre] = entry

        crear_campo("Código del proveedor", "codigo_proveedor")
        crear_campo("Cantidad inicial", "cantidad_inicial")
        

        def guardar():
            seleccionado = combo_reactivo.get()

            if not seleccionado:
                messagebox.showwarning("Campo obligatorio", "Seleccioná un reactivo.")
                return

            id_reactivo = None

            for item in self.reactivos_combo:
                if item[1] == seleccionado:
                    id_reactivo = item[0]
                    break

            if id_reactivo is None:
                messagebox.showerror("Error", "No se pudo identificar el reactivo seleccionado.")
                return

            cantidad = campos["cantidad_inicial"].get().strip()
            

            try:
                cantidad = float(cantidad.replace(",", ".")) if cantidad else 0
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Cantidad inicial debe ser un número."
                )
                return

            try:
                db.insertar_reactivo_proveedor(
                    id_reactivo,
                    self.id_proveedor_seleccionado,
                    campos["codigo_proveedor"].get().strip(),
                    cantidad
                )

                self.cargar_reactivos_del_proveedor()
                ventana.destroy()
                messagebox.showinfo("Correcto", "Reactivo asociado correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo asociar el reactivo.\n\n{e}")

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
            text="Guardar Asociación",
            command=guardar,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        ).pack(side="right")

    def abrir_formulario_editar_proveedor(self):
        seleccionado = self.tabla_proveedores.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Sin selección",
                "Seleccioná un proveedor de la tabla superior para editar."
            )
            return

        valores = self.tabla_proveedores.item(seleccionado[0], "values")
        id_proveedor = valores[0]

        proveedor = db.obtener_proveedor_por_id(id_proveedor)

        if not proveedor:
            messagebox.showerror("Error", "No se encontró el proveedor seleccionado.")
            return

        (
            id_proveedor,
            codigo_sap,
            cufe,
            nombre,
            tipo_proveedor,
            email,
            telefono,
            activo
        ) = proveedor

        ventana = tk.Toplevel(self)
        ventana.title("Editar Proveedor")
        ventana.geometry("540x620")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        canvas = tk.Canvas(ventana, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)

        contenido = tk.Frame(canvas, bg="white")

        contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        window_canvas = canvas.create_window(
            (0, 0),
            window=contenido,
            anchor="nw"
        )

        def ajustar_ancho(event):
            canvas.itemconfig(window_canvas, width=event.width)

        canvas.bind("<Configure>", ajustar_ancho)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(
            contenido,
            text="Editar Proveedor",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(contenido, bg="white")
        frame.pack(fill="both", expand=True, padx=30)

        campos = {}

        def crear_campo(label, nombre, valor=""):
            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(frame, font=("Segoe UI", 10), relief="solid", bd=1)
            entry.pack(fill="x", ipady=6)
            entry.insert(0, "" if valor is None else str(valor))
            campos[nombre] = entry

        crear_campo("Código SAP", "codigo_sap", codigo_sap)
        crear_campo("CUFE", "cufe", cufe)
        crear_campo("Nombre *", "nombre", nombre)

        tk.Label(
            frame,
            text="Tipo proveedor",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_tipo = ttk.Combobox(
            frame,
            values=["Fisico Quimico", "Microbiologico", "Ambos"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_tipo.pack(fill="x", ipady=6)
        combo_tipo.set(tipo_proveedor if tipo_proveedor else "Ambos")

        crear_campo("Email", "email", email)
        crear_campo("Teléfono", "telefono", telefono)

        tk.Label(
            frame,
            text="Estado",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_activo = ttk.Combobox(
            frame,
            values=["Activo", "Inactivo"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_activo.pack(fill="x", ipady=6)
        combo_activo.set("Activo" if activo == 1 else "Inactivo")

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        ventana.bind("<MouseWheel>", _on_mousewheel)

        def cerrar():
            ventana.unbind("<MouseWheel>")
            ventana.destroy()

        def guardar_edicion():
            nombre_editado = campos["nombre"].get().strip()

            if not nombre_editado:
                messagebox.showwarning(
                    "Campo obligatorio",
                    "El nombre del proveedor es obligatorio."
                )
                return

            activo_valor = 1 if combo_activo.get() == "Activo" else 0

            try:
                db.actualizar_proveedor(
                    id_proveedor,
                    campos["codigo_sap"].get().strip(),
                    campos["cufe"].get().strip(),
                    nombre_editado,
                    combo_tipo.get(),
                    campos["email"].get().strip(),
                    campos["telefono"].get().strip(),
                    activo_valor
                )
    
                self.cargar_tabla_proveedores()
                self.cargar_reactivos_del_proveedor()
                cerrar()

                messagebox.showinfo("Correcto", "Proveedor actualizado correctamente.")

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo actualizar el proveedor.\n\n{e}"
                )

        botones = tk.Frame(contenido, bg="white")
        botones.pack(fill="x", padx=30, pady=25)

        tk.Button(
            botones,
            text="Cancelar",
            command=cerrar,
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
            text="Guardar Cambios",
            command=guardar_edicion,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="right")

    def abrir_formulario_editar_reactivo_proveedor(self):
        seleccionado = self.tabla_reactivos.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Sin selección",
                "Seleccioná un reactivo asociado de la tabla inferior para editar."
            )
            return

        valores = self.tabla_reactivos.item(seleccionado[0], "values")
        id_reactivo_proveedor = valores[0]

        dato = db.obtener_reactivo_proveedor_por_id(id_reactivo_proveedor)

        if not dato:
            messagebox.showerror("Error", "No se encontró la asociación seleccionada.")
            return

        (
            id_reactivo_proveedor,
            reactivo,
            codigo_proveedor,
            cantidad_inicial,
            activo
        ) = dato

        ventana = tk.Toplevel(self)
        ventana.title("Editar Reactivo del Proveedor")
        ventana.geometry("540x430")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Editar Asociación",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(ventana, bg="white")
        frame.pack(fill="both", expand=True, padx=30)

        tk.Label(
            frame,
            text="Reactivo",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        entry_reactivo = tk.Entry(frame, font=("Segoe UI", 10), relief="solid", bd=1)
        entry_reactivo.pack(fill="x", ipady=6)
        entry_reactivo.insert(0, reactivo)
        entry_reactivo.config(state="disabled")

        campos = {}

        def crear_campo(label, nombre, valor=""):
            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(frame, font=("Segoe UI", 10), relief="solid", bd=1)
            entry.pack(fill="x", ipady=6)
            entry.insert(0, "" if valor is None else str(valor))
            campos[nombre] = entry

        crear_campo("Código proveedor", "codigo_proveedor", codigo_proveedor)
        crear_campo("Cantidad inicial", "cantidad_inicial", cantidad_inicial)

        tk.Label(
            frame,
            text="Estado",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_activo = ttk.Combobox(
            frame,
            values=["Activo", "Inactivo"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_activo.pack(fill="x", ipady=6)
        combo_activo.set("Activo" if activo == 1 else "Inactivo")

        def guardar_edicion():
            cantidad = campos["cantidad_inicial"].get().strip()

            try:
                cantidad = float(cantidad.replace(",", ".")) if cantidad else 0
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "La cantidad inicial debe ser un número."
                )
                return

            activo_valor = 1 if combo_activo.get() == "Activo" else 0

            try:
                db.actualizar_reactivo_proveedor(
                    id_reactivo_proveedor,
                    campos["codigo_proveedor"].get().strip(),
                    cantidad,
                    activo_valor
                )

                self.cargar_reactivos_del_proveedor()
                ventana.destroy()

                messagebox.showinfo(
                    "Correcto",
                    "Asociación actualizada correctamente."
                )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo actualizar la asociación.\n\n{e}"
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
            pady=8
        ).pack(side="left")

        tk.Button(
            botones,
            text="Guardar Cambios",
            command=guardar_edicion,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        ).pack(side="right")


