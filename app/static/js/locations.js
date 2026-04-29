// Escuta a mudança no campo Estado
// Usamos um seletor que pega qualquer elemento cujo ID termina com "-estado"
document.querySelectorAll('select[id$="-estado"]').forEach(selectEstado => {
    selectEstado.addEventListener("change", function() {
        const estadoId = this.value;
        
        // Descobre o prefixo (ex: "id_conscrito" ou "id_endereco")
        // Isso assume que o ID do município segue o mesmo padrão: prefixo + "-municipio"
        const prefixo = this.id.replace("-estado", "");
        const selectMunicipio = document.getElementById(`${prefixo}-municipio`);
        
        if (!estadoId) {
            selectMunicipio.innerHTML = '<option value="">Selecione o município</option>';
            return;
        }

        const url = URL_AJAX_MUNICIPIOS;

        fetch(`${url}?estado_id=${estadoId}`)
            .then(response => response.json())
            .then(data => {
                selectMunicipio.innerHTML = '<option value="">Selecione o município</option>';
                
                data.forEach(item => {
                    let option = document.createElement("option");
                    option.value = item.id;
                    option.text = item.nome;
                    selectMunicipio.appendChild(option);
                });
            })
            .catch(error => console.error('Erro ao carregar municípios:', error));
    });
});