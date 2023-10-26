document.getElementById("login-btn").addEventListener("click", function () {
    var email = document.getElementById("email").value;
    var senha = document.getElementById("senha").value;

    if (!email || !senha) {
        console.log("Por favor, preencha todos os campos.");
        return;
    }

    // Enviar uma solicitação POST para a rota /login usando Axios
    axios.post("/login", { email: email, senha: senha })
      .then(function (response) {
        console.log(response.data);
        if (response.data === "Login bem-sucedido") {
          // Redirecionar o usuário após o login
          window.location.href = "/home";
        } else {
          console.log("Falha no login: " + response.data);
        }
      })
      .catch(function (error) {
        console.log("Erro na solicitação: " + error);
      });
});
