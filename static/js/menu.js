// Menu filter helper

document.addEventListener('DOMContentLoaded', () => {
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', () => {
            document.getElementById('menu-filter-form').submit();
        });
    });
});
