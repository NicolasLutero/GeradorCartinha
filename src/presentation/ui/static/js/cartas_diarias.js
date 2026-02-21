// cartas_diarias.js Revisar
import { criarCartaDiv } from "./carta.js";


fetch("/api/usuario/cartas-diarias")
.then(res => res.json())
.then(res => {

    const cartasContainer = document.getElementById("cartas");
    const msg = document.getElementById("mensagem");

    // Caso já tenha pego as cartas
    if (!res.sucesso) {
        msg.innerText = res.mensagem || "As cartas diárias já foram coletadas.";
        return;
    }

    const cartas = res.cartas;

    cartas.forEach(c => {
        const div = document.createElement("div");
        criarCartaDiv(c, div);
        cartasContainer.appendChild(div);
    });

})
.catch(err => {
    console.error("Erro ao buscar cartas diárias:", err);
});


document.getElementById("btn-receber").addEventListener("click", () => {
    window.location.href = "/home";
});
