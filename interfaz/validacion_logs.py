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
    FONDO_APP,
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
    COLOR_ERROR
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

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            5,
            weight=1
        )

        self.crear_encabezado()

        self.crear_selector_archivo()

        self.crear_filtros()

        self.crear_resumen()

        self.crear_estado()

        self.crear_area_resultados()

        self.mostrar_mensaje_inicial()

        self.after(
            150,
            self.cargar_log_hoy
        )

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
            padx=30,
            pady=(20, 8),
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
            pady=(0, 5)
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
            self,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_archivo.grid(
            row=1,
            column=0,
            padx=30,
            pady=8,
            sticky="ew"
        )

        self.frame_archivo.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_archivo.grid_columnconfigure(
            1,
            weight=1
        )

        self.frame_archivo.grid_columnconfigure(
            2,
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
            pady=(14, 5),
            sticky="w"
        )

        self.lbl_archivo = ctk.CTkLabel(
            self.frame_archivo,
            text="Ningún archivo seleccionado.",
            text_color=TEXTO_SUAVE,
            anchor="w",
            justify="left",
            wraplength=700
        )

        self.lbl_archivo.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=20,
            pady=(0, 10),
            sticky="ew"
        )

        self.btn_hoy = ctk.CTkButton(
            self.frame_archivo,
            text="Log de hoy",
            command=self.cargar_log_hoy,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            height=36
        )

        self.btn_hoy.grid(
            row=2,
            column=0,
            padx=(20, 5),
            pady=(0, 15),
            sticky="ew"
        )

        self.btn_seleccionar = ctk.CTkButton(
            self.frame_archivo,
            text="Seleccionar archivo",
            command=self.seleccionar_archivo,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            height=36
        )

        self.btn_seleccionar.grid(
            row=2,
            column=1,
            padx=5,
            pady=(0, 15),
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
            height=36,
            state="disabled"
        )

        self.btn_actualizar.grid(
            row=2,
            column=2,
            padx=(5, 20),
            pady=(0, 15),
            sticky="ew"
        )

    # =========================================================
    # FILTROS
    # =========================================================

    def crear_filtros(self):

        self.frame_filtros = ctk.CTkFrame(
            self,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_filtros.grid(
            row=2,
            column=0,
            padx=30,
            pady=(2, 8),
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
            pady=(12, 8),
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
            pady=(0, 14),
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
            height=34
        )

        self.selector_nivel.grid(
            row=1,
            column=1,
            padx=(0, 15),
            pady=(0, 14),
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
            pady=(0, 14),
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
            height=34
        )

        self.selector_modulo.grid(
            row=1,
            column=3,
            padx=(0, 15),
            pady=(0, 14),
            sticky="ew"
        )

        self.selector_modulo.set(
            "Todos"
        )

        # -----------------------------------------------------
        # LIMPIAR
        # -----------------------------------------------------

        self.btn_limpiar_filtros = ctk.CTkButton(
            self.frame_filtros,
            text="Limpiar filtros",
            command=self.limpiar_filtros,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            height=34,
            width=130
        )

        self.btn_limpiar_filtros.grid(
            row=1,
            column=4,
            padx=(0, 20),
            pady=(0, 14)
        )

    # =========================================================
    # RESUMEN
    # =========================================================

    def crear_resumen(self):

        self.frame_resumen = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.frame_resumen.grid(
            row=3,
            column=0,
            padx=30,
            pady=(4, 2),
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
            padx=(0, 6),
            sticky="ew"
        )

        ctk.CTkLabel(
            self.card_validos,
            text="Registros válidos",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            pady=(9, 0)
        )

        self.lbl_validos = ctk.CTkLabel(
            self.card_validos,
            text="0",
            text_color=COLOR_EXITO,
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            )
        )

        self.lbl_validos.pack(
            pady=(0, 9)
        )

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
            padx=(6, 0),
            sticky="ew"
        )

        ctk.CTkLabel(
            self.card_invalidos,
            text="Registros inválidos",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            pady=(9, 0)
        )

        self.lbl_invalidos = ctk.CTkLabel(
            self.card_invalidos,
            text="0",
            text_color=COLOR_ERROR,
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            )
        )

        self.lbl_invalidos.pack(
            pady=(0, 9)
        )

    # =========================================================
    # ESTADO
    # =========================================================

    def crear_estado(self):

        self.lbl_estado = ctk.CTkLabel(
            self,
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
            row=4,
            column=0,
            padx=35,
            pady=(5, 5),
            sticky="ew"
        )

    # =========================================================
    # RESULTADOS
    # =========================================================

    def crear_area_resultados(self):

        self.frame_resultados = ctk.CTkFrame(
            self,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_resultados.grid(
            row=5,
            column=0,
            padx=30,
            pady=(5, 20),
            sticky="nsew"
        )

        self.frame_resultados.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_resultados.grid_rowconfigure(
            1,
            weight=1
        )

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
            padx=15,
            pady=(12, 5),
            sticky="w"
        )

        self.txt_validos = ctk.CTkTextbox(
            self.frame_resultados,
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
            padx=15,
            pady=(0, 10),
            sticky="nsew"
        )

        self.txt_validos.configure(
            state="disabled"
        )

        ctk.CTkLabel(
            self.frame_resultados,
            text="Registros inválidos detectados",
            text_color=COLOR_ADVERTENCIA,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=(2, 5),
            sticky="w"
        )

        self.txt_invalidos = ctk.CTkTextbox(
            self.frame_resultados,
            height=105,
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
            row=3,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        self.txt_invalidos.configure(
            state="disabled"
        )

    # =========================================================
    # TEXTBOX
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

            self.lbl_validos.configure(
                text="0"
            )

            self.lbl_invalidos.configure(
                text="0"
            )

            self.btn_actualizar.configure(
                state="disabled"
            )

            return

        self.cargar_archivo(
            ruta
        )

    # =========================================================
    # ACTUALIZAR
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

            return

        self.cargar_archivo(
            self.ruta_actual
        )

    # =========================================================
    # CARGAR ARCHIVO
    # =========================================================

    def cargar_archivo(
        self,
        ruta
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

            self.actualizar_modulos()

            self.mostrar_resultado_general()

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
    # ACTUALIZAR MÓDULOS DISPONIBLES
    # =========================================================

    def actualizar_modulos(self):

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

        self.selector_modulo.set(
            "Todos"
        )

        self.selector_nivel.set(
            "Todos"
        )

    # =========================================================
    # CAMBIO DE FILTRO
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

        if (
            nivel_seleccionado == "Todos"
            and modulo_seleccionado == "Todos"
        ):

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

        if (
            self.resultado_actual[
                "cantidad_invalidos"
            ]
            > 0
        ):

            self.lbl_estado.configure(
                text=(
                    texto_estado
                    + " Existen registros inválidos."
                ),
                text_color=COLOR_ADVERTENCIA
            )

        else:

            self.lbl_estado.configure(
                text=texto_estado,
                text_color=COLOR_EXITO
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

            numero = (
                registro[
                    "numero_linea"
                ]
            )

            fecha_hora = (
                registro[
                    "fecha_hora"
                ]
            )

            nivel = (
                registro[
                    "nivel"
                ]
            )

            modulo = (
                registro[
                    "modulo"
                ]
            )

            mensaje = (
                registro[
                    "mensaje"
                ]
            )

            lineas.append(
                (
                    f"Línea {numero}\n"
                    f"{fecha_hora} | "
                    f"{nivel} | "
                    f"{modulo}\n"
                    f"Mensaje: {mensaje}\n"
                    + "-" * 70
                )
            )

        if lineas:

            texto = "\n".join(
                lineas
            )

        else:

            texto = (
                "No existen registros que coincidan "
                "con los filtros seleccionados."
            )

        self.escribir_textbox(
            self.txt_validos,
            texto
        )

    # =========================================================
    # MOSTRAR RESULTADO GENERAL
    # =========================================================

    def mostrar_resultado_general(self):

        if self.resultado_actual is None:

            return

        resultado = (
            self.resultado_actual
        )

        cantidad_validos = (
            resultado[
                "cantidad_validos"
            ]
        )

        cantidad_invalidos = (
            resultado[
                "cantidad_invalidos"
            ]
        )

        self.lbl_validos.configure(
            text=str(
                cantidad_validos
            )
        )

        self.lbl_invalidos.configure(
            text=str(
                cantidad_invalidos
            )
        )

        # -----------------------------------------------------
        # INVÁLIDOS
        # -----------------------------------------------------

        lineas_invalidas = []

        for registro in (
            resultado[
                "registros_invalidos"
            ]
        ):

            numero = (
                registro[
                    "numero_linea"
                ]
            )

            contenido = (
                registro[
                    "contenido"
                ]
            )

            error = (
                registro[
                    "error"
                ]
            )

            lineas_invalidas.append(
                (
                    f"Línea {numero}: {error}\n"
                    f"Contenido: {contenido}\n"
                    + "-" * 70
                )
            )

        if lineas_invalidas:

            texto_invalidos = "\n".join(
                lineas_invalidas
            )

        else:

            texto_invalidos = (
                "No se detectaron registros inválidos."
            )

        self.escribir_textbox(
            self.txt_invalidos,
            texto_invalidos
        )

        # -----------------------------------------------------
        # BARRA PRINCIPAL
        # -----------------------------------------------------

        if cantidad_invalidos == 0:

            self.ventana_principal.actualizar_barra_estado(
                (
                    f"Estado: Logs validados - "
                    f"{cantidad_validos} válidos"
                ),
                "exito"
            )

        else:

            self.ventana_principal.actualizar_barra_estado(
                (
                    f"Estado: Logs validados - "
                    f"{cantidad_validos} válidos, "
                    f"{cantidad_invalidos} inválidos"
                ),
                "advertencia"
            )