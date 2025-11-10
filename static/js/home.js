function toggleReadMore(btn) {
    const contentDiv = btn.previousElementSibling;

    if (!contentDiv.classList.contains("expanded")) {
        // Expand: show full note from data-full
        contentDiv.innerHTML = contentDiv.dataset.full;
        contentDiv.classList.add("expanded");
        btn.textContent = "Show Less";
    } else {
        // Collapse: show truncated preview
        let preview = contentDiv.dataset.full;
        if(preview.length > 100) {
            preview = preview.slice(0, 100) + '...';
        }
        contentDiv.innerHTML = preview;
        contentDiv.classList.remove("expanded");
        btn.textContent = "Read More";
    }
}
