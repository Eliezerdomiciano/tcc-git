const btnOpen = document.querySelector("#btn-pesquisar")
const btnClose = document.querySelector("#btn-close")
const modal = document.querySelector("#modal")

btnOpen.onclick = function () {
    modal.showModal()
}

btnClose.onclick = function () {
    modal.close()
}
