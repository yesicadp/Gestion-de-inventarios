"""Lectura y validación de parámetros de consulta (?q=&categoria_id=&desde=...).

Todas lanzan ErrorValidacion (400). Llámalas ANTES del try/obtener_conexion de la ruta.
"""
from datetime import datetime, timedelta

from flask import request

from app.shared.exceptions.errores import ErrorValidacion

FORMATO_FECHA_HORA = "%Y-%m-%d %H:%M:%S"
POR_PAGINA_MAXIMO = 100


def texto_opcional(nombre):
    valor = (request.args.get(nombre) or "").strip()
    return valor or None


def entero_opcional(nombre):
    crudo = (request.args.get(nombre) or "").strip()
    if not crudo:
        return None
    if not crudo.isdigit() or int(crudo) <= 0:
        raise ErrorValidacion(f"El parámetro '{nombre}' debe ser un entero positivo")
    return int(crudo)


def booleano_opcional(nombre):
    """?nombre=1|0|true|false|si|no -> 1, 0 o None si no viene."""
    crudo = (request.args.get(nombre) or "").strip().lower()
    if not crudo:
        return None
    if crudo in ("1", "true", "si", "sí"):
        return 1
    if crudo in ("0", "false", "no"):
        return 0
    raise ErrorValidacion(f"El parámetro '{nombre}' debe ser 1 o 0")


def estado_opcional(nombre="estado"):
    """?estado=activo|inactivo|1|0|todos -> 1, 0 o None (sin filtrar)."""
    crudo = (request.args.get(nombre) or "").strip().lower()
    if crudo in ("", "todos"):
        return None
    if crudo in ("activo", "1", "true"):
        return 1
    if crudo in ("inactivo", "0", "false"):
        return 0
    raise ErrorValidacion(f"El parámetro '{nombre}' debe ser activo, inactivo o todos")


def tipo_movimiento_opcional(nombre="tipo"):
    crudo = (request.args.get(nombre) or "").strip().upper()
    if not crudo:
        return None
    if crudo not in ("ENTRADA", "SALIDA"):
        raise ErrorValidacion(f"El parámetro '{nombre}' debe ser ENTRADA o SALIDA")
    return crudo


def rango_fechas():
    """?desde=AAAA-MM-DD&hasta=AAAA-MM-DD -> (inicio, fin_exclusivo) como texto de fecha y hora.

    'hasta' incluye todo ese día (se devuelve el día siguiente a las 00:00 como límite exclusivo).
    """
    def leer(nombre):
        crudo = (request.args.get(nombre) or "").strip()
        if not crudo:
            return None
        try:
            return datetime.strptime(crudo, "%Y-%m-%d")
        except ValueError:
            raise ErrorValidacion(f"El parámetro '{nombre}' debe tener formato AAAA-MM-DD")

    desde, hasta = leer("desde"), leer("hasta")
    if desde and hasta and desde > hasta:
        raise ErrorValidacion("'desde' no puede ser posterior a 'hasta'")

    return (
        desde.strftime(FORMATO_FECHA_HORA) if desde else None,
        (hasta + timedelta(days=1)).strftime(FORMATO_FECHA_HORA) if hasta else None,
    )


def paginacion(obligatoria=False, por_pagina_defecto=10):
    """?pagina=1&por_pagina=10 -> (pagina, por_pagina), o None si no se pidió paginar.

    Con obligatoria=True siempre devuelve valores (por defecto pagina=1).
    """
    hay_pagina = request.args.get("pagina") not in (None, "")
    hay_por_pagina = request.args.get("por_pagina") not in (None, "")

    if not obligatoria and not hay_pagina and not hay_por_pagina:
        return None

    try:
        pagina = int(request.args.get("pagina") or 1)
        por_pagina = int(request.args.get("por_pagina") or por_pagina_defecto)
    except ValueError:
        raise ErrorValidacion("'pagina' y 'por_pagina' deben ser números enteros")

    if pagina < 1 or por_pagina < 1 or por_pagina > POR_PAGINA_MAXIMO:
        raise ErrorValidacion(
            f"'pagina' debe ser mayor o igual a 1 y 'por_pagina' debe estar entre 1 y {POR_PAGINA_MAXIMO}"
        )

    return pagina, por_pagina


def datos_paginacion(pagina, por_pagina, total):
    return {
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total_paginas": max(1, -(-total // por_pagina)),
    }


def fecha_iso(valor):
    """datetime -> 'AAAA-MM-DDTHH:MM:SS'. Evita el formato HTTP/GMT de jsonify, que desplaza las horas."""
    if valor is None:
        return None
    return valor.isoformat() if hasattr(valor, "isoformat") else str(valor).replace(" ", "T")
