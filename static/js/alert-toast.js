// Alert toast -> Alerta de mensagem
function showToast(message, isError) {
    const toastElement = document.getElementById("toast");
    const toastBodyElement = $('#toast-body');
    toastElement.classList.remove('bg-danger', 'bg-success')

    toastBodyElement.text(message);
    if (isError) {
        toastElement.classList.add('bg-danger');
    } else {
        toastElement.classList.add('bg-success');
    }
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    setTimeout(() => {
        toast.hide()
    }, 5000);
}