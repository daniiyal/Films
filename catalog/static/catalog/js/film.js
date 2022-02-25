window.onload = function () {

    let rating = document.querySelector('form[name=rating]')

    rating.addEventListener("change", function (e) {
        let data = new FormData(this)
        fetch(`${this.action}`, {
            method: 'POST',
            body: data
        })
            .then(r => alert("Рейтинг установлен"))
            .catch(e => alert("Ошибка"))
    })
}