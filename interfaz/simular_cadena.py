import customtkinter as ctk

from tkinter import messagebox

from algoritmos.simulador import (
    simular_afd_detallado,
    formatear_resultado_afd,
    simular_afn_detallado,
    formatear_resultado_afn
)

from utilidades.validaciones import (
    validar_cadena
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


class SimularCadenaFrame(
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

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.crear_encabezado()

        self.crear_informacion_automata()

        self.crear_formulario()

        self.crear_resultado()

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        lbl_titulo = ctk.CTkLabel(
            self,
            text="SIMULAR CADENA",
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
                "Ingrese una cadena para comprobar "
                "si el autómata la acepta o la rechaza."
            ),
            text_color=TEXTO_NORMAL,
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

    def crear_informacion_automata(self):

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
            text="Autómata cargado",
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
        # SIN AUTÓMATA
        # -----------------------------------------------------

        if self.automata is None:

            lbl_sin_automata = ctk.CTkLabel(
                self.frame_info,
                text=(
                    "No hay ningún autómata cargado.\n"
                    "Primero debe crear un AFD o AFN."
                ),
                text_color=COLOR_ADVERTENCIA,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            )

            lbl_sin_automata.grid(
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
            text=self.tipo,
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
            row=3,
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
            row=3,
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
            row=4,
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
            row=4,
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
            row=5,
            column=0,
            padx=20,
            pady=(7, 18),
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=finales,
            text_color=TEXTO_NORMAL
        ).grid(
            row=5,
            column=1,
            padx=20,
            pady=(7, 18),
            sticky="w"
        )

    # =========================================================
    # FORMULARIO DE CADENA
    # =========================================================

    def crear_formulario(self):

        self.frame_simulacion = ctk.CTkFrame(
            self,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_simulacion.grid(
            row=3,
            column=0,
            padx=30,
            pady=15,
            sticky="ew"
        )

        self.frame_simulacion.grid_columnconfigure(
            1,
            weight=1
        )

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------

        lbl_titulo = ctk.CTkLabel(
            self.frame_simulacion,
            text="Cadena a evaluar",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        lbl_titulo.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=20,
            pady=(18, 8)
        )

        # -----------------------------------------------------
        # CADENA
        # -----------------------------------------------------

        lbl_cadena = ctk.CTkLabel(
            self.frame_simulacion,
            text="Cadena:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        lbl_cadena.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=15
        )

        self.entry_cadena = ctk.CTkEntry(
            self.frame_simulacion,
            placeholder_text="Ejemplo: 00101",
            height=42,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_color=COLOR_BORDE
        )

        self.entry_cadena.grid(
            row=1,
            column=1,
            padx=10,
            pady=15,
            sticky="ew"
        )

        self.entry_cadena.bind(
            "<Return>",
            lambda event: self.simular()
        )

        # -----------------------------------------------------
        # SIMULAR
        # -----------------------------------------------------

        self.btn_simular = ctk.CTkButton(
            self.frame_simulacion,
            text="Simular",
            height=42,
            width=130,
            command=self.simular,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_simular.grid(
            row=1,
            column=2,
            padx=10,
            pady=15
        )

        # -----------------------------------------------------
        # LIMPIAR
        # -----------------------------------------------------

        self.btn_limpiar = ctk.CTkButton(
            self.frame_simulacion,
            text="Limpiar",
            height=42,
            width=100,
            command=self.limpiar,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        )

        self.btn_limpiar.grid(
            row=1,
            column=3,
            padx=(0, 20),
            pady=15
        )

        # -----------------------------------------------------
        # NOTA
        # -----------------------------------------------------

        lbl_nota = ctk.CTkLabel(
            self.frame_simulacion,
            text=(
                "Puede dejar el campo vacío "
                "para evaluar la cadena ε."
            ),
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=12
            )
        )

        lbl_nota.grid(
            row=2,
            column=0,
            columnspan=4,
            padx=20,
            pady=(0, 15)
        )

        if self.automata is None:

            self.entry_cadena.configure(
                state="disabled"
            )

            self.btn_simular.configure(
                state="disabled"
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

        lbl_titulo = ctk.CTkLabel(
            self.frame_resultado,
            text="Resultado de la simulación",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        lbl_titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 5)
        )

        self.lbl_estado_resultado = (
            ctk.CTkLabel(
                self.frame_resultado,
                text=(
                    "Ingrese una cadena y "
                    "presione Simular."
                ),
                text_color=TEXTO_SUAVE,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            )
        )

        self.lbl_estado_resultado.grid(
            row=1,
            column=0,
            padx=20,
            pady=10
        )

        self.txt_resultado = ctk.CTkTextbox(
            self.frame_resultado,
            height=280,
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
    # SIMULAR
    # =========================================================

    def simular(self):

        if self.automata is None:

            registrar_warning(
                "SIMULACION",
                (
                    "Se intentó simular una cadena "
                    "sin un autómata cargado"
                )
            )

            self.ventana_principal.actualizar_barra_estado(
                "Estado: No hay un autómata para simular.",
                "advertencia"
            )

            messagebox.showwarning(
                "Sin autómata",
                (
                    "Primero debe crear "
                    "un autómata."
                )
            )

            return

        try:

            cadena = validar_cadena(
                self.entry_cadena.get(),
                self.automata.alfabeto
            )

            if self.tipo == "AFD":

                resultado = simular_afd_detallado(
                    self.automata,
                    cadena
                )

                texto = formatear_resultado_afd(
                    resultado
                )

            elif self.tipo == "AFN":

                resultado = simular_afn_detallado(
                    self.automata,
                    cadena
                )

                texto = formatear_resultado_afn(
                    resultado
                )

            else:

                raise ValueError(
                    "Tipo de autómata desconocido."
                )

            self.mostrar_resultado(
                texto,
                resultado["aceptada"]
            )

            cadena_log = (
                cadena
                if cadena
                else "ε"
            )

            if resultado["aceptada"]:

                estado_texto = (
                    "Cadena aceptada"
                )

                tipo_barra = "exito"

                registrar_info(
                    "SIMULACION",
                    (
                        f"Cadena {cadena_log} ACEPTADA "
                        f"por {self.tipo} "
                        f"{self.automata.nombre}"
                    )
                )

            else:

                estado_texto = (
                    "Cadena rechazada"
                )

                tipo_barra = "advertencia"

                registrar_info(
                    "SIMULACION",
                    (
                        f"Cadena {cadena_log} RECHAZADA "
                        f"por {self.tipo} "
                        f"{self.automata.nombre}"
                    )
                )

            self.ventana_principal.actualizar_barra_estado(
                (
                    f"Estado: {self.tipo} - "
                    f"{self.automata.nombre} | "
                    f"{estado_texto}"
                ),
                tipo_barra
            )

        except ValueError as error:

            self.lbl_estado_resultado.configure(
                text="CADENA INVÁLIDA",
                text_color=COLOR_ADVERTENCIA
            )

            self.ventana_principal.actualizar_barra_estado(
                "Estado: Cadena inválida.",
                "advertencia"
            )

            registrar_warning(
                "SIMULACION",
                (
                    "No fue posible simular "
                    f"la cadena: {error}"
                )
            )

            messagebox.showerror(
                "Cadena inválida",
                str(error)
            )

        except Exception as error:

            self.lbl_estado_resultado.configure(
                text="ERROR DE SIMULACIÓN",
                text_color=COLOR_ERROR
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    "Estado: Error inesperado "
                    "durante la simulación."
                ),
                "error"
            )

            registrar_error(
                "SIMULACION",
                (
                    "Error inesperado durante "
                    f"la simulación: {error}"
                )
            )

            messagebox.showerror(
                "Error de simulación",
                (
                    "Ocurrió un error inesperado "
                    "al simular la cadena.\n\n"
                    f"Detalle: {error}"
                )
            )

    # =========================================================
    # MOSTRAR RESULTADO
    # =========================================================

    def mostrar_resultado(
        self,
        texto,
        aceptada
    ):

        if aceptada:

            self.lbl_estado_resultado.configure(
                text="CADENA ACEPTADA ✓",
                text_color=COLOR_EXITO
            )

        else:

            self.lbl_estado_resultado.configure(
                text="CADENA RECHAZADA ✗",
                text_color=COLOR_ERROR
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
            texto
        )

        self.txt_resultado.configure(
            state="disabled"
        )

    # =========================================================
    # LIMPIAR
    # =========================================================

    def limpiar(self):

        if self.automata is not None:

            self.entry_cadena.configure(
                state="normal"
            )

            self.entry_cadena.delete(
                0,
                "end"
            )

        self.lbl_estado_resultado.configure(
            text=(
                "Ingrese una cadena y "
                "presione Simular."
            ),
            text_color=TEXTO_SUAVE
        )

        self.txt_resultado.configure(
            state="normal"
        )

        self.txt_resultado.delete(
            "1.0",
            "end"
        )

        self.txt_resultado.configure(
            state="disabled"
        )