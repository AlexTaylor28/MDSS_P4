document.addEventListener("DOMContentLoaded", function() {
    const addQuestionModal = document.getElementById("addQuestionModal");
    const openModalBtn = document.getElementById("addQuestionBtn");
    const closeModalBtn = document.querySelector(".btn-cancel");

    openModalBtn.onclick = function() {
        addQuestionModal.style.display = "flex";
    };

    closeModalBtn.onclick = function() {
        addQuestionModal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target === addQuestionModal) {
            addQuestionModal.style.display = "none";
        }
    };
});
