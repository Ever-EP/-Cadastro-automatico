// Adiciona máscaras aos campos
function aplicarMascaras() {
    const telefoneInput = document.getElementById('telefone');
    const cpfInput = document.getElementById('cpf');
    const cepInput = document.getElementById('cep');

    telefoneInput.addEventListener('input', function (e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) {
            value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
            value = value.replace(/(\d)(\d{4})$/, '$1-$2');
            e.target.value = value;
        }
    });

    cpfInput.addEventListener('input', function (e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 11) {
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
            e.target.value = value;
        }
    });

    cepInput.addEventListener('input', function (e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length <= 8) {
            value = value.replace(/^(\d{5})(\d)/, '$1-$2');
            e.target.value = value;
        }
    });
}

// Função para mostrar mensagem de status
function mostrarStatus(mensagem, tipo) {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = mensagem;
    statusDiv.className = `status ${tipo}`;
    statusDiv.style.display = 'block';
    
    // Esconde a mensagem após 5 segundos
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 5000);
}

document.getElementById('dadosForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        nome: document.getElementById('nome').value,
        email: document.getElementById('email').value,
        telefone: document.getElementById('telefone').value,
        cpf: document.getElementById('cpf').value,
        endereco: document.getElementById('endereco').value,
        cidade: document.getElementById('cidade').value,
        estado: document.getElementById('estado').value,
        cep: document.getElementById('cep').value
    };
    
    try {
        const response = await fetch('/salvar_dados', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarStatus('✅ Seus dados foram salvos com sucesso!', 'success');
            carregarDados();
        } else {
            mostrarStatus('❌ Erro ao salvar dados: ' + data.error, 'error');
        }
        
    } catch (error) {
        console.error('Erro:', error);
        mostrarStatus('❌ Erro ao conectar com o servidor', 'error');
    }
});

async function carregarDados() {
    try {
        const response = await fetch('/carregar_dados');
        const dados = await response.json();
        
        if (response.ok) {
            document.getElementById('nome').value = dados.nome || '';
            document.getElementById('email').value = dados.email || '';
            document.getElementById('telefone').value = dados.telefone || '';
            document.getElementById('cpf').value = dados.cpf || '';
            document.getElementById('endereco').value = dados.endereco || '';
            document.getElementById('cidade').value = dados.cidade || '';
            document.getElementById('estado').value = dados.estado || '';
            document.getElementById('cep').value = dados.cep || '';
        }
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
}

// Inicialização
window.addEventListener('load', () => {
    carregarDados();
    aplicarMascaras();
}); 