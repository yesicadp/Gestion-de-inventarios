
document.addEventListener("DOMContentLoaded", () => {
  const API_MOVIMIENTOS = "http://127.0.0.1:5000/api/movimientos";

  const token = localStorage.getItem("token");

  const buscar = document.getElementById("buscar-historial");
  const filtroTipo = document.getElementById("filtro-tipo");
  const fechaDesde = document.getElementById("fecha-desde");
  const fechaHasta = document.getElementById("fecha-hasta");
  const botonLimpiar = document.getElementById("btn-limpiar-filtros");

  const tabla = document.getElementById("tabla-historial");
  const mensaje = document.getElementById("mensaje-historial");
  const contador = document.getElementById("contador-historial");
  const paginaActual = document.getElementById("pagina-actual");
  const anterior = document.getElementById("pagina-anterior");
  const siguiente = document.getElementById("pagina-siguiente");

  const porPagina = 10;

  let pagina = 1;
  let totalMovimientos = 0;

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  function mostrarMensaje(texto) {
    mensaje.textContent = texto;
  }

  function crearCelda(texto) {
    const celda = document.createElement("td");
    celda.textContent = texto ?? "—";
    return celda;
  }

  function formatearFecha(fecha) {
    if (!fecha) return "—";

    const fechaValida = new Date(fecha);

    if (Number.isNaN(fechaValida.getTime())) {
      return fecha;
    }

    return fechaValida.toLocaleString("es-CO", {
      dateStyle: "short",
      timeStyle: "short"
    });
  }

  function crearEtiquetaTipo(tipo) {
    const celda = document.createElement("td");
    const etiqueta = document.createElement("span");

    etiqueta.className = `history-type ${
      tipo === "ENTRADA" ? "entry" : "exit"
    }`;

    etiqueta.textContent = tipo || "—";

    celda.appendChild(etiqueta);
    return celda;
  }

  async function cargarHistorial() {
    mostrarMensaje("Consultando movimientos...");
    tabla.replaceChildren();

    const parametros = new URLSearchParams();

    parametros.set("pagina", pagina);
    parametros.set("por_pagina", porPagina);

    if (buscar.value.trim()) {
      parametros.set("q", buscar.value.trim());
    }

    if (filtroTipo.value) {
      parametros.set("tipo", filtroTipo.value);
    }

    if (fechaDesde.value) {
      parametros.set("desde", fechaDesde.value);
    }

    if (fechaHasta.value) {
      parametros.set("hasta", fechaHasta.value);
    }

    try {
      const respuesta = await fetch(
        `${API_MOVIMIENTOS}?${parametros.toString()}`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      const datos = await respuesta.json();

      if (respuesta.status === 401 || respuesta.status === 403) {
        mostrarMensaje(
          "Tu sesión no está autorizada. Inicia sesión nuevamente."
        );
        return;
      }

      if (!respuesta.ok) {
        throw new Error(
          datos.mensaje || "No fue posible consultar el historial."
        );
      }

      const movimientos = datos.movimientos || [];

      totalMovimientos = Number(datos.total || 0);

      renderizarMovimientos(movimientos);

      const totalPaginas = Math.max(
        1,
        Math.ceil(totalMovimientos / porPagina)
      );

      contador.textContent =
        `${totalMovimientos} movimiento${totalMovimientos === 1 ? "" : "s"}`;

      paginaActual.textContent =
        `Página ${pagina} de ${totalPaginas}`;

      anterior.disabled = pagina <= 1;
      siguiente.disabled = pagina >= totalPaginas;

      mostrarMensaje(
        movimientos.length
          ? "Historial consultado correctamente."
          : "No se encontraron movimientos con los filtros seleccionados."
      );

    } catch (error) {
      console.error("Error al consultar historial:", error);
      mostrarMensaje(
        error.message || "No fue posible conectar con el servidor."
      );
    }
  }

  function renderizarMovimientos(movimientos) {
    tabla.replaceChildren();

    if (movimientos.length === 0) {
      const fila = document.createElement("tr");
      const celda = crearCelda("No hay movimientos registrados.");
      celda.colSpan = 8;
      fila.appendChild(celda);
      tabla.appendChild(fila);
      return;
    }

    movimientos.forEach((movimiento) => {
      const fila = document.createElement("tr");

      fila.appendChild(crearCelda(movimiento.id_movimiento));
      fila.appendChild(crearCelda(formatearFecha(movimiento.fecha)));
      fila.appendChild(crearCelda(movimiento.producto));
      fila.appendChild(crearEtiquetaTipo(movimiento.tipo_movimiento));
      fila.appendChild(crearCelda(movimiento.cantidad));
      fila.appendChild(crearCelda(movimiento.existencia_resultante));
      fila.appendChild(crearCelda(movimiento.usuario));
      fila.appendChild(crearCelda(movimiento.motivo));

      tabla.appendChild(fila);
    });
  }

  // Aplicar filtros.
  buscar.addEventListener("input", () => {
    pagina = 1;
    cargarHistorial();
  });

  [filtroTipo, fechaDesde, fechaHasta].forEach((control) => {
    control.addEventListener("change", () => {
      pagina = 1;
      cargarHistorial();
    });
  });

  // Limpiar filtros.
  botonLimpiar.addEventListener("click", () => {
    buscar.value = "";
    filtroTipo.value = "";
    fechaDesde.value = "";
    fechaHasta.value = "";

    pagina = 1;
    cargarHistorial();
  });

  // Navegación entre páginas.
  anterior.addEventListener("click", () => {
    if (pagina > 1) {
      pagina--;
      cargarHistorial();
    }
  });

  siguiente.addEventListener("click", () => {
    const totalPaginas = Math.ceil(totalMovimientos / porPagina);

    if (pagina < totalPaginas) {
      pagina++;
      cargarHistorial();
    }
  });

  cargarHistorial();
});
