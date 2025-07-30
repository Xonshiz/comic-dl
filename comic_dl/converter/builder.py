"""
Convert downloaded images into CBZ or PDF.
"""

import zipfile
from pathlib import Path
from PIL     import Image

class Converter:
    def __init__(self, format: str = "cbz"):
        self.format = format.lower()

    def build(self, images: list, output: Path) -> None:
        if self.format == "cbz":
            with zipfile.ZipFile(output, "w") as zf:
                for img in images:
                    zf.write(img, arcname=img.name)
        elif self.format == "pdf":
            pil_imgs = []
            for img_path in images:
                img = Image.open(img_path)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                pil_imgs.append(img)
            if pil_imgs:
                pil_imgs[0].save(
                    output,
                    save_all=True,
                    append_images=pil_imgs[1:],
                    format="PDF"
                )
        else:
            raise ValueError(f"Unknown format: {self.format}")
