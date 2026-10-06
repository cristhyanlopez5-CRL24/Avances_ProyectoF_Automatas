import customtkinter as ctk

from tkinter import messagebox

from utilidades.logs_validacion import (
    cargar_logs,
    limpiar_logs
)


class LogsValidacionFrame(
    ctk.CTkScrollableFrame
):

    def __init__(
        self,
        master,
        ventana_principal
    ):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent"
        )

        self.ventana_principal = (
            ventana_principal
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.crear_encabezado()

        self.crear_acciones()

        self.crear_lista()

        self.refrescar()

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        titulo = ctk.CTkLabel(
            self,
            text="Logs de validación",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        descripcion = ctk.CTkLabel(
            self,
            text=(
                "Historial de cadenas evaluadas "
                "mediante expresiones regulares."
            ),
            font=ctk.CTkFont(
                size=14
            )
        )

        descripcion.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

    # =========================================================
    # ACCIONES
    # =========================================================

    def crear_acciones(self):

        self.frame_acciones = ctk.CTkFrame(
            self
        )

        self.frame_acciones.grid(
            row=2,
            column=0,
            padx=30,
            pady=10,
            sticky="ew"
        )

        self.frame_acciones.grid_columnconfigure(
            0,
            weight=1
        )

        self.btn_actualizar = ctk.CTkButton(
            self.frame_acciones,
            text="Actualizar historial",
            width=170,
            height=40,
            command=self.refrescar
        )

        self.btn_actualizar.grid(
            row=0,
            column=0,
            padx=10,
            pady=15,
            sticky="e"
        )

        self.btn_limpiar = ctk.CTkButton(
            self.frame_acciones,
            text="Limpiar historial",
            width=170,
            height=40,
            command=self.confirmar_limpiar
        )

        self.btn_limpiar.grid(
            row=0,
            column=1,
            padx=10,
            pady=15,
            sticky="w"
        )

    # =========================================================
    # LISTA
    # =========================================================

    def crear_lista(self):

        self.frame_lista = ctk.CTkFrame(
            self
        )

        self.frame_lista.grid(
            row=3,
            column=0,
            padx=30,
            pady=(10, 30),
            sticky="ew"
        )

        self.frame_lista.grid_columnconfigure(
            0,
            weight=1
        )

    # =========================================================
    # REFRESCAR
    # =========================================================

    def refrescar(self):

        for widget in (
            self.frame_lista.winfo_children()
        ):
            widget.destroy()

        logs = cargar_logs()

        if not logs:

            ctk.CTkLabel(
                self.frame_lista,
                text=(
                    "Todavía no existen "
                    "validaciones registradas."
                ),
                font=ctk.CTkFont(
                    size=16
                )
            ).grid(
                row=0,
                column=0,
                padx=20,
                pady=40
            )

            return

        ctk.CTkLabel(
            self.frame_lista,
            text=(
                f"Validaciones registradas: "
                f"{len(logs)}"
            ),
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 10)
        )

        # Los registros más recientes
        # aparecen primero.
        logs = list(
            reversed(logs)
        )

        for indice, registro in enumerate(
            logs,
            start=1
        ):

            frame_registro = ctk.CTkFrame(
                self.frame_lista
            )

            frame_registro.grid(
                row=indice,
                column=0,
                padx=20,
                pady=6,
                sticky="ew"
            )

            frame_registro.grid_columnconfigure(
                1,
                weight=1
            )

            ctk.CTkLabel(
                frame_registro,
                text="Fecha y hora:",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=0,
                column=0,
                padx=15,
                pady=(12, 4),
                sticky="w"
            )

            ctk.CTkLabel(
                frame_registro,
                text=registro[
                    "fecha_hora"
                ]
            ).grid(
                row=0,
                column=1,
                padx=15,
                pady=(12, 4),
                sticky="w"
            )

            ctk.CTkLabel(
                frame_registro,
                text="Regex:",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=1,
                column=0,
                padx=15,
                pady=4,
                sticky="w"
            )

            ctk.CTkLabel(
                frame_registro,
                text=registro[
                    "expresion"
                ],
                wraplength=650,
                justify="left"
            ).grid(
                row=1,
                column=1,
                padx=15,
                pady=4,
                sticky="w"
            )

            ctk.CTkLabel(
                frame_registro,
                text="Cadena:",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=2,
                column=0,
                padx=15,
                pady=4,
                sticky="w"
            )

            ctk.CTkLabel(
                frame_registro,
                text=registro[
                    "cadena"
                ]
            ).grid(
                row=2,
                column=1,
                padx=15,
                pady=4,
                sticky="w"
            )

            ctk.CTkLabel(
                frame_registro,
                text="Resultado:",
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=3,
                column=0,
                padx=15,
                pady=(4, 12),
                sticky="w"
            )

            ctk.CTkLabel(
                frame_registro,
                text=registro[
                    "resultado"
                ],
                font=ctk.CTkFont(
                    weight="bold"
                )
            ).grid(
                row=3,
                column=1,
                padx=15,
                pady=(4, 12),
                sticky="w"
            )

    # =========================================================
    # LIMPIAR HISTORIAL
    # =========================================================

    def confirmar_limpiar(self):

        respuesta = messagebox.askyesno(
            "Limpiar historial",
            (
                "¿Desea eliminar todos los "
                "logs de validación?\n\n"
                "Esta acción no se puede deshacer."
            )
        )

        if not respuesta:
            return

        limpiar_logs()

        self.refrescar()

        self.ventana_principal.lbl_estado.configure(
            text=(
                "Estado: Historial de "
                "validaciones eliminado."
            )
        )

        messagebox.showinfo(
            "Historial eliminado",
            (
                "Los logs de validación "
                "fueron eliminados correctamente."
            )
        )
        