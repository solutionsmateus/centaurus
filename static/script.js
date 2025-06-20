const BACKEND_URL = "https://centursus-back-end-render.onrender.com"; 

async function executeScript(loja) {
    const response = await fetch(`${BACKEND_URL}/executar_script`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ loja: loja })
    });
    const data = await response.json();
    console.log(data.message);
}