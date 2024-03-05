// ################# O TITULO COM APENAS 3 QUEBRAS DE LINHAS
window.addEventListener('load', function () {
    // Seleciona todos os elementos com a classe "title"
    var titles = document.querySelectorAll('.product-name');

    // Para cada elemento .title
    titles.forEach(function (title) {
        // Calcula a altura do título
        var textHeight = title.scrollHeight;
        
        // Calcula a altura equivalente a três linhas
        var numberOfLines = title.offsetHeight / parseFloat(window.getComputedStyle(title).lineHeight);

        var threeLinesHeight = parseFloat(window.getComputedStyle(title).lineHeight) * 3;

        
        // Se a altura atual do título for menor que a altura equivalente a três linhas
        if (numberOfLines > 3) {

            while (numberOfLines > 3) {
                title.innerHTML = title.innerHTML.slice(0, -1);
                numberOfLines = title.offsetHeight / parseFloat(window.getComputedStyle(title).lineHeight);
            }

            title.innerHTML += '...'

        } else if (numberOfLines < 3) {

            var diff = threeLinesHeight - textHeight;
            // Calcula o número de linhas adicionais necessárias para alcançar três linhas
            var additionalLines = Math.ceil(diff / parseFloat(window.getComputedStyle(title).lineHeight));
            // Adiciona quebras de linha ou espaços em branco para preencher as linhas adicionais
            var newLine = '<br>';
            var filler = '';
            for (var i = 1; i < additionalLines; i++) {
                title.innerHTML += newLine; // Adiciona espaço em branco
            }

            title.innerHTML += filler;
        }
        
    });
});


// ################# O TITULO COM APENAS 3 QUEBRAS DE LINHAS - OUTTRO MODELO
// window.addEventListener('load', function () {
//     // Seleciona todos os elementos com a classe "product-name"
//     var productNames = document.querySelectorAll('.product-namess');

//     // Para cada elemento .product-name
//     productNames.forEach(function (productName) {
//         // Calcula a altura máxima permitida para o nome do produto
//         var maxHeight = parseFloat(window.getComputedStyle(productName).height);

//         // Calcula a altura equivalente a três linhas
//         var threeLinesHeight = parseFloat(window.getComputedStyle(productName).lineHeight) * 3;

//         // Calcula a altura real do texto
//         var textHeight = productName.scrollHeight;

//         // Se a altura real for maior que a altura equivalente a três linhas, ajusta o texto
//         if (textHeight > threeLinesHeight) {
//             // Remove caracteres até que o número de linhas seja igual a 3
//             while (textHeight > threeLinesHeight) {
//                 productName.innerHTML = productName.innerHTML.slice(0, -1);
//                 textHeight = productName.scrollHeight;
//             }
//             // Adiciona '...' ao final do texto
//             productName.innerHTML += '...';
//         } else if (textHeight < threeLinesHeight) {
//             // Calcula a diferença entre a altura real e a altura equivalente a três linhas
//             var diff = threeLinesHeight - textHeight;
//             // Calcula o número de linhas adicionais necessárias para alcançar três linhas
//             var additionalLines = Math.ceil(diff / parseFloat(window.getComputedStyle(productName).lineHeight));
//             // Adiciona quebras de linha ou espaços em branco para preencher as linhas adicionais
//             for (var i = 1; i < additionalLines; i++) {
//                 productName.innerHTML += '<br>';
//             }
//         }
//     });
// });

