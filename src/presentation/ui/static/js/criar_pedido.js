// Controle do campo "Outro"
const radiosTipoObra = document.querySelectorAll("input[name='tipo_obra']");
const campoOutroTexto = document.getElementById("tipoOutroTexto");

radiosTipoObra.forEach(radio => {
    radio.addEventListener("change", () => {
        if (radio.value === "outro") {
            campoOutroTexto.disabled = false;
            campoOutroTexto.focus();
        } else {
            campoOutroTexto.disabled = true;
            campoOutroTexto.value = "";
        }
    });
});

// Envio do formulário
document.getElementById("pedidoForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const metragem = parseFloat(document.getElementById("metragem").value);
    if (isNaN(metragem) || metragem <= 0) {
        document.getElementById("mensagem").innerText =
            "A metragem deve ser um valor positivo.";
        return;
    }

    const radioSelecionado = document.querySelector(
        "input[name='tipo_obra']:checked"
    );

    if (!radioSelecionado) {
        document.getElementById("mensagem").innerText =
            "Selecione o tipo da obra.";
        return;
    }

    if (
        radioSelecionado.value === "outro" &&
        campoOutroTexto.value.trim() === ""
    ) {
        document.getElementById("mensagem").innerText =
            "Descreva o tipo da obra.";
        return;
    }

    // Normalização explícita
    let tipo = "";
    let outro = "";

    if (radioSelecionado.value === "execucao") {
        tipo = "Execução";
    } else if (radioSelecionado.value === "reforma") {
        tipo = "Reforma";
    } else {
        tipo = "Outro";
        outro = campoOutroTexto.value.trim();
    }

    const formData = new FormData();
    formData.append("cliente", document.getElementById("nome").value);
    formData.append("telefone", document.getElementById("telefone").value);
    formData.append("email", document.getElementById("email").value);
    formData.append("endereco", document.getElementById("endereco").value);
    formData.append("metragem", metragem);
    formData.append("tipo", tipo);
    formData.append("outro", outro);

    const fotos = document.getElementById("fotos").files;
    for (let i = 0; i < fotos.length; i++) {
        formData.append("arq_fotos", fotos[i]);
    }

    const arquivos = document.getElementById("arquivos").files;
    for (let i = 0; i < arquivos.length; i++) {
        formData.append("arq_projetos", arquivos[i]);
    }

    fetch("/criar_pedido", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(() => {
        document.getElementById("mensagem").innerText =
            "Pedido criado com sucesso!";
        document.getElementById("pedidoForm").reset();
        campoOutroTexto.disabled = true;
    })
    .catch(error => {
        console.error(error);
        document.getElementById("mensagem").innerText =
            "Erro ao enviar pedido.";
    });
});
