OPERADORES_BINARIOS = {
    "|"
}

OPERADORES_UNARIOS = {
    "*",
    "+",
    "?"
}

EPSILON = "ε"


def normalizar_expresion(expresion):
    """
    Elimina espacios de una expresión regular.

    Ejemplo:
    ( a | b ) *
    se convierte en:
    (a|b)*
    """

    if expresion is None:
        raise ValueError(
            "La expresión regular no puede ser nula."
        )

    expresion = "".join(
        str(expresion).split()
    )

    if not expresion:
        raise ValueError(
            "La expresión regular no puede estar vacía."
        )

    return expresion


def validar_expresion_regular(expresion):
    """
    Comprueba que una expresión regular tenga
    una estructura sintáctica válida.

    Operadores soportados:

    |  unión
    *  cero o más
    +  uno o más
    ?  cero o uno
    () agrupación

    La concatenación es implícita.
    """

    expresion = normalizar_expresion(
        expresion
    )

    analizador = _AnalizadorRegex(
        expresion
    )

    analizador.validar()

    return expresion


class _AnalizadorRegex:
    """
    Analizador sintáctico sencillo para
    expresiones regulares.

    Utiliza una estructura similar a:

    expresión -> término ('|' término)*
    término   -> factor+
    factor    -> base operador_unario?
    base      -> símbolo | ε | '(' expresión ')'
    """

    def __init__(
        self,
        expresion
    ):
        self.expresion = expresion
        self.posicion = 0

    # =========================================================
    # UTILIDADES
    # =========================================================

    def actual(self):

        if self.posicion >= len(
            self.expresion
        ):
            return None

        return self.expresion[
            self.posicion
        ]

    def avanzar(self):

        self.posicion += 1

    # =========================================================
    # VALIDACIÓN PRINCIPAL
    # =========================================================

    def validar(self):

        self._expresion()

        if self.actual() is not None:

            if self.actual() == ")":

                raise ValueError(
                    "Existe un paréntesis ')' "
                    "sin su correspondiente '('."
                )

            raise ValueError(
                f"Símbolo inesperado "
                f"'{self.actual()}' en la expresión."
            )

        return True

    # =========================================================
    # EXPRESIÓN
    # =========================================================

    def _expresion(self):

        self._termino()

        while self.actual() == "|":

            self.avanzar()

            siguiente = self.actual()

            if (
                siguiente is None
                or siguiente == ")"
            ):

                raise ValueError(
                    "El operador '|' necesita "
                    "una expresión a su derecha."
                )

            self._termino()

    # =========================================================
    # TÉRMINO
    # =========================================================

    def _termino(self):

        cantidad_factores = 0

        while (
            self.actual() is not None
            and self.actual()
            not in {"|", ")"}
        ):

            self._factor()

            cantidad_factores += 1

        if cantidad_factores == 0:

            raise ValueError(
                "Se esperaba un símbolo "
                "o una subexpresión."
            )

    # =========================================================
    # FACTOR
    # =========================================================

    def _factor(self):

        self._base()

        actual = self.actual()

        if actual in OPERADORES_UNARIOS:

            self.avanzar()

            if (
                self.actual()
                in OPERADORES_UNARIOS
            ):

                raise ValueError(
                    "No se permiten operadores "
                    "de repetición consecutivos."
                )

    # =========================================================
    # BASE
    # =========================================================

    def _base(self):

        actual = self.actual()

        if actual is None:

            raise ValueError(
                "La expresión regular está incompleta."
            )

        # =====================================================
        # PARÉNTESIS
        # =====================================================

        if actual == "(":

            self.avanzar()

            if self.actual() == ")":

                raise ValueError(
                    "Los paréntesis no pueden "
                    "estar vacíos."
                )

            self._expresion()

            if self.actual() != ")":

                raise ValueError(
                    "Existe un paréntesis '(' "
                    "sin su correspondiente ')'."
                )

            self.avanzar()

            return

        # =====================================================
        # CIERRE SIN APERTURA
        # =====================================================

        if actual == ")":

            raise ValueError(
                "Existe un paréntesis ')' "
                "sin su correspondiente '('."
            )

        # =====================================================
        # UNIÓN
        # =====================================================

        if actual in OPERADORES_BINARIOS:

            raise ValueError(
                f"El operador '{actual}' "
                "no puede aparecer en esta posición."
            )

        # =====================================================
        # OPERADOR UNARIO SIN OPERANDO
        # =====================================================

        if actual in OPERADORES_UNARIOS:

            raise ValueError(
                f"El operador '{actual}' necesita "
                "una expresión antes de él."
            )

        # =====================================================
        # SÍMBOLO NORMAL O EPSILON
        # =====================================================

        self.avanzar()