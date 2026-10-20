
document.addEventListener("DOMContentLoaded", () => {
  const productosIniciales = [
    {
      codigo: "PROD-001",
      nombre: "Teclado USB",
      categoria: "Periféricos",
      existencia: 18,
      minimo: 5,
      estado: true
    },
    {
      codigo: "PROD-002",
      nombre: "Mouse inalámbrico",
      categoria: "Periféricos",
      existencia: 3,
      minimo: 5,
      estado: true
    },
    {
      codigo: "PROD-003",
      nombre: "Monitor 24 pulgadas",
      categoria: "Pantallas",
      existencia: 12,
      minimo: 3,
      estado: true
    },
    {
      codigo: "PROD-004",
      nombre: "Cable HDMI",
      categoria: "Accesorios",
      existencia: 0,
      minimo: 4,
      estado: false
    },
    {
      codigo: "PROD-005",
      nombre: "Memoria USB",
      categoria: "Accesorios",
      existencia: 25,
      minimo: 8,
      estado: true
    },
    {
      codigo: "PROD-006",
      nombre: "Base para portátil",
      categoria: "Accesorios",
      existencia: 9,
      minimo: 3,
      estado: true
    }
  ];

  let productosPrueba = [];

try {
  const guardados = JSON.parse(
    localStorage.getItem("productosDemo") || "[]"
  );

  productosPrueba = [
    ...productosIniciales,
    ...(Array.isArray(guardados) ? guardados : [])
  ];
} catch (error) {
  productosPrueba = [...productosIniciales];
}

  const buscar = document.getElementById("buscar-producto");
  const filtroCategoria = document.getElementById("filtro-categoria");
  const filtroEstado = document.getElementById("filtro-estado");
  const tabla = document.getElementById("tabla-productos");
  const mensaje = document.getElementById("mensaje-productos");
  const contador = document.getElementById("contador-productos");
  const paginaActual = document.getElementById("pagina-actual");
  const anterior = document.getElementById("pagina-anterior");
  const siguiente = document.getElementById("pagina-siguiente");

  const porPagina = 5;
  let pagina = 1;

  const categorias = [...new Set(
    productosPrueba.map(producto => producto.categoria)
  )];

  categorias.forEach(categoria => {
    const opcion = document.createElement("option");
    opcion.value = categoria;
    opcion.textContent = categoria;
    filtroCategoria.appendChild(opcion);
  });

  function obtenerFiltrados() {
    const texto = buscar.value.trim().toLowerCase();

    return productosPrueba.filter(producto => {
      const coincideTexto = [
        producto.codigo,
        producto.nombre,
        producto.categoria
      ].some(valor => valor.toLowerCase().includes(texto));

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

  function renderizar() {
    const filtrados = obtenerFiltrados();
    const totalPaginas = Math.max(1, Math.ceil(filtrados.length / porPagina));

    if (pagina > totalPaginas) pagina = totalPaginas;

    const inicio = (pagina - 1) * porPagina;
    const visibles = filtrados.slice(inicio, inicio + porPagina);

    tabla.replaceChildren();

    visibles.forEach(producto => {
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
      const boton = document.createElement("button");
      boton.type = "button";
      boton.className = "product-action";
      boton.textContent = "Editar";
      boton.addEventListener("click", () => {
        const codigo = encodeURIComponent(producto.codigo);
        window.location.href =
            `producto-formulario.html?codigo=${codigo}`;
      });
      acciones.appendChild(boton);
      fila.appendChild(acciones);

      tabla.appendChild(fila);
    });

    mensaje.textContent =
      "Vista de demostración: estos productos son ficticios y todavía no vienen de la base de datos.";

    contador.textContent =
      `${filtrados.length} producto${filtrados.length === 1 ? "" : "s"}`;

    paginaActual.textContent = `Página ${pagina} de ${totalPaginas}`;
    anterior.disabled = pagina === 1;
    siguiente.disabled = pagina >= totalPaginas;
  }

  [buscar, filtroCategoria, filtroEstado].forEach(control => {
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
    const totalPaginas = Math.ceil(obtenerFiltrados().length / porPagina);

    if (pagina < totalPaginas) {
      pagina++;
      renderizar();
    }
  });

  document.getElementById("btn-nuevo-producto").addEventListener("click", () => {
  window.location.href = "producto-formulario.html";
});

  renderizar();
});
