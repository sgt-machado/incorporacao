// Script para validação dos formulários usando as classes de validação do Bootstrap
(() => {
    'use strict'

    // Procura por todos os formulários que possuem a classe 'needs-validation'
    const forms = document.querySelectorAll('.needs-validation')

    // Realiza um loop sobre os formulários e impede o envio se algum campo for inválido
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
        }, false)
    })
})()