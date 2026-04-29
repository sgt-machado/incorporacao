// Este script lida com a exibição condicional de campos de texto com base na seleção de rádios "Sim" ou "Não".
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os rádios que possuem a classe de toggle
    const toggleRadios = document.querySelectorAll('.radio-toggle');

    function handleToggle(radio, event) {
        // Busca o ID da div alvo através do data-attribute 'data-target'
        const targetId = radio.getAttribute('data-target');
        const containerTexto = document.getElementById(targetId);
        
        if (!containerTexto) return;
        
        const inputTexto = containerTexto.querySelector('input, textarea');
        const isSim = (radio.value === 'Sim' || radio.value === 'True');

        if (radio.checked && isSim) {
            // Exibe e limpa o valor "Não"
            containerTexto.style.display = 'block';
            if (inputTexto.value === 'Não') {
                inputTexto.value = '';
            }
            inputTexto.setAttribute('required', 'required');
            
            // Foco apenas se for clique real do usuário
            if (event && event.isTrusted) { 
                inputTexto.focus();
            }
        } else if (radio.checked) {
            // Esconde e preenche com "Não"
            containerTexto.style.display = 'none';
            inputTexto.value = 'Não';
            inputTexto.removeAttribute('required');
        }
    }

    toggleRadios.forEach(radio => {
        // Escuta mudanças de rádio
        radio.addEventListener('change', function(e) {
            // Quando um rádio muda, precisamos checar o grupo todo
            // pois o rádio desmarcado não dispara 'change'
            const radioGroupName = this.name;
            document.querySelectorAll(`input[name="${radioGroupName}"]`).forEach(r => {
                handleToggle(r, e);
            });
        });

        // Dispara ao carregar a página (Estado inicial)
        if (radio.checked) {
            handleToggle(radio);
        }
    });
});