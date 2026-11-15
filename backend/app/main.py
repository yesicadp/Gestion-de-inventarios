from flask import Flask, jsonify
from flask_cors import CORS
from app.modules.authentication.routes import authentication_bp
from app.modules.authentication.decorators import requiere_token
from app.modules.products.routes import products_bp
from app.modules.categories.routes import categories_bp
from app.modules.inventory.routes import inventory_bp
from app.modules.movements.routes import movements_bp
from app.modules.audit.routes import audit_bp
from app.shared.exceptions.errores import registrar_manejadores

app = Flask(__name__)
CORS(app)
app.register_blueprint(authentication_bp)
app.register_blueprint(products_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(movements_bp)
app.register_blueprint(audit_bp)
registrar_manejadores(app)

@app.get("/")
def inicio():
    return jsonify({"mensaje": "API de inventarios funcionando"}), 200

@app.get("/api/health")
def estado():
    return jsonify({
        "status": "ok",
        "mensaje": "La API esta disponible"
    }), 200

@app.get("/api/perfil")
@requiere_token
def perfil(datos_usuario):
    return jsonify({
        "mensaje": "Acceso autorizado",
        "usuario": datos_usuario["usuario"]
    }), 200

if __name__ == "__main__":
    app.run(debug=True)

