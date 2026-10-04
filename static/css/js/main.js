document.addEventListener("DOMContentLoaded", () => {

    console.log("FixTrack 2.0 loaded.");

    setupDeleteConfirmation();
    setupKeyboardShortcut();
    setupSearch();

});


function showToast(message) {

    const container =
        document.getElementById("toast-container");

    if (!container) {
        return;
    }

    const toast =
        document.createElement("div");

    toast.className = "toast";

    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}


function setupDeleteConfirmation() {

    const deleteLinks =
        document.querySelectorAll(".action-link.danger");

    deleteLinks.forEach(link => {

        link.addEventListener("click", event => {

            const confirmed =
                confirm(
                    "Are you sure you want to delete this item?"
                );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

}


function setupKeyboardShortcut() {

    document.addEventListener("keydown", event => {

        if (
            (event.ctrlKey || event.metaKey) &&
            event.key.toLowerCase() === "k"
        ) {

            event.preventDefault();

            const search =
                document.getElementById("globalSearch");

            if (search) {
                search.focus();
            }

        }

    });

}


function setupSearch() {

    const search =
        document.getElementById("globalSearch");

    if (!search) {
        return;
    }

    search.addEventListener("input", event => {

        const query =
            event.target.value.toLowerCase().trim();

        const rows =
            document.querySelectorAll("tbody tr");

        rows.forEach(row => {

            const text =
                row.textContent.toLowerCase();

            if (!query || text.includes(query)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }

        });

    });

}