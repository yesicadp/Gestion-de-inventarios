const API_BASE = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    // Comprobar que el token funciona en el backend.
    verificarSesionConBackend(token);
});

async function verificarSesionConBackend(token) {
    const statusDot = document.getElementById("status-dot");
    const statusText = document.getElementById("status-text");

    try {
        const response = await fetch(`${API_BASE}/api/perfil`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.ok) {
            if (statusDot) statusDot.classList.remove("error");

            if (statusText) {
                statusText.textContent = "Conectado al backend — token válido.";
            }

            // Cargar las estadísticas del dashboard.
            cargarTotalProductos(token);
            cargarTotalCategorias(token);
            cargarExistenciasBajas(token);

        } else if (response.status === 401) {
            if (statusDot) statusDot.classList.add("error");

            if (statusText) {
                statusText.textContent =
                    "Tu sesión expiró o el token no es válido. Vuelve a iniciar sesión.";
            }

        } else {
            if (statusDot) statusDot.classList.add("error");

            if (statusText) {
                statusText.textContent =
                    "El backend respondió con un error inesperado.";
            }
        }

    } catch (error) {
        console.error("Error de conexión:", error);

        if (statusDot) statusDot.classList.add("error");

        if (statusText) {
            statusText.textContent =
                "No se pudo conectar con el backend. Verifica que esté funcionando.";
        }
    }
}

async function cargarTotalProductos(token) {
    const elemento = document.getElementById("total-productos");
    if (!elemento) return;

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

        elemento.textContent =
            datos.total ?? (datos.productos || []).length;

    } catch (error) {
        console.error("Error al cargar productos:", error);
        elemento.textContent = "Error";
    }
}

async function cargarTotalCategorias(token) {
    const elemento = document.getElementById("total-categorias");
    if (!elemento) return;

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

        elemento.textContent =
            datos.total ?? (datos.categorias || []).length;

    } catch (error) {
        console.error("Error al cargar categorías:", error);
        elemento.textContent = "Error";
    }
}

async function cargarExistenciasBajas(token) {
    const elemento = document.getElementById("total-existencias-bajas");
    if (!elemento) return;

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
