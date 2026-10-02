from modelos.afn import AFN
from modelos.expresion_regular import (
    ExpresionRegular
)

from algoritmos.procesador_regex import (
    convertir_a_postfija
)


EPSILON = "ε"

OPERADORES = {
    "|",
    "·",
    "*",
    "+",
    "?"
}


class _GeneradorEstados:
    """
    Genera nombres de estados consecutivos:

    q0, q1, q2, q3...
    """

    def __init__(self):
        self.contador = 0

    def nuevo(self):

        estado = (
            f"q{self.contador}"
        )

        self.contador += 1

        return estado


class _Fragmento:
    """
    Representa temporalmente una parte
    del AFN durante la construcción
    de Thompson.
    """

    def __init__(
        self,
        inicio,
        fin,
        estados=None,
        transiciones=None
    ):

        self.inicio = inicio
        self.fin = fin

        self.estados = set(
            estados or []
        )

        self.transiciones = list(
            transiciones or []
        )


def _crear_fragmento_simbolo(
    simbolo,
    generador
):
    """
    Construye el fragmento básico
    correspondiente a un símbolo.

    q0 --a--> q1

    También permite ε.
    """

    inicio = generador.nuevo()
    fin = generador.nuevo()

    return _Fragmento(
        inicio=inicio,
        fin=fin,
        estados={
            inicio,
            fin
        },
        transiciones=[
            (
                inicio,
                simbolo,
                fin
            )
        ]
    )


def _concatenar(
    izquierdo,
    derecho
):
    """
    Une dos fragmentos mediante ε.

    A seguido de B:

    A.fin --ε--> B.inicio
    """

    estados = (
        izquierdo.estados
        | derecho.estados
    )

    transiciones = (
        izquierdo.transiciones
        + derecho.transiciones
        + [
            (
                izquierdo.fin,
                EPSILON,
                derecho.inicio
            )
        ]
    )

    return _Fragmento(
        inicio=izquierdo.inicio,
        fin=derecho.fin,
        estados=estados,
        transiciones=transiciones
    )


def _unir(
    izquierdo,
    derecho,
    generador
):
    """
    Construcción de Thompson
    para la unión A|B.
    """

    inicio = generador.nuevo()
    fin = generador.nuevo()

    estados = (
        izquierdo.estados
        | derecho.estados
        | {
            inicio,
            fin
        }
    )

    transiciones = (
        izquierdo.transiciones
        + derecho.transiciones
        + [
            (
                inicio,
                EPSILON,
                izquierdo.inicio
            ),
            (
                inicio,
                EPSILON,
                derecho.inicio
            ),
            (
                izquierdo.fin,
                EPSILON,
                fin
            ),
            (
                derecho.fin,
                EPSILON,
                fin
            )
        ]
    )

    return _Fragmento(
        inicio=inicio,
        fin=fin,
        estados=estados,
        transiciones=transiciones
    )


def _estrella(
    fragmento,
    generador
):
    """
    Construcción de Thompson
    para A*.

    Permite cero o más repeticiones.
    """

    inicio = generador.nuevo()
    fin = generador.nuevo()

    estados = (
        fragmento.estados
        | {
            inicio,
            fin
        }
    )

    transiciones = (
        fragmento.transiciones
        + [
            (
                inicio,
                EPSILON,
                fragmento.inicio
            ),
            (
                inicio,
                EPSILON,
                fin
            ),
            (
                fragmento.fin,
                EPSILON,
                fragmento.inicio
            ),
            (
                fragmento.fin,
                EPSILON,
                fin
            )
        ]
    )

    return _Fragmento(
        inicio=inicio,
        fin=fin,
        estados=estados,
        transiciones=transiciones
    )


def _mas(
    fragmento,
    generador
):
    """
    Construcción para A+.

    Permite una o más repeticiones.
    """

    inicio = generador.nuevo()
    fin = generador.nuevo()

    estados = (
        fragmento.estados
        | {
            inicio,
            fin
        }
    )

    transiciones = (
        fragmento.transiciones
        + [
            (
                inicio,
                EPSILON,
                fragmento.inicio
            ),
            (
                fragmento.fin,
                EPSILON,
                fragmento.inicio
            ),
            (
                fragmento.fin,
                EPSILON,
                fin
            )
        ]
    )

    return _Fragmento(
        inicio=inicio,
        fin=fin,
        estados=estados,
        transiciones=transiciones
    )


def _opcional(
    fragmento,
    generador
):
    """
    Construcción para A?.

    Permite cero o una aparición.
    """

    inicio = generador.nuevo()
    fin = generador.nuevo()

    estados = (
        fragmento.estados
        | {
            inicio,
            fin
        }
    )

    transiciones = (
        fragmento.transiciones
        + [
            (
                inicio,
                EPSILON,
                fragmento.inicio
            ),
            (
                inicio,
                EPSILON,
                fin
            ),
            (
                fragmento.fin,
                EPSILON,
                fin
            )
        ]
    )

    return _Fragmento(
        inicio=inicio,
        fin=fin,
        estados=estados,
        transiciones=transiciones
    )


def construir_afn_thompson(
    expresion,
    nombre="AFN generado por Thompson"
):
    """
    Convierte una expresión regular
    en un AFN-ε utilizando la
    Construcción de Thompson.

    Devuelve un objeto AFN compatible
    con todos los módulos desarrollados
    durante la Fase 1.
    """

    regex = ExpresionRegular(
        nombre=nombre,
        expresion=expresion
    )

    postfija = convertir_a_postfija(
        regex.expresion
    )

    generador = _GeneradorEstados()

    pila = []

    for simbolo in postfija:

        # =====================================================
        # OPERANDO
        # =====================================================

        if simbolo not in OPERADORES:

            pila.append(
                _crear_fragmento_simbolo(
                    simbolo,
                    generador
                )
            )

            continue

        # =====================================================
        # CONCATENACIÓN
        # =====================================================

        if simbolo == "·":

            if len(pila) < 2:
                raise ValueError(
                    "No existen suficientes "
                    "operandos para concatenar."
                )

            derecho = pila.pop()
            izquierdo = pila.pop()

            pila.append(
                _concatenar(
                    izquierdo,
                    derecho
                )
            )

            continue

        # =====================================================
        # UNIÓN
        # =====================================================

        if simbolo == "|":

            if len(pila) < 2:
                raise ValueError(
                    "No existen suficientes "
                    "operandos para realizar la unión."
                )

            derecho = pila.pop()
            izquierdo = pila.pop()

            pila.append(
                _unir(
                    izquierdo,
                    derecho,
                    generador
                )
            )

            continue

        # =====================================================
        # ESTRELLA
        # =====================================================

        if simbolo == "*":

            if not pila:
                raise ValueError(
                    "El operador '*' no tiene operando."
                )

            fragmento = pila.pop()

            pila.append(
                _estrella(
                    fragmento,
                    generador
                )
            )

            continue

        # =====================================================
        # UNA O MÁS
        # =====================================================

        if simbolo == "+":

            if not pila:
                raise ValueError(
                    "El operador '+' no tiene operando."
                )

            fragmento = pila.pop()

            pila.append(
                _mas(
                    fragmento,
                    generador
                )
            )

            continue

        # =====================================================
        # OPCIONAL
        # =====================================================

        if simbolo == "?":

            if not pila:
                raise ValueError(
                    "El operador '?' no tiene operando."
                )

            fragmento = pila.pop()

            pila.append(
                _opcional(
                    fragmento,
                    generador
                )
            )

    # =========================================================
    # VALIDAR RESULTADO
    # =========================================================

    if len(pila) != 1:

        raise ValueError(
            "No fue posible construir correctamente "
            "el AFN a partir de la expresión regular."
        )

    fragmento_final = pila.pop()

    # =========================================================
    # CREAR AFN REAL
    # =========================================================

    afn = AFN(
        nombre=nombre,
        estados=fragmento_final.estados,
        alfabeto=regex.obtener_alfabeto(),
        estado_inicial=fragmento_final.inicio,
        estados_finales={
            fragmento_final.fin
        }
    )

    # =========================================================
    # AGREGAR TRANSICIONES
    # =========================================================

    for (
        origen,
        simbolo,
        destino
    ) in fragmento_final.transiciones:

        afn.agregar_transicion(
            origen,
            simbolo,
            destino
        )

    # =========================================================
    # INFORMACIÓN ADICIONAL
    # =========================================================

    afn.expresion_regular = (
        regex.expresion
    )

    afn.expresion_postfija = (
        postfija
    )

    afn.metodo_generacion = (
        "Construcción de Thompson"
    )

    return afn

# SI SE PUDO HJPTM ;D