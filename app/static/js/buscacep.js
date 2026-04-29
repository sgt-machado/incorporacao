const campos = ['id_endereco-logradouro', 'id_endereco-bairro', 'id_endereco-municipio', 'id_endereco-estado', 'id_endereco-numero', 'id_endereco-complemento'];

const preencher = (v) => campos.forEach(c => document.getElementById(c).value = v[c] || v);

document.addEventListener('blur', async (e) => {
    if (e.target.id !== 'id_endereco-cep') return;
    
    const cep = e.target.value.replace(/\D/g, '');
    if (!/^[0-9]{8}$/.test(cep)) return preencher("");

    // Preenche os campos com "..." enquanto busca os dados
    preencher("...");
    try {
        const res = await fetch(`https://viacep.com.br{cep}/json/`);
        const dados = await res.json();
        
        if (dados.erro) throw new Error();
        preencher({ rua: dados.logradouro, bairro: dados.bairro, municipio: dados.localidade, estado: dados.uf });
    } catch {
        preencher("");
        alert("CEP não encontrado.");
    }
}, true);