from pathlib import Path

from PIL import Image
from pdf2image import convert_from_path

from backend.models import PageImage


def load_pages(path, output_dir):
    path = Path(path)
    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    if path.suffix.lower() == ".pdf":
        images = convert_from_path(
            str(path),
            dpi=200
        )
    else:
        images = [
            Image.open(path).convert("RGB")
        ]

    pages = []

    for index, image in enumerate(images):
        output = output_dir / f"page_{index}.png"

        image.save(output)

        pages.append(
            PageImage(
                index=index,
                path=str(output),
                width=image.width,
                height=image.height
            )
        )

    return pages