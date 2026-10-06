import json

import utilidades.logs_validacion as logs


def test_registrar_validacion_aceptada(
    tmp_path,
    monkeypatch
):

    archivo = (
        tmp_path
        / "logs.json"
    )

    monkeypatch.setattr(
        logs,
        "ARCHIVO_LOGS",
        archivo
    )

    registro = (
        logs.registrar_validacion(
            "(0|1)*01",
            "1101",
            True
        )
    )

    assert (
        registro["expresion"]
        == "(0|1)*01"
    )

    assert (
        registro["cadena"]
        == "1101"
    )

    assert (
        registro["resultado"]
        == "Aceptada"
    )


def test_registrar_validacion_rechazada(
    tmp_path,
    monkeypatch
):

    archivo = (
        tmp_path
        / "logs.json"
    )

    monkeypatch.setattr(
        logs,
        "ARCHIVO_LOGS",
        archivo
    )

    logs.registrar_validacion(
        "a*",
        "b",
        False
    )

    datos = json.loads(
        archivo.read_text(
            encoding="utf-8"
        )
    )

    assert len(datos) == 1

    assert (
        datos[0]["resultado"]
        == "Rechazada"
    )


def test_cadena_vacia_se_guarda_como_epsilon(
    tmp_path,
    monkeypatch
):

    archivo = (
        tmp_path
        / "logs.json"
    )

    monkeypatch.setattr(
        logs,
        "ARCHIVO_LOGS",
        archivo
    )

    logs.registrar_validacion(
        "a*",
        "",
        True
    )

    datos = logs.cargar_logs()

    assert (
        datos[0]["cadena"]
        == "ε"
    )


def test_cargar_logs_vacio(
    tmp_path,
    monkeypatch
):

    archivo = (
        tmp_path
        / "logs.json"
    )

    monkeypatch.setattr(
        logs,
        "ARCHIVO_LOGS",
        archivo
    )

    assert (
        logs.cargar_logs()
        == []
    )


def test_limpiar_logs(
    tmp_path,
    monkeypatch
):

    archivo = (
        tmp_path
        / "logs.json"
    )

    monkeypatch.setattr(
        logs,
        "ARCHIVO_LOGS",
        archivo
    )

    logs.registrar_validacion(
        "a",
        "a",
        True
    )

    logs.limpiar_logs()

    assert (
        logs.cargar_logs()
        == []
    )
    