document.addEventListener("DOMContentLoaded", () => {
    const dropArea = document.body;
    const fileInput = document.getElementById("uploadForm").elements['image'];

    const preventDefaults = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    dropArea.addEventListener("dragover", (e) => {
        preventDefaults(e);
    });

    dropArea.addEventListener("dragleave", (e) => {
        preventDefaults(e);
    });

    dropArea.addEventListener("drop", (e) => {
        preventDefaults(e);

        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
        }
    });
});