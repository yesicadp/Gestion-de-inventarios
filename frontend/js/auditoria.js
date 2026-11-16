
const API_AUDITORIA = "http://127.0.0.1:5000/api/auditoria";
const API_USUARIOS = "http://127.0.0.1:5000/api/usuarios";

document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  const usuario = JSON.parse(localStorage.getItem("usuario") || "{}");

  const rol = usuario.rol || usuario.nombre_rol || "";
  const esAdministrador = rol.toLowerCase() === "administrador";

  const formulario = document.getElementById("form-filtros");
  const filtroBusqueda = document.getElementById("filtro-busqueda");
  const filtroUsuario = document.getElementById("filtro-usuario");
  const filtroModulo = document.getElementById("filtro-modulo");
  const filtroAccion = document.getElementById("filtro-accion");
  const filtroDesde = document.getElementById("filtro-desde");
  const filtroHasta = document.getElementById("filtro-hasta");

  const tabla = document.getElementById("tabla-auditoria");
  const mensaje = document.getElementById("mensaje-auditoria");
  const contador = document.getElementById("contador-auditoria");

  const botonAnterior = document.getElementById("btn-anterior");
  const botonSiguiente = document.getElementById("btn-siguiente");
  const botonLimpiar = document.getElementById("btn-limpiar-filtros");
  const numerosPagina = document.getElementById("numeros-pagina");

  const POR_PAGINA = 10;

  let paginaActual = 1;
  let totalRegistros = 0;

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  if (!esAdministrador) {
    window.location.href = "dashboard.html";
    return;
  }

  function agregarCelda(fila, valor) {
    const celda = document.createElement("td");
    celda.textContent = valor ?? "—";
    fila.appendChild(celda);
  }

  async function consultarUsuarios() {
    try {
      const respuesta = await fetch(API_USUARIOS, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(datos.mensaje || "No se pudieron consultar los usuarios.");
      }

      filtroUsuario.innerHTML =
        '<option value="">Todos los usuarios</option>';

      (datos.usuarios || []).forEach((usuario) => {
        const opcion = document.createElement("option");
        opcion.value = usuario.id_usuario;
        opcion.textContent = usuario.nombre;
        filtroUsuario.appendChild(opcion);
      });

    } catch (error) {
      console.error("Error al consultar usuarios:", error);
    }
  }

  function mostrarPaginacion(totalPaginas) {
    numerosPagina.innerHTML = "";

    function agregarBoton(numero) {
      const boton = document.createElement("button");

      boton.type = "button";
      boton.textContent = numero;
      boton.className = numero === paginaActual
        ? "btn-primary active-page"
        : "btn-secondary";

      boton.addEventListener("click", () => {
        if (numero !== paginaActual) {
          paginaActual = numero;
          consultarAuditoria();
        }
      });

      numerosPagina.appendChild(boton);
    }

    function agregarPuntos() {
      const puntos = document.createElement("span");
      puntos.textContent = "...";
      puntos.className = "pagination-dots";
      numerosPagina.appendChild(puntos);
    }

    if (totalPaginas <= 7) {
      for (let i = 1; i <= totalPaginas; i++) {
        agregarBoton(i);
      }
      return;
    }

    agregarBoton(1);

    let inicio = Math.max(2, paginaActual - 1);
    let fin = Math.min(totalPaginas - 1, paginaActual + 1);

    if (paginaActual <= 3) {
      inicio = 2;
      fin = 4;
    }

    if (paginaActual >= totalPaginas - 2) {
      inicio = totalPaginas - 3;
      fin = totalPaginas - 1;
    }

    if (inicio > 2) {
      agregarPuntos();
    }

    for (let i = inicio; i <= fin; i++) {
      agregarBoton(i);
    }

    if (fin < totalPaginas - 1) {
      agregarPuntos();
    }

    agregarBoton(totalPaginas);
  }

  async function consultarAuditoria() {
    mensaje.textContent = "Cargando registros...";
    tabla.innerHTML = "";

    const parametros = new URLSearchParams();

    parametros.set("pagina", paginaActual);
    parametros.set("por_pagina", POR_PAGINA);

    if (filtroBusqueda.value.trim()) {
      parametros.set("q", filtroBusqueda.value.trim());
    }

    if (filtroUsuario.value) {
      parametros.set("usuario_id", filtroUsuario.value);
    }

    if (filtroModulo.value.trim()) {
      parametros.set("modulo", filtroModulo.value.trim());
    }

    if (filtroAccion.value.trim()) {
      parametros.set("accion", filtroAccion.value.trim());
    }

    if (filtroDesde.value) {
      parametros.set("desde", filtroDesde.value);
    }

    if (filtroHasta.value) {
      parametros.set("hasta", filtroHasta.value);
    }

    try {
      const respuesta = await fetch(
        `${API_AUDITORIA}?${parametros.toString()}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      const datos = await respuesta.json();

      if (respuesta.status === 401 || respuesta.status === 403) {
        mensaje.textContent = "No tienes autorización para consultar la auditoría.";
        return;
      }

      if (!respuesta.ok) {
        throw new Error(
          datos.mensaje || "No se pudieron consultar los registros."
        );
      }

      const registros = datos.auditoria || [];

      totalRegistros = Number(datos.total || 0);

      registros.forEach((registro) => {
        const fila = document.createElement("tr");

        agregarCelda(fila, registro.id_auditoria);
        agregarCelda(fila, registro.usuario);
        agregarCelda(fila, registro.modulo);
        agregarCelda(fila, registro.accion);

        agregarCelda(
          fila,
          registro.fecha
            ? new Date(registro.fecha).toLocaleString("es-CO")
            : "—"
        );

        agregarCelda(fila, registro.detalle);

        tabla.appendChild(fila);
      });

      if (registros.length === 0) {
        const fila = document.createElement("tr");
        const celda = document.createElement("td");

        celda.colSpan = 6;
        celda.textContent = "No se encontraron registros de auditoría.";

        fila.appendChild(celda);
        tabla.appendChild(fila);
      }

      const totalPaginas = Math.max(
        1,
        Math.ceil(totalRegistros / POR_PAGINA)
      );

      contador.textContent =
        `${totalRegistros} ${totalRegistros === 1 ? "registro" : "registros"}`;

      mostrarPaginacion(totalPaginas);

      botonAnterior.disabled = paginaActual <= 1;
      botonSiguiente.disabled = paginaActual >= totalPaginas;

      mensaje.textContent = registros.length
        ? "Registros consultados correctamente."
        : "No hay registros para mostrar.";

    } catch (error) {
      console.error("Error al consultar auditoría:", error);
      mensaje.textContent =
        error.message || "No fue posible conectar con el servidor.";
    }
  }

  formulario.addEventListener("submit", (evento) => {
    evento.preventDefault();
    paginaActual = 1;
    consultarAuditoria();
  });

  botonLimpiar.addEventListener("click", () => {
    formulario.reset();
    paginaActual = 1;
    consultarAuditoria();
  });

  botonAnterior.addEventListener("click", () => {
    if (paginaActual > 1) {
      paginaActual--;
      consultarAuditoria();
    }
  });

  botonSiguiente.addEventListener("click", () => {
    const totalPaginas = Math.max(
      1,
      Math.ceil(totalRegistros / POR_PAGINA)
    );

    if (paginaActual < totalPaginas) {
      paginaActual++;
      consultarAuditoria();
    }
  });

  async function iniciar() {
    await consultarUsuarios();
    await consultarAuditoria();
  }

  iniciar();
});
