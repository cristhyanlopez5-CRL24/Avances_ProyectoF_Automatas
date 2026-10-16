import customtkinter as ctk

from pathlib import Path

from tkinter import (
    filedialog,
    messagebox
)

from algoritmos.analizador_logs import (
    analizar_archivo_logs
)

from utilidades.registro_logs import (
    obtener_ruta_log
)

from utilidades.tema import (
    FONDO_PANEL,
    FONDO_ENTRADA,
    TEXTO_TITULO,
    TEXTO_NORMAL,
    TEXTO_SUAVE,
    TEXTO_DESHABILITADO,
    BOTON_PRINCIPAL,
    BOTON_PRINCIPAL_HOVER,
    TEXTO_BOTON,
    COLOR_BORDE,
    COLOR_EXITO,
    COLOR_ADVERTENCIA,
    COLOR_ERROR,
    COLOR_INFO,
    COLOR_CRITICAL
)


class ValidacionLogsFrame(ctk.CTkFrame):

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

        self.ruta_actual = None

        self.resultado_actual = None

        # =====================================================
        # CONTENEDOR GENERAL
        # =====================================================

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # ÁREA DESPLAZABLE
        # =====================================================

        self.scroll_principal = (
            ctk.CTkScrollableFrame(
                self,
                fg_color="transparent",
                corner_radius=0,
                orientation="vertical"
            )
        )

        self.scroll_principal.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scroll_principal.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_encabezado()

        self.crear_selector_archivo()

        self.crear_filtros()

        self.crear_resumen_severidad()

        self.crear_resumen_validacion()

        self.crear_estado()

        self.crear_area_resultados()

        self.mostrar_mensaje_inicial()

        # Cargar automáticamente
        # el archivo del día actual.
        self.after(
            150,
            self.cargar_log_hoy
        )

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        frame = ctk.CTkFrame(
            self.scroll_principal,
            fg_color="transparent"
        )

        frame.grid(
            row=0,
            column=0,
            padx=30,
            pady=(16, 6),
            sticky="ew"
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            frame,
            text="VALIDACIÓN DE LOGS",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=28,
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
                "Revisa, valida y filtra los registros "
                "generados por la aplicación."
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
    # SELECCIÓN DE ARCHIVO
    # =========================================================

    def crear_selector_archivo(self):

        self.frame_archivo = ctk.CTkFrame(
            self.scroll_principal,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_archivo.grid(
            row=1,
            column=0,
            padx=30,
            pady=6,
            sticky="ew"
        )

        for columna in range(3):

            self.frame_archivo.grid_columnconfigure(
                columna,
                weight=1
            )

        ctk.CTkLabel(
            self.frame_archivo,
            text="Archivo de logs",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            padx=20,
            pady=(11, 4),
            sticky="w"
        )

        self.lbl_archivo = ctk.CTkLabel(
            self.frame_archivo,
            text="Ningún archivo seleccionado.",
            text_color=TEXTO_SUAVE,
            anchor="w",
            justify="left",
            wraplength=850
        )

        self.lbl_archivo.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=20,
            pady=(0, 8),
            sticky="ew"
        )

        self.btn_hoy = ctk.CTkButton(
            self.frame_archivo,
            text="Log de hoy",
            command=self.cargar_log_hoy,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            height=34
        )

        self.btn_hoy.grid(
            row=2,
            column=0,
            padx=(20, 5),
            pady=(0, 12),
            sticky="ew"
        )

        self.btn_seleccionar = ctk.CTkButton(
            self.frame_archivo,
            text="Seleccionar archivo",
            command=self.seleccionar_archivo,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            height=34
        )

        self.btn_seleccionar.grid(
            row=2,
            column=1,
            padx=5,
            pady=(0, 12),
            sticky="ew"
        )

        self.btn_actualizar = ctk.CTkButton(
            self.frame_archivo,
            text="Actualizar",
            command=self.actualizar_log,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            text_color_disabled=TEXTO_DESHABILITADO,
            height=34,
            state="disabled"
        )

        self.btn_actualizar.grid(
            row=2,
            column=2,
            padx=(5, 20),
            pady=(0, 12),
            sticky="ew"
        )

    # =========================================================
    # FILTROS
    # =========================================================

    def crear_filtros(self):

        self.frame_filtros = ctk.CTkFrame(
            self.scroll_principal,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_filtros.grid(
            row=2,
            column=0,
            padx=30,
            pady=(2, 6),
            sticky="ew"
        )

        self.frame_filtros.grid_columnconfigure(
            1,
            weight=1
        )

        self.frame_filtros.grid_columnconfigure(
            3,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_filtros,
            text="Filtros",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=5,
            padx=20,
            pady=(10, 6),
            sticky="w"
        )

        # -----------------------------------------------------
        # NIVEL
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_filtros,
            text="Nivel:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=(20, 8),
            pady=(0, 11),
            sticky="w"
        )

        self.selector_nivel = ctk.CTkOptionMenu(
            self.frame_filtros,
            values=[
                "Todos",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL"
            ],
            command=self.al_cambiar_filtro,
            fg_color=BOTON_PRINCIPAL,
            button_color=BOTON_PRINCIPAL,
            button_hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            height=32
        )

        self.selector_nivel.grid(
            row=1,
            column=1,
            padx=(0, 15),
            pady=(0, 11),
            sticky="ew"
        )

        self.selector_nivel.set(
            "Todos"
        )

        # -----------------------------------------------------
        # MÓDULO
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_filtros,
            text="Módulo:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=1,
            column=2,
            padx=(5, 8),
            pady=(0, 11),
            sticky="w"
        )

        self.selector_modulo = ctk.CTkOptionMenu(
            self.frame_filtros,
            values=[
                "Todos"
            ],
            command=self.al_cambiar_filtro,
            fg_color=BOTON_PRINCIPAL,
            button_color=BOTON_PRINCIPAL,
            button_hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            height=32
        )

        self.selector_modulo.grid(
            row=1,
            column=3,
            padx=(0, 15),
            pady=(0, 11),
            sticky="ew"
        )

        self.selector_modulo.set(
            "Todos"
        )

        # -----------------------------------------------------
        # LIMPIAR FILTROS
        # -----------------------------------------------------

        self.btn_limpiar_filtros = ctk.CTkButton(
            self.frame_filtros,
            text="Limpiar filtros",
            command=self.limpiar_filtros,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            height=32,
            width=130
        )

        self.btn_limpiar_filtros.grid(
            row=1,
            column=4,
            padx=(0, 20),
            pady=(0, 11)
        )

    # =========================================================
    # CREAR TARJETA DE SEVERIDAD
    # =========================================================

    def crear_card_severidad(
        self,
        master,
        columna,
        titulo,
        color
    ):

        card = ctk.CTkFrame(
            master,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=10
        )

        card.grid(
            row=0,
            column=columna,
            padx=4,
            sticky="ew"
        )

        ctk.CTkLabel(
            card,
            text=titulo,
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            pady=(6, 0)
        )

        label = ctk.CTkLabel(
            card,
            text="0",
            text_color=color,
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        )

        label.pack(
            pady=(0, 6)
        )

        return label

    # =========================================================
    # RESUMEN POR SEVERIDAD
    # =========================================================

    def crear_resumen_severidad(self):

        self.frame_severidad = ctk.CTkFrame(
            self.scroll_principal,
            fg_color="transparent"
        )

        self.frame_severidad.grid(
            row=3,
            column=0,
            padx=30,
            pady=(1, 4),
            sticky="ew"
        )

        for columna in range(4):

            self.frame_severidad.grid_columnconfigure(
                columna,
                weight=1
            )

        self.lbl_info = self.crear_card_severidad(
            self.frame_severidad,
            0,
            "INFO",
            COLOR_INFO
        )

        self.lbl_warning = self.crear_card_severidad(
            self.frame_severidad,
            1,
            "WARNING",
            COLOR_ADVERTENCIA
        )

        self.lbl_error = self.crear_card_severidad(
            self.frame_severidad,
            2,
            "ERROR",
            COLOR_ERROR
        )

        self.lbl_critical = self.crear_card_severidad(
            self.frame_severidad,
            3,
            "CRITICAL",
            COLOR_CRITICAL
        )

    # =========================================================
    # RESUMEN DE VALIDACIÓN
    # =========================================================

    def crear_resumen_validacion(self):

        self.frame_resumen = ctk.CTkFrame(
            self.scroll_principal,
            fg_color="transparent"
        )

        self.frame_resumen.grid(
            row=4,
            column=0,
            padx=30,
            pady=(0, 2),
            sticky="ew"
        )

        self.frame_resumen.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_resumen.grid_columnconfigure(
            1,
            weight=1
        )

        # -----------------------------------------------------
        # VÁLIDOS
        # -----------------------------------------------------

        self.card_validos = ctk.CTkFrame(
            self.frame_resumen,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=10
        )

        self.card_validos.grid(
            row=0,
            column=0,
            padx=(0, 5),
            sticky="ew"
        )

        ctk.CTkLabel(
            self.card_validos,
            text="Registros válidos",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            pady=(5, 0)
        )

        self.lbl_validos = ctk.CTkLabel(
            self.card_validos,
            text="0",
            text_color=COLOR_EXITO,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        self.lbl_validos.pack(
            pady=(0, 5)
        )

        # -----------------------------------------------------
        # INVÁLIDOS
        # -----------------------------------------------------

        self.card_invalidos = ctk.CTkFrame(
            self.frame_resumen,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=10
        )

        self.card_invalidos.grid(
            row=0,
            column=1,
            padx=(5, 0),
            sticky="ew"
        )

        ctk.CTkLabel(
            self.card_invalidos,
            text="Registros inválidos",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(
            pady=(5, 0)
        )

        self.lbl_invalidos = ctk.CTkLabel(
            self.card_invalidos,
            text="0",
            text_color=COLOR_ERROR,
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        self.lbl_invalidos.pack(
            pady=(0, 5)
        )

    # =========================================================
    # ESTADO
    # =========================================================

    def crear_estado(self):

        self.lbl_estado = ctk.CTkLabel(
            self.scroll_principal,
            text=(
                "Seleccione un archivo de logs "
                "para comenzar."
            ),
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            anchor="w"
        )

        self.lbl_estado.grid(
            row=5,
            column=0,
            padx=35,
            pady=(3, 3),
            sticky="ew"
        )

    # =========================================================
    # ÁREA DE RESULTADOS
    # =========================================================

    def crear_area_resultados(self):

        self.frame_resultados = ctk.CTkFrame(
            self.scroll_principal,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12,
            height=320
        )

        self.frame_resultados.grid(
            row=6,
            column=0,
            padx=30,
            pady=(3, 20),
            sticky="ew"
        )

        # Más espacio para los registros válidos.
        self.frame_resultados.grid_columnconfigure(
            0,
            weight=3
        )

        # Menos espacio para los inválidos.
        self.frame_resultados.grid_columnconfigure(
            1,
            weight=1
        )

        self.frame_resultados.grid_rowconfigure(
            1,
            weight=1,
            minsize=230
        )

        # =====================================================
        # REGISTROS VÁLIDOS
        # =====================================================

        ctk.CTkLabel(
            self.frame_resultados,
            text="Registros válidos",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=(15, 8),
            pady=(12, 6),
            sticky="w"
        )

        self.txt_validos = ctk.CTkTextbox(
            self.frame_resultados,
            height=230,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_width=1,
            border_color=COLOR_BORDE,
            font=(
                "Consolas",
                12
            ),
            wrap="word"
        )

        self.txt_validos.grid(
            row=1,
            column=0,
            padx=(15, 8),
            pady=(0, 15),
            sticky="nsew"
        )

        self.txt_validos.configure(
            state="disabled"
        )

        # =====================================================
        # REGISTROS INVÁLIDOS
        # =====================================================

        ctk.CTkLabel(
            self.frame_resultados,
            text="Registros inválidos",
            text_color=COLOR_ADVERTENCIA,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=0,
            column=1,
            padx=(8, 15),
            pady=(12, 6),
            sticky="w"
        )

        self.txt_invalidos = ctk.CTkTextbox(
            self.frame_resultados,
            height=230,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_width=1,
            border_color=COLOR_BORDE,
            font=(
                "Consolas",
                12
            ),
            wrap="word"
        )

        self.txt_invalidos.grid(
            row=1,
            column=1,
            padx=(8, 15),
            pady=(0, 15),
            sticky="nsew"
        )

        self.txt_invalidos.configure(
            state="disabled"
        )

    # =========================================================
    # ESCRIBIR EN TEXTBOX
    # =========================================================

    def escribir_textbox(
        self,
        textbox,
        texto
    ):

        textbox.configure(
            state="normal"
        )

        textbox.delete(
            "1.0",
            "end"
        )

        textbox.insert(
            "end",
            texto
        )

        textbox.configure(
            state="disabled"
        )

    # =========================================================
    # MENSAJE INICIAL
    # =========================================================

    def mostrar_mensaje_inicial(self):

        self.escribir_textbox(
            self.txt_validos,
            (
                "Aquí aparecerán los registros "
                "que cumplen con el formato esperado.\n\n"
                "Puede filtrar por nivel y módulo."
            )
        )

        self.escribir_textbox(
            self.txt_invalidos,
            (
                "Las líneas que no cumplan con "
                "el formato del sistema aparecerán aquí."
            )
        )

    # =========================================================
    # SELECCIONAR ARCHIVO
    # =========================================================

    def seleccionar_archivo(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de logs",
            filetypes=[
                (
                    "Archivos de logs",
                    "*.txt *.log"
                ),
                (
                    "Archivos TXT",
                    "*.txt"
                ),
                (
                    "Archivos LOG",
                    "*.log"
                ),
                (
                    "Todos los archivos",
                    "*.*"
                )
            ]
        )

        if not ruta:

            return

        self.cargar_archivo(
            ruta
        )

    # =========================================================
    # LOG DE HOY
    # =========================================================

    def cargar_log_hoy(self):

        ruta = obtener_ruta_log()

        if not ruta.exists():

            self.ruta_actual = None

            self.resultado_actual = None

            self.lbl_archivo.configure(
                text=str(
                    ruta
                )
            )

            self.lbl_estado.configure(
                text=(
                    "Todavía no existe un archivo "
                    "de logs para el día de hoy."
                ),
                text_color=COLOR_ADVERTENCIA
            )

            self.reiniciar_contadores()

            self.btn_actualizar.configure(
                state="disabled"
            )

            return

        self.cargar_archivo(
            ruta
        )

    # =========================================================
    # REINICIAR CONTADORES
    # =========================================================

    def reiniciar_contadores(self):

        self.lbl_info.configure(
            text="0"
        )

        self.lbl_warning.configure(
            text="0"
        )

        self.lbl_error.configure(
            text="0"
        )

        self.lbl_critical.configure(
            text="0"
        )

        self.lbl_validos.configure(
            text="0"
        )

        self.lbl_invalidos.configure(
            text="0"
        )

    # =========================================================
    # ACTUALIZAR LOG
    # =========================================================

    def actualizar_log(self):

        if self.ruta_actual is None:

            self.lbl_estado.configure(
                text=(
                    "No existe un archivo cargado "
                    "para actualizar."
                ),
                text_color=COLOR_ADVERTENCIA
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    "Estado: No hay un archivo "
                    "de logs cargado."
                ),
                "advertencia"
            )

            return

        nivel_actual = (
            self.selector_nivel.get()
        )

        modulo_actual = (
            self.selector_modulo.get()
        )

        self.cargar_archivo(
            self.ruta_actual,
            conservar_filtros=True,
            nivel_anterior=nivel_actual,
            modulo_anterior=modulo_actual
        )

    # =========================================================
    # CARGAR ARCHIVO
    # =========================================================

    def cargar_archivo(
        self,
        ruta,
        conservar_filtros=False,
        nivel_anterior="Todos",
        modulo_anterior="Todos"
    ):

        try:

            ruta = Path(
                ruta
            )

            resultado = analizar_archivo_logs(
                ruta
            )

            self.ruta_actual = ruta

            self.resultado_actual = resultado

            self.lbl_archivo.configure(
                text=str(
                    ruta
                )
            )

            self.btn_actualizar.configure(
                state="normal"
            )

            self.actualizar_modulos(
                conservar_filtros=(
                    conservar_filtros
                ),
                nivel_anterior=(
                    nivel_anterior
                ),
                modulo_anterior=(
                    modulo_anterior
                )
            )

            self.actualizar_resumen()

            self.mostrar_invalidos()

            self.aplicar_filtros()

        except ValueError as error:

            self.lbl_estado.configure(
                text=(
                    "No fue posible validar "
                    "el archivo seleccionado."
                ),
                text_color=COLOR_ADVERTENCIA
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    "Estado: No fue posible validar "
                    "el archivo de logs."
                ),
                "advertencia"
            )

            messagebox.showerror(
                "Archivo de logs inválido",
                str(error)
            )

        except Exception as error:

            self.lbl_estado.configure(
                text=(
                    "Ocurrió un error inesperado "
                    "al leer los logs."
                ),
                text_color=COLOR_ERROR
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    "Estado: Error al leer "
                    "los archivos de logs."
                ),
                "error"
            )

            messagebox.showerror(
                "Error",
                (
                    "Ocurrió un error inesperado "
                    "durante la validación.\n\n"
                    f"Detalle: {error}"
                )
            )

    # =========================================================
    # ACTUALIZAR RESUMEN
    # =========================================================

    def actualizar_resumen(self):

        if self.resultado_actual is None:

            self.reiniciar_contadores()

            return

        resumen = (
            self.resultado_actual[
                "resumen_niveles"
            ]
        )

        self.lbl_info.configure(
            text=str(
                resumen["INFO"]
            )
        )

        self.lbl_warning.configure(
            text=str(
                resumen["WARNING"]
            )
        )

        self.lbl_error.configure(
            text=str(
                resumen["ERROR"]
            )
        )

        self.lbl_critical.configure(
            text=str(
                resumen["CRITICAL"]
            )
        )

        self.lbl_validos.configure(
            text=str(
                self.resultado_actual[
                    "cantidad_validos"
                ]
            )
        )

        self.lbl_invalidos.configure(
            text=str(
                self.resultado_actual[
                    "cantidad_invalidos"
                ]
            )
        )

    # =========================================================
    # ACTUALIZAR MÓDULOS
    # =========================================================

    def actualizar_modulos(
        self,
        conservar_filtros=False,
        nivel_anterior="Todos",
        modulo_anterior="Todos"
    ):

        if self.resultado_actual is None:

            return

        modulos = sorted({
            registro["modulo"]
            for registro
            in self.resultado_actual[
                "registros_validos"
            ]
        })

        opciones = [
            "Todos"
        ] + modulos

        self.selector_modulo.configure(
            values=opciones
        )

        if conservar_filtros:

            niveles_permitidos = [
                "Todos",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL"
            ]

            if (
                nivel_anterior
                in niveles_permitidos
            ):

                self.selector_nivel.set(
                    nivel_anterior
                )

            else:

                self.selector_nivel.set(
                    "Todos"
                )

            if (
                modulo_anterior
                in opciones
            ):

                self.selector_modulo.set(
                    modulo_anterior
                )

            else:

                self.selector_modulo.set(
                    "Todos"
                )

        else:

            self.selector_modulo.set(
                "Todos"
            )

            self.selector_nivel.set(
                "Todos"
            )

    # =========================================================
    # CAMBIAR FILTRO
    # =========================================================

    def al_cambiar_filtro(
        self,
        opcion=None
    ):

        self.aplicar_filtros()

    # =========================================================
    # LIMPIAR FILTROS
    # =========================================================

    def limpiar_filtros(self):

        self.selector_nivel.set(
            "Todos"
        )

        self.selector_modulo.set(
            "Todos"
        )

        self.aplicar_filtros()

    # =========================================================
    # APLICAR FILTROS
    # =========================================================

    def aplicar_filtros(self):

        if self.resultado_actual is None:

            return

        nivel_seleccionado = (
            self.selector_nivel.get()
        )

        modulo_seleccionado = (
            self.selector_modulo.get()
        )

        registros = (
            self.resultado_actual[
                "registros_validos"
            ]
        )

        filtrados = []

        for registro in registros:

            cumple_nivel = (
                nivel_seleccionado == "Todos"
                or registro["nivel"]
                == nivel_seleccionado
            )

            cumple_modulo = (
                modulo_seleccionado == "Todos"
                or registro["modulo"]
                == modulo_seleccionado
            )

            if (
                cumple_nivel
                and cumple_modulo
            ):

                filtrados.append(
                    registro
                )

        self.mostrar_registros_filtrados(
            filtrados
        )

        total = len(
            registros
        )

        cantidad_filtrada = len(
            filtrados
        )

        sin_filtros = (
            nivel_seleccionado == "Todos"
            and modulo_seleccionado == "Todos"
        )

        if sin_filtros:

            texto_estado = (
                f"Mostrando los {total} "
                "registros válidos."
            )

        else:

            texto_estado = (
                f"Filtro aplicado: "
                f"{cantidad_filtrada} de "
                f"{total} registros."
            )

        cantidad_invalidos = (
            self.resultado_actual[
                "cantidad_invalidos"
            ]
        )

        if cantidad_invalidos > 0:

            self.lbl_estado.configure(
                text=(
                    texto_estado
                    + f" Se detectaron "
                    f"{cantidad_invalidos} "
                    "registros inválidos."
                ),
                text_color=COLOR_ADVERTENCIA
            )

        else:

            self.lbl_estado.configure(
                text=texto_estado,
                text_color=COLOR_EXITO
            )

        # -----------------------------------------------------
        # BARRA INFERIOR
        # -----------------------------------------------------

        if sin_filtros:

            if cantidad_invalidos == 0:

                self.ventana_principal.actualizar_barra_estado(
                    (
                        f"Estado: Logs validados - "
                        f"{total} válidos"
                    ),
                    "exito"
                )

            else:

                self.ventana_principal.actualizar_barra_estado(
                    (
                        f"Estado: Logs validados - "
                        f"{total} válidos, "
                        f"{cantidad_invalidos} inválidos"
                    ),
                    "advertencia"
                )

        else:

            tipo_barra = (
                "advertencia"
                if cantidad_invalidos > 0
                else "exito"
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    "Estado: Filtro de logs - "
                    f"{cantidad_filtrada} de "
                    f"{total} registros"
                ),
                tipo_barra
            )

    # =========================================================
    # MOSTRAR REGISTROS FILTRADOS
    # =========================================================

    def mostrar_registros_filtrados(
        self,
        registros
    ):

        lineas = []

        for registro in registros:

            lineas.append(
                (
                    f"Línea "
                    f"{registro['numero_linea']}\n"
                    f"{registro['fecha_hora']} | "
                    f"{registro['nivel']} | "
                    f"{registro['modulo']}\n"
                    f"Mensaje: "
                    f"{registro['mensaje']}\n"
                    + "-" * 70
                )
            )

        if lineas:

            texto = "\n".join(
                lineas
            )

        else:

            texto = (
                "No se encontraron registros "
                "que coincidan con los filtros "
                "seleccionados.\n\n"
                "Esto no representa un error. "
                "Simplemente no existen registros "
                "con esa combinación de nivel "
                "y módulo."
            )

        self.escribir_textbox(
            self.txt_validos,
            texto
        )

    # =========================================================
    # MOSTRAR REGISTROS INVÁLIDOS
    # =========================================================

    def mostrar_invalidos(self):

        if self.resultado_actual is None:

            return

        lineas = []

        for registro in (
            self.resultado_actual[
                "registros_invalidos"
            ]
        ):

            lineas.append(
                (
                    f"Línea "
                    f"{registro['numero_linea']}: "
                    f"{registro['error']}\n"
                    f"Contenido: "
                    f"{registro['contenido']}\n"
                    + "-" * 70
                )
            )

        if lineas:

            texto = "\n".join(
                lineas
            )

        else:

            texto = (
                "No se detectaron registros inválidos."
            )

        self.escribir_textbox(
            self.txt_invalidos,
            texto
        )