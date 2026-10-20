
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-producto");
  const mensaje = document.getElementById("mensaje-formulario");
  const titulo = document.getElementById("titulo-formulario");
  const botonGuardar = document.getElementById("btn-guardar");

  const campos = {
    codigo: document.getElementById("codigo"),
    nombre: document.getElementById("nombre"),
    categoria: document.getElementById("categoria"),
    existencia: document.getElementById("existencia"),
    minimo: document.getElementById("minimo"),
    estado: document.getElementById("estado")
  };

  const claveDemo = "productosDemo";
  const parametros = new URLSearchParams(window.location.search);
  const codigoEditar = parametros.get("codigo");

  let productos = [];

  try {
    productos = JSON.parse(localStorage.getItem(claveDemo) || "[]");

    if (!Array.isArray(productos)) {
      productos = [];
    }
  } catch (error) {
    productos = [];
  }
  
  function generarCodigo() {
    const codigosExistentes = productos.map(p => p.codigo);

    let numero = 1;
    let codigo;

    do {
        codigo = `PROD-${String(numero).padStart(3, "0")}`;
        numero++;
    } while (codigosExistentes.includes(codigo));

    return codigo;
  }
  if (!codigoEditar) {
  campos.codigo.value = generarCodigo();
  }

  if (codigoEditar) {
    const producto = productos.find(p => p.codigo === codigoEditar);

    if (producto) {
      titulo.textContent = "Editar producto";
      botonGuardar.textContent = "Guardar cambios";

      campos.codigo.value = producto.codigo;
      campos.codigo.readOnly = true;
      campos.nombre.value = producto.nombre;
      campos.categoria.value = producto.categoria;
      campos.existencia.value = producto.existencia;
      campos.minimo.value = producto.minimo;
      campos.estado.value = producto.estado ? "activo" : "inactivo";
    } else {
      mensaje.textContent =
        "No se encontró ese producto en los datos de demostración.";
      mensaje.className = "form-message error";
      form.querySelectorAll("input, select, button").forEach(campo => {
        campo.disabled = true;
      });
      return;
    }
  }

  form.addEventListener("submit", event => {
    event.preventDefault();

    const codigo = campos.codigo.value.trim();
    const nombre = campos.nombre.value.trim();
    const categoria = campos.categoria.value;
    const existencia = Number(campos.existencia.value);
    const minimo = Number(campos.minimo.value);
    const estado = campos.estado.value === "activo";

    if (!codigo || !nombre || !categoria) {
      mostrarMensaje("Completa todos los campos obligatorios.", true);
      return;
    }

    if (
      campos.existencia.value.trim() === "" ||
      campos.minimo.value.trim() === "" ||
      !Number.isInteger(existencia) ||
      !Number.isInteger(minimo) ||
      existencia < 0 ||
      minimo < 0
    ) {
      mostrarMensaje(
        "Las existencias deben ser números enteros iguales o mayores que cero.",
        true
      );
      return;
    }

    const existeCodigo = productos.some(p =>
        p.codigo.toLowerCase() === codigo.toLowerCase() &&
        p.codigo !== codigoEditar
    );

    if (existeCodigo) {
        campos.codigo.value = generarCodigo();
        mostrarMensaje(
            "El código ya estaba registrado. Se asignó uno nuevo; vuelve a guardar.",
            true
        );
        return;
    }

    if (existeCodigo) {
      mostrarMensaje("Ya existe un producto con ese código.", true);
      return;
    }

    const producto = {
      codigo,
      nombre,
      categoria,
      existencia,
      minimo,
      estado
    };

    if (codigoEditar) {
      productos = productos.map(p =>
        p.codigo === codigoEditar ? producto : p
      );
    } else {
      productos.push(producto);
    }

    try {
      localStorage.setItem(claveDemo, JSON.stringify(productos));
      mostrarMensaje("Producto guardado en la demostración.", false);

      setTimeout(() => {
        window.location.href = "productos.html";
      }, 700);
    } catch (error) {
      mostrarMensaje(
        "No se pudo guardar en el navegador. Revisa el almacenamiento disponible.",
        true
      );
    }
  });

  function mostrarMensaje(texto, esError) {
    mensaje.textContent = texto;
    mensaje.className = `form-message ${esError ? "error" : "success"}`;
  }
});
