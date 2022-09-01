from PIL import Image
from make_cppn import make_cppn

# generate a CPPN
cppn = make_cppn(20, 100, 20, 100)

# open a starting point image
image = Image.open("cppns/44/image.png")
image_new = Image.new("RGB")

# for each pixel, get the rgb components
pixels = image.load()
for i in range(image.size[0]):
    for j in range(image.size[1]):
        r, g, b = pixels[i, j]
        pixels[i, j] = (r, g, b)

        cppn.graph.nodes[1]['value'] = r
        cppn.graph.nodes[2]['value'] = g
        cppn.graph.nodes[3]['value'] = b
        out = cppn.evaluate()
        red = int(abs(out[0]) * 255)
        green = int(abs(out[1]) * 255)
        blue = int(abs(out[2]) * 255)
        image.putpixel((j, i), (red, green, blue))

image = image.resize((256, 256), Image.ANTIALIAS)
image.show()