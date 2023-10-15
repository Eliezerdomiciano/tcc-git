const btnOpen = querySelector("#btn-pesquisar")
const btnClose = querySelector("#btn-close")
const modal = querySelector("#modal")

btnOpen.onclick = function () {
    modal.showModal()
}

btnClose.onclick = function () {
    modal.close()
}

// Função para preencher a tabela com os dados do JSON
function preencherTabela(data) {
    // Limpar a tabela existente
    const tabela = document.querySelector('.table-container .tbody-modal');
    tabela.innerHTML = '';

    // Preencher a tabela com os dados do JSON
    for (let i = 0; i < data.site.length; i++) {
        tabela.innerHTML += `
            <tr>
                <td>${data.nome[i]}</td>
                <td>${data.preco[i]}</td>
                <td>${data.site[i]}</td>
                <td>Ação</td>
                <td>
                    <button class="btn btn-sm" id="btn-comprar">Comprar</button>
                    <button class="btn btn-sm" id="btn-close">Cancelar</button>
                </td>
            </tr>
        `;
    }

};