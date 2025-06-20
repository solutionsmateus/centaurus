function downloadReport() {
    const loja = document.getElementById("loja-select").value;
    const estado = document.getElementById("estado-select").value;

    fetch("/executar_script", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ loja: loja, estado: estado })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        alert("Erro ao executar o script: " + error);
    });
}
