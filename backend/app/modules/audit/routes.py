from flask import Blueprint, jsonify

from app.database.connection import obtener_conexion
from app.shared.security.permisos import requiere_admin
from app.shared.utilities.consultas import (
    datos_paginacion,
    entero_opcional,
    fecha_iso,
    paginacion,
    rango_fechas,
    texto_opcional,
)

audit_bp = Blueprint("audit", __name__)


@audit_bp.get("/api/auditoria")
@requiere_admin
def consultar_auditoria(datos_usuario):
    # Solo Administrador. Filtros opcionales (se validan antes de abrir la conexión):
    #   usuario_id=N  modulo=productos|categorias|movimientos  accion=CREAR|EDITAR|...
    #   desde=AAAA-MM-DD  hasta=AAAA-MM-DD  q=texto (busca en el detalle)
    #   pagina=N&por_pagina=N (por defecto pagina 1, 50 por página, máximo 100)
    usuario_id = entero_opcional("usuario_id")
    modulo = texto_opcional("modulo")
    accion = texto_opcional("accion")
    texto = texto_opcional("q")
    desde, hasta_exclusivo = rango_fechas()
    numero, por_pagina = paginacion(obligatoria=True, por_pagina_defecto=50)

    condiciones = []
    parametros = []

    if usuario_id is not None:
        condiciones.append("a.usuario_id = %s")
        parametros.append(usuario_id)

    if modulo:
        condiciones.append("a.modulo = %s")
        parametros.append(modulo.lower())

    if accion:
        condiciones.append("a.accion = %s")
        parametros.append(accion.upper())

    if desde:
        condiciones.append("a.fecha >= %s")
        parametros.append(desde)

    if hasta_exclusivo:
        condiciones.append("a.fecha < %s")
        parametros.append(hasta_exclusivo)

    if texto:
        condiciones.append("a.detalle LIKE %s")
        parametros.append(f"%{texto}%")

    donde = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(f"""
            SELECT COUNT(*) AS total
            FROM auditoria a
            {donde}
        """, parametros)
        total = cursor.fetchone()["total"]

        cursor.execute(f"""
            SELECT
                a.id_auditoria,
                a.usuario_id,
                u.nombre AS usuario,
                a.modulo,
                a.accion,
                a.fecha,
                a.detalle
            FROM auditoria a
            INNER JOIN usuarios u
                ON a.usuario_id = u.id_usuario
            {donde}
            ORDER BY a.fecha DESC, a.id_auditoria DESC
            LIMIT %s OFFSET %s
        """, parametros + [por_pagina, (numero - 1) * por_pagina])

        registros = cursor.fetchall()

        for registro in registros:
            registro["fecha"] = fecha_iso(registro["fecha"])

        respuesta = {
            "mensaje": "Auditoría consultada correctamente",
            "total": total,
            "auditoria": registros
        }
        respuesta.update(datos_paginacion(numero, por_pagina, total))

        return jsonify(respuesta), 200

    except Exception:
        return jsonify({
            "mensaje": "No fue posible consultar la auditoría"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()
