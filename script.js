const API_URL = "https://centursus-back-end-render.onrender.com";
const FileUpload = document.getElementById("fileUpload")
const BaixarButao = document.getElementById("BaixarButao")


async function fileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/fileUpload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("Erro do backend:", data.message);
            alert("Erro no servidor: " + data.message);
            return;
        }

        alert(data.message);
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro na conexão com o servidor.");
    }
}