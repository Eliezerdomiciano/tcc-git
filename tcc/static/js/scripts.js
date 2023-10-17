document.getElementById("btn-pesquisar").addEventListener("click", function() {
    fetch('/stock', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const dados = data["arquivo.json"]["site_menor_preco"];
        const modal = document.getElementById("modal");
        const tbody = document.querySelector(".tbody-modal");
        tbody.innerHTML = '';

        const row = document.createElement("tr");
        row.innerHTML = `
            <td id="nome_prod">${dados.nome}</td>
            <td id="preco_prod">R$${dados.preco},00</td>
            <td id="fornecedor_prod">${dados.fornecedor}</td>
            <td>
                <button id="btn-close" data-action="fecharModal">Fechar</button>
                <button id="btn-comprar" data-action="abrirModalCompra">Comprar</button>
            </td>
        `;
        tbody.appendChild(row);

        modal.showModal();
    });
});

// Ouvinte de evento para os botões dentro da tabela modal
document.querySelector(".tbody-modal").addEventListener("click", function(event) {
    if (event.target.getAttribute("data-action") === "fecharModal") {
        fecharModal();
    } else if (event.target.getAttribute("data-action") === "abrirModalCompra") {
        abrirModalCompra();
    }
});

function abrirModalCompra() {
    const modalCompra = document.getElementById("modal-comprar");
    const alerta = document.getElementById("alerta");

    alerta.style.display = "none"; // Esconde o alerta inicialmente

    modalCompra.showModal();

    const btnConfirmarCompra = document.getElementById("btn-confirmar-compra");

    btnConfirmarCompra.addEventListener("click", function () {
        const quantidade = parseFloat(document.getElementById("quantidade").value);
        if (quantidade > 0) {
            console.log(`Compra confirmada para ${quantidade} unidades.`);
            modalCompra.close();
        } else {
            alerta.style.display = "block"; // Exibe o alerta
        }
    });
}