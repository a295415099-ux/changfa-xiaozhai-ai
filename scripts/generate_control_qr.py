from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
URL = "https://a295415099-ux.github.io/changfa-xiaozhai-ai/"
OUT = ROOT / "assets/qr"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    qr = QrCodeWidget(URL)
    qr.barLevel = "H"
    qr.barBorder = 4
    qr.qr.make()

    module_count = qr.qr.getModuleCount()
    quiet_zone = 4
    box = 16
    size = (module_count + quiet_zone * 2) * box
    image = Image.new("RGB", (size, size), "#fffdf8")
    draw = ImageDraw.Draw(image)
    dark = "#0f5148"

    for row in range(module_count):
        for col in range(module_count):
            if qr.qr.isDark(row, col):
                x0 = (col + quiet_zone) * box
                y0 = (row + quiet_zone) * box
                draw.rectangle([x0, y0, x0 + box - 1, y0 + box - 1], fill=dark)

    image = image.resize((720, 720), Image.Resampling.NEAREST)
    image.save(OUT / "changfa-ai-control-qr.png")
    (OUT / "changfa-ai-control-url.txt").write_text(URL + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
