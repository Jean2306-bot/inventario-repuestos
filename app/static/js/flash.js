document.addEventListener("DOMContentLoaded", function() {
  const flashOverlay = document.getElementById("flash-overlay");
  if (flashOverlay) {
    document.body.classList.add("flash-active");

    // Animación de entrada
    setTimeout(() => flashOverlay.classList.add("show"), 50);

    // Cerrar al hacer clic fuera
    document.addEventListener("click", function(e) {
      if (!flashOverlay.contains(e.target)) {
        closeFlash();
      }
    });

    // Cerrar con la X
    document.querySelectorAll(".btn-close").forEach(btn => {
      btn.addEventListener("click", closeFlash);
    });

    // Autocierre a los 1 segundos
    setTimeout(closeFlash, 2000);

    function closeFlash() {
      flashOverlay.classList.remove("show");
      setTimeout(() => {
        flashOverlay.remove();
        document.body.classList.remove("flash-active");
      }, 300);
    }
  }
});
