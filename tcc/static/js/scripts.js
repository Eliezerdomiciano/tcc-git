document.getElementById("btn-pesquisar").addEventListener("click", function() {
    fetch('/stock', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Acesse os dados corretamente
        const dados = data["arquivo.json"]["site_menor_preco"];

        const modal = document.getElementById("modal");
        const tbody = document.querySelector(".tbody-modal");
        tbody.innerHTML = ''; // Limpa o conteúdo anterior

        // Preencha a tabela com os dados
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${dados.nome}</td>
            <td>R$${dados.preco},00</td>
            <td>${dados.fornecedor}</td>
            <td><button id="btn-close" onclick="fecharModal()">Fechar</button>
            <button id="btn-comprar">Comprar</button>
            </td>
        `;
        tbody.appendChild(row);

        modal.showModal();
    });
});



function fecharModal() {
    const modal = document.getElementById("modal");
    modal.close();
    console.log("Função fecharModal() chamada");
}
