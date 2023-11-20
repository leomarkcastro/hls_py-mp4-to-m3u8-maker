from PIL import Image


def create(img_path, new_path):
    im1 = Image.open(img_path)

    # invert image color
    im2 = im1.convert(mode="L")
    im2 = im2.point(lambda x: 255 - x)
    im2.save(new_path)
