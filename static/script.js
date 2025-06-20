function downloadReport() {
    const loja = document.getElementById("loja-select").value
    path_execute = "centaurus/back-end/app.py"

    fetch(path_execute("/executarscript"), {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ loja: loja })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        alert("Erro ao executar o script: " + error);
    });
}
