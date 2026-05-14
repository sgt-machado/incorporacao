$(document).ready(function(){
    // Máscara de CPF
    $('#id_conscrito-cpf').mask('000.000.000-00', {reverse: true});
    $('#id_cpf').mask('000.000.000-00', {reverse: true});

    // Máscara para o CEP
    $('#id_endereco-cep').mask('00000-000', {reverse: true});

    // Máscara de Telefone Celular (9 dígitos) ou Fixo (8 dígitos)
    var SPMaskBehavior = function (val) {
        return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
    },
    spOptions = {
        onKeyPress: function(val, e, field, options) {
            field.mask(SPMaskBehavior.apply({}, arguments), options);
        }
    };

    $('#id_contato-telefone_pessoal').mask(SPMaskBehavior, spOptions);
    $('#id_contato-telefone_emergencia').mask(SPMaskBehavior, spOptions);
});

// Preenchimento automático de nome do residente com base no parentesco selecionado
document.addEventListener('change', function(e) {
    // 1. Verifica se a mudança ocorreu em um campo de parentesco de residente
    if (e.target.name && e.target.name.includes('-parentesco')) {
        const selectParentesco = e.target;
        const valorSelecionado = selectParentesco.options[selectParentesco.selectedIndex].text;
        
        // 2. Localiza a linha (row) onde este select está
        const row = selectParentesco.closest('.dynamic-form-row');
        const inputNomeResidente = row.querySelector('input[name$="-nome"]');

        if (!inputNomeResidente) return;

        // 3. Mapeia os campos do Conscrito (Pai e Mãe)
        // O Django gera IDs como id_conscrito-pai e id_conscrito-mae
        const nomePai = document.getElementById('id_conscrito-pai').value;
        const nomeMae = document.getElementById('id_conscrito-mae').value;

        // 4. Lógica de preenchimento automático
        if (valorSelecionado === "Pai") {
            inputNomeResidente.value = nomePai;
        } else if (valorSelecionado === "Mãe") {
            inputNomeResidente.value = nomeMae;
        } else {
            inputNomeResidente.value = ""; // Limpa o campo se for outro parentesco
        }
    }
});