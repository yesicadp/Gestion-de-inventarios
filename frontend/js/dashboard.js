const API_BASE = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  const usuarioRaw = localStorage.getItem("usuario");

  // Guardia de sesión: sin token, no hay dashboard.
  if (!token || !usuarioRaw) {
    window.location.href = "login.html";
    return;
  }

  let usuario;
  try {
    usuario = JSON.parse(usuarioRaw);
  } catch (e) {
    // Datos de sesión corruptos: mejor forzar login de nuevo.
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    window.location.href = "login.html";
    return;
  }

  // Mostrar nombre y rol en la barra superior.
  document.getElementById("user-name").textContent = usuario.nombre || usuario.correo;
  document.getElementById("user-role").textContent = usuario.rol;

  // Mostrar/ocultar opciones de menú exclusivas de Administrador.
  const esAdmin = usuario.rol === "Administrador";
  document.querySelectorAll("[data-solo-admin]").forEach((el) => {
    el.classList.toggle("hidden", !esAdmin);
  });

  // Logout.
  document.getElementById("btn-logout").addEventListener("click", () => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    window.location.href = "login.html";
  });

  // Prueba real de que el token funciona: llama a la ruta protegida /api/perfil.
  verificarSesionConBackend(token);
});

async function verificarSesionConBackend(token) {
  const statusDot = document.getElementById("status-dot");
  const statusText = document.getElementById("status-text");

  try {
    const response = await fetch(`${API_BASE}/api/perfil`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.ok) {
      statusDot.classList.remove("error");
      statusText.textContent = "Conectado al backend — token válido.";
      cargarTotalProductos(token);
      cargarTotalCategorias(token);
      cargarExistenciasBajas(token);
    } else if (response.status === 401) {
      statusDot.classList.add("error");
      statusText.textContent = "Tu sesión expiró o el token no es válido. Vuelve a iniciar sesión.";
    } else {
      statusDot.classList.add("error");
      statusText.textContent = "El backend respondió con un error inesperado.";
    }
  } catch (error) {
    statusDot.classList.add("error");
    statusText.textContent = "No se pudo conectar con el backend (¿está corriendo en el puerto 5000?).";
  }
}

async function cargarTotalProductos(token) {
  const elemento = document.getElementById("total-productos");

  try {
    const respuesta = await fetch(`${API_BASE}/api/productos`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!respuesta.ok) {
      throw new Error("No se pudieron consultar los productos.");
    }

    const datos = await respuesta.json();
    elemento.textContent = datos.total ?? (datos.productos || []).length;
  } catch (error) {
    console.error("Error al cargar productos:", error);
    elemento.textContent = "Error";
  }
}

async function cargarTotalCategorias(token) {
  const elemento = document.getElementById("total-categorias");

  try {
    const respuesta = await fetch(`${API_BASE}/api/categorias`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!respuesta.ok) {
      throw new Error("No se pudieron consultar las categorías.");
    }

    const datos = await respuesta.json();

    elemento.textContent = datos.total ?? (datos.categorias || []).length;

  } catch (error) {
    console.error("Error al cargar categorías:", error);
    elemento.textContent = "Error";
  }
}

async function cargarExistenciasBajas(token) {
  const elemento = document.getElementById("total-existencias-bajas");

  try {
    const respuesta = await fetch(`${API_BASE}/api/inventario`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!respuesta.ok) {
      throw new Error("No se pudo consultar el inventario.");
    }

    const datos = await respuesta.json();

    elemento.textContent = datos.total_existencias_bajas ?? 0;
  } catch (error) {
    console.error("Error al cargar existencias bajas:", error);
    elemento.textContent = "Error";
  }
}
