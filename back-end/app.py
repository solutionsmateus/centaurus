import flask
from selenium import webdriver


path_html = "centaurus/encartes_concorrentes.html"

SCRIPTS = {
    "assai.py",
    "atacadão.py",
    "frangolandia.py",
    "novoatacarejo.py",
    "gbarbosa.py",
    "cometa.py"
}


def read_lojas():
    