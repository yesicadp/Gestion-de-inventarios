// URL base de tu backend Flask (ajusta el puerto si tu servidor usa uno diferente, e.g. 5000 o 8000)
const API_URL = "http://127.0.0.1:5000/api/auth/login";

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("login-form");
  const alertBox = document.getElementById("alert-message");

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const usernameInput = document.getElementById("username").value.trim();
      const passwordInput = document.getElementById("password").value.trim();

      // Ocultar alertas previas
      ocultarAlerta();

      try {
        const response = await fetch(API_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: usernameInput,
            password: passwordInput,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          // Guardar token JWT y datos del usuario (incluye el rol) en localStorage
          localStorage.setItem("token", data.token);
          localStorage.setItem("usuario", JSON.stringify(data.usuario));

          mostrarAlerta(data.mensaje || "Inicio de sesión exitoso", "success");

          // Redirigir al panel principal
          setTimeout(() => {
            window.location.href = "dashboard.html";
          }, 1200);

        } else {
          // Error devuelto por el backend (e.g. "Credenciales inválidas")
          mostrarAlerta(data.mensaje || "Credenciales incorrectas", "error");
        }
      } catch (error) {
        console.error("Error en la petición:", error);
        mostrarAlerta("No se pudo conectar con el servidor. Revisa tu conexión.", "error");
      }
    });
  }
});

// Función para manejar el token devuelto por el SDK de Google
function handleGoogleLogin(response) {
  const idTokenGoogle = response.credential;
  console.log("Token de Google obtenido:", idTokenGoogle);

  // Aquí envías 'idTokenGoogle' a la ruta del backend de Google cuando la creen
  /*
  fetch("http://127.0.0.1:5000/api/auth/google", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: idTokenGoogle })
  })
  .then(res => res.json())
  .then(data => { ... });
  */
}

// Funciones auxiliares para mostrar/ocultar mensajes
function mostrarAlerta(mensaje, tipo) {
  const alertBox = document.getElementById("alert-message");
  if (!alertBox) return;

  alertBox.textContent = mensaje;
  alertBox.className = `alert ${tipo}`;
}

function ocultarAlerta() {
  const alertBox = document.getElementById("alert-message");
  if (alertBox) {
    alertBox.className = "alert hidden";
  }
}