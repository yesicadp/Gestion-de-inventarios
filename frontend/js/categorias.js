
const API_CATEGORIAS = "http://127.0.0.1:5000/api/categorias";

document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  const formulario = document.getElementById("form-categoria");
  const botonNueva = document.getElementById("btn-nueva-categoria");
  const botonCancelar = document.getElementById("btn-cancelar-categoria");
  const campoNombre = document.getElementById("nombre-categoria");
  const campoPadre = document.getElementById("categoria-padre");
  const buscador = document.getElementById("buscar-categoria");
  const tabla = document.getElementById("tabla-categorias");
  const mensaje = document.getElementById("mensaje-categorias");
  const mensajeFormulario = document.getElementById("mensaje-formulario");
  const contador = document.getElementById("contador-categorias");
  const botonGuardar = document.getElementById("btn-guardar-categoria");

  let categorias = [];

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  // Consultar la API utilizando el token del inicio de sesión.
  async function consultarCategorias() {
    mensaje.textContent = "Cargando categorías...";

    try {
      const respuesta = await fetch(API_CATEGORIAS, {
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
        throw new Error(datos.mensaje || "No se pudieron consultar las categorías.");
      }

      categorias = datos.categorias || [];

      llenarCategoriasPadre();
      mostrarCategorias();

      mensaje.textContent = categorias.length
        ? "Categorías consultadas correctamente."
        : "Todavía no hay categorías registradas.";
    } catch (error) {
      console.error("Error al consultar categorías:", error);
      mensaje.textContent =
        error.message || "No fue posible conectar con el servidor.";
    }
  }

  // Llenar la lista de categorías principales del formulario.
  function llenarCategoriasPadre() {
    const valorAnterior = campoPadre.value;

    campoPadre.innerHTML =
      '<option value="">Sin categoría principal</option>';

    categorias.forEach((categoria) => {
      const opcion = document.createElement("option");
      opcion.value = categoria.id_categoria;
      opcion.textContent = categoria.nombre;
      campoPadre.appendChild(opcion);
    });

    if (
      [...campoPadre.options].some(
        (opcion) => opcion.value === valorAnterior
      )
    ) {
      campoPadre.value = valorAnterior;
    }
  }

  // Mostrar las categorías en la tabla y aplicar la búsqueda.
  function mostrarCategorias() {
    const texto = buscador.value.trim().toLowerCase();

    const filtradas = categorias.filter((categoria) => {
      return categoria.nombre.toLowerCase().includes(texto);
    });

    tabla.innerHTML = "";

    if (filtradas.length === 0) {
      const fila = document.createElement("tr");
      const celda = document.createElement("td");

      celda.colSpan = 3;
      celda.textContent = texto
        ? "No se encontraron categorías con esa búsqueda."
        : "No hay categorías para mostrar.";

      fila.appendChild(celda);
      tabla.appendChild(fila);
    } else {
      filtradas.forEach((categoria) => {
        const fila = document.createElement("tr");

        const celdaId = document.createElement("td");
        celdaId.textContent = categoria.id_categoria;

        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = categoria.nombre;

        const celdaPadre = document.createElement("td");
        const padre = categorias.find(
          (item) => item.id_categoria === categoria.categoria_padre_id
        );

        celdaPadre.textContent = padre ? padre.nombre : "—";

        fila.append(celdaId, celdaNombre, celdaPadre);
        tabla.appendChild(fila);
      });
    }

    contador.textContent =
      `${filtradas.length} ${filtradas.length === 1 ? "categoría" : "categorías"}`;
  }

  // Mostrar el formulario para registrar una categoría.
  botonNueva.addEventListener("click", () => {
    formulario.reset();
    mensajeFormulario.textContent = "";
    formulario.classList.remove("hidden");
    campoNombre.focus();
  });

  // Ocultar el formulario sin guardar.
  botonCancelar.addEventListener("click", () => {
    formulario.reset();
    mensajeFormulario.textContent = "";
    formulario.classList.add("hidden");
  });

  // Buscar categorías por nombre.
  buscador.addEventListener("input", mostrarCategorias);

  // Registrar una categoría nueva.
  formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const nombre = campoNombre.value.trim();
    const valorPadre = campoPadre.value;

    if (!nombre) {
      mensajeFormulario.textContent =
        "Escribe el nombre de la categoría.";
      return;
    }

    const datosCategoria = {
      nombre: nombre,
      categoria_padre_id: valorPadre ? Number(valorPadre) : null
    };

    botonGuardar.disabled = true;
    mensajeFormulario.textContent = "Guardando categoría...";

    try {
      const respuesta = await fetch(API_CATEGORIAS, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(datosCategoria)
      });

      const datos = await respuesta.json();

      if (respuesta.status === 401 || respuesta.status === 403) {
        mensajeFormulario.textContent =
          "Tu sesión no está autorizada. Inicia sesión nuevamente.";
        return;
      }

      if (!respuesta.ok) {
        throw new Error(datos.mensaje || "No se pudo guardar la categoría.");
      }

      formulario.reset();
      formulario.classList.add("hidden");
      mensaje.textContent = datos.mensaje || "Categoría registrada correctamente.";

      await consultarCategorias();
    } catch (error) {
      console.error("Error al registrar categoría:", error);
      mensajeFormulario.textContent =
        error.message || "No fue posible conectar con el servidor.";
    } finally {
      botonGuardar.disabled = false;
    }
  });

  // Cargar las categorías al entrar en la página.
  consultarCategorias();
});