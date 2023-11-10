function atualizarEquipamento() {
    // Obtenha os valores dos campos do modal
  // No seu atualizar.js
    var modelo = document.getElementById('modelo').value;
    var nome_cliente = document.getElementById('nome_cliente').value;
    var marca = document.getElementById('marca').value;
    var data_recebida = document.getElementById('data_recebida').value;
    var numero_serial = document.getElementById('numero_serial').value;


    // Faça uma requisição AJAX para atualizar os dados
    fetch('/atualizar_equipamento', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            modelo: modelo,
            nome_cliente: nome_cliente,
            marca: marca,
            data_recebida: data_recebida,
            numero_serial: numero_serial,
        }),
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.message); // Pode lidar com a resposta do servidor
        // Atualize a tabela na página recebimento
        window.location.href = '/receipt';
    });
}
