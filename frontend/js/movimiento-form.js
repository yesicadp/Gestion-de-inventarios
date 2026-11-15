
document.addEventListener("DOMContentLoaded", () => {
  const API_PRODUCTOS = "http://127.0.0.1:5000/api/productos";
  const API_MOVIMIENTOS = "http://127.0.0.1:5000/api/movimientos";

  const token = localStorage.getItem("token");

  const formulario = document.getElementById("form-movimiento");
  const productoSelect = document.getElementById("producto-movimiento");
  const tipoSelect = document.getElementById("tipo-movimiento");
  const cantidadInput = document.getElementById("cantidad-movimiento");
  const motivoInput = document.getElementById("motivo-movimiento");
  const existenciaInput = document.getElementById("existencia-actual");
  const mensaje = document.getElementById("mensaje-movimiento");
  const botonRegistrar = document.getElementById("btn-registrar-movimiento");

  let productos = [];

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  function mostrarMensaje(texto, tipo = "") {
    mensaje.textContent = texto;
    mensaje.className = "products-message";

    if (tipo) {
      mensaje.classList.add(tipo);
    }
  }

  function esActivo(producto) {
    return (
      producto.estado === true ||
      producto.estado === 1 ||
      producto.estado === "1"
    );
  }

  // Consultar productos y mostrar únicamente los activos.
  async function cargarProductos(idSeleccionado = "") {
    mostrarMensaje("Cargando productos...");

    try {
      const respuesta = await fetch(API_PRODUCTOS, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const datos = await respuesta.json();

      if (respuesta.status === 401 || respuesta.status === 403) {
        mostrarMensaje("Tu sesión no está autorizada. Inicia sesión nuevamente.");
        return;
      }

      if (!respuesta.ok) {
        throw new Error(datos.mensaje || "No fue posible consultar los productos.");
      }

      productos = (datos.productos || []).filter(esActivo);

      productoSelect.innerHTML =
        '<option value="">Selecciona un producto</option>';

      productos.forEach((producto) => {
        const opcion = document.createElement("option");
        opcion.value = producto.id_producto;
        opcion.textContent = `${producto.codigo} - ${producto.nombre}`;
        productoSelect.appendChild(opcion);
      });

      if (idSeleccionado) {
        productoSelect.value = String(idSeleccionado);
      }

      actualizarExistencia();

      mostrarMensaje(
        productos.length
          ? "Productos disponibles para registrar movimientos."
          : "No hay productos activos disponibles."
      );

    } catch (error) {
      console.error("Error al cargar productos:", error);
      mostrarMensaje(error.message || "No fue posible conectar con el servidor.");
    }
  }

  // Mostrar las existencias del producto seleccionado.
  function actualizarExistencia() {
    const idProducto = Number(productoSelect.value);

    const producto = productos.find(
      (item) => Number(item.id_producto) === idProducto
    );

    existenciaInput.value = producto
      ? producto.existencia_actual
      : "Selecciona un producto";
  }

  productoSelect.addEventListener("change", actualizarExistencia);

  // Registrar entrada o salida.
  formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const productoId = Number(productoSelect.value);
    const tipo = tipoSelect.value;
    const cantidad = Number(cantidadInput.value);
    const motivo = motivoInput.value.trim();

    if (!productoId) {
      mostrarMensaje("Debes seleccionar un producto.");
      return;
    }

    if (!tipo) {
      mostrarMensaje("Debes seleccionar el tipo de movimiento.");
      return;
    }

    if (!Number.isInteger(cantidad) || cantidad <= 0) {
      mostrarMensaje("La cantidad debe ser un número entero mayor que cero.");
      return;
    }

    if (!motivo) {
      mostrarMensaje("Debes escribir el motivo del movimiento.");
      return;
    }

    const producto = productos.find(
      (item) => Number(item.id_producto) === productoId
    );

    if (!producto) {
      mostrarMensaje("El producto seleccionado no está disponible.");
      return;
    }

    if (
      tipo === "SALIDA" &&
      cantidad > Number(producto.existencia_actual)
    ) {
      mostrarMensaje(
        `No hay existencias suficientes. Disponibles: ${producto.existencia_actual}.`
      );
      return;
    }

    botonRegistrar.disabled = true;
    botonRegistrar.textContent = "Registrando...";

    try {
      const respuesta = await fetch(API_MOVIMIENTOS, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          producto_id: productoId,
          tipo_movimiento: tipo,
          cantidad: cantidad,
          motivo: motivo
        })
      });

      const datos = await respuesta.json();

      if (respuesta.status === 401 || respuesta.status === 403) {
        mostrarMensaje("Tu sesión no está autorizada para registrar movimientos.");
        return;
      }

      if (!respuesta.ok) {
        throw new Error(
          datos.mensaje || "No fue posible registrar el movimiento."
        );
      }

      const movimiento = datos.movimiento;

      mostrarMensaje(
        `${datos.mensaje}. Nueva existencia de ${movimiento.producto}: ${movimiento.existencia_resultante}.`
      );

      formulario.reset();

      // Actualizar la existencia consultando nuevamente el backend.
      await cargarProductos();

    } catch (error) {
      console.error("Error al registrar movimiento:", error);
      mostrarMensaje(error.message || "No fue posible conectar con el servidor.");
    } finally {
      botonRegistrar.disabled = false;
      botonRegistrar.textContent = "Registrar movimiento";
    }
  });

  // Limpiar también el dato de existencias al reiniciar el formulario.
  formulario.addEventListener("reset", () => {
    setTimeout(() => {
      actualizarExistencia();
    }, 0);
  });

  cargarProductos();
});
