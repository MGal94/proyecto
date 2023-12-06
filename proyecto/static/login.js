function validateLogin() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var errorMessage = document.getElementById("errorMessage");

    // Validar credenciales (esto debe hacerse en el servidor en un entorno real)
    if (username === "admin" && password === "admin") {
        // Credenciales válidas, redirigir o realizar otras acciones necesarias
        alert("Inicio de sesión exitoso");
        window.location.href = "./index.html";
    } else {
        // Credenciales inválidas, mostrar mensaje de error
        errorMessage.textContent = "Credenciales incorrectas. Inténtalo de nuevo.";
    }
}