import os
import tkinter as tk

import customtkinter as ctk

from tkinter import messagebox

from PIL import Image, ImageTk

from utilidades.graficador import (
    generar_diagrama
)

from utilidades.registro_logs import (
    registrar_info,
    registrar_warning,
    registrar_error
)

from utilidades.tema import (
    FONDO_APP,
    FONDO_ENTRADA,
    TEXTO_TITULO,
    TEXTO_NORMAL,
    TEXTO_SUAVE,
    BOTON_PRINCIPAL,
    BOTON_PRINCIPAL_HOVER,
    TEXTO_BOTON,
    COLOR_BORDE,
    COLOR_EXITO,
    COLOR_ADVERTENCIA,
    COLOR_ERROR
)


# =============================================================
# VENTANA AMPLIADA DEL DIAGRAMA
# =============================================================

class VentanaDiagramaAmpliado(
    ctk.CTkToplevel
):

    def __init__(
        self,
        master,
        imagen_original,
        automata,
        alias_estados
    ):
        super().__init__(
            master
        )

        self.imagen_original = (
            imagen_original.copy()
        )

        self.automata = automata

        self.alias_estados = (
            alias_estados.copy()
        )

        self.imagen_tk = None

        self.factor_zoom = 1.0

        self.modo_ajuste = True

        self._ajuste_pendiente = None

        self.title(
            "Diagrama del autómata"
        )

        self.geometry(
            "1200x780"
        )

        self.minsize(
            800,
            550
        )

        self.configure(
            fg_color=FONDO_APP
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        self.crear_encabezado()

        self.crear_controles()

        self.crear_area_diagrama()

        self.actualizar_leyenda()

        self.after(
            150,
            self.ajustar_a_ventana
        )

        self.after(
            200,
            self.lift
        )

    # =========================================================
    # COLOR ACTUAL
    # =========================================================

    def resolver_color(
        self,
        color
    ):

        if isinstance(
            color,
            (tuple, list)
        ):

            if (
                ctk.get_appearance_mode()
                == "Dark"
            ):

                return color[1]

            return color[0]

        return color

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame.grid(
            row=0,
            column=0,
            padx=20,
            pady=(15, 5),
            sticky="ew"
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            frame,
            text=(
                "DIAGRAMA DEL AUTÓMATA"
            ),
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            pady=(0, 3)
        )

        ctk.CTkLabel(
            frame,
            text=(
                f"{self.automata.nombre}"
            ),
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=14
            )
        ).grid(
            row=1,
            column=0
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
            row=1,
            column=0,
            padx=20,
            pady=5
        )

        self.btn_alejar = ctk.CTkButton(
            self.frame_controles,
            text="−",
            width=45,
            height=36,
            command=self.alejar,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.btn_alejar.grid(
            row=0,
            column=0,
            padx=4
        )

        self.btn_ajustar = ctk.CTkButton(
            self.frame_controles,
            text="Ajustar",
            width=95,
            height=36,
            command=self.ajustar_a_ventana,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_ajustar.grid(
            row=0,
            column=1,
            padx=4
        )

        self.btn_acercar = ctk.CTkButton(
            self.frame_controles,
            text="+",
            width=45,
            height=36,
            command=self.acercar,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.btn_acercar.grid(
            row=0,
            column=2,
            padx=4
        )

        self.btn_100 = ctk.CTkButton(
            self.frame_controles,
            text="100 %",
            width=75,
            height=36,
            command=self.tamano_original,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_100.grid(
            row=0,
            column=3,
            padx=4
        )

        self.lbl_zoom = ctk.CTkLabel(
            self.frame_controles,
            text="100 %",
            text_color=TEXTO_NORMAL,
            width=60,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        self.lbl_zoom.grid(
            row=0,
            column=4,
            padx=(10, 4)
        )

    # =========================================================
    # ÁREA DEL DIAGRAMA
    # =========================================================

    def crear_area_diagrama(self):

        self.frame_diagrama = ctk.CTkFrame(
            self,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_diagrama.grid(
            row=2,
            column=0,
            padx=20,
            pady=(5, 20),
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

        # -----------------------------------------------------
        # CANVAS
        # -----------------------------------------------------

        self.canvas_diagrama = tk.Canvas(
            self.frame_diagrama,
            bg=self.resolver_color(
                FONDO_ENTRADA
            ),
            highlightthickness=0,
            bd=0
        )

        self.canvas_diagrama.grid(
            row=0,
            column=0,
            padx=(12, 0),
            pady=(12, 0),
            sticky="nsew"
        )

        # -----------------------------------------------------
        # SCROLL VERTICAL
        # -----------------------------------------------------

        self.scroll_vertical = (
            ctk.CTkScrollbar(
                self.frame_diagrama,
                orientation="vertical",
                command=(
                    self.canvas_diagrama
                    .yview
                )
            )
        )

        self.scroll_vertical.grid(
            row=0,
            column=1,
            padx=(5, 10),
            pady=(12, 0),
            sticky="ns"
        )

        # -----------------------------------------------------
        # SCROLL HORIZONTAL
        # -----------------------------------------------------

        self.scroll_horizontal = (
            ctk.CTkScrollbar(
                self.frame_diagrama,
                orientation="horizontal",
                command=(
                    self.canvas_diagrama
                    .xview
                )
            )
        )

        self.scroll_horizontal.grid(
            row=1,
            column=0,
            padx=(12, 0),
            pady=(5, 0),
            sticky="ew"
        )

        self.canvas_diagrama.configure(
            xscrollcommand=(
                self.scroll_horizontal.set
            ),
            yscrollcommand=(
                self.scroll_vertical.set
            )
        )

        self.canvas_diagrama.bind(
            "<Configure>",
            self.al_redimensionar
        )

        # -----------------------------------------------------
        # LEYENDA DE SÍMBOLOS
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_diagrama,
            text=(
                "→ Estado inicial     "
                "Doble círculo = Estado final     "
                "ε = Transición vacía"
            ),
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=12
            )
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            padx=20,
            pady=(8, 4)
        )

        # -----------------------------------------------------
        # LEYENDA DE ESTADOS
        # -----------------------------------------------------

        self.txt_leyenda = ctk.CTkTextbox(
            self.frame_diagrama,
            height=95,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_width=1,
            border_color=COLOR_BORDE,
            font=(
                "Consolas",
                12
            )
        )

        self.txt_leyenda.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=15,
            pady=(5, 12),
            sticky="ew"
        )

        self.txt_leyenda.configure(
            state="disabled"
        )

    # =========================================================
    # ACTUALIZAR LEYENDA
    # =========================================================

    def actualizar_leyenda(self):

        lineas = []

        for estado in sorted(
            self.automata.estados
        ):

            alias = (
                self.alias_estados[
                    estado
                ]
            )

            indicadores = []

            if (
                estado
                == self.automata.estado_inicial
            ):

                indicadores.append(
                    "inicial"
                )

            if (
                estado
                in self.automata.estados_finales
            ):

                indicadores.append(
                    "final"
                )

            detalle = ""

            if indicadores:

                detalle = (
                    "  ["
                    + ", ".join(
                        indicadores
                    )
                    + "]"
                )

            lineas.append(
                f"{alias} = {estado}{detalle}"
            )

        self.txt_leyenda.configure(
            state="normal"
        )

        self.txt_leyenda.delete(
            "1.0",
            "end"
        )

        self.txt_leyenda.insert(
            "end",
            "\n".join(
                lineas
            )
        )

        self.txt_leyenda.configure(
            state="disabled"
        )

    # =========================================================
    # MOSTRAR IMAGEN
    # =========================================================

    def mostrar_imagen(self):

        if self.imagen_original is None:

            return

        ancho = max(
            1,
            int(
                self.imagen_original.width
                * self.factor_zoom
            )
        )

        alto = max(
            1,
            int(
                self.imagen_original.height
                * self.factor_zoom
            )
        )

        try:

            filtro = Image.Resampling.LANCZOS

        except AttributeError:

            filtro = Image.LANCZOS

        imagen = self.imagen_original.resize(
            (
                ancho,
                alto
            ),
            filtro
        )

        self.imagen_tk = ImageTk.PhotoImage(
            imagen
        )

        self.canvas_diagrama.delete(
            "all"
        )

        self.canvas_diagrama.update_idletasks()

        ancho_canvas = max(
            self.canvas_diagrama.winfo_width(),
            1
        )

        alto_canvas = max(
            self.canvas_diagrama.winfo_height(),
            1
        )

        posicion_x = max(
            (
                ancho_canvas
                - ancho
            ) // 2,
            0
        )

        posicion_y = max(
            (
                alto_canvas
                - alto
            ) // 2,
            0
        )

        self.canvas_diagrama.create_image(
            posicion_x,
            posicion_y,
            image=self.imagen_tk,
            anchor="nw"
        )

        ancho_region = max(
            ancho_canvas,
            posicion_x + ancho
        )

        alto_region = max(
            alto_canvas,
            posicion_y + alto
        )

        self.canvas_diagrama.configure(
            scrollregion=(
                0,
                0,
                ancho_region,
                alto_region
            )
        )

        porcentaje = int(
            round(
                self.factor_zoom
                * 100
            )
        )

        self.lbl_zoom.configure(
            text=f"{porcentaje} %"
        )

    # =========================================================
    # AJUSTAR
    # =========================================================

    def ajustar_a_ventana(self):

        if self.imagen_original is None:

            return

        self.modo_ajuste = True

        self.update_idletasks()

        self.canvas_diagrama.update_idletasks()

        ancho_disponible = (
            self.canvas_diagrama.winfo_width()
            - 40
        )

        alto_disponible = (
            self.canvas_diagrama.winfo_height()
            - 40
        )

        if ancho_disponible <= 100:

            ancho_disponible = 1000

        if alto_disponible <= 100:

            alto_disponible = 500

        escala_ancho = (
            ancho_disponible
            / self.imagen_original.width
        )

        escala_alto = (
            alto_disponible
            / self.imagen_original.height
        )

        self.factor_zoom = min(
            escala_ancho,
            escala_alto,
            1.0
        )

        self.factor_zoom = max(
            0.05,
            self.factor_zoom
        )

        self.mostrar_imagen()

    # =========================================================
    # ACERCAR
    # =========================================================

    def acercar(self):

        self.modo_ajuste = False

        self.factor_zoom = min(
            3.0,
            self.factor_zoom + 0.10
        )

        self.mostrar_imagen()

    # =========================================================
    # ALEJAR
    # =========================================================

    def alejar(self):

        self.modo_ajuste = False

        self.factor_zoom = max(
            0.05,
            self.factor_zoom - 0.10
        )

        self.mostrar_imagen()

    # =========================================================
    # 100 %
    # =========================================================

    def tamano_original(self):

        self.modo_ajuste = False

        self.factor_zoom = 1.0

        self.mostrar_imagen()

    # =========================================================
    # REDIMENSIONAR
    # =========================================================

    def al_redimensionar(
        self,
        event
    ):

        if not self.modo_ajuste:

            return

        if self._ajuste_pendiente is not None:

            try:

                self.after_cancel(
                    self._ajuste_pendiente
                )

            except Exception:

                pass

        self._ajuste_pendiente = self.after(
            100,
            self.ajustar_a_ventana
        )


# =============================================================
# VISOR PRINCIPAL
# =============================================================

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

        self.ruta_diagrama = None

        self.imagen_original = None

        self.imagen_tk = None

        self.factor_zoom = 1.0

        self.modo_ajuste = True

        self.alias_estados = {}

        self._ajuste_pendiente = None

        self.ventana_ampliada = None

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            4,
            weight=1
        )

        self.crear_encabezado()

        self.crear_informacion()

        self.crear_controles()

        self.crear_area_diagrama()

        if self.automata is not None:

            self.generar_y_mostrar_diagrama()

        else:

            self.mostrar_sin_automata()

    # =========================================================
    # COLOR
    # =========================================================

    def resolver_color(
        self,
        color
    ):

        if isinstance(
            color,
            (tuple, list)
        ):

            if (
                ctk.get_appearance_mode()
                == "Dark"
            ):

                return color[1]

            return color[0]

        return color

    # =========================================================
    # GENERAR A, B, C...
    # =========================================================

    def generar_alias(
        self,
        indice
    ):

        resultado = ""

        numero = indice

        while True:

            resultado = (
                chr(
                    65
                    + (
                        numero % 26
                    )
                )
                + resultado
            )

            numero = (
                numero // 26
            ) - 1

            if numero < 0:

                break

        return resultado

    # =========================================================
    # PREPARAR ALIAS
    # =========================================================

    def preparar_alias_estados(self):

        self.alias_estados = {}

        if self.automata is None:

            return

        for indice, estado in enumerate(
            sorted(
                self.automata.estados
            )
        ):

            self.alias_estados[
                estado
            ] = self.generar_alias(
                indice
            )

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        ctk.CTkLabel(
            self,
            text="DIAGRAMA DEL AUTÓMATA",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            self,
            text=(
                "Representación gráfica del autómata "
                "con estados simplificados mediante leyenda."
            ),
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=14
            )
        ).grid(
            row=1,
            column=0,
            pady=(0, 12)
        )

    # =========================================================
    # INFORMACIÓN
    # =========================================================

    def crear_informacion(self):

        self.frame_info = ctk.CTkFrame(
            self,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_info.grid(
            row=2,
            column=0,
            padx=30,
            pady=(5, 8),
            sticky="ew"
        )

        self.frame_info.grid_columnconfigure(
            1,
            weight=1
        )

        self.frame_info.grid_columnconfigure(
            3,
            weight=1
        )

        if self.automata is None:

            ctk.CTkLabel(
                self.frame_info,
                text=(
                    "No hay ningún autómata cargado."
                ),
                text_color=COLOR_ADVERTENCIA,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=0,
                columnspan=4,
                padx=20,
                pady=20
            )

            return

        ctk.CTkLabel(
            self.frame_info,
            text="Tipo:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=(20, 8),
            pady=6,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.tipo,
            text_color=TEXTO_NORMAL
        ).grid(
            row=0,
            column=1,
            padx=8,
            pady=6,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Autómata:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=(20, 8),
            pady=6,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.automata.nombre,
            text_color=TEXTO_NORMAL,
            wraplength=800,
            justify="left"
        ).grid(
            row=1,
            column=1,
            columnspan=3,
            padx=8,
            pady=6,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Estados:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=(20, 8),
            pady=(6, 14),
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=str(
                len(
                    self.automata.estados
                )
            ),
            text_color=TEXTO_NORMAL
        ).grid(
            row=2,
            column=1,
            padx=8,
            pady=(6, 14),
            sticky="w"
        )

        cantidad = sum(
            len(destinos)
            for destinos
            in self.automata.transiciones.values()
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Transiciones:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=2,
            column=2,
            padx=(30, 8),
            pady=(6, 14),
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=str(
                cantidad
            ),
            text_color=TEXTO_NORMAL
        ).grid(
            row=2,
            column=3,
            padx=(8, 20),
            pady=(6, 14),
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
            pady=(0, 6),
            sticky="ew"
        )

        self.frame_controles.grid_columnconfigure(
            0,
            weight=1
        )

        self.lbl_estado = ctk.CTkLabel(
            self.frame_controles,
            text="",
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        self.lbl_estado.grid(
            row=0,
            column=0,
            padx=10,
            pady=6,
            sticky="w"
        )

        # -----------------------------------------------------
        # ACTUALIZAR
        # -----------------------------------------------------

        self.btn_actualizar = ctk.CTkButton(
            self.frame_controles,
            text="Actualizar diagrama",
            width=165,
            height=36,
            command=self.generar_y_mostrar_diagrama,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_actualizar.grid(
            row=0,
            column=1,
            padx=5
        )

        # -----------------------------------------------------
        # ABRIR EN VENTANA
        # -----------------------------------------------------

        self.btn_ventana = ctk.CTkButton(
            self.frame_controles,
            text="Abrir en ventana",
            width=155,
            height=36,
            command=self.abrir_ventana_ampliada,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_ventana.grid(
            row=0,
            column=2,
            padx=5
        )

        # -----------------------------------------------------
        # ZOOM
        # -----------------------------------------------------

        self.frame_zoom = ctk.CTkFrame(
            self.frame_controles,
            fg_color="transparent"
        )

        self.frame_zoom.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=10,
            pady=(4, 0)
        )

        self.btn_alejar = ctk.CTkButton(
            self.frame_zoom,
            text="−",
            width=42,
            height=34,
            command=self.alejar,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_alejar.grid(
            row=0,
            column=0,
            padx=3
        )

        self.btn_ajustar = ctk.CTkButton(
            self.frame_zoom,
            text="Ajustar",
            width=82,
            height=34,
            command=self.ajustar_a_ventana,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_ajustar.grid(
            row=0,
            column=1,
            padx=3
        )

        self.btn_acercar = ctk.CTkButton(
            self.frame_zoom,
            text="+",
            width=42,
            height=34,
            command=self.acercar,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_acercar.grid(
            row=0,
            column=2,
            padx=3
        )

        self.lbl_zoom = ctk.CTkLabel(
            self.frame_zoom,
            text="100 %",
            width=55,
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        self.lbl_zoom.grid(
            row=0,
            column=3,
            padx=(8, 3)
        )

        if self.automata is None:

            for boton in (
                self.btn_actualizar,
                self.btn_ventana,
                self.btn_alejar,
                self.btn_ajustar,
                self.btn_acercar
            ):

                boton.configure(
                    state="disabled"
                )

    # =========================================================
    # ÁREA DEL DIAGRAMA
    # =========================================================

    def crear_area_diagrama(self):

        self.frame_diagrama = ctk.CTkFrame(
            self,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_diagrama.grid(
            row=4,
            column=0,
            padx=30,
            pady=(2, 20),
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

        self.canvas_diagrama = tk.Canvas(
            self.frame_diagrama,
            bg=self.resolver_color(
                FONDO_ENTRADA
            ),
            highlightthickness=0,
            bd=0
        )

        self.canvas_diagrama.grid(
            row=0,
            column=0,
            padx=(12, 0),
            pady=(12, 0),
            sticky="nsew"
        )

        self.scroll_vertical = (
            ctk.CTkScrollbar(
                self.frame_diagrama,
                orientation="vertical",
                command=self.canvas_diagrama.yview
            )
        )

        self.scroll_vertical.grid(
            row=0,
            column=1,
            padx=(5, 10),
            pady=(12, 0),
            sticky="ns"
        )

        self.scroll_horizontal = (
            ctk.CTkScrollbar(
                self.frame_diagrama,
                orientation="horizontal",
                command=self.canvas_diagrama.xview
            )
        )

        self.scroll_horizontal.grid(
            row=1,
            column=0,
            padx=(12, 0),
            pady=(5, 0),
            sticky="ew"
        )

        self.canvas_diagrama.configure(
            xscrollcommand=(
                self.scroll_horizontal.set
            ),
            yscrollcommand=(
                self.scroll_vertical.set
            )
        )

        self.canvas_diagrama.bind(
            "<Configure>",
            self.al_redimensionar
        )

        self.lbl_simbolos = ctk.CTkLabel(
            self.frame_diagrama,
            text=(
                "→ Estado inicial     "
                "Doble círculo = Estado final     "
                "ε = Transición vacía"
            ),
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=12
            )
        )

        self.lbl_simbolos.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=20,
            pady=(7, 4)
        )

        self.frame_leyenda = ctk.CTkFrame(
            self.frame_diagrama,
            fg_color="transparent"
        )

        self.frame_leyenda.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        self.frame_leyenda.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_leyenda,
            text="Leyenda de estados",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            pady=(2, 4)
        )

        self.txt_leyenda = ctk.CTkTextbox(
            self.frame_leyenda,
            height=75,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_width=1,
            border_color=COLOR_BORDE,
            font=(
                "Consolas",
                12
            )
        )

        self.txt_leyenda.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.txt_leyenda.configure(
            state="disabled"
        )

        self.frame_leyenda.grid_remove()

        self.mostrar_texto_canvas(
            "El diagrama aparecerá aquí."
        )

    # =========================================================
    # TEXTO EN CANVAS
    # =========================================================

    def mostrar_texto_canvas(
        self,
        texto
    ):

        self.canvas_diagrama.delete(
            "all"
        )

        self.canvas_diagrama.update_idletasks()

        ancho = max(
            self.canvas_diagrama.winfo_width(),
            300
        )

        alto = max(
            self.canvas_diagrama.winfo_height(),
            220
        )

        self.canvas_diagrama.create_text(
            ancho // 2,
            alto // 2,
            text=texto,
            fill=self.resolver_color(
                TEXTO_SUAVE
            ),
            font=(
                "Arial",
                14,
                "bold"
            ),
            justify="center"
        )

    # =========================================================
    # LEYENDA
    # =========================================================

    def actualizar_leyenda(self):

        lineas = []

        for estado in sorted(
            self.automata.estados
        ):

            alias = self.alias_estados[
                estado
            ]

            indicadores = []

            if (
                estado
                == self.automata.estado_inicial
            ):

                indicadores.append(
                    "inicial"
                )

            if (
                estado
                in self.automata.estados_finales
            ):

                indicadores.append(
                    "final"
                )

            detalle = ""

            if indicadores:

                detalle = (
                    "  ["
                    + ", ".join(
                        indicadores
                    )
                    + "]"
                )

            lineas.append(
                f"{alias} = {estado}{detalle}"
            )

        self.txt_leyenda.configure(
            state="normal"
        )

        self.txt_leyenda.delete(
            "1.0",
            "end"
        )

        self.txt_leyenda.insert(
            "end",
            "\n".join(
                lineas
            )
        )

        self.txt_leyenda.configure(
            state="disabled"
        )

        self.frame_leyenda.grid()

    # =========================================================
    # SIN AUTÓMATA
    # =========================================================

    def mostrar_sin_automata(self):

        self.mostrar_texto_canvas(
            (
                "No hay un autómata disponible.\n\n"
                "Primero cree un AFD o AFN."
            )
        )

        self.lbl_estado.configure(
            text="Sin autómata cargado.",
            text_color=COLOR_ADVERTENCIA
        )

    # =========================================================
    # MOSTRAR IMAGEN
    # =========================================================

    def mostrar_imagen(self):

        if self.imagen_original is None:

            return

        ancho = max(
            1,
            int(
                self.imagen_original.width
                * self.factor_zoom
            )
        )

        alto = max(
            1,
            int(
                self.imagen_original.height
                * self.factor_zoom
            )
        )

        try:

            filtro = Image.Resampling.LANCZOS

        except AttributeError:

            filtro = Image.LANCZOS

        imagen = self.imagen_original.resize(
            (
                ancho,
                alto
            ),
            filtro
        )

        self.imagen_tk = ImageTk.PhotoImage(
            imagen
        )

        self.canvas_diagrama.delete(
            "all"
        )

        self.canvas_diagrama.update_idletasks()

        ancho_canvas = max(
            self.canvas_diagrama.winfo_width(),
            1
        )

        alto_canvas = max(
            self.canvas_diagrama.winfo_height(),
            1
        )

        posicion_x = max(
            (
                ancho_canvas
                - ancho
            ) // 2,
            0
        )

        posicion_y = max(
            (
                alto_canvas
                - alto
            ) // 2,
            0
        )

        self.canvas_diagrama.create_image(
            posicion_x,
            posicion_y,
            image=self.imagen_tk,
            anchor="nw"
        )

        self.canvas_diagrama.configure(
            scrollregion=(
                0,
                0,
                max(
                    ancho_canvas,
                    posicion_x + ancho
                ),
                max(
                    alto_canvas,
                    posicion_y + alto
                )
            )
        )

        porcentaje = int(
            round(
                self.factor_zoom
                * 100
            )
        )

        self.lbl_zoom.configure(
            text=f"{porcentaje} %"
        )

    # =========================================================
    # AJUSTAR
    # =========================================================

    def ajustar_a_ventana(self):

        if self.imagen_original is None:

            return

        self.modo_ajuste = True

        self.update_idletasks()

        ancho_disponible = (
            self.canvas_diagrama.winfo_width()
            - 40
        )

        alto_disponible = (
            self.canvas_diagrama.winfo_height()
            - 40
        )

        if ancho_disponible <= 100:

            ancho_disponible = 850

        if alto_disponible <= 100:

            alto_disponible = 350

        self.factor_zoom = min(
            (
                ancho_disponible
                / self.imagen_original.width
            ),
            (
                alto_disponible
                / self.imagen_original.height
            ),
            1.0
        )

        self.factor_zoom = max(
            0.05,
            self.factor_zoom
        )

        self.mostrar_imagen()

    # =========================================================
    # ACERCAR
    # =========================================================

    def acercar(self):

        if self.imagen_original is None:

            return

        self.modo_ajuste = False

        self.factor_zoom = min(
            3.0,
            self.factor_zoom + 0.10
        )

        self.mostrar_imagen()

    # =========================================================
    # ALEJAR
    # =========================================================

    def alejar(self):

        if self.imagen_original is None:

            return

        self.modo_ajuste = False

        self.factor_zoom = max(
            0.05,
            self.factor_zoom - 0.10
        )

        self.mostrar_imagen()

    # =========================================================
    # REDIMENSIONAR
    # =========================================================

    def al_redimensionar(
        self,
        event
    ):

        if (
            self.imagen_original is None
            or not self.modo_ajuste
        ):

            return

        if self._ajuste_pendiente is not None:

            try:

                self.after_cancel(
                    self._ajuste_pendiente
                )

            except Exception:

                pass

        self._ajuste_pendiente = self.after(
            100,
            self.ajustar_a_ventana
        )

    # =========================================================
    # ABRIR VENTANA AMPLIADA
    # =========================================================

    def abrir_ventana_ampliada(self):

        if (
            self.imagen_original is None
            or self.automata is None
        ):

            self.ventana_principal.actualizar_barra_estado(
                "Estado: No hay un diagrama para visualizar.",
                "advertencia"
            )

            messagebox.showwarning(
                "Sin diagrama",
                (
                    "Primero debe generarse "
                    "el diagrama."
                )
            )

            return

        try:

            if (
                self.ventana_ampliada
                is not None
                and self.ventana_ampliada.winfo_exists()
            ):

                self.ventana_ampliada.lift()

                self.ventana_ampliada.focus()

                self.ventana_principal.actualizar_barra_estado(
                    (
                        f"Estado: {self.tipo} - "
                        f"{self.automata.nombre} | "
                        "Diagrama abierto en ventana"
                    ),
                    "exito"
                )

                return

        except Exception:

            self.ventana_ampliada = None

        self.ventana_ampliada = (
            VentanaDiagramaAmpliado(
                self,
                self.imagen_original,
                self.automata,
                self.alias_estados
            )
        )

        self.ventana_principal.actualizar_barra_estado(
            (
                f"Estado: {self.tipo} - "
                f"{self.automata.nombre} | "
                "Diagrama abierto en ventana"
            ),
            "exito"
        )

        registrar_info(
            "DIAGRAMA",
            (
                "Diagrama abierto "
                "en ventana ampliada"
            )
        )

    # =========================================================
    # GENERAR DIAGRAMA
    # =========================================================

    def generar_y_mostrar_diagrama(self):

        if self.automata is None:

            registrar_warning(
                "DIAGRAMA",
                (
                    "Se intentó generar un diagrama "
                    "sin un autómata cargado"
                )
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    "Estado: No hay un autómata "
                    "para visualizar."
                ),
                "advertencia"
            )

            messagebox.showwarning(
                "Sin autómata",
                (
                    "Primero debe crear un "
                    "AFD o AFN."
                )
            )

            return

        try:

            self.lbl_estado.configure(
                text="Generando diagrama...",
                text_color=TEXTO_SUAVE
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    f"Estado: {self.tipo} - "
                    f"{self.automata.nombre} | "
                    "Generando diagrama..."
                ),
                "normal"
            )

            self.preparar_alias_estados()

            if (
                len(
                    self.automata.estados
                )
                <= 7
            ):

                orientacion = "LR"

            else:

                orientacion = "TB"

            ruta_base = os.path.join(
                "recursos",
                "diagramas",
                "automata_actual"
            )

            self.ruta_diagrama = generar_diagrama(
                self.automata,
                ruta_base,
                formato="png",
                abrir=False,
                etiquetas_estados=(
                    self.alias_estados
                ),
                rankdir=orientacion
            )

            with Image.open(
                self.ruta_diagrama
            ) as imagen_original:

                self.imagen_original = (
                    imagen_original
                    .convert("RGBA")
                    .copy()
                )

            self.actualizar_leyenda()

            self.modo_ajuste = True

            self.factor_zoom = 1.0

            self.after(
                120,
                self.ajustar_a_ventana
            )

            self.lbl_estado.configure(
                text=(
                    "Diagrama generado correctamente."
                ),
                text_color=COLOR_EXITO
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    f"Estado: {self.tipo} - "
                    f"{self.automata.nombre} | "
                    "Diagrama generado"
                ),
                "exito"
            )

            registrar_info(
                "DIAGRAMA",
                (
                    f"Diagrama generado correctamente "
                    f"para {self.tipo} "
                    f"{self.automata.nombre}"
                )
            )

        except Exception as error:

            self.lbl_estado.configure(
                text=(
                    "No fue posible generar "
                    "el diagrama."
                ),
                text_color=COLOR_ERROR
            )

            self.ventana_principal.actualizar_barra_estado(
                "Estado: Error al generar el diagrama.",
                "error"
            )

            registrar_error(
                "DIAGRAMA",
                (
                    "No fue posible generar el "
                    f"diagrama de "
                    f"{self.automata.nombre}: "
                    f"{error}"
                )
            )

            messagebox.showerror(
                "Error al generar diagrama",
                (
                    "No fue posible generar "
                    "el diagrama.\n\n"
                    f"Detalle: {error}"
                )
            )