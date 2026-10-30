"""Sube esta carpeta al repo público Lushows/apa-noticias y activa GitHub Pages. Lo corre Luis.
Usa la cuenta Lushows sin cambiar la cuenta activa del PC (que es la de BIO-SETA)."""
import os
import subprocess
import time
from pathlib import Path

AQUI = Path(__file__).parent
REPO = "Lushows/apa-noticias"


def gh(*args, **k):
    return subprocess.run(["gh", *args], cwd=AQUI, env=ENV, text=True, capture_output=True, **k)


token = subprocess.run(["gh", "auth", "token", "-u", "Lushows"], text=True, capture_output=True).stdout.strip()
ENV = {**os.environ, "GH_TOKEN": token}
if gh("repo", "view", REPO).returncode != 0:
    r = gh("repo", "create", REPO, "--public", "--source", ".", "--remote", "origin", "--push",
           "--description", "APA Noticias — privacidad y eliminación de datos")
    print(r.stdout or r.stderr)
else:
    subprocess.run(["git", "-c", f"http.extraheader=AUTHORIZATION: bearer {token}", "push", "origin", "main"],
                   cwd=AQUI)
gh("api", "-X", "POST", f"repos/{REPO}/pages", "-f", "source[branch]=main", "-f", "source[path]=/")
time.sleep(5)
base = "https://lushows.github.io/apa-noticias"
print("\nListo. Lo que va en Meta (tarda 1-2 minutos en abrir la primera vez):")
print("  URL de la política de privacidad:", f"{base}/privacidad.html")
print("  Eliminación de datos de usuario: ", f"{base}/eliminacion-datos.html")
