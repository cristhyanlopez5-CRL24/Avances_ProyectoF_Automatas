import os

import customtkinter as ctk

from tkinter import messagebox

from PIL import Image

from utilidades.graficador import (
    generar_diagrama
)


class VerDiagramaFrame(ctk.CTkFrame):

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

        self.automata = (
            ventana_principal.automata_actual
        )

        self.tipo = (
            ventana_principal.tipo_automata_actual
        )

        # Mantener referencia de la imagen.
        # Es importante para que Tkinter
        # no la elimine de memoria.
        self.imagen_ctk = None

        self.ruta_diagrama = None

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            3,
            weight=1
        )

        # =====================================================
        # INTERFAZ
        # =====================================================

        self.crear_encabezado()

        self.crear_informacion()

        self.crear_controles()

        self.crear_area_diagrama()

        # Generar automáticamente
        if self.automata is not None:

            self.generar_y_mostrar_diagrama()

        else:

            self.mostrar_sin_automata()

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        lbl_titulo = ctk.CTkLabel(
            self,
            text="Diagrama del autómata",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        lbl_titulo.grid(
            row=0,
            column=0,
            pady=(25, 5)
        )

        lbl_descripcion = ctk.CTkLabel(
            self,
            text=(
                "Representación gráfica generada "
                "automáticamente con Graphviz."
            ),
            font=ctk.CTkFont(
                size=14
            )
        )

        lbl_descripcion.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

    # =========================================================
    # INFORMACIÓN DEL AUTÓMATA
    # =========================================================

    def crear_informacion(self):

        self.frame_info = ctk.CTkFrame(
            self
        )

        self.frame_info.grid(
            row=2,
            column=0,
            padx=30,
            pady=(5, 10),
            sticky="ew"
        )

        self.frame_info.grid_columnconfigure(
            1,
            weight=1
        )

        if self.automata is None:

            ctk.CTkLabel(
                self.frame_info,
                text=(
                    "No hay ningún autómata cargado."
                ),
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=0,
                columnspan=2,
                padx=20,
                pady=20
            )

            return

        # -----------------------------------------------------
        # TIPO
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_info,
            text="Tipo:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.tipo
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # NOMBRE
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_info,
            text="Autómata:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.automata.nombre
        ).grid(
            row=1,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ESTADOS
        # -----------------------------------------------------

        estados = (
            "{"
            + ", ".join(
                sorted(
                    self.automata.estados
                )
            )
            + "}"
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Estados:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=estados
        ).grid(
            row=2,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # TRANSICIONES
        # -----------------------------------------------------

        cantidad = sum(
            len(destinos)
            for destinos
            in self.automata.transiciones.values()
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Transiciones:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=3,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=str(cantidad)
        ).grid(
            row=3,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

    # =========================================================
    # CONTROLES
    # =========================================================

    def crear_controles(self):

        self.frame_controles = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.frame_controles.grid(
            row=3,
            column=0,
            padx=30,
            pady=5,
            sticky="ew"
        )

        self.frame_controles.grid_columnconfigure(
            0,
            weight=1
        )

        self.lbl_estado = ctk.CTkLabel(
            self.frame_controles,
            text="",
            font=ctk.CTkFont(
                size=13
            )
        )

        self.lbl_estado.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.btn_actualizar = ctk.CTkButton(
            self.frame_controles,
            text="Actualizar diagrama",
            width=170,
            command=self.generar_y_mostrar_diagrama
        )

        self.btn_actualizar.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        if self.automata is None:

            self.btn_actualizar.configure(
                state="disabled"
            )

    # =========================================================
    # ÁREA DEL DIAGRAMA
    # =========================================================

    def crear_area_diagrama(self):

        self.frame_diagrama = ctk.CTkFrame(
            self
        )

        self.frame_diagrama.grid(
            row=4,
            column=0,
            padx=30,
            pady=(5, 30),
            sticky="nsew"
        )

        self.frame_diagrama.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_diagrama.grid_rowconfigure(
            0,
            weight=1
        )

        self.lbl_diagrama = ctk.CTkLabel(
            self.frame_diagrama,
            text=(
                "El diagrama aparecerá aquí."
            ),
            font=ctk.CTkFont(
                size=16
            )
        )

        self.lbl_diagrama.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )

    # =========================================================
    # SIN AUTÓMATA
    # =========================================================

    def mostrar_sin_automata(self):

        self.lbl_diagrama.configure(
            text=(
                "No hay un autómata disponible.\n\n"
                "Primero cree un AFD o AFN y "
                "agregue sus transiciones."
            )
        )

        self.lbl_estado.configure(
            text="Sin autómata cargado."
        )

    # =========================================================
    # GENERAR DIAGRAMA
    # =========================================================

    def generar_y_mostrar_diagrama(self):

        if self.automata is None:

            messagebox.showwarning(
                "Sin autómata",
                (
                    "Primero debe crear un "
                    "AFD o AFN."
                )
            )

            return

        try:

            # -------------------------------------------------
            # RUTA
            # -------------------------------------------------

            ruta_base = os.path.join(
                "recursos",
                "diagramas",
                "automata_actual"
            )

            # -------------------------------------------------
            # GENERAR PNG
            # -------------------------------------------------

            self.ruta_diagrama = generar_diagrama(
                self.automata,
                ruta_base,
                formato="png",
                abrir=False
            )

            # -------------------------------------------------
            # CARGAR IMAGEN
            # -------------------------------------------------

            with Image.open(
                self.ruta_diagrama
            ) as imagen_original:

                imagen = (
                    imagen_original
                    .convert("RGBA")
                    .copy()
                )

            # -------------------------------------------------
            # CALCULAR TAMAÑO
            # -------------------------------------------------

            ancho_original = imagen.width
            alto_original = imagen.height

            ancho_maximo = 900
            alto_maximo = 430

            escala_ancho = (
                ancho_maximo
                / ancho_original
            )

            escala_alto = (
                alto_maximo
                / alto_original
            )

            escala = min(
                escala_ancho,
                escala_alto,
                1
            )

            ancho_final = max(
                1,
                int(
                    ancho_original
                    * escala
                )
            )

            alto_final = max(
                1,
                int(
                    alto_original
                    * escala
                )
            )

            # -------------------------------------------------
            # CREAR IMAGEN DE CUSTOMTKINTER
            # -------------------------------------------------

            self.imagen_ctk = ctk.CTkImage(
                light_image=imagen,
                dark_image=imagen,
                size=(
                    ancho_final,
                    alto_final
                )
            )

            # -------------------------------------------------
            # MOSTRAR
            # -------------------------------------------------

            self.lbl_diagrama.configure(
                image=self.imagen_ctk,
                text=""
            )

            self.lbl_estado.configure(
                text=(
                    "Diagrama generado correctamente."
                )
            )

            self.ventana_principal.lbl_estado.configure(
                text=(
                    f"Estado: {self.tipo} - "
                    f"{self.automata.nombre} | "
                    f"Diagrama generado"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error al generar diagrama",
                (
                    "No fue posible generar "
                    "el diagrama.\n\n"
                    f"Detalle: {error}"
                )
            )