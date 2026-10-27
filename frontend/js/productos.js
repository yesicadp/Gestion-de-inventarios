document.addEventListener("DOMContentLoaded", () => {
  const API_PRODUCTOS = "http://127.0.0.1:5000/api/productos";

  const token = localStorage.getItem("token");

  const buscar = document.getElementById("buscar-producto");
  const filtroCategoria = document.getElementById("filtro-categoria");
  const filtroEstado = document.getElementById("filtro-estado");
  const tabla = document.getElementById("tabla-productos");
  const mensaje = document.getElementById("mensaje-productos");
  const contador = document.getElementById("contador-productos");
  const paginaActual = document.getElementById("pagina-actual");
  const anterior = document.getElementById("pagina-anterior");
  const siguiente = document.getElementById("pagina-siguiente");
  const botonNuevo = document.getElementById("btn-nuevo-producto");

  const porPagina = 5;

  let productos = [];
  let pagina = 1;

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  // Consultar los productos registrados en la base de datos.
  async function cargarProductos() {
    mensaje.textContent = "Cargando productos...";

    try {
      const respuesta = await fetch(API_PRODUCTOS, {
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
          datos.mensaje || "No fue posible consultar los productos."
        );
      }

      productos = (datos.productos || []).map((producto) => ({
        id: producto.id_producto,
        codigo: producto.codigo,
        nombre: producto.nombre,
        categoria: producto.categoria,
        existencia: Number(producto.existencia_actual),
        minimo: Number(producto.existencia_minima),
        estado:
          producto.estado === true ||
          producto.estado === 1 ||
          producto.estado === "1"
      }));

      cargarFiltroCategorias();
      renderizar();

      mensaje.textContent = productos.length
        ? "Productos consultados correctamente."
        : "Todavía no hay productos registrados en la base de datos.";
    } catch (error) {
      console.error("Error al consultar productos:", error);
      mensaje.textContent =
        error.message || "No fue posible conectar con el servidor.";
    }
  }

  // Llenar el filtro con las categorías que realmente tienen productos.
  function cargarFiltroCategorias() {
    const seleccionAnterior = filtroCategoria.value;

    filtroCategoria.innerHTML =
      '<option value="">Todas las categorías</option>';

    const categorias = [
      ...new Set(productos.map((producto) => producto.categoria))
    ].sort((a, b) => a.localeCompare(b, "es"));

    categorias.forEach((categoria) => {
      const opcion = document.createElement("option");
      opcion.value = categoria;
      opcion.textContent = categoria;
      filtroCategoria.appendChild(opcion);
    });

    if (categorias.includes(seleccionAnterior)) {
      filtroCategoria.value = seleccionAnterior;
    }
  }

  // Aplicar búsqueda y filtros.
  function obtenerFiltrados() {
    const texto = buscar.value.trim().toLowerCase();

    return productos.filter((producto) => {
      const coincideTexto = [
        producto.codigo,
        producto.nombre,
        producto.categoria
      ].some((valor) =>
        String(valor || "").toLowerCase().includes(texto)
      );

      const coincideCategoria =
        !filtroCategoria.value ||
        producto.categoria === filtroCategoria.value;

      const coincideEstado =
        !filtroEstado.value ||
        (filtroEstado.value === "activo" && producto.estado) ||
        (filtroEstado.value === "inactivo" && !producto.estado);

      return coincideTexto && coincideCategoria && coincideEstado;
    });
  }

  function crearCelda(texto) {
    const celda = document.createElement("td");
    celda.textContent = texto;
    return celda;
  }

  // Mostrar la información en la tabla.
  function renderizar() {
    const filtrados = obtenerFiltrados();
    const totalPaginas = Math.max(
      1,
      Math.ceil(filtrados.length / porPagina)
    );

    if (pagina > totalPaginas) {
      pagina = totalPaginas;
    }

    const inicio = (pagina - 1) * porPagina;
    const visibles = filtrados.slice(inicio, inicio + porPagina);

    tabla.replaceChildren();

    if (visibles.length === 0) {
      const fila = document.createElement("tr");
      const celda = crearCelda(
        productos.length === 0
          ? "No hay productos registrados."
          : "No se encontraron productos con esos filtros."
      );

      celda.colSpan = 6;
      fila.appendChild(celda);
      tabla.appendChild(fila);
    }

    visibles.forEach((producto) => {
      const fila = document.createElement("tr");

      fila.appendChild(crearCelda(producto.codigo));
      fila.appendChild(crearCelda(producto.nombre));
      fila.appendChild(crearCelda(producto.categoria));

      const existencias = crearCelda(String(producto.existencia));

      if (producto.estado && producto.existencia <= producto.minimo) {
        existencias.style.color = "var(--error-color)";
        existencias.style.fontWeight = "700";
      }

      fila.appendChild(existencias);

      const celdaEstado = document.createElement("td");
      const etiqueta = document.createElement("span");

      etiqueta.className = `product-status ${
        producto.estado ? "active" : "inactive"
      }`;

      etiqueta.textContent = producto.estado ? "Activo" : "Inactivo";
      celdaEstado.appendChild(etiqueta);
      fila.appendChild(celdaEstado);

      const acciones = document.createElement("td");
      const botonEditar = document.createElement("button");

      botonEditar.type = "button";
      botonEditar.className = "product-action";
      botonEditar.textContent = "Editar";

      botonEditar.addEventListener("click", () => {
        window.location.href = `producto-formulario.html?id=${producto.id}`;
      });

      acciones.appendChild(botonEditar);
      fila.appendChild(acciones);

      tabla.appendChild(fila);
    });

    contador.textContent =
      `${filtrados.length} producto${filtrados.length === 1 ? "" : "s"}`;

    paginaActual.textContent = `Página ${pagina} de ${totalPaginas}`;
    anterior.disabled = pagina === 1;
    siguiente.disabled = pagina >= totalPaginas;
  }

  // Actualizar la tabla al cambiar los filtros.
  [buscar, filtroCategoria, filtroEstado].forEach((control) => {
    control.addEventListener("input", () => {
      pagina = 1;
      renderizar();
    });

    control.addEventListener("change", () => {
      pagina = 1;
      renderizar();
    });
  });

  anterior.addEventListener("click", () => {
    if (pagina > 1) {
      pagina--;
      renderizar();
    }
  });

  siguiente.addEventListener("click", () => {
    const totalPaginas = Math.ceil(
      obtenerFiltrados().length / porPagina
    );

    if (pagina < totalPaginas) {
      pagina++;
      renderizar();
    }
  });

  botonNuevo.addEventListener("click", () => {
    window.location.href = "producto-formulario.html";
  });

  // Cargar los datos al entrar a la página.
  cargarProductos();
});