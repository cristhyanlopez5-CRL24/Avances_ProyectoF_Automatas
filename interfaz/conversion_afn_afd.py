import customtkinter as ctk

from tkinter import messagebox

from algoritmos.conversion import (
    convertir_afn_a_afd,
    obtener_tabla_conversion,
    formatear_conversion
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


class ConversionAFNaAFDFrame(
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

        self.automata = (
            ventana_principal.automata_actual
        )

        self.tipo = (
            ventana_principal.tipo_automata_actual
        )

        self.afd_convertido = None

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.crear_encabezado()

        self.crear_informacion_afn()

        self.crear_controles()

        self.crear_resultado()

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        lbl_titulo = ctk.CTkLabel(
            self,
            text="CONVERSIÓN AFN → AFD",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        lbl_titulo.grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        lbl_descripcion = ctk.CTkLabel(
            self,
            text=(
                "Convierte un Autómata Finito "
                "No Determinista en un AFD "
                "equivalente mediante construcción "
                "de subconjuntos."
            ),
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=14
            ),
            wraplength=850,
            justify="center"
        )

        lbl_descripcion.grid(
            row=1,
            column=0,
            padx=30,
            pady=(0, 15)
        )

    # =========================================================
    # INFORMACIÓN DEL AFN
    # =========================================================

    def crear_informacion_afn(self):

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
            pady=10,
            sticky="ew"
        )

        self.frame_info.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_info,
            text="AFN cargado",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(18, 10)
        )

        # -----------------------------------------------------
        # NO HAY AUTÓMATA
        # -----------------------------------------------------

        if self.automata is None:

            ctk.CTkLabel(
                self.frame_info,
                text=(
                    "No hay ningún autómata cargado.\n"
                    "Primero debe crear un AFN."
                ),
                text_color=COLOR_ADVERTENCIA,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).grid(
                row=1,
                column=0,
                columnspan=2,
                padx=20,
                pady=(5, 25)
            )

            return

        # -----------------------------------------------------
        # NO ES AFN
        # -----------------------------------------------------

        if self.tipo != "AFN":

            ctk.CTkLabel(
                self.frame_info,
                text=(
                    f"El autómata actual es de tipo "
                    f"{self.tipo}.\n"
                    "La conversión AFN → AFD solamente "
                    "puede realizarse sobre un AFN."
                ),
                text_color=COLOR_ADVERTENCIA,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).grid(
                row=1,
                column=0,
                columnspan=2,
                padx=20,
                pady=(5, 25)
            )

            return

        # -----------------------------------------------------
        # TIPO
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_info,
            text="Tipo:",
            text_color=TEXTO_NORMAL,
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
            text="AFN",
            text_color=TEXTO_NORMAL
        ).grid(
            row=1,
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
            text_color=TEXTO_NORMAL,
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
            text=self.automata.nombre,
            text_color=TEXTO_NORMAL,
            wraplength=700,
            justify="left"
        ).grid(
            row=2,
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
            text_color=TEXTO_NORMAL,
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
            text=estados,
            text_color=TEXTO_NORMAL,
            wraplength=700,
            justify="left"
        ).grid(
            row=3,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ALFABETO
        # -----------------------------------------------------

        alfabeto = (
            "{"
            + ", ".join(
                sorted(
                    self.automata.alfabeto
                )
            )
            + "}"
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Alfabeto:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=4,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=alfabeto,
            text_color=TEXTO_NORMAL
        ).grid(
            row=4,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ESTADO INICIAL
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_info,
            text="Estado inicial:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=5,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.automata.estado_inicial,
            text_color=TEXTO_NORMAL
        ).grid(
            row=5,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ESTADOS FINALES
        # -----------------------------------------------------

        finales = (
            "{"
            + ", ".join(
                sorted(
                    self.automata.estados_finales
                )
            )
            + "}"
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Estados finales:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=6,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=finales,
            text_color=TEXTO_NORMAL
        ).grid(
            row=6,
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
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=7,
            column=0,
            padx=20,
            pady=(7, 18),
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=str(
                cantidad
            ),
            text_color=TEXTO_NORMAL
        ).grid(
            row=7,
            column=1,
            padx=20,
            pady=(7, 18),
            sticky="w"
        )

    # =========================================================
    # CONTROLES
    # =========================================================

    def crear_controles(self):

        self.frame_controles = ctk.CTkFrame(
            self,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_controles.grid(
            row=3,
            column=0,
            padx=30,
            pady=10,
            sticky="ew"
        )

        self.frame_controles.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_controles.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_controles,
            text="Conversión",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(18, 5)
        )

        self.lbl_estado_conversion = ctk.CTkLabel(
            self.frame_controles,
            text=(
                "Presione Convertir para iniciar "
                "la construcción de subconjuntos."
            ),
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=14
            )
        )

        self.lbl_estado_conversion.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=20,
            pady=(5, 12)
        )

        self.btn_convertir = ctk.CTkButton(
            self.frame_controles,
            text="Convertir AFN → AFD",
            width=210,
            height=42,
            command=self.convertir,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_convertir.grid(
            row=2,
            column=0,
            padx=(20, 10),
            pady=(5, 20),
            sticky="e"
        )

        self.btn_usar_afd = ctk.CTkButton(
            self.frame_controles,
            text="Usar AFD convertido",
            width=210,
            height=42,
            command=self.usar_afd_convertido,
            state="disabled",
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            text_color_disabled=(
                "#969696",
                "#A8A8A8"
            )
        )

        self.btn_usar_afd.grid(
            row=2,
            column=1,
            padx=(10, 20),
            pady=(5, 20),
            sticky="w"
        )

        if (
            self.automata is None
            or self.tipo != "AFN"
        ):

            self.btn_convertir.configure(
                state="disabled"
            )

            self.lbl_estado_conversion.configure(
                text=(
                    "Debe cargar un AFN para "
                    "utilizar esta función."
                ),
                text_color=COLOR_ADVERTENCIA
            )

    # =========================================================
    # RESULTADO
    # =========================================================

    def crear_resultado(self):

        self.frame_resultado = ctk.CTkFrame(
            self,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_resultado.grid(
            row=4,
            column=0,
            padx=30,
            pady=(10, 30),
            sticky="ew"
        )

        self.frame_resultado.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_resultado,
            text="Resultado de la conversión",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 5)
        )

        self.lbl_resumen = ctk.CTkLabel(
            self.frame_resultado,
            text=(
                "Todavía no se ha realizado "
                "ninguna conversión."
            ),
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.lbl_resumen.grid(
            row=1,
            column=0,
            padx=20,
            pady=10
        )

        self.txt_resultado = ctk.CTkTextbox(
            self.frame_resultado,
            height=390,
            font=(
                "Consolas",
                14
            ),
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_width=1,
            border_color=COLOR_BORDE
        )

        self.txt_resultado.grid(
            row=2,
            column=0,
            padx=20,
            pady=(5, 20),
            sticky="ew"
        )

        self.txt_resultado.configure(
            state="disabled"
        )

    # =========================================================
    # CONVERTIR
    # =========================================================

    def convertir(self):

        if self.automata is None:

            registrar_warning(
                "CONVERSION",
                (
                    "Se intentó convertir un AFN "
                    "sin un autómata cargado"
                )
            )

            messagebox.showwarning(
                "Sin autómata",
                "Primero debe crear un AFN."
            )

            return

        if self.tipo != "AFN":

            registrar_warning(
                "CONVERSION",
                (
                    "Se intentó realizar una conversión "
                    f"AFN → AFD utilizando un {self.tipo}"
                )
            )

            messagebox.showwarning(
                "Tipo incorrecto",
                (
                    "La conversión AFN → AFD "
                    "solamente puede utilizarse "
                    "sobre un AFN."
                )
            )

            return

        try:

            self.afd_convertido = (
                convertir_afn_a_afd(
                    self.automata
                )
            )

            texto = formatear_conversion(
                self.afd_convertido
            )

            tabla = obtener_tabla_conversion(
                self.afd_convertido
            )

            texto_tabla = (
                self.formatear_tabla(
                    tabla
                )
            )

            texto_completo = (
                texto
                + "\n\n"
                + "=" * 60
                + "\n"
                + "TABLA DE TRANSICIÓN\n"
                + "=" * 60
                + "\n\n"
                + texto_tabla
            )

            self.txt_resultado.configure(
                state="normal"
            )

            self.txt_resultado.delete(
                "1.0",
                "end"
            )

            self.txt_resultado.insert(
                "end",
                texto_completo
            )

            self.txt_resultado.configure(
                state="disabled"
            )

            cantidad_afn = len(
                self.automata.estados
            )

            cantidad_afd = len(
                self.afd_convertido.estados
            )

            self.lbl_resumen.configure(
                text=(
                    f"Conversión completada: "
                    f"{cantidad_afn} estados en el AFN → "
                    f"{cantidad_afd} estados en el AFD"
                ),
                text_color=COLOR_EXITO
            )

            self.lbl_estado_conversion.configure(
                text=(
                    "AFD equivalente generado "
                    "correctamente."
                ),
                text_color=COLOR_EXITO
            )

            self.btn_usar_afd.configure(
                state="normal"
            )

            self.ventana_principal.lbl_estado.configure(
                text=(
                    f"Estado: AFN - "
                    f"{self.automata.nombre} | "
                    f"AFD equivalente generado"
                )
            )

            registrar_info(
                "CONVERSION",
                (
                    "Conversión AFN → AFD completada "
                    f"correctamente para "
                    f"{self.automata.nombre}. "
                    f"Estados AFN: {cantidad_afn}. "
                    f"Estados AFD: {cantidad_afd}"
                )
            )

        except Exception as error:

            self.lbl_estado_conversion.configure(
                text=(
                    "No fue posible realizar "
                    "la conversión."
                ),
                text_color=COLOR_ERROR
            )

            registrar_error(
                "CONVERSION",
                (
                    "No fue posible convertir "
                    f"el AFN a AFD: {error}"
                )
            )

            messagebox.showerror(
                "Error de conversión",
                (
                    "No fue posible convertir "
                    "el AFN a AFD.\n\n"
                    f"Detalle: {error}"
                )
            )

    # =========================================================
    # FORMATEAR TABLA
    # =========================================================

    def formatear_tabla(
        self,
        tabla
    ):

        if not tabla:

            return "No existen datos."

        simbolos = sorted(
            self.afd_convertido.alfabeto
        )

        ancho_estado = max(
            15,
            max(
                len(
                    str(
                        fila["estado"]
                    )
                )
                for fila in tabla
            ) + 2
        )

        anchos_simbolos = {}

        for simbolo in simbolos:

            ancho = max(
                10,
                len(
                    str(
                        simbolo
                    )
                ) + 2
            )

            for fila in tabla:

                destino = fila.get(
                    simbolo,
                    ""
                )

                ancho = max(
                    ancho,
                    len(
                        str(
                            destino
                        )
                    ) + 2
                )

            anchos_simbolos[
                simbolo
            ] = ancho

        encabezado = (
            "Estado".ljust(
                ancho_estado
            )
        )

        for simbolo in simbolos:

            encabezado += (
                str(
                    simbolo
                ).center(
                    anchos_simbolos[
                        simbolo
                    ]
                )
            )

        lineas = [
            encabezado,
            "-" * len(
                encabezado
            )
        ]

        for fila in tabla:

            estado = fila[
                "estado"
            ]

            prefijo = ""

            if (
                estado
                == self.afd_convertido.estado_inicial
            ):

                prefijo += "→ "

            if (
                estado
                in self.afd_convertido.estados_finales
            ):

                prefijo += "* "

            estado_texto = (
                prefijo
                + estado
            )

            linea = (
                estado_texto.ljust(
                    ancho_estado
                )
            )

            for simbolo in simbolos:

                destino = fila.get(
                    simbolo,
                    ""
                )

                linea += (
                    str(
                        destino
                    ).center(
                        anchos_simbolos[
                            simbolo
                        ]
                    )
                )

            lineas.append(
                linea
            )

        lineas.append("")

        lineas.append(
            "→ Estado inicial"
        )

        lineas.append(
            "* Estado final"
        )

        return "\n".join(
            lineas
        )

    # =========================================================
    # USAR AFD CONVERTIDO
    # =========================================================

    def usar_afd_convertido(self):

        if self.afd_convertido is None:

            registrar_warning(
                "CONVERSION",
                (
                    "Se intentó usar un AFD convertido "
                    "sin realizar primero la conversión"
                )
            )

            messagebox.showwarning(
                "Sin conversión",
                (
                    "Primero debe convertir "
                    "el AFN a AFD."
                )
            )

            return

        respuesta = messagebox.askyesno(
            "Usar AFD convertido",
            (
                "¿Desea convertir el AFD generado "
                "en el autómata actualmente cargado?\n\n"
                "Después podrá simularlo, visualizar "
                "su diagrama y minimizarlo."
            )
        )

        if not respuesta:

            return

        self.ventana_principal.establecer_automata(
            self.afd_convertido,
            "AFD"
        )

        registrar_info(
            "CONVERSION",
            (
                "AFD convertido establecido "
                "como autómata actual: "
                f"{self.afd_convertido.nombre}"
            )
        )

        self.lbl_estado_conversion.configure(
            text=(
                "El AFD convertido fue cargado "
                "como autómata actual."
            ),
            text_color=COLOR_EXITO
        )

        self.btn_usar_afd.configure(
            state="disabled"
        )

        messagebox.showinfo(
            "AFD cargado",
            (
                "El AFD convertido ahora es "
                "el autómata actual."
            )
        )