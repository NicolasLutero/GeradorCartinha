document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const senha = document.getElementById("senha").value;
    const msg = document.getElementById("mensagem");

    if (!nome || !senha) {
        msg.innerText = "Preencha todos os campos.";
        return;
    }

    const payload = { nome, senha };

    fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            // REDIRECIONA
            window.location.href = "/home";
        } else {
            msg.innerText = data.mensagem || "Usuário ou senha inválidos.";
        }
    })
    .catch(err => {
        console.error(err);
        msg.innerText = "Erro de comunicação com o servidor.";
    });
});
