
const API_INVENTARIO = "http://127.0.0.1:5000/api/inventario";
const API_CATEGORIAS = "http://127.0.0.1:5000/api/categorias";

document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  const buscador = document.getElementById("buscar-inventario");
  const filtroCategoria = document.getElementById("filtro-categoria");
  const filtroExistencia = document.getElementById("filtro-existencia");
  const tabla = document.getElementById("tabla-inventario");
  const mensaje = document.getElementById("mensaje-inventario");
  const totalProductos = document.getElementById("total-productos");
  const totalBajos = document.getElementById("total-bajos");
  const contador = document.getElementById("contador-inventario");

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  let productos = [];

  // Consultar las categorías para llenar el filtro.
  async function consultarCategorias() {
    try {
      const respuesta = await fetch(API_CATEGORIAS, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(datos.mensaje || "No se pudieron consultar las categorías.");
      }

      filtroCategoria.innerHTML =
        '<option value="">Todas las categorías</option>';

      (datos.categorias || []).forEach((categoria) => {
        const opcion = document.createElement("option");
        opcion.value = categoria.id_categoria;
        opcion.textContent = categoria.nombre;
        filtroCategoria.appendChild(opcion);
      });

    } catch (error) {
      console.error("Error al consultar categorías:", error);
    }
  }

  // Consultar inventario aplicando los filtros seleccionados.
  async function consultarInventario() {
    mensaje.textContent = "Cargando inventario...";

    const parametros = new URLSearchParams();

    const texto = buscador.value.trim();
    const categoriaId = filtroCategoria.value;
    const existenciaBaja = filtroExistencia.value;

    if (texto) {
      parametros.append("q", texto);
    }

    if (categoriaId) {
      parametros.append("categoria_id", categoriaId);
    }

    if (existenciaBaja !== "") {
      parametros.append("existencia_baja", existenciaBaja);
    }

    const url = parametros.toString()
      ? `${API_INVENTARIO}?${parametros.toString()}`
      : API_INVENTARIO;

    try {
      const respuesta = await fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const datos = await respuesta.json();

      if (respuesta.status === 401 || respuesta.status === 403) {
        mensaje.textContent =
          "Tu sesión no está autorizada. Inicia sesión nuevamente.";
        return;
      }

      if (!respuesta.ok) {
        throw new Error(
          datos.mensaje || "No se pudo consultar el inventario."
        );
      }

      productos = datos.productos || [];

      mostrarInventario(datos);

      mensaje.textContent = productos.length
        ? "Inventario consultado correctamente."
        : "No se encontraron productos con los filtros seleccionados.";

    } catch (error) {
      console.error("Error al consultar inventario:", error);
      productos = [];
      mostrarInventario({
        total: 0,
        total_existencias_bajas: 0,
        productos: []
      });
      mensaje.textContent =
        error.message || "No fue posible conectar con el servidor.";
    }
  }

  // Mostrar los productos en la tabla.
  function mostrarInventario(datos) {
    tabla.innerHTML = "";

    totalProductos.textContent = datos.total ?? productos.length;
    totalBajos.textContent = datos.total_existencias_bajas ?? 0;

    if (productos.length === 0) {
      const fila = document.createElement("tr");
      const celda = document.createElement("td");

      celda.colSpan = 6;
      celda.textContent = "No hay productos para mostrar.";

      fila.appendChild(celda);
      tabla.appendChild(fila);
    } else {
      productos.forEach((producto) => {
        const fila = document.createElement("tr");

        const celdaCodigo = document.createElement("td");
        celdaCodigo.textContent = producto.codigo || "—";

        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = producto.nombre;

        const celdaCategoria = document.createElement("td");
        celdaCategoria.textContent = producto.categoria || "Sin categoría";

        const celdaActual = document.createElement("td");
        celdaActual.textContent = producto.existencia_actual;

        const celdaMinima = document.createElement("td");
        celdaMinima.textContent = producto.existencia_minima;

        const celdaEstado = document.createElement("td");
        const estado = document.createElement("span");

        const existenciaBaja = Number(producto.existencia_baja) === 1;

        estado.classList.add(
          "inventory-status",
          existenciaBaja ? "low" : "normal"
        );

        estado.textContent = existenciaBaja
          ? "Existencia baja"
          : "Normal";

        celdaEstado.appendChild(estado);

        fila.append(
          celdaCodigo,
          celdaNombre,
          celdaCategoria,
          celdaActual,
          celdaMinima,
          celdaEstado
        );

        tabla.appendChild(fila);
      });
    }

    contador.textContent =
      `${productos.length} ${productos.length === 1 ? "producto" : "productos"}`;
  }

  // Actualizar consulta al cambiar los filtros.
  buscador.addEventListener("input", consultarInventario);
  filtroCategoria.addEventListener("change", consultarInventario);
  filtroExistencia.addEventListener("change", consultarInventario);

  // Cargar categorías e inventario al entrar.
  async function iniciarInventario() {
    await consultarCategorias();
    await consultarInventario();
  }

  iniciarInventario();
});
