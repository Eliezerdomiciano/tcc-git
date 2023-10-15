document.getElementById("login-btn").addEventListener("click", function () {
    var email = document.getElementById("email").value;
    var senha = document.getElementById("senha").value;

    // Envie os dados de login para o servidor via Axios ou outra biblioteca de solicitação HTTP
    axios.post("/authenticate", { email: email, senha: senha })
        .then(function (response) {
            if (response.data === "Login bem-sucedido") {
                // Redirecione o usuário após o login
                window.location.href = "/home";
            } else {
                // Exiba uma mensagem de erro, se necessário
                console.log("Falha no login: " + response.data);
            }
        })
        .catch(function (error) {
            console.log("Erro na solicitação: " + error);
        });
});