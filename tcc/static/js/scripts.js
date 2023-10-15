document.getElementById("btn-pesquisar").addEventListener("click", function () {
    // Fazer uma solicitação para ler o nome do arquivo JSON
    fetch("/stock", {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const nome_arquivo = data.arquivo_json;

        // Fazer outra solicitação para ler o conteúdo do arquivo JSON
        fetch(nome_arquivo)
        .then(response => response.json())
        .then(data => {
            document.getElementById("nome-produto").textContent = data["Nome Produto"];
            document.getElementById("preco-un").textContent = data["Preço Un."];
            document.getElementById("fornecedor").textContent = data["Fornecedor"];
        });
    });

    // Exibir o modal
    const modal = document.getElementById("modal");
    modal.showModal();
});