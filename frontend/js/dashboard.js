
const API_BASE = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "login.html";
        return;
    }

    verificarSesionConBackend(token);
});

async function verificarSesionConBackend(token) {
    const statusDot = document.getElementById("status-dot");
    const statusText = document.getElementById("status-text");

    try {
        const respuesta = await fetch(`${API_BASE}/api/perfil`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (respuesta.ok) {
            statusDot.classList.remove("error");
            statusText.textContent = "Conectado al backend. Token válido.";

            cargarTotalProductos(token);
            cargarTotalCategorias(token);
            cargarExistenciasBajas(token);
            cargarMovimientosHoy(token);
            cargarUltimosMovimientos(token);

        } else if (respuesta.status === 401) {
            statusDot.classList.add("error");
            statusText.textContent =
                "Tu sesión expiró o el token no es válido. Vuelve a iniciar sesión.";

        } else {
            statusDot.classList.add("error");
            statusText.textContent =
                "El backend respondió con un error inesperado.";
        }

    } catch (error) {
        console.error("Error de conexión:", error);

        statusDot.classList.add("error");
        statusText.textContent =
            "No se pudo conectar con el backend. Verifica que esté funcionando.";
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

        elemento.textContent =
            datos.total ?? (datos.productos || []).length;

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

        elemento.textContent =
            datos.total ?? (datos.categorias || []).length;

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

// Obtener la fecha local sin convertirla a UTC.
function obtenerFechaLocal() {
    const fecha = new Date();
    const anio = fecha.getFullYear();
    const mes = String(fecha.getMonth() + 1).padStart(2, "0");
    const dia = String(fecha.getDate()).padStart(2, "0");

    return `${anio}-${mes}-${dia}`;
}

// Consultar el total de movimientos realizados durante el día.
async function cargarMovimientosHoy(token) {
    const elemento = document.getElementById("total-movimientos-hoy");
    const hoy = obtenerFechaLocal();

    const parametros = new URLSearchParams({
        desde: hoy,
        hasta: hoy,
        pagina: 1,
        por_pagina: 1
    });

    try {
        const respuesta = await fetch(
            `${API_BASE}/api/movimientos?${parametros.toString()}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!respuesta.ok) {
            throw new Error("No se pudieron consultar los movimientos de hoy.");
        }

        const datos = await respuesta.json();

        elemento.textContent = datos.total ?? 0;

    } catch (error) {
        console.error("Error al cargar movimientos de hoy:", error);
        elemento.textContent = "Error";
    }
}

// Consultar los cinco movimientos más recientes.
async function cargarUltimosMovimientos(token) {
    const tabla = document.getElementById("tabla-ultimos-movimientos");
    const mensaje = document.getElementById("mensaje-movimientos");

    const parametros = new URLSearchParams({
        pagina: 1,
        por_pagina: 5
    });

    try {
        const respuesta = await fetch(
            `${API_BASE}/api/movimientos?${parametros.toString()}`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        if (!respuesta.ok) {
            throw new Error("No se pudieron consultar los últimos movimientos.");
        }

        const datos = await respuesta.json();
        const movimientos = datos.movimientos || [];

        tabla.innerHTML = "";

        if (movimientos.length === 0) {
            const fila = document.createElement("tr");
            const celda = document.createElement("td");

            celda.colSpan = 6;
            celda.textContent = "Todavía no hay movimientos registrados.";

            fila.appendChild(celda);
            tabla.appendChild(fila);

            mensaje.textContent = "No hay movimientos para mostrar.";
            return;
        }

        movimientos.forEach((movimiento) => {
            const fila = document.createElement("tr");

            agregarCeldaDashboard(fila, movimiento.producto);

            const celdaTipo = document.createElement("td");
            const etiqueta = document.createElement("span");

            etiqueta.textContent = movimiento.tipo_movimiento;
            etiqueta.classList.add("movement-badge");

            etiqueta.classList.add(
                movimiento.tipo_movimiento === "ENTRADA"
                    ? "movement-entry"
                    : "movement-exit"
            );

            celdaTipo.appendChild(etiqueta);
            fila.appendChild(celdaTipo);

            agregarCeldaDashboard(fila, movimiento.cantidad);
            agregarCeldaDashboard(fila, movimiento.usuario);

            agregarCeldaDashboard(
                fila,
                movimiento.fecha
                    ? new Date(movimiento.fecha).toLocaleString("es-CO")
                    : "—"
            );

            agregarCeldaDashboard(fila, movimiento.motivo);

            tabla.appendChild(fila);
        });

        mensaje.textContent = "Últimos movimientos consultados correctamente.";

    } catch (error) {
        console.error("Error al cargar últimos movimientos:", error);
        tabla.innerHTML = "";
        mensaje.textContent = error.message;
    }
}

function agregarCeldaDashboard(fila, valor) {
    const celda = document.createElement("td");
    celda.textContent = valor ?? "—";
    fila.appendChild(celda);
}
