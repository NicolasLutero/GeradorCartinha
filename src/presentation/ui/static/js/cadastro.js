// cadastro.js Revisar

const cadastroForm = document.getElementById("cadastroForm");
cadastroForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const senha = document.getElementById("senha").value;
    const confirmarSenha = document.getElementById("confirmarSenha").value;
    const msg = document.getElementById("mensagem");

    if (!nome || !senha || !confirmarSenha) {
        msg.innerText = "Preencha todos os campos.";
        return;
    }

    if (senha.length < 6) {
        msg.innerText = "A senha deve ter no mínimo 6 caracteres.";
        return;
    }

    if (senha !== confirmarSenha) {
        msg.innerText = "As senhas não coincidem.";
        return;
    }

    const payload = { nome, senha };

    fetch("/api/cadastro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            window.location.href = "/home";
        } else {
            msg.innerText = data.mensagem || "Erro ao cadastrar usuário.";
        }
    })
    .catch(err => {
        console.error(err);
        msg.innerText = "Erro de comunicação com o servidor.";
    });
});
