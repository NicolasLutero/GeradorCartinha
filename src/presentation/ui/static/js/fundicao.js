const cartaBaseId = localStorage.getItem("cartaBaseFundicao");
const cartaSacrificioId = localStorage.getItem("cartaSacrificioFundicao");

const cartaBase = document.getElementById("carta-base");
const cartaSacrificio = document.getElementById("carta-sacrificio");
const cartaResultado = document.getElementById("carta-resultado");
const btnFundir = document.getElementById("btn-fundir");

function selecionarBase() {
    localStorage.setItem("retornoInventario", "selecionandoBaseFundicao");
    window.location.href = "/inventario";
}

function selecionarSacrificio() {
    localStorage.setItem("retornoInventario", "selecionandoSacrificioFundicao");
    window.location.href = "/inventario";
}

function bloquearInterface() {
    cartaBase.classList.add("bloqueado");
    cartaSacrificio.classList.add("bloqueado");
    btnFundir.classList.add("bloqueado");
}

function gerarCarta(div, c) {
// ===== Mapa de cores por raridade =====
        const raridadeStyle = {
            "Comum": {
                carta: "linear-gradient(180deg, #f2f2f2, #d9d9d9)",
                stats: "rgba(120,120,120,0.15)",
                borda: "#8a8a8a"
            },
            "Bom": {
                carta: "linear-gradient(180deg, #e6f7ee, #bfe8d5)",
                stats: "rgba(0,168,107,0.15)",
                borda: "#00a86b"
            },
            "Ótimo": {
                carta: "linear-gradient(180deg, #e6f0ff, #c2d9ff)",
                stats: "rgba(44,123,229,0.15)",
                borda: "#2c7be5"
            },
            "Top": {
                carta: "linear-gradient(180deg, #f1e6ff, #d6c2ff)",
                stats: "rgba(120,70,200,0.18)",
                borda: "#7a3fd1"
            },
            "Perfeito": {
                carta: "linear-gradient(180deg, #fff6d6, #f0d98c)",
                stats: "rgba(212,175,55,0.25)",
                borda: "#d4af37" // dourado
            }
        };

    div.innerHTML = `
        <h3 class="titulo">${c.personagem} da ${c.fundo} ${c.borda}</h3>
        <div class="imagem-container">
            <img alt="${c.personagem}" class="imagem-carta">
        </div>
        <div class="stats">
            <div><span>Força</span><span>${c.stats.for[0]} (${c.stats.for[1]}%)</span></div>
            <div><span>Destreza</span><span>${c.stats.des[0]} (${c.stats.des[1]}%)</span></div>
            <div><span>Constituição</span><span>${c.stats.con[0]} (${c.stats.con[1]}%)</span></div>
            <div><span>Inteligência</span><span>${c.stats.int[0]} (${c.stats.int[1]}%)</span></div>
            <div><span>Sabedoria</span><span>${c.stats.sab[0]} (${c.stats.sab[1]}%)</span></div>
            <div><span>Carisma</span><span>${c.stats.car[0]} (${c.stats.car[1]}%)</span></div>
        </div>
    `;

    const estilo = raridadeStyle[c.borda];

    if (estilo) {
        div.style.background = estilo.carta;
        div.style.borderColor = estilo.borda;

        const statsDiv = div.querySelector(".stats");
        statsDiv.style.background = estilo.stats;
        statsDiv.style.border = `1px solid ${estilo.borda}55`;
    }

    fetch("/img", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            fundo: c.fundo,
            personagem: c.personagem,
            borda: c.borda
        })
    })
    .then(r => r.json())
    .then(imgRes => {
        if (imgRes.sucesso) {
            div.querySelector(".imagem-carta").src =
                `data:image/png;base64,${imgRes.imagem}`;
        }
    });
}

function carregarCarta(id, elemento) {
    fetch("/api/inventario/carta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id })
    })
    .then(r => r.json())
    .then(res => gerarCarta(elemento, res.carta));
}

function fundir() {
    if (!cartaBaseId || !cartaSacrificioId) {
        alert("Escolha as duas cartas.");
        return;
    }

    bloquearInterface();

    fetch("/api/usuario/fundicao", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            base_id: cartaBaseId,
            sacrificio_id: cartaSacrificioId
        })
    })
    .then(r => r.json())
    .then(res => {
        gerarCarta(cartaResultado, res.carta);
    });
}

/* =========================
   Inicialização
========================= */

cartaBase.addEventListener("click", selecionarBase);
cartaSacrificio.addEventListener("click", selecionarSacrificio);
btnFundir.addEventListener("click", fundir);

if (cartaBaseId) carregarCarta(cartaBaseId, cartaBase);
if (cartaSacrificioId) carregarCarta(cartaSacrificioId, cartaSacrificio);
