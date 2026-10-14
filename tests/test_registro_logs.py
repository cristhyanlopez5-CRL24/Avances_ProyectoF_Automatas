import pytest

import utilidades.registro_logs as logs


def preparar_logs(
    tmp_path,
    monkeypatch
):

    logs.cerrar_logging()

    carpeta = (
        tmp_path
        / "logs"
    )

    monkeypatch.setattr(
        logs,
        "CARPETA_LOGS",
        carpeta
    )

    return carpeta


def test_crear_archivo_txt(
    tmp_path,
    monkeypatch
):

    preparar_logs(
        tmp_path,
        monkeypatch
    )

    ruta = logs.registrar_info(
        "SISTEMA",
        "Aplicación iniciada correctamente"
    )

    assert ruta.exists()

    assert (
        ruta.suffix
        == ".txt"
    )

    assert (
        ruta.name.startswith(
            "logs_"
        )
    )

    logs.cerrar_logging()


def test_registrar_info(
    tmp_path,
    monkeypatch
):

    preparar_logs(
        tmp_path,
        monkeypatch
    )

    ruta = logs.registrar_info(
        "REGEX",
        "Expresión regular analizada"
    )

    contenido = ruta.read_text(
        encoding="utf-8"
    )

    assert "INFO" in contenido

    assert "REGEX" in contenido

    assert (
        "Expresión regular analizada"
        in contenido
    )

    logs.cerrar_logging()


def test_registrar_error(
    tmp_path,
    monkeypatch
):

    preparar_logs(
        tmp_path,
        monkeypatch
    )

    ruta = logs.registrar_error(
        "ARCHIVO",
        "No se pudo abrir el archivo"
    )

    contenido = ruta.read_text(
        encoding="utf-8"
    )

    assert "ERROR" in contenido

    assert "ARCHIVO" in contenido

    assert (
        "No se pudo abrir el archivo"
        in contenido
    )

    logs.cerrar_logging()


def test_varios_eventos_mismo_archivo(
    tmp_path,
    monkeypatch
):

    preparar_logs(
        tmp_path,
        monkeypatch
    )

    ruta = logs.registrar_info(
        "SISTEMA",
        "Aplicación iniciada"
    )

    logs.registrar_warning(
        "REGEX",
        "Expresión inválida"
    )

    logs.registrar_error(
        "ARCHIVO",
        "Error de lectura"
    )

    contenido = ruta.read_text(
        encoding="utf-8"
    )

    assert "INFO" in contenido

    assert "WARNING" in contenido

    assert "ERROR" in contenido

    logs.cerrar_logging()


def test_rechazar_nivel_invalido(
    tmp_path,
    monkeypatch
):

    preparar_logs(
        tmp_path,
        monkeypatch
    )

    with pytest.raises(
        ValueError
    ):

        logs.registrar_evento(
            "DESCONOCIDO",
            "SISTEMA",
            "Prueba"
        )

    logs.cerrar_logging()


def test_rechazar_mensaje_vacio(
    tmp_path,
    monkeypatch
):

    preparar_logs(
        tmp_path,
        monkeypatch
    )

    with pytest.raises(
        ValueError
    ):

        logs.registrar_error(
            "SISTEMA",
            ""
        )

    logs.cerrar_logging()