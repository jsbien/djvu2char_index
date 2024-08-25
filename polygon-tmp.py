# https://stackoverflow.com/questions/28591117/how-do-i-segment-a-document-using-tesseract-then-output-the-resulting-bounding-b
#
# answered Mar 3, 2020 at 8:42
# Tom Monnier
# https://pypi.org/project/tesserocr/

from PIL import Image, ImageDraw
from tesserocr import PyTessBaseAPI, RIL, iterate_level, PSM

img = Image.open("Hochfeder-02_PT01_020bis.png")

results = []
with PyTessBaseAPI() as api:
    api.SetImage(img)
    api.SetPageSegMode(PSM.AUTO_ONLY)
    iterator = api.AnalyseLayout()
    for w in iterate_level(iterator, RIL.BLOCK):
        if w is not None:
            results.append((w.BlockType(), w.BlockPolygon()))
print('Found {} block elements.'.format(len(results)))

draw = ImageDraw.Draw(img)
for block_type, poly in results:
    draw.line(poly + [poly[0]], fill=(0, 255, 0), width=2)

# Display the image
img.show()

# Optionally, save the image
img.save('output_image.png')
