import fitz
import matplotlib.pyplot as plt
import io
from PIL import Image

doc = fitz.open("documents/format.pdf")
page = doc[0]

pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

img = Image.open(io.BytesIO(pix.tobytes("png")))

fig, ax = plt.subplots(figsize=(10, 14))
ax.imshow(img)

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        print(f"({int(event.xdata)}, {int(event.ydata)})")

fig.canvas.mpl_connect("button_press_event", onclick)

plt.show()