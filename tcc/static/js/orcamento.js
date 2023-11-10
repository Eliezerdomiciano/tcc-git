$(document).ready(function () {
    // Exibir o modal ao clicar no botão
    $("#btn-realizar").click(function () {
        $("#orcamentoModal").modal("show");
    });

    // Manipular o evento de clique no botão de salvar no modal
    $("#salvarOrcamento").click(function () {
        // Coletar dados do formulário
        var valor = $("#valor").val();
        var defeito = $("#defeito").val();
        var peca = $("#peca").val();
        var prazo = $("#prazo").val();

        // Aqui você pode enviar os dados para o servidor (usando AJAX, por exemplo)
        // e redirecionar para a página orcamento.html após o salvamento bem-sucedido
        // Por agora, vamos apenas imprimir os dados no console
        console.log("Valor: " + valor);
        console.log("Defeito: " + defeito);
        console.log("Peça: " + peca);
        console.log("Prazo: " + prazo);

        // Fechar o modal após salvar
        $("#orcamentoModal").modal("hide");
    });
});