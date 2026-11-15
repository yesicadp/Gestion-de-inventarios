"""Pruebas de las rutas de inventario, movimientos, búsqueda/filtros, auditoría y permisos.

Ejecutar desde backend/:   python -m unittest discover -s tests -t . -v      (o: pytest)
"""
import os
import tempfile
import unittest
from unittest import mock

os.environ.setdefault("JWT_SECRET_KEY", "clave-de-pruebas-suficientemente-larga-123456")

import jwt  # noqa: E402
from flask import Flask  # noqa: E402

from tests import soporte  # noqa: E402,F401  (debe importarse antes que la app)
from app.database import connection  # noqa: E402
from app.modules.audit.routes import audit_bp  # noqa: E402
from app.modules.categories.routes import categories_bp  # noqa: E402
from app.modules.inventory.routes import inventory_bp  # noqa: E402
from app.modules.movements.routes import movements_bp  # noqa: E402
from app.modules.products.routes import products_bp  # noqa: E402
from app.shared.exceptions.errores import registrar_manejadores  # noqa: E402


def token(usuario_id, nombre, rol):
    return jwt.encode({"usuario_id": usuario_id, "usuario": nombre, "rol": rol},
                      os.environ["JWT_SECRET_KEY"], algorithm="HS256")


class BaseApi(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.fabrica = soporte.crear_base(os.path.join(self.dir.name, "t.db"))
        for destino in ("app.database.connection.obtener_conexion",
                        "app.modules.products.routes.obtener_conexion",
                        "app.modules.categories.routes.obtener_conexion",
                        "app.modules.inventory.routes.obtener_conexion",
                        "app.modules.movements.routes.obtener_conexion",
                        "app.modules.audit.routes.obtener_conexion"):
            parche = mock.patch(destino, self.fabrica)
            parche.start()
            self.addCleanup(parche.stop)

        app = Flask(__name__)
        for bp in (products_bp, categories_bp, inventory_bp, movements_bp, audit_bp):
            app.register_blueprint(bp)
        registrar_manejadores(app)
        self.c = app.test_client()
        self.admin = {"Authorization": f"Bearer {token(1, 'Admin Demo', 'Administrador')}"}
        self.user = {"Authorization": f"Bearer {token(2, 'Usuario Demo', 'Usuario')}"}

    # ---- ayudas ----
    def categoria(self, nombre="Periféricos", padre=None):
        r = self.c.post("/api/categorias", json={"nombre": nombre, "categoria_padre_id": padre}, headers=self.admin)
        self.assertEqual(r.status_code, 201, r.get_json())
        return r.get_json()["categoria"]["id_categoria"]

    def producto(self, categoria_id, codigo="PROD-001", nombre="Teclado USB", actual=10, minimo=5, estado=1):
        r = self.c.post("/api/productos", headers=self.admin, json={
            "codigo": codigo, "nombre": nombre, "categoria_id": categoria_id,
            "existencia_actual": actual, "existencia_minima": minimo, "estado": estado})
        self.assertEqual(r.status_code, 201, r.get_json())
        return r.get_json()["producto"]["id_producto"]

    def mover(self, producto_id, tipo, cantidad, motivo="prueba", headers=None):
        return self.c.post("/api/movimientos", headers=headers or self.user, json={
            "producto_id": producto_id, "tipo_movimiento": tipo, "cantidad": cantidad, "motivo": motivo})

    def sql(self, consulta, params=()):
        con = self.fabrica()
        cur = con.cursor(dictionary=True)
        cur.execute(consulta, params)
        filas = cur.fetchall()
        con.close()
        return filas


class TestPermisos(BaseApi):
    def test_sin_token_401_en_todas_las_rutas(self):
        for ruta in ("/api/productos", "/api/categorias", "/api/inventario", "/api/movimientos", "/api/auditoria"):
            self.assertEqual(self.c.get(ruta).status_code, 401, ruta)

    def test_usuario_normal_no_puede_crear_ni_editar_ni_ver_auditoria(self):
        cat = self.categoria()
        prod = self.producto(cat)
        cuerpo_prod = {"codigo": "X", "nombre": "X", "categoria_id": cat, "existencia_actual": 1,
                       "existencia_minima": 1, "estado": 1}
        for metodo, ruta, cuerpo in (("post", "/api/productos", cuerpo_prod),
                                     ("put", f"/api/productos/{prod}", cuerpo_prod),
                                     ("post", "/api/categorias", {"nombre": "Otra"}),
                                     ("get", "/api/auditoria", None)):
            r = getattr(self.c, metodo)(ruta, json=cuerpo, headers=self.user)
            self.assertEqual(r.status_code, 403, ruta)
            self.assertIn("administrador", r.get_json()["mensaje"])

    def test_usuario_normal_si_puede_consultar_y_mover(self):
        cat = self.categoria()
        prod = self.producto(cat)
        for ruta in ("/api/productos", f"/api/productos/{prod}", "/api/categorias", "/api/inventario", "/api/movimientos"):
            self.assertEqual(self.c.get(ruta, headers=self.user).status_code, 200, ruta)
        self.assertEqual(self.mover(prod, "salida", 1).status_code, 201)

    def test_admin_accede_a_todo(self):
        self.assertEqual(self.c.get("/api/auditoria", headers=self.admin).status_code, 200)

    def test_rol_falso_en_token_no_pasa(self):
        falso = {"Authorization": "Bearer " + jwt.encode({"usuario_id": 2, "rol": "Administrador"}, "otra-clave-distinta-1234567890123", algorithm="HS256")}
        self.assertEqual(self.c.get("/api/auditoria", headers=falso).status_code, 401)


class TestBusquedaYFiltros(BaseApi):
    def setUp(self):
        super().setUp()
        self.raiz = self.categoria("Electrónica")
        self.hija = self.categoria("Pantallas", self.raiz)
        self.otra = self.categoria("Papelería")
        self.producto(self.raiz, "ELE-001", "Teclado USB")
        self.producto(self.hija, "PAN-001", "Monitor 24")
        self.producto(self.otra, "PAP-001", "Cuaderno", estado=0)

    def codigos(self, ruta):
        r = self.c.get(ruta, headers=self.user)
        self.assertEqual(r.status_code, 200, r.get_json())
        d = r.get_json()
        self.assertEqual(d["total"], len(d["productos"]))
        return sorted(p["codigo"] for p in d["productos"])

    def test_busqueda_por_nombre_y_codigo(self):
        self.assertEqual(self.codigos("/api/productos?q=teclado"), ["ELE-001"])
        self.assertEqual(self.codigos("/api/productos?q=PAN-"), ["PAN-001"])
        self.assertEqual(self.codigos("/api/productos?q=inexistente"), [])

    def test_filtro_categoria_incluye_subcategorias(self):
        self.assertEqual(self.codigos(f"/api/productos?categoria_id={self.raiz}"), ["ELE-001", "PAN-001"])
        self.assertEqual(self.codigos(f"/api/productos?categoria_id={self.hija}"), ["PAN-001"])

    def test_filtro_estado(self):
        self.assertEqual(self.codigos("/api/productos?estado=inactivo"), ["PAP-001"])
        self.assertEqual(self.codigos("/api/productos?estado=0"), ["PAP-001"])
        self.assertEqual(self.codigos("/api/productos?estado=activo"), ["ELE-001", "PAN-001"])
        self.assertEqual(self.codigos("/api/productos?estado=todos"), ["ELE-001", "PAN-001", "PAP-001"])

    def test_filtros_combinados(self):
        self.assertEqual(self.codigos(f"/api/productos?categoria_id={self.raiz}&q=monitor&estado=activo"), ["PAN-001"])
        self.assertEqual(self.codigos(f"/api/productos?categoria_id={self.otra}&estado=activo"), [])

    def test_parametros_invalidos_400(self):
        for ruta in ("/api/productos?estado=raro", "/api/productos?categoria_id=abc", "/api/productos?categoria_id=-1"):
            r = self.c.get(ruta, headers=self.user)
            self.assertEqual(r.status_code, 400, ruta)
            self.assertIn("mensaje", r.get_json())

    def test_formato_compatible_con_el_frontend(self):
        d = self.c.get("/api/productos", headers=self.user).get_json()
        self.assertEqual(set(d), {"mensaje", "total", "productos"})
        self.assertTrue({"id_producto", "nombre", "codigo", "categoria_id", "categoria", "existencia_actual",
                         "existencia_minima", "estado"} <= set(d["productos"][0]))


class TestInventario(BaseApi):
    def setUp(self):
        super().setUp()
        self.cat = self.categoria()
        self.hija = self.categoria("Teclados", self.cat)
        self.a = self.producto(self.cat, "A-1", "Mouse", actual=4, minimo=5)      # bajo
        self.b = self.producto(self.cat, "B-1", "Cable", actual=5, minimo=5)      # borde: igual al mínimo = bajo
        self.c_ = self.producto(self.hija, "C-1", "Teclado", actual=6, minimo=5)  # ok
        self.d = self.producto(self.cat, "D-1", "Viejo", actual=0, minimo=5, estado=0)  # inactivo: no cuenta

    def test_calculo_de_existencias_bajas(self):
        d = self.c.get("/api/inventario", headers=self.user).get_json()
        self.assertEqual((d["total"], d["total_existencias_bajas"]), (3, 2))
        banderas = {p["codigo"]: p["existencia_baja"] for p in d["productos"]}
        self.assertEqual(banderas, {"A-1": 1, "B-1": 1, "C-1": 0})  # D-1 inactivo no aparece

    def test_filtros(self):
        def codigos(q):
            return sorted(p["codigo"] for p in self.c.get("/api/inventario" + q, headers=self.user).get_json()["productos"])
        self.assertEqual(codigos("?existencia_baja=1"), ["A-1", "B-1"])
        self.assertEqual(codigos("?existencia_baja=0"), ["C-1"])
        self.assertEqual(codigos("?q=teclado"), ["C-1"])
        self.assertEqual(codigos(f"?categoria_id={self.cat}"), ["A-1", "B-1", "C-1"])
        self.assertEqual(codigos(f"?categoria_id={self.hija}&existencia_baja=1"), [])
        self.assertEqual(self.c.get("/api/inventario?existencia_baja=quizas", headers=self.user).status_code, 400)

    def test_una_salida_cambia_el_calculo(self):
        self.mover(self.c_, "SALIDA", 1)  # 6 -> 5 = mínimo
        d = self.c.get("/api/inventario", headers=self.user).get_json()
        self.assertEqual(d["total_existencias_bajas"], 3)
        self.mover(self.a, "ENTRADA", 10)  # 4 -> 14
        self.assertEqual(self.c.get("/api/inventario", headers=self.user).get_json()["total_existencias_bajas"], 2)


class TestMovimientos(BaseApi):
    def setUp(self):
        super().setUp()
        self.cat = self.categoria()
        self.p = self.producto(self.cat, actual=10, minimo=5)

    def existencia(self):
        return self.sql("SELECT existencia_actual FROM productos WHERE id_producto = ?", (self.p,))[0]["existencia_actual"]

    def test_entrada_y_salida_actualizan_existencias_y_guardan_todo(self):
        r = self.mover(self.p, "salida", 3, "Venta mostrador")  # minúsculas se aceptan
        d = r.get_json()
        self.assertEqual(r.status_code, 201)
        self.assertEqual((d["tipo_movimiento"], d["cantidad"], d["existencia_resultante"]), ("SALIDA", 3, 7))
        m = d["movimiento"]
        self.assertEqual((m["existencia_anterior"], m["existencia_resultante"], m["existencia_baja"]), (10, 7, 0))
        self.assertEqual(self.existencia(), 7)
        r = self.mover(self.p, "ENTRADA", 8, "Compra")
        self.assertEqual(r.get_json()["existencia_resultante"], 15)
        fila = self.sql("SELECT * FROM movimientos ORDER BY id_movimiento")
        self.assertEqual(len(fila), 2)
        self.assertEqual((fila[0]["usuario_id"], fila[0]["tipo_movimiento"], fila[0]["cantidad"], fila[0]["motivo"],
                          fila[0]["existencia_resultante"]), (2, "SALIDA", 3, "Venta mostrador", 7))
        self.assertTrue(fila[0]["fecha"])  # fecha guardada

    def test_guarda_el_usuario_que_hace_el_movimiento(self):
        self.mover(self.p, "SALIDA", 1, headers=self.user)
        self.mover(self.p, "SALIDA", 1, headers=self.admin)
        self.assertEqual([f["usuario_id"] for f in self.sql("SELECT usuario_id FROM movimientos ORDER BY id_movimiento")], [2, 1])

    def test_no_permite_salida_mayor_a_la_existencia(self):
        r = self.mover(self.p, "SALIDA", 11)
        self.assertEqual(r.status_code, 400)
        d = r.get_json()
        self.assertEqual((d["existencia_disponible"], d["cantidad_solicitada"]), (10, 11))
        self.assertEqual(self.existencia(), 10)
        self.assertEqual(self.sql("SELECT COUNT(*) AS n FROM movimientos")[0]["n"], 0)
        self.assertEqual(self.mover(self.p, "SALIDA", 10).status_code, 201)  # justo todo el stock sí
        self.assertEqual(self.existencia(), 0)
        self.assertEqual(self.mover(self.p, "SALIDA", 1).status_code, 400)

    def test_validaciones(self):
        casos = [
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": 0, "motivo": "x"},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": -3, "motivo": "x"},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": 1.5, "motivo": "x"},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": "5", "motivo": "x"},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": True, "motivo": "x"},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": None, "motivo": "x"},
            {"producto_id": self.p, "tipo_movimiento": "AJUSTE", "cantidad": 1, "motivo": "x"},
            {"producto_id": self.p, "tipo_movimiento": "", "cantidad": 1, "motivo": "x"},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": 1, "motivo": ""},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": 1, "motivo": "   "},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": 1},
            {"producto_id": self.p, "tipo_movimiento": "ENTRADA", "cantidad": 1, "motivo": "x" * 256},
            {"producto_id": "abc", "tipo_movimiento": "ENTRADA", "cantidad": 1, "motivo": "x"},
            {"producto_id": 0, "tipo_movimiento": "ENTRADA", "cantidad": 1, "motivo": "x"},
            {"tipo_movimiento": "ENTRADA", "cantidad": 1, "motivo": "x"},
        ]
        for cuerpo in casos:
            r = self.c.post("/api/movimientos", json=cuerpo, headers=self.user)
            self.assertEqual(r.status_code, 400, cuerpo)
        for crudo in ("no es json", "[1,2]"):
            r = self.c.post("/api/movimientos", data=crudo, headers={**self.user, "Content-Type": "application/json"})
            self.assertEqual(r.status_code, 400, crudo)
        self.assertEqual(self.existencia(), 10)
        self.assertEqual(self.sql("SELECT COUNT(*) AS n FROM movimientos")[0]["n"], 0)

    def test_producto_inexistente_e_inactivo(self):
        self.assertEqual(self.mover(9999, "ENTRADA", 1).status_code, 404)
        self.c.put(f"/api/productos/{self.p}", headers=self.admin, json={
            "nombre": "Teclado USB", "codigo": "PROD-001", "categoria_id": self.cat,
            "existencia_actual": 10, "existencia_minima": 5, "estado": 0})
        r = self.mover(self.p, "ENTRADA", 1)
        self.assertEqual(r.status_code, 409)
        self.assertIn("inactivo", r.get_json()["mensaje"])

    def test_transaccion_si_falla_la_auditoria_no_queda_nada(self):
        with mock.patch("app.modules.movements.routes.registrar_auditoria", side_effect=RuntimeError("falla")):
            r = self.mover(self.p, "SALIDA", 4)
        self.assertEqual(r.status_code, 500)
        self.assertEqual(self.existencia(), 10)  # rollback: la existencia no cambió
        self.assertEqual(self.sql("SELECT COUNT(*) AS n FROM movimientos")[0]["n"], 0)
        self.assertEqual(self.mover(self.p, "SALIDA", 4).status_code, 201)  # y luego funciona normal
        self.assertEqual(self.existencia(), 6)

    def test_existencia_resultante_cuadra_en_una_secuencia(self):
        esperado = 10
        for tipo, cant in (("SALIDA", 3), ("ENTRADA", 5), ("SALIDA", 12), ("ENTRADA", 1), ("SALIDA", 1)):
            esperado += cant if tipo == "ENTRADA" else -cant
            self.mover(self.p, tipo, cant)
        resultantes = [f["existencia_resultante"] for f in self.sql("SELECT existencia_resultante FROM movimientos ORDER BY id_movimiento")]
        self.assertEqual(resultantes, [7, 12, 0, 1, 0])
        self.assertEqual(self.existencia(), esperado)


class TestHistorial(BaseApi):
    def setUp(self):
        super().setUp()
        cat = self.categoria()
        self.a = self.producto(cat, "A-1", "Mouse", actual=50)
        self.b = self.producto(cat, "B-1", "Teclado", actual=50)
        self.mover(self.a, "SALIDA", 2, headers=self.user)
        self.mover(self.a, "ENTRADA", 3, headers=self.admin)
        self.mover(self.b, "SALIDA", 4, headers=self.user)

    def get(self, q=""):
        r = self.c.get("/api/movimientos" + q, headers=self.user)
        self.assertEqual(r.status_code, 200, r.get_json())
        return r.get_json()

    def test_listado_completo_con_datos_utiles(self):
        d = self.get()
        self.assertEqual((d["total"], len(d["movimientos"])), (3, 3))
        self.assertNotIn("pagina", d)  # sin paginar, devuelve todo
        m = d["movimientos"][0]  # el más reciente primero
        self.assertEqual((m["codigo"], m["producto"], m["usuario"], m["tipo_movimiento"]), ("B-1", "Teclado", "Usuario Demo", "SALIDA"))
        self.assertIn("T", m["fecha"])  # ISO 8601, no formato HTTP/GMT
        self.assertTrue({"id_movimiento", "producto_id", "usuario_id", "cantidad", "motivo", "existencia_resultante"} <= set(m))

    def test_filtros(self):
        self.assertEqual(self.get(f"?producto_id={self.a}")["total"], 2)
        self.assertEqual(self.get("?tipo=salida")["total"], 2)
        self.assertEqual(self.get("?tipo=ENTRADA")["total"], 1)
        self.assertEqual(self.get("?usuario_id=1")["total"], 1)
        self.assertEqual(self.get("?q=tecl")["total"], 1)
        self.assertEqual(self.get("?q=A-1")["total"], 2)
        self.assertEqual(self.get(f"?producto_id={self.a}&tipo=SALIDA&usuario_id=2")["total"], 1)
        self.assertEqual(self.get("?desde=2000-01-01&hasta=2100-01-01")["total"], 3)
        self.assertEqual(self.get("?desde=2000-01-01&hasta=2000-01-31")["total"], 0)
        self.assertEqual(self.get("?desde=2100-01-01")["total"], 0)

    def test_paginacion(self):
        d = self.get("?pagina=2&por_pagina=2")
        self.assertEqual((d["total"], len(d["movimientos"]), d["pagina"], d["por_pagina"], d["total_paginas"]), (3, 1, 2, 2, 2))
        d = self.get("?por_pagina=2&tipo=SALIDA")
        self.assertEqual((d["total"], len(d["movimientos"]), d["total_paginas"]), (2, 2, 1))

    def test_parametros_invalidos_400(self):
        for q in ("?tipo=otro", "?desde=ayer", "?hasta=2026-13-45", "?desde=2026-02-01&hasta=2026-01-01",
                  "?producto_id=x", "?pagina=0", "?por_pagina=500", "?pagina=a"):
            self.assertEqual(self.c.get("/api/movimientos" + q, headers=self.user).status_code, 400, q)


class TestAuditoria(BaseApi):
    def get(self, q="", headers=None):
        r = self.c.get("/api/auditoria" + q, headers=headers or self.admin)
        self.assertEqual(r.status_code, 200, r.get_json())
        return r.get_json()

    def test_registra_creacion_edicion_desactivacion_y_movimientos(self):
        cat = self.categoria("Periféricos")
        prod = self.producto(cat, "PROD-001", "Teclado", actual=10, minimo=5)
        self.c.put(f"/api/productos/{prod}", headers=self.admin, json={
            "nombre": "Teclado Pro", "codigo": "PROD-001", "categoria_id": cat,
            "existencia_actual": 10, "existencia_minima": 8, "estado": 1})
        self.mover(prod, "SALIDA", 3, "Venta", headers=self.user)
        self.mover(prod, "ENTRADA", 1, "Compra", headers=self.user)
        self.c.put(f"/api/productos/{prod}", headers=self.admin, json={
            "nombre": "Teclado Pro", "codigo": "PROD-001", "categoria_id": cat,
            "existencia_actual": 8, "existencia_minima": 8, "estado": 0})
        d = self.get()
        acciones = [(r["modulo"], r["accion"], r["usuario_id"]) for r in reversed(d["auditoria"])]
        self.assertEqual(acciones, [("categorias", "CREAR", 1), ("productos", "CREAR", 1), ("productos", "EDITAR", 1),
                                    ("movimientos", "SALIDA", 2), ("movimientos", "ENTRADA", 2), ("productos", "DESACTIVAR", 1)])
        por_accion = {(r["modulo"], r["accion"]): r["detalle"] for r in d["auditoria"]}
        self.assertIn("nombre Teclado -> Teclado Pro", por_accion[("productos", "EDITAR")])
        self.assertIn("existencia_minima 5 -> 8", por_accion[("productos", "EDITAR")])
        self.assertIn("10 -> 7", por_accion[("movimientos", "SALIDA")])
        self.assertIn("estado 1 -> 0", por_accion[("productos", "DESACTIVAR")])
        self.assertEqual({"mensaje", "total", "auditoria", "pagina", "por_pagina", "total_paginas"}, set(d))
        self.assertIn("T", d["auditoria"][0]["fecha"])
        self.assertEqual(d["auditoria"][0]["usuario"], "Admin Demo")

    def test_reactivar_registra_activar(self):
        cat = self.categoria()
        prod = self.producto(cat, estado=0)
        self.c.put(f"/api/productos/{prod}", headers=self.admin, json={
            "nombre": "Teclado USB", "codigo": "PROD-001", "categoria_id": cat,
            "existencia_actual": 10, "existencia_minima": 5, "estado": 1})
        self.assertEqual(self.get("?accion=activar")["total"], 1)

    def test_no_audita_lo_que_falla_ni_lo_que_no_cambia(self):
        cat = self.categoria()
        prod = self.producto(cat)
        antes = self.get()["total"]
        self.mover(prod, "SALIDA", 999)                                    # rechazada
        self.c.post("/api/productos", headers=self.admin, json={"codigo": "PROD-001", "nombre": "Dup", "categoria_id": cat})  # duplicado
        self.c.post("/api/categorias", headers=self.admin, json={"nombre": ""})
        self.c.put(f"/api/productos/{prod}", headers=self.admin, json={          # sin cambios
            "nombre": "Teclado USB", "codigo": "PROD-001", "categoria_id": cat,
            "existencia_actual": 10, "existencia_minima": 5, "estado": 1})
        self.c.post("/api/productos", headers=self.user, json={"codigo": "Z", "nombre": "Z", "categoria_id": cat})  # sin permiso
        self.assertEqual(self.get()["total"], antes)

    def test_filtros_y_paginacion(self):
        cat = self.categoria()
        prod = self.producto(cat, actual=50)
        for _ in range(4):
            self.mover(prod, "SALIDA", 1, headers=self.user)
        self.assertEqual(self.get("?modulo=movimientos")["total"], 4)
        self.assertEqual(self.get("?modulo=Movimientos&accion=salida")["total"], 4)
        self.assertEqual(self.get("?usuario_id=2")["total"], 4)
        self.assertEqual(self.get("?usuario_id=1")["total"], 2)
        self.assertEqual(self.get("?q=PROD-001")["total"], 5)
        self.assertEqual(self.get("?desde=2000-01-01&hasta=2000-01-02")["total"], 0)
        d = self.get("?por_pagina=4&pagina=2")
        self.assertEqual((d["total"], len(d["auditoria"]), d["total_paginas"]), (6, 2, 2))
        self.assertEqual(self.get()["por_pagina"], 50)  # paginación por defecto
        for q in ("?usuario_id=x", "?desde=hoy", "?por_pagina=101", "?pagina=0"):
            self.assertEqual(self.c.get("/api/auditoria" + q, headers=self.admin).status_code, 400, q)


class TestProductosYCategorias(BaseApi):
    def test_crud_basico_y_errores(self):
        cat = self.categoria()
        prod = self.producto(cat)
        self.assertEqual(self.c.post("/api/productos", headers=self.admin, json={
            "codigo": "PROD-001", "nombre": "Otro", "categoria_id": cat}).status_code, 409)
        self.assertEqual(self.c.post("/api/productos", headers=self.admin, json={
            "codigo": "N", "nombre": "N", "categoria_id": 999}).status_code, 400)
        self.assertEqual(self.c.post("/api/categorias", headers=self.admin, json={"nombre": "periféricos"}).status_code, 409)
        self.assertEqual(self.c.post("/api/categorias", headers=self.admin, json={"nombre": "X", "categoria_padre_id": 999}).status_code, 404)
        d = self.c.get(f"/api/productos/{prod}", headers=self.user).get_json()
        self.assertEqual(d["producto"]["codigo"], "PROD-001")
        self.assertEqual(self.c.get("/api/productos/999", headers=self.user).status_code, 404)
        self.assertEqual(self.c.put("/api/productos/999", headers=self.admin, json={
            "nombre": "x", "codigo": "x", "categoria_id": cat, "existencia_actual": 1, "existencia_minima": 1, "estado": 1}).status_code, 404)


class TestMain(unittest.TestCase):
    def test_main_registra_todas_las_rutas(self):
        try:
            from app.main import app
        except ImportError as e:  # librerías opcionales no instaladas en este entorno
            self.skipTest(f"no se pudo importar app.main: {e}")
        rutas = {r.rule for r in app.url_map.iter_rules()}
        for ruta in ("/api/auth/login", "/api/productos", "/api/categorias", "/api/inventario",
                     "/api/movimientos", "/api/auditoria", "/api/health"):
            self.assertIn(ruta, rutas)


if __name__ == "__main__":
    unittest.main()
