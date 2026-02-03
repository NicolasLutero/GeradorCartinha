fetch("/api/usuario/status-diario")
.then(res => res.json())
.then(res => {

    if (!res.sucesso) {
        console.error("Erro ao carregar status diário:", res.mensagem);
        return;
    }

    const data = res.data; // <- aqui estão os valores verdadeiros

    const reforjar = document.getElementById("reforjar");
    const cartas = document.getElementById("cartas_diarias");
    const fundir = document.getElementById("fundir");

    // Mapa de status
    const mapa = {
        reforjar: data.reforjar,
        cartas_diarias: data.cartas_diarias,
        fundir: data.fundir
    };

    Object.keys(mapa).forEach(id => {
        const card = document.getElementById(id);
        const disponivel = mapa[id];

        if (!disponivel) {
            card.classList.add("bloqueado");
        }

        card.addEventListener("click", () => {
            if (!disponivel) return;
            const rota = card.getAttribute("data-rota");
            window.location.href = rota;
        });
    });

})
.catch(err => {
    console.error("Erro ao carregar status diário:", err);
});
