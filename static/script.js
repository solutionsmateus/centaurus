API_URL = "https://centursus-back-end-render.onrender.com"

async function executeScript(loja) {
    const response = await fetch(`${API_URL}/executar_script`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ loja: loja })
    });
    const data = await response.json();

    if (!response.ok) {
        console.error("Erro do backend:", data.message);
        alert("Erro no servidor: " + data.message);
        return;
    }

    alert(data.message); 

    if (data.files && data.files.length > 0) {
        const downloadContainer = document.getElementById('download-links-container'); 
        if (!downloadContainer) {
            console.error("Elemento 'download-links-container' não encontrado!");
            return;
        }
        downloadContainer.innerHTML = '<h3>Arquivos Disponíveis:</h3>'; 

        data.files.forEach(relativePath => {
            relativePath = "https://centursus-back-end-render.onrender.com/downloads"
            const fileUrl = `${API_URL}${relativePath}`; 

            const link = document.createElement('a');
            link.href = fileUrl;
            link.download = relativePath.split('/').pop(); 
            link.textContent = `Baixar ${link.download}`;
            link.style.display = 'block'; 
            link.style.margin = '5px 0';
            downloadContainer.appendChild(link);
        });
        alert("Arquivos estão prontos para download! Clique nos links.");
    } else {
        alert("Nenhum arquivo encontrado para download.");
    }
}
