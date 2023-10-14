const buttonOpen = document.querySelector("#btn-pesquisar")
const modal = document.querySelector("#modal")
const buttonClose = document.querySelector("#btn-close")

buttonOpen.onclick = function () {
    modal.showModal()
}

buttonClose.onclick = function () {
    modal.close()
}