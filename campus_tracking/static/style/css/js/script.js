// static/js/script.js

document.addEventListener("DOMContentLoaded", function () {
    console.log(" Script loaded successfully!");

    // --- Sidebar toggle for smaller screens ---
    const sidebarToggle = document.querySelector("#sidebarToggle");
    const sidebar = document.querySelector(".sidebar");

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", () => {
            sidebar.classList.toggle("active");
        });
    }

  

});
