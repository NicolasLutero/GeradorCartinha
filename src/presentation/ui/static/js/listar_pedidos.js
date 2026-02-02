document.addEventListener("DOMContentLoaded", carregarPedidos);

function carregarPedidos() {
    const container = document.getElementById("listaPedidos");
    container.innerHTML = "<p>Carregando pedidos...</p>";

    fetch("/listar_pedidos")
        .then(response => response.json())
        .then(pedidos => {
            container.innerHTML = "";

            if (pedidos.length === 0) {
                container.innerHTML = "<p>Nenhum pedido encontrado.</p>";
                return;
            }

            pedidos.forEach(pedido => {
                const card = document.createElement("div");
                card.className = "card";

                const valorFormatado = new Intl.NumberFormat('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                }).format(pedido.valor);

                card.innerHTML = `
                    <h3>Pedido #${pedido.id}</h3>
                    <p><strong>Cliente:</strong> ${pedido.cliente}</p>
                    <p><strong>E-mail:</strong> ${pedido.email}</p>
                    <p><strong>Número:</strong> ${pedido.telefone}</p>
                    <p><strong>Tipo Serviço:</strong> ${pedido.tipo}</p>
                    <p><strong>Outro:</strong> ${pedido.outro}</p>
                    <p><strong>Endereço:</strong> ${pedido.endereco}</p>
                    <p><strong>Metragem:</strong> ${pedido.metragem}</p>
                    <a href="download_arquivos/${pedido.id}/foto">Fotos(${pedido.qtd_fotos})</a>
                    <a href="download_arquivos/${pedido.id}/projeto">Projetos(${pedido.qtd_projetos})</a>
                    <button onclick="deletarPedido(${pedido.id})">Deletar</button>
                `;

                container.appendChild(card);
            });
        })
        .catch(() => {
            container.innerHTML = "<p>Erro ao carregar pedidos.</p>";
        });
}

function deletarPedido(pedidoId) {
    fetch(`/deletar_pedido/${pedidoId}`, {
        method: "DELETE"
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro ao deletar");
        }
        // limpa e reconstrói a lista
        carregarPedidos();
    })
    .catch(() => {
        alert("Não foi possível deletar o pedido.");
    });
}
