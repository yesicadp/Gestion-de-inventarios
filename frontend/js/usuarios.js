
const API_USUARIOS = "http://127.0.0.1:5000/api/usuarios";
const API_ROLES = "http://127.0.0.1:5000/api/roles";

document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  const usuarioSesion = JSON.parse(localStorage.getItem("usuario") || "{}");
  const rolSesion = usuarioSesion.rol || usuarioSesion.nombre_rol || "";

  const formulario = document.getElementById("form-usuario");
  const botonNuevo = document.getElementById("btn-nuevo-usuario");
  const botonCancelar = document.getElementById("btn-cancelar-usuario");
  const botonGuardar = document.getElementById("btn-guardar-usuario");

  const campoNombre = document.getElementById("nombre-usuario");
  const campoCorreo = document.getElementById("correo-usuario");
  const campoRol = document.getElementById("rol-usuario");
  const campoPassword = document.getElementById("password-usuario");

  const tituloFormulario = document.getElementById("titulo-formulario");
  const labelPassword = document.getElementById("label-password");
  const ayudaPassword = document.getElementById("ayuda-password");

  const buscador = document.getElementById("buscar-usuario");
  const tabla = document.getElementById("tabla-usuarios");
  const mensaje = document.getElementById("mensaje-usuarios");
  const mensajeFormulario = document.getElementById("mensaje-formulario");
  const contador = document.getElementById("contador-usuarios");

  let usuarios = [];
  let idUsuarioEditando = null;

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  if (rolSesion.toLowerCase() !== "administrador") {
    window.location.href = "dashboard.html";
    return;
  }

  function usuarioActivo(usuario) {
    return usuario.estado === true ||
      usuario.estado === 1 ||
      usuario.estado === "1";
  }

  async function consultarRoles() {
    const respuesta = await fetch(API_ROLES, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const datos = await respuesta.json();

    if (!respuesta.ok) {
      throw new Error(datos.mensaje || "No se pudieron consultar los roles.");
    }

    campoRol.innerHTML = '<option value="">Selecciona un rol</option>';

    (datos.roles || []).forEach(rol => {
      const opcion = document.createElement("option");
      opcion.value = rol.id_rol;
      opcion.textContent = rol.nombre_rol;
      campoRol.appendChild(opcion);
    });
  }

  async function consultarUsuarios() {
    mensaje.textContent = "Cargando usuarios...";

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

      usuarios = datos.usuarios || [];
      mostrarUsuarios();

      mensaje.textContent = usuarios.length
        ? "Usuarios consultados correctamente."
        : "Todavía no hay usuarios registrados.";

    } catch (error) {
      console.error("Error al consultar usuarios:", error);
      mensaje.textContent = error.message;
    }
  }

  function mostrarUsuarios() {
    const texto = buscador.value.trim().toLowerCase();

    const filtrados = usuarios.filter(usuario =>
      usuario.nombre.toLowerCase().includes(texto) ||
      usuario.correo.toLowerCase().includes(texto)
    );

    tabla.innerHTML = "";

    if (filtrados.length === 0) {
      const fila = document.createElement("tr");
      const celda = document.createElement("td");

      celda.colSpan = 6;
      celda.textContent = texto
        ? "No se encontraron usuarios."
        : "No hay usuarios para mostrar.";

      fila.appendChild(celda);
      tabla.appendChild(fila);
    } else {
      filtrados.forEach(usuario => {
        const fila = document.createElement("tr");

        const celdaId = document.createElement("td");
        celdaId.textContent = usuario.id_usuario;

        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = usuario.nombre;

        const celdaCorreo = document.createElement("td");
        celdaCorreo.textContent = usuario.correo;

        const celdaRol = document.createElement("td");
        celdaRol.textContent = usuario.nombre_rol;

        const celdaEstado = document.createElement("td");
        const activo = usuarioActivo(usuario);
        const estado = document.createElement("span");

        estado.classList.add("user-status", activo ? "active" : "inactive");
        estado.textContent = activo ? "Activo" : "Inactivo";
        celdaEstado.appendChild(estado);

        const celdaAcciones = document.createElement("td");

        const botonEditar = document.createElement("button");
        botonEditar.type = "button";
        botonEditar.textContent = "Editar";
        botonEditar.classList.add("btn-secondary");
        botonEditar.addEventListener("click", () => editarUsuario(usuario));

        const botonEstado = document.createElement("button");
        botonEstado.type = "button";
        botonEstado.textContent = activo ? "Desactivar" : "Activar";
        botonEstado.classList.add("btn-secondary");
        botonEstado.addEventListener("click", () => cambiarEstado(usuario));

        celdaAcciones.append(botonEditar, botonEstado);

        fila.append(
          celdaId,
          celdaNombre,
          celdaCorreo,
          celdaRol,
          celdaEstado,
          celdaAcciones
        );

        tabla.appendChild(fila);
      });
    }

    contador.textContent =
      `${filtrados.length} ${filtrados.length === 1 ? "usuario" : "usuarios"}`;
  }

  function abrirFormulario() {
    formulario.reset();
    idUsuarioEditando = null;

    tituloFormulario.textContent = "Nuevo usuario";
    botonGuardar.textContent = "Guardar usuario";
    campoPassword.required = true;
    labelPassword.textContent = "Contraseña *";
    campoPassword.placeholder = "Mínimo 8 caracteres";
    ayudaPassword.textContent = "La contraseña debe tener al menos 8 caracteres.";

    mensajeFormulario.textContent = "";
    formulario.classList.remove("hidden");
    campoNombre.focus();
  }

  function cerrarFormulario() {
    formulario.reset();
    formulario.classList.add("hidden");
    mensajeFormulario.textContent = "";
    idUsuarioEditando = null;
  }

  function editarUsuario(usuario) {
    idUsuarioEditando = usuario.id_usuario;

    tituloFormulario.textContent = "Editar usuario";
    botonGuardar.textContent = "Guardar cambios";

    campoNombre.value = usuario.nombre;
    campoCorreo.value = usuario.correo;
    campoRol.value = usuario.rol_id;

    campoPassword.value = "";
    campoPassword.required = false;
    labelPassword.textContent = "Nueva contraseña (opcional)";
    campoPassword.placeholder = "Dejar vacío para conservarla";
    ayudaPassword.textContent =
      "Si deseas cambiar la contraseña, escribe una de al menos 8 caracteres.";

    mensajeFormulario.textContent = "";
    formulario.classList.remove("hidden");
    campoNombre.focus();
  }

  async function cambiarEstado(usuario) {
    const activo = usuarioActivo(usuario);
    const nuevoEstado = !activo;
    const accion = nuevoEstado ? "activar" : "desactivar";

    const confirmar = confirm(
      `¿Estás segura de que deseas ${accion} la cuenta de ${usuario.nombre}?`
    );

    if (!confirmar) return;

    try {
      const respuesta = await fetch(
        `${API_USUARIOS}/${usuario.id_usuario}/estado`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ estado: nuevoEstado })
        }
      );

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(datos.mensaje || "No se pudo cambiar el estado.");
      }

      mensaje.textContent = datos.mensaje;
      await consultarUsuarios();

    } catch (error) {
      console.error("Error al cambiar estado:", error);
      mensaje.textContent = error.message;
    }
  }

  botonNuevo.addEventListener("click", abrirFormulario);
  botonCancelar.addEventListener("click", cerrarFormulario);
  buscador.addEventListener("input", mostrarUsuarios);

  formulario.addEventListener("submit", async evento => {
    evento.preventDefault();

    const datosUsuario = {
      nombre: campoNombre.value.trim(),
      correo: campoCorreo.value.trim(),
      rol_id: Number(campoRol.value),
      password: campoPassword.value
    };

    if (!datosUsuario.nombre || !datosUsuario.correo || !datosUsuario.rol_id) {
      mensajeFormulario.textContent = "Completa todos los campos obligatorios.";
      return;
    }

    if (!idUsuarioEditando && datosUsuario.password.length < 8) {
      mensajeFormulario.textContent =
        "La contraseña debe tener al menos 8 caracteres.";
      return;
    }

    if (datosUsuario.password && datosUsuario.password.length < 8) {
      mensajeFormulario.textContent =
        "La contraseña debe tener al menos 8 caracteres.";
      return;
    }

    const editando = idUsuarioEditando !== null;
    const url = editando
      ? `${API_USUARIOS}/${idUsuarioEditando}`
      : API_USUARIOS;

    botonGuardar.disabled = true;
    mensajeFormulario.textContent = editando
      ? "Actualizando usuario..."
      : "Creando usuario...";

    try {
      const respuesta = await fetch(url, {
        method: editando ? "PUT" : "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(datosUsuario)
      });

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        throw new Error(datos.mensaje || "No se pudo guardar el usuario.");
      }

      cerrarFormulario();
      mensaje.textContent = datos.mensaje;
      await consultarUsuarios();

    } catch (error) {
      console.error("Error al guardar usuario:", error);
      mensajeFormulario.textContent = error.message;

    } finally {
      botonGuardar.disabled = false;
    }
  });

  async function iniciarModulo() {
    try {
      await consultarRoles();
      await consultarUsuarios();
    } catch (error) {
      console.error("Error al iniciar el módulo:", error);
      mensaje.textContent = error.message;
    }
  }

  iniciarModulo();
});
