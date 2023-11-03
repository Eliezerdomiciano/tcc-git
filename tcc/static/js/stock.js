// Após obter o arquivo JSON na resposta da pesquisa
fetch('/salvar_dados', {
    method: 'POST',
    body: JSON.stringify(data), // Envie os dados JSON para o servidor
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => {
    // Trate a resposta do servidor (pode ser uma confirmação de sucesso)
});
