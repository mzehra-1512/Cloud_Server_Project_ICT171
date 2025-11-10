function toggleReadMore(btn) {
    const contentDiv = btn.previousElementSibling;

    if (!contentDiv.classList.contains("expanded")) {
        contentDiv.innerHTML = contentDiv.dataset.full;
        contentDiv.classList.add("expanded");
        btn.textContent = "Show Less";
    } else {
        let preview = contentDiv.dataset.full;
        if(preview.length > 100) {
            preview = preview.slice(0, 100) + '...';
        }
        contentDiv.innerHTML = preview;
        contentDiv.classList.remove("expanded");
        btn.textContent = "Read More";
    }
}
