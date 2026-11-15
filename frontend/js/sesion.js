
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("token");
    const usuarioGuardado = localStorage.getItem("usuario");

    // Comprobar que exista una sesión.
    if (!token || !usuarioGuardado) {
        window.location.href = "login.html";
        return;
    }

    let usuario;

    try {
        usuario = JSON.parse(usuarioGuardado);
    } catch (error) {
        localStorage.removeItem("token");
        localStorage.removeItem("usuario");
        window.location.href = "login.html";
        return;
    }

    // Obtener el nombre y el rol del usuario.
    const nombre =
        usuario.nombre ||
        usuario.nombre_usuario ||
        usuario.username ||
        usuario.correo ||
        "Usuario";

    const rol = usuario.rol || usuario.nombre_rol || "";

    // Mostrar los datos del usuario si los elementos existen.
    const elementoNombre = document.getElementById("user-name");
    const elementoRol = document.getElementById("user-role");

    if (elementoNombre) {
        elementoNombre.textContent = nombre;
    }

    if (elementoRol) {
        elementoRol.textContent = rol;
    }

    // Ocultar las opciones exclusivas del administrador.
    const esAdministrador =
        rol.toLowerCase() === "administrador";

    document.querySelectorAll("[data-solo-admin]").forEach(elemento => {
        if (!esAdministrador) {
            elemento.classList.add("hidden");
        }
    });

    // Cerrar sesión.
    document.querySelectorAll("[data-cerrar-sesion], #btn-logout").forEach(boton => {
        boton.addEventListener("click", () => {
            localStorage.removeItem("token");
            localStorage.removeItem("usuario");
            window.location.href = "login.html";
        });
    });
});
