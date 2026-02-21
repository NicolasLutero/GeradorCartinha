// carta.js

export const raridadeStyle = {
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
        borda: "#d4af37"
    }
};


const imageCache = new Map();
export function buscarImagem(c) {
    const key = `${c.personagem}|${c.fundo}|${c.borda}`;

    if (!imageCache.has(key)) {
        const promise = fetch("/img", {
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
            if (!imgRes.sucesso) {
                throw new Error("Erro ao buscar imagem");
            }
            return imgRes.imagem;
        })
        .catch(err => {
            imageCache.delete(key);
            throw err;
        });

        imageCache.set(key, promise);
    }

    return imageCache.get(key);
}


export function criarCartaDiv(carta, div) {
    div.classList.add("carta");

    div.innerHTML = `
        <h3 class="titulo">${carta.personagem} da ${carta.fundo} ${carta.borda}</h3>
        <div class="imagem-container">
            <img alt="${carta.personagem}" class="imagem-carta">
        </div>
        <div class="stats">
            <div><span>Força</span><span>${carta.stats.for[0]} (${carta.stats.for[1]}%)</span></div>
            <div><span>Destreza</span><span>${carta.stats.des[0]} (${carta.stats.des[1]}%)</span></div>
            <div><span>Constituição</span><span>${carta.stats.con[0]} (${carta.stats.con[1]}%)</span></div>
            <div><span>Inteligência</span><span>${carta.stats.int[0]} (${carta.stats.int[1]}%)</span></div>
            <div><span>Sabedoria</span><span>${carta.stats.sab[0]} (${carta.stats.sab[1]}%)</span></div>
            <div><span>Carisma</span><span>${carta.stats.car[0]} (${carta.stats.car[1]}%)</span></div>
        </div>
    `;

    const estilo = raridadeStyle[carta.borda];
    if (estilo) {
        div.style.background = estilo.carta;
        div.style.borderColor = estilo.borda;

        const statsDiv = div.querySelector(".stats");
        statsDiv.style.background = estilo.stats;
        statsDiv.style.border = `1px solid ${estilo.borda}55`;
    }

    const imgElement = div.querySelector(".imagem-carta");

    buscarImagem(carta)
        .then(base64 => {
            imgElement.src = `data:image/png;base64,${base64}`;
        })
        .catch(err => console.error("Erro ao carregar imagem:", err));

    return div;
}


export async function carregarCarta(id, elemento) {
    const res = await fetch("/api/inventario/carta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id })
    });
    const obj = await res.json();
    return criarCartaDiv(obj.carta, elemento);
}
