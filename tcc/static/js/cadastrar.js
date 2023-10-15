document.addEventListener("DOMContentLoaded", function () {
    var cadastrarBtn = document.getElementById("cadastrar");
    if (cadastrarBtn) {
        cadastrarBtn.addEventListener("click", function () {
            var nome = document.getElementById("nome").value;
            var sobrenome = document.getElementById("sobrenome").value;
            var email = document.getElementById("email").value;
            var cpf = document.getElementById("cpf").value;
            var senha = document.getElementById("senha").value;

            axios
                .post("/registration", {
                    nome: nome,
                    sobrenome: sobrenome,
                    email: email,
                    cpf: cpf,
                    senha: senha,
                })
                .then(function (response) {
                    alert("Cadastro realizado com sucesso!");
                    // Redirecionar para a página de login
                    window.location.href = "/login";
                })
                .catch(function (error) {
                    alert("Erro no cadastro: " + error);
                });
        });
    }
});