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
        "hero-portrait.webp": ((0, 103, 681, 638), (681, 535), 82),
        "hero-products.webp": ((640, 439, 1341, 638), (700, 199), 82),
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
