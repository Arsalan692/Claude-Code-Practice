// main.js — students will add JavaScript here as features are built

// Set the "How it works" YouTube link here when it's ready (any youtube.com/watch?v= or youtu.be/ URL).
const HOW_IT_WORKS_VIDEO_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("how-it-works-modal");
    if (!modal) return;

    const trigger = document.querySelector("[data-modal-trigger='how-it-works']");
    const closeBtn = modal.querySelector("[data-modal-close]");
    const videoSlot = document.getElementById("how-it-works-video");

    function getEmbedUrl(url) {
        const match = url.match(/(?:youtu\.be\/|v=)([\w-]{11})/);
        return match ? `https://www.youtube.com/embed/${match[1]}?autoplay=1` : null;
    }

    function openModal() {
        const embedUrl = getEmbedUrl(HOW_IT_WORKS_VIDEO_URL);
        videoSlot.innerHTML = embedUrl
            ? `<iframe src="${embedUrl}" title="How Spendly works" allow="autoplay; encrypted-media" allowfullscreen></iframe>`
            : `<p class="modal-placeholder-text">Video coming soon — check back shortly.</p>`;
        modal.hidden = false;
        document.body.style.overflow = "hidden";
    }

    function closeModal() {
        modal.hidden = true;
        videoSlot.innerHTML = "";
        document.body.style.overflow = "";
    }

    trigger?.addEventListener("click", openModal);
    closeBtn?.addEventListener("click", closeModal);
    modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !modal.hidden) closeModal();
    });
});
