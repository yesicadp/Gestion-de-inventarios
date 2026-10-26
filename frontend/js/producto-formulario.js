
document.addEventListener("DOMContentLoaded", () => {
  const API_PRODUCTOS = "http://127.0.0.1:5000/api/productos";
  const API_CATEGORIAS = "http://127.0.0.1:5000/api/categorias";

  const token = localStorage.getItem("token");

  const form = document.getElementById("form-producto");
  const mensaje = document.getElementById("mensaje-formulario");
  const botonGuardar = document.getElementById("btn-guardar");

  const campos = {
    codigo: document.getElementById("codigo"),
    nombre: document.getElementById("nombre"),
    categoria: document.getElementById("categoria"),
    existencia: document.getElementById("existencia"),
    minimo: document.getElementById("minimo"),
    estado: document.getElementById("estado")
  };

  let categoriasCargadas = false;

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  function mostrarMensaje(texto, esError = false) {
    mensaje.textContent = texto;
    mensaje.className = `form-message ${esError ? "error" : "success"}`;
  }

  // Cargar las categorías reales desde el backend.
  async function cargarCategorias() {
    campos.categoria.disabled = true;
    campos.categoria.innerHTML =
      '<option value="">Cargando categorías...</option>';

    try {
      const respuesta = await fetch(API_CATEGORIAS, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const datos = await respuesta.json();

      if (respuesta.status === 401 || respuesta.status === 403) {
        throw new Error(
          "Tu sesión no está autorizada. Inicia sesión nuevamente."
        );
      }

      if (!respuesta.ok) {
        throw new Error(datos.mensaje || "No se pudieron cargar las categorías.");
      }

      const categorias = datos.categorias || [];

      campos.categoria.innerHTML =
        '<option value="">Selecciona una categoría</option>';

      categorias.forEach((categoria) => {
        const opcion = document.createElement("option");
        opcion.value = categoria.id_categoria;
        opcion.textContent = categoria.nombre;
        campos.categoria.appendChild(opcion);
      });

      categoriasCargadas = true;
      campos.categoria.disabled = false;

      if (categorias.length === 0) {
        mostrarMensaje(
          "Primero debes registrar una categoría antes de crear un producto.",
          true
        );
      }
    } catch (error) {
      console.error("Error al cargar categorías:", error);
      campos.categoria.innerHTML =
        '<option value="">No se pudieron cargar las categorías</option>';
      mostrarMensaje(error.message, true);
    }
  }

  // Guardar un producto en la base de datos.
  form.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    if (!categoriasCargadas) {
      mostrarMensaje("Espera a que se carguen las categorías.", true);
      return;
    }

    const codigo = campos.codigo.value.trim();
    const nombre = campos.nombre.value.trim();
    const categoriaId = Number(campos.categoria.value);
    const existenciaTexto = campos.existencia.value.trim();
    const minimoTexto = campos.minimo.value.trim();
    const existencia = Number(existenciaTexto);
    const minimo = Number(minimoTexto);
    const estado = campos.estado.value === "activo" ? 1 : 0;

    if (!codigo || !nombre || !campos.categoria.value) {
      mostrarMensaje("Completa todos los campos obligatorios.", true);
      return;
    }

    if (
      existenciaTexto === "" ||
      minimoTexto === "" ||
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

    botonGuardar.disabled = true;
    mostrarMensaje("Guardando producto...");

    try {
      const respuesta = await fetch(API_PRODUCTOS, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          codigo,
          nombre,
          categoria_id: categoriaId,
          existencia_actual: existencia,
          existencia_minima: minimo,
          estado
        })
      });

      const datos = await respuesta.json();

      if (respuesta.status === 401 || respuesta.status === 403) {
        mostrarMensaje(
          "Tu sesión no está autorizada. Inicia sesión nuevamente.",
          true
        );
        return;
      }

      if (!respuesta.ok) {
        mostrarMensaje(
          datos.mensaje || "No se pudo registrar el producto.",
          true
        );
        return;
      }

      mostrarMensaje(
        datos.mensaje || "Producto registrado correctamente."
      );

      form.reset();

      setTimeout(() => {
        window.location.href = "productos.html";
      }, 900);
    } catch (error) {
      console.error("Error al guardar producto:", error);
      mostrarMensaje(
        "No fue posible conectar con el servidor. Verifica que Flask esté ejecutándose.",
        true
      );
    } finally {
      botonGuardar.disabled = false;
    }
  });

  cargarCategorias();
});
