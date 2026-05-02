// Define os IDs dos campos que serão preenchidos.
const campos = ['id_endereco-logradouro', 'id_endereco-bairro', 'id_endereco-numero', 'id_endereco-complemento'];

// Função para preencher os campos com os dados do endereço ou limpar se for string vazia
const preencherCampos = (dadosEndereco) => {
    campos.forEach(idCampo => {
        // Se for objeto, busca a chave. Se não (string como "..." ou ""), usa o próprio valor.
        const valor = (typeof dadosEndereco === 'object') ? dadosEndereco[idCampo] : dadosEndereco;
        
        // O "?? ''" garante que se o valor for nulo/indefinido, o campo fique vazio
        document.getElementById(idCampo).value = valor ?? "";
    });
};

// Escuta o evento de blur (perda de foco) no campo de CEP
document.addEventListener('blur', async (evento) => {
    const campoCep = evento.target; // Referência direta ao campo de CEP
    if (campoCep.id !== 'id_endereco-cep') return; // Se não for o campo de CEP, ignora
    
    const cep = campoCep.value.replace(/\D/g, '');
    campoCep.classList.remove('is-invalid');
    preencherCampos("");
    document.getElementById('id_endereco-estado').value = "";
    document.getElementById('id_endereco-municipio').value = "";

    // Validações básicas do CEP (campo vazio ou tamanho incorreto)
    if (cep === "") { preencherCampos(""); return; }
    if (cep.length !== 8) {
        preencherCampos("");
        document.getElementById('id_endereco-estado').value = "";
        document.getElementById('id_endereco-municipio').value = "";
        campoCep.classList.add('is-invalid');
        campoCep.focus();
        return;
    }
    
    // Consulta à API ViaCEP com o CEP fornecido
    try {
    const resposta = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
    const json = await resposta.json();

    // Preenche os campos de texto com os dados retornados ou limpa os campos onde não houver dados
    preencherCampos({
        'id_endereco-logradouro': json.logradouro,
        'id_endereco-bairro': json.bairro,
        'id_endereco-numero': "",
        'id_endereco-complemento': ""
    });

    // Preenche os selects de estado e município
    const idEstado = json.ibge.substring(0, 2); // Pega apenas o código do estado, Ex: "35" para SP
    const idMunicipio = json.ibge;             // Ex: "3550308" para São Paulo

    const selectEstado = document.getElementById('id_endereco-estado');
    const selectMunicipio = document.getElementById('id_endereco-municipio');

    // Define o estado e dispara o evento para carregar as cidades via AJAX
    selectEstado.value = idEstado;
    selectEstado.dispatchEvent(new Event('change'));

    // Espera as cidades carregarem para selecionar a cidade correta com o mesmo código IBGE
    // Criamos um observador simples para detectar quando o select de municípios mudar
    const observer = new MutationObserver(() => {
        if (selectMunicipio.options.length > 1) { 
            selectMunicipio.value = idMunicipio;
            observer.disconnect();
        }
    });

    // Observa mudanças no select de municípios (quando as opções forem carregadas)
    observer.observe(selectMunicipio, { childList: true });

    document.getElementById('id_endereco-numero').focus();

    } catch {
        preencherCampos("");
        campoCep.classList.add('is-invalid');
        campoCep.focus();
    }
}, true);