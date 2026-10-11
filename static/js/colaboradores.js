document.addEventListener('DOMContentLoaded', function () {
    const inputNome = document.getElementById('id_nome');
    const inputCpf = document.getElementById('id_cpf');
    const inputMatricula = document.getElementById('id_matricula');
    const inputFuncao = document.getElementById('id_funcao');
    const inputTelefone = document.getElementById('id_telefone');

    // 1. Bloqueia números e caracteres especiais indesejados em Nome e Função
    function impedirNumeros(event) {
        if (['Backspace', 'Tab', 'ArrowLeft', 'ArrowRight', 'Delete'].includes(event.key)) return;
        const regex = /^[A-Za-zÀ-ÖØ-öø-ÿ\s'\-\.]$/;
        if (!regex.test(event.key)) {
            event.preventDefault();
        }
    }

    if (inputNome) inputNome.addEventListener('keydown', impedirNumeros);
    if (inputFuncao) inputFuncao.addEventListener('keydown', impedirNumeros);

    // 2. Máscara de CPF em tempo real: 000.000.000-00
    if (inputCpf) {
        inputCpf.addEventListener('input', function (e) {
            let v = e.target.value.replace(/\D/g, '').slice(0, 11);
            if (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
            else if (v.length > 6) v = v.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
            else if (v.length > 3) v = v.replace(/(\d{3})(\d{1,3})/, '$1.$2');
            e.target.value = v;
        });
    }

    // 3. Máscara de Matrícula: começa obrigatoriamente com 'F' + 5 números (ex: F12345)
    if (inputMatricula) {
        inputMatricula.addEventListener('input', function (e) {
            let v = e.target.value.toUpperCase();

            // Se o usuário começar a digitar números direto, adiciona o 'F' automaticamente na frente
            if (v.length > 0 && !v.startsWith('F')) {
                v = 'F' + v.replace(/\D/g, '');
            }

            // Pega o 'F' e no máximo 5 números seguintes
            let numeros = v.slice(1).replace(/\D/g, '').slice(0, 5);
            e.target.value = v.startsWith('F') ? 'F' + numeros : '';
        });
    }


    // 4. Máscara de Telefone em tempo real: (00) 00000-0000
    if (inputTelefone) {
        inputTelefone.addEventListener('input', function (e) {
            let v = e.target.value.replace(/\D/g, '').slice(0, 11);
            if (v.length > 6) v = v.replace(/(\d{2})(\d{5})(\d{1,4})/, '($1) $2-$3');
            else if (v.length > 2) v = v.replace(/(\d{2})(\d{1,5})/, '($1) $2');
            else if (v.length > 0) v = v.replace(/(\d{1,2})/, '($1');
            e.target.value = v;
        });
    }
});
