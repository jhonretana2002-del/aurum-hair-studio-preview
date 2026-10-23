"""Genera los recursos web ligeros a partir de la referencia proporcionada."""

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "design" / "reference.png"
OUTPUT = ROOT / "assets"
OUTPUT.mkdir(exist_ok=True)

with Image.open(SOURCE) as source:
    source = source.convert("RGB")
    crops = {
        "category-makeup.webp": ((23, 650, 143, 740), (360, 270), 78),
        "category-skincare.webp": ((286, 650, 406, 740), (360, 270), 78),
        "category-perfume.webp": ((547, 650, 667, 740), (360, 270), 78),
        "category-hair.webp": ((808, 650, 928, 740), (360, 270), 78),
        "category-kits.webp": ((1072, 650, 1192, 740), (360, 270), 78),
    }
    for filename, (box, size, quality) in crops.items():
        image = source.crop(box)
        if image.size != size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        image.save(OUTPUT / filename, "WEBP", quality=quality, method=6)
        print(f"{filename}: {(OUTPUT / filename).stat().st_size / 1024:.1f} KiB")

for source_name, filename, size in (
    ("portrait-master.png", "hero-portrait.webp", (1200, 900)),
    ("products-master.png", "hero-products.webp", (1200, 400)),
):
    with Image.open(ROOT / "design" / source_name) as master:
        image = master.convert("RGB").resize(size, Image.Resampling.LANCZOS)
        image.save(OUTPUT / filename, "WEBP", quality=80, method=6)
        print(f"{filename}: {(OUTPUT / filename).stat().st_size / 1024:.1f} KiB")

# Elimina solo el fondo negro; el arte y la tipografía originales permanecen.
with Image.open(ROOT / "design" / "aurum-logo-original.png") as logo:
    original = logo.convert("RGB").crop((88, 137, 325, 279))
    transparent = Image.new("RGBA", original.size)
    pixels = []
    for red, green, blue in original.get_flattened_data():
        alpha = max(0, min(255, round((max(red, green, blue) - 5) * 255 / 190)))
        if alpha == 0:
            pixels.append((0, 0, 0, 0))
        else:
            pixels.append(tuple(min(255, round(value * 255 / alpha)) for value in (red, green, blue)) + (alpha,))
    transparent.putdata(pixels)
    transparent.save(OUTPUT / "aurum-logo-transparent.png", optimize=True)
    print(f"aurum-logo-transparent.png: {(OUTPUT / 'aurum-logo-transparent.png').stat().st_size / 1024:.1f} KiB")
