function downloadReport() {
    const loja = document.getElementById("loja-select").value

    fetch("/executarscript", {
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
