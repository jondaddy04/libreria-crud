"""
app.py  –  Aplicación CRUD Librería
Interfaz gráfica con CustomTkinter + MySQL (XAMPP)
Autor: Jonathan Zamora Cruz
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from database import (
    insertar_libro, obtener_todos, buscar_libros,
    obtener_por_id, actualizar_libro, eliminar_libro
)

# ── Tema global ──────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLS = ("ID", "Título", "Autor", "Género", "Año", "Precio", "Stock", "ISBN")
COL_WIDTHS = (45, 200, 160, 110, 55, 75, 60, 145)


# ══════════════════════════════════════════════════
class LibreriaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("📚  Sistema de Librería  –  CRUD")
        self.geometry("1100x680")
        self.minsize(900, 580)
        self.configure(fg_color="#0f1117")

        self._libro_seleccionado_id = None
        self._build_ui()
        self._cargar_tabla()

    # ─────────────────────────────────────────────
    # UI
    # ─────────────────────────────────────────────
    def _build_ui(self):
        # ── Encabezado ──
        header = ctk.CTkFrame(self, fg_color="#1a1f2e", corner_radius=0, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📚  Sistema de Librería",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#4d9fff"
        ).pack(side="left", padx=24, pady=14)

        ctk.CTkLabel(
            header,
            text="Jonathan Zamora Cruz  |  Universidad Bancaria de México",
            font=ctk.CTkFont(size=11),
            text_color="#4a5568"
        ).pack(side="right", padx=24)

        # ── Layout principal ──
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=12)
        body.columnconfigure(0, weight=0)   # panel izquierdo fijo
        body.columnconfigure(1, weight=1)   # tabla expande
        body.rowconfigure(0, weight=1)

        # ── Panel formulario (izquierda) ──
        self._build_form(body)

        # ── Panel tabla + búsqueda (derecha) ──
        self._build_table_panel(body)

    def _build_form(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="#1a1f2e", corner_radius=12, width=280)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        panel.pack_propagate(False)

        ctk.CTkLabel(
            panel,
            text="Datos del Libro",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4d9fff"
        ).pack(pady=(18, 10), padx=16)

        # ── Campos ──
        campos = [
            ("Título *",   "titulo"),
            ("Autor *",    "autor"),
            ("Género *",   "genero"),
            ("Año *",      "año"),
            ("Precio *",   "precio"),
            ("Stock *",    "stock"),
            ("ISBN",       "isbn"),
        ]

        self._entries = {}
        for label_text, key in campos:
            ctk.CTkLabel(
                panel,
                text=label_text,
                font=ctk.CTkFont(size=11),
                text_color="#94a3b8",
                anchor="w"
            ).pack(fill="x", padx=16, pady=(6, 1))

            entry = ctk.CTkEntry(
                panel,
                height=32,
                corner_radius=8,
                fg_color="#0f1117",
                border_color="#2d3748",
                text_color="#e2e8f0",
                font=ctk.CTkFont(size=12)
            )
            entry.pack(fill="x", padx=16)
            self._entries[key] = entry

        # ── Botones CRUD ──
        btn_frame = ctk.CTkFrame(panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=(18, 8))
        btn_frame.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame, text="➕  Agregar",
            fg_color="#22c55e", hover_color="#16a34a",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36, corner_radius=8,
            command=self._agregar
        ).grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))

        ctk.CTkButton(
            btn_frame, text="✏️  Actualizar",
            fg_color="#4d9fff", hover_color="#2563eb",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36, corner_radius=8,
            command=self._actualizar
        ).grid(row=1, column=0, sticky="ew", padx=(0, 4))

        ctk.CTkButton(
            btn_frame, text="🗑️  Eliminar",
            fg_color="#ef4444", hover_color="#dc2626",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=36, corner_radius=8,
            command=self._eliminar
        ).grid(row=1, column=1, sticky="ew")

        ctk.CTkButton(
            btn_frame, text="🧹  Limpiar",
            fg_color="#374151", hover_color="#4b5563",
            font=ctk.CTkFont(size=12),
            height=32, corner_radius=8,
            command=self._limpiar_form
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))

        # ── Indicador de selección ──
        self._lbl_seleccion = ctk.CTkLabel(
            panel, text="Ningún libro seleccionado",
            font=ctk.CTkFont(size=10),
            text_color="#4a5568"
        )
        self._lbl_seleccion.pack(pady=8)

    def _build_table_panel(self, parent):
        panel = ctk.CTkFrame(parent, fg_color="#1a1f2e", corner_radius=12)
        panel.grid(row=0, column=1, sticky="nsew")

        # ── Barra superior: título + búsqueda ──
        top = ctk.CTkFrame(panel, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(14, 8))

        ctk.CTkLabel(
            top, text="Inventario de Libros",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#e2e8f0"
        ).pack(side="left")

        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._buscar())

        ctk.CTkEntry(
            top,
            textvariable=self._search_var,
            placeholder_text="🔍  Buscar por título, autor, género o ISBN...",
            height=32, corner_radius=8,
            fg_color="#0f1117", border_color="#2d3748",
            text_color="#e2e8f0", font=ctk.CTkFont(size=12),
            width=320
        ).pack(side="right")

        # ── Treeview (tabla) ──
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
            background="#0f1117", fieldbackground="#0f1117",
            foreground="#e2e8f0", rowheight=28,
            borderwidth=0, font=("Segoe UI", 10)
        )
        style.configure("Custom.Treeview.Heading",
            background="#1e293b", foreground="#4d9fff",
            font=("Segoe UI", 10, "bold"), borderwidth=0
        )
        style.map("Custom.Treeview",
            background=[("selected", "#2d3748")],
            foreground=[("selected", "#ffffff")]
        )

        frame_tree = ctk.CTkFrame(panel, fg_color="transparent")
        frame_tree.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical")
        scrollbar_x = ttk.Scrollbar(frame_tree, orient="horizontal")

        self._tree = ttk.Treeview(
            frame_tree,
            columns=COLS,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            selectmode="browse"
        )

        scrollbar_y.config(command=self._tree.yview)
        scrollbar_x.config(command=self._tree.xview)

        for col, w in zip(COLS, COL_WIDTHS):
            anchor = "center" if col in ("ID", "Año", "Precio", "Stock") else "w"
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor=anchor, minwidth=40)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self._tree.pack(fill="both", expand=True)

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # ── Barra de estado ──
        self._lbl_status = ctk.CTkLabel(
            panel, text="",
            font=ctk.CTkFont(size=10),
            text_color="#4a5568"
        )
        self._lbl_status.pack(pady=(0, 8))

    # ─────────────────────────────────────────────
    # CRUD HANDLERS
    # ─────────────────────────────────────────────
    def _agregar(self):
        datos = self._get_form_data()
        if datos is None:
            return
        try:
            insertar_libro(*datos)
            self._cargar_tabla()
            self._limpiar_form()
            self._set_status("✅  Libro agregado correctamente.", "#22c55e")
        except Exception as e:
            messagebox.showerror("Error al agregar", str(e))

    def _actualizar(self):
        if not self._libro_seleccionado_id:
            messagebox.showwarning("Aviso", "Selecciona un libro de la tabla primero.")
            return
        datos = self._get_form_data()
        if datos is None:
            return
        try:
            actualizar_libro(self._libro_seleccionado_id, *datos)
            self._cargar_tabla()
            self._limpiar_form()
            self._set_status("✏️  Libro actualizado correctamente.", "#4d9fff")
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def _eliminar(self):
        if not self._libro_seleccionado_id:
            messagebox.showwarning("Aviso", "Selecciona un libro de la tabla primero.")
            return
        titulo = self._entries["titulo"].get()
        ok = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el libro:\n\n«{titulo}»?\n\nEsta acción no se puede deshacer."
        )
        if ok:
            try:
                eliminar_libro(self._libro_seleccionado_id)
                self._cargar_tabla()
                self._limpiar_form()
                self._set_status("🗑️  Libro eliminado.", "#ef4444")
            except Exception as e:
                messagebox.showerror("Error al eliminar", str(e))

    # ─────────────────────────────────────────────
    # TABLA
    # ─────────────────────────────────────────────
    def _cargar_tabla(self, filas=None):
        self._tree.delete(*self._tree.get_children())
        datos = filas if filas is not None else obtener_todos()
        for i, row in enumerate(datos):
            precio_fmt = f"${float(row[5]):,.2f}"
            fila = (row[0], row[1], row[2], row[3], row[4], precio_fmt, row[6], row[7] or "")
            tag = "even" if i % 2 == 0 else "odd"
            self._tree.insert("", "end", values=fila, tags=(tag,))
        self._tree.tag_configure("even", background="#111827")
        self._tree.tag_configure("odd",  background="#0f1117")
        self._lbl_status.configure(text=f"{len(datos)} libro(s) en total.")

    def _buscar(self):
        texto = self._search_var.get().strip()
        if texto:
            self._cargar_tabla(buscar_libros(texto))
        else:
            self._cargar_tabla()

    def _on_select(self, _event=None):
        sel = self._tree.selection()
        if not sel:
            return
        vals = self._tree.item(sel[0], "values")
        libro_id = int(vals[0])
        row = obtener_por_id(libro_id)
        if not row:
            return
        self._libro_seleccionado_id = libro_id
        self._lbl_seleccion.configure(
            text=f"Editando ID: {libro_id}", text_color="#4d9fff"
        )
        keys = ["titulo", "autor", "genero", "año", "precio", "stock", "isbn"]
        for key, val in zip(keys, row[1:]):
            e = self._entries[key]
            e.delete(0, "end")
            e.insert(0, str(val) if val is not None else "")

    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────
    def _get_form_data(self):
        titulo  = self._entries["titulo"].get().strip()
        autor   = self._entries["autor"].get().strip()
        genero  = self._entries["genero"].get().strip()
        año_str = self._entries["año"].get().strip()
        prec_str= self._entries["precio"].get().strip()
        stk_str = self._entries["stock"].get().strip()
        isbn    = self._entries["isbn"].get().strip()

        if not all([titulo, autor, genero, año_str, prec_str, stk_str]):
            messagebox.showwarning("Campos incompletos", "Completa todos los campos obligatorios (*).")
            return None

        try:
            año = int(año_str)
            assert 1000 <= año <= 2100
        except (ValueError, AssertionError):
            messagebox.showerror("Error", "El año debe ser un número entre 1000 y 2100.")
            return None

        try:
            precio = float(prec_str)
            assert precio >= 0
        except (ValueError, AssertionError):
            messagebox.showerror("Error", "El precio debe ser un número positivo.")
            return None

        try:
            stock = int(stk_str)
            assert stock >= 0
        except (ValueError, AssertionError):
            messagebox.showerror("Error", "El stock debe ser un número entero positivo.")
            return None

        return titulo, autor, genero, año, precio, stock, isbn or None

    def _limpiar_form(self):
        for e in self._entries.values():
            e.delete(0, "end")
        self._libro_seleccionado_id = None
        self._lbl_seleccion.configure(
            text="Ningún libro seleccionado", text_color="#4a5568"
        )

    def _set_status(self, msg, color="#4a5568"):
        self._lbl_status.configure(text=msg, text_color=color)
        self.after(4000, lambda: self._lbl_status.configure(
            text=f"{len(self._tree.get_children())} libro(s) en total.",
            text_color="#4a5568"
        ))


# ══════════════════════════════════════════════════
if __name__ == "__main__":
    app = LibreriaApp()
    app.mainloop()
