from utilidades.validador_regex import (
    validar_expresion_regular
)


class ExpresionRegular:
    """
    Representa una expresión regular dentro del sistema.

    Almacena:
    - Nombre
    - Expresión regular
    - Alfabeto detectado

    Antes de crear el objeto se comprueba
    que la expresión tenga una sintaxis válida.
    """

    OPERADORES = {
        "|",
        "*",
        "+",
        "?",
        "(",
        ")"
    }

    EPSILON = "ε"

    def __init__(
        self,
        nombre,
        expresion
    ):

        self.nombre = nombre.strip()

        self.expresion = (
            expresion.strip()
            if expresion is not None
            else ""
        )

        self._validar_datos_basicos()

        # =====================================================
        # VALIDACIÓN SINTÁCTICA
        # =====================================================

        self.expresion = (
            validar_expresion_regular(
                self.expresion
            )
        )

        # =====================================================
        # ALFABETO
        # =====================================================

        self.alfabeto = (
            self._obtener_alfabeto()
        )

    # =========================================================
    # VALIDACIONES BÁSICAS
    # =========================================================

    def _validar_datos_basicos(self):

        if not self.nombre:

            raise ValueError(
                "La expresión regular debe "
                "tener un nombre."
            )

        if not self.expresion:

            raise ValueError(
                "La expresión regular no "
                "puede estar vacía."
            )

    # =========================================================
    # OBTENER ALFABETO
    # =========================================================

    def _obtener_alfabeto(self):

        alfabeto = set()

        for simbolo in self.expresion:

            if simbolo.isspace():

                continue

            if simbolo in self.OPERADORES:

                continue

            if simbolo == self.EPSILON:

                continue

            alfabeto.add(
                simbolo
            )

        return alfabeto

    # =========================================================
    # DEVOLVER ALFABETO
    # =========================================================

    def obtener_alfabeto(self):

        return set(
            self.alfabeto
        )

    # =========================================================
    # REPRESENTACIÓN
    # =========================================================

    def __str__(self):

        return (
            f"Nombre: {self.nombre}\n"
            f"Expresión: {self.expresion}\n"
            f"Alfabeto: {sorted(self.alfabeto)}"
        )