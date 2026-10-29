"""Une la plantilla con chess.js y Stockfish y genera ajedrez.html (un solo archivo, sin internet)."""
import base64
from pathlib import Path

root = Path(__file__).parent
src = root / "src"
html = (src / "app.template.html").read_text(encoding="utf-8")
for name in ("64", "180"):
    data = base64.b64encode((root / "assets" / f"icon-{name}.png").read_bytes()).decode()
    html = html.replace(f"/*ICON{name}*/", "data:image/png;base64," + data)
html = html.replace("/*STOCKFISH*/", (src / "stockfish.min.js").read_text(encoding="utf-8"))
html = html.replace("/*CHESSJS*/", (src / "chess.min.js").read_text(encoding="utf-8"))
(root / "ajedrez.html").write_text(html, encoding="utf-8")
print("OK ->", root / "ajedrez.html", f"{len(html) / 1e6:.2f} MB")
