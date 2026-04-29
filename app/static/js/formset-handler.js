document.addEventListener('DOMContentLoaded', function() {

    // --- FUNÇÃO DE REINDEXAÇÃO ---
    function reindexFormset(wrapper) {
        const rows = wrapper.querySelectorAll('.dynamic-form-row');
        const prefix = wrapper.getAttribute('data-prefix');
        const totalForms = wrapper.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
        
        rows.forEach((row, index) => {
            row.querySelectorAll('input, select, textarea').forEach(input => {
                // Substitui qualquer índice central pelo novo (ex: residentes-3-nome -> residentes-0-nome)
                const regex = new RegExp(`${prefix}-\\d+-`, 'g');
                input.name = input.name.replace(regex, `${prefix}-${index}-`);
                input.id = input.id.replace(regex, `${prefix}-${index}-`);
            });
        });
        totalForms.value = rows.length;
    }

    // --- EVENTO DE ADICIONAR ---
    document.addEventListener('click', function(e) {
        if (e.target.closest('.btn-add')) {
            const btn = e.target.closest('.btn-add');
            const wrapper = btn.closest('.formset-wrapper');
            const container = wrapper.querySelector('.formset-container');
            const prefix = wrapper.getAttribute('data-prefix');
            const totalForms = wrapper.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
            const template = wrapper.querySelector('.empty-form');
            
            const currentCount = parseInt(totalForms.value);
            const newFormHtml = template.innerHTML.replace(/__prefix__/g, currentCount);
            
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = newFormHtml;
            const newRow = tempDiv.firstElementChild;

            // Limpa seleções
            newRow.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(input => {
                input.checked = false;
            });

            container.appendChild(newRow);
            totalForms.value = currentCount + 1;
        }
    });

    // --- EVENTO DE REMOVER ---
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.btn-remove');
        if (!btn) return;

        const row = btn.closest('.dynamic-form-row');
        const wrapper = btn.closest('.formset-wrapper');
        const idInput = row.querySelector('input[name$="-id"]');
        const deleteCheckbox = row.querySelector('input[name$="-DELETE"]');

        const isNewForm = !idInput || idInput.value === "";

        if (isNewForm) {
            row.remove();
            reindexFormset(wrapper);
        } else {
            if (deleteCheckbox) {
                deleteCheckbox.checked = true;
                row.style.display = 'none';
                // Remove required para não travar validação do navegador
                row.querySelectorAll('[required]').forEach(el => el.removeAttribute('required'));
            }
        }
    });
});