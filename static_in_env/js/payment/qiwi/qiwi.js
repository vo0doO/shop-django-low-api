window.addEventListener('load', function () {

    var urlSuccess = $("#UrlSuccess").attr("data-urlsuccess")
    var urlError = $("#UrlError").attr("data-urlerror")
    var qpk = $("#Qpk").attr("data-qpk")
    var amount = $("#Amount").attr("data-amount")
    var user = $("#User").attr("data-user")
    var description = $("#description").attr("data-description")
    var items = $("#items").attr("data-items")
    var ordered = $("#ordered").attr("data-ordered")
    var billing_address = $("#billing_address").attr("data-billingAddress")
    var start_date = $("#start_date").attr("data-startDate")
    var ordered_date = $("#ordered_date").attr("data-orderedDate")

    var params = {
        publicKey: qpk,
        amount: amount,
        account: user,
        comment: description,
        customFields: {
            items: items,
            ordered: ordered,
            billing_address: billing_address,
            start_date: start_date,
            ordered_date: ordered_date,
        }
    }

    QiwiCheckout.createInvoice(params)
        .then(data => {
            console.log("Платеж отправлен: ", data)
            this.window.location = urlSuccess
        })
        .catch(error => {
            console.log("Возникла ошибка: ", error)
            this.window.location = urlError
        })
})