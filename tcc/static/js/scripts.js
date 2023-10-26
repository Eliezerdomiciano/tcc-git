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

// JavaScript
function abrirModalCompra() {
    const modalCompra = document.getElementById("modal-comprar");
    const alerta = document.getElementById("alerta");

    alerta.style.display = "none"; // Esconde o alerta inicialmente

    modalCompra.showModal();

    const btnConfirmarCompra = document.getElementById("btn-confirmar-compra");
    const quantidadeInput = document.getElementById("quantidade"); // Obtém o campo de entrada da quantidade
    const precoProduto = parseFloat(document.getElementById("preco_prod").textContent.replace("R$", "").replace(",", ".")); // Obtém o valor do produto e converte para número
    
    btnConfirmarCompra.addEventListener("click", function () {
        const quantidade = parseFloat(quantidadeInput.value);
        const valorTotal = quantidade * precoProduto;

        if (quantidade > 0) {
            console.log(`Compra confirmada para ${quantidade} unidades. Valor total: R$${valorTotal.toFixed(2)}`);
            modalCompra.close();
        } else {
            alerta.style.display = "block"; // Exibe o alerta
        }
    });

}