"""Dibuja el logo (caballo sobre fondo verde) y genera logo.png, logo.ico y los iconos para la página."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).parent
out = root / "assets"
out.mkdir(exist_ok=True)

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

# Fondo: cuadrado redondeado con degradado verde.
grad = Image.new("RGBA", (S, S))
gd = ImageDraw.Draw(grad)
top, bottom = (76, 195, 138), (22, 101, 72)
for y in range(S):
    t = y / (S - 1)
    gd.line([(0, y), (S, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)) + (255,))
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 0.22, fill=255)
# Tablero sutil en la parte inferior, mezclado sobre el degradado.
overlay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
cell = S // 8
for c in range(8):
    if c % 2 == 0:
        od.rectangle([c * cell, S - cell, (c + 1) * cell, S], fill=(255, 255, 255, 38))
grad = Image.alpha_composite(grad, overlay)
img.paste(grad, (0, 0), mask)

# Caballo: glifo de Segoe UI Symbol con contorno oscuro.
font = ImageFont.truetype(r"C:\Windows\Fonts\seguisym.ttf", int(S * 0.74))
glyph = "\u265E"
d = ImageDraw.Draw(img)
bbox = d.textbbox((0, 0), glyph, font=font)
x = (S - (bbox[2] - bbox[0])) / 2 - bbox[0]
y = (S - (bbox[3] - bbox[1])) / 2 - bbox[1] - S * 0.04
d = ImageDraw.Draw(img)
d.text((x + S * 0.015, y + S * 0.025), glyph, font=font, fill=(0, 0, 0, 90))  # sombra
d.text((x, y), glyph, font=font, fill=(255, 255, 255, 255), stroke_width=int(S * 0.018), stroke_fill=(16, 60, 44, 255))

img.resize((512, 512), Image.LANCZOS).save(out / "logo.png")
img.resize((180, 180), Image.LANCZOS).save(out / "icon-180.png")
img.resize((64, 64), Image.LANCZOS).save(out / "icon-64.png")
img.save(out / "logo.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("OK ->", out)
