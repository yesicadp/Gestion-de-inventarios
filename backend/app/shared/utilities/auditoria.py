"""Registro automático de auditoría.

Se llama con el MISMO cursor de la operación, antes del commit: la acción y su registro de auditoría
se guardan juntos o no se guarda ninguno (si falla uno, el rollback deshace ambos).
"""


def registrar_auditoria(cursor, usuario_id, modulo, accion, detalle=None):
    cursor.execute(
        """
        INSERT INTO auditoria (usuario_id, modulo, accion, detalle)
        VALUES (%s, %s, %s, %s)
        """,
        (usuario_id, modulo, accion, (detalle or "")[:255] or None),
    )
