import os

import lib.img2binvis as img2binvis
import numpy as np
import qrcode.constants
from PIL import Image
from qrcode.main import QRCode

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def get_flag():
    try:
        with open("../46_flag.txt", "r") as f:
            return f.read().strip()
    except:
        return "flag{this_is_a_fake_flag}"


FLAG = get_flag()


LORE_TEXT = """We're no strangers to love
You know the rules and so do I (do I)
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (to say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you




No way you thought I'd make it this easy, did you? Anyways, good luck!! :D"""

BASE_IMG_LOC = "res/image.tiff"
EXT = BASE_IMG_LOC.split(".")[-1]
SINGING_MAN_LOC = "res/singing_man_gen.png"
SINGING_MAN_OFFSET = (938, 194)
SUS_PIXEL_DATA_OFFSET = (4816304, 10156750)
FLAG_QR_OFFSET = (157, 19)
QR_OPACITY = 0.61

if __name__ == "__main__":
    os.makedirs("./temp", exist_ok=True)
    # load images and generate QR codes
    im = Image.open(BASE_IMG_LOC)
    exif = im.getexif()
    base_im = np.array(im)
    singing_man_im = np.array(Image.open(SINGING_MAN_LOC))
    qr_gen = QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr_gen.add_data(FLAG)
    flag_qr_im = np.array(
        qr_gen.make_image(fill_color=(0, 0, 0), back_color=(39, 217, 254))
    )
    Image.fromarray(flag_qr_im).save("./temp/flag_qr.png")

    qr_gen = QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=0,
    )
    qr_gen.add_data(LORE_TEXT)
    lore_qr_im = np.array(
        qr_gen.make_image(fill_color=(0, 0, 0), back_color=(255, 255, 255))
    )
    Image.fromarray(lore_qr_im).save("./temp/lore_qr.png")

    # overlay lore qr code on base image
    im_center = (base_im.shape[0] // 2, base_im.shape[1] // 2)
    qr_center = (lore_qr_im.shape[0] // 2, lore_qr_im.shape[1] // 2)
    offset = (im_center[0] - qr_center[0], im_center[1] - qr_center[1])
    base_im[
        offset[0] : offset[0] + lore_qr_im.shape[0],
        offset[1] : offset[1] + lore_qr_im.shape[1],
        :3,
    ] *= (
        lore_qr_im // 255
    )

    os.makedirs("./temp", exist_ok=True)
    Image.fromarray(base_im).save("./temp/imgwlore." + EXT, exif=exif)

    # get binvis image
    data = img2binvis.get_binary("./temp/imgwlore." + EXT)
    np_img = img2binvis.binary_to_img(data, clrschm=img2binvis.ByteDetail)
    Image.fromarray(np_img).save("./temp/ImgWithLore_binvis.png")

    # replace part of img with singing
    np_img[
        SINGING_MAN_OFFSET[0] : SINGING_MAN_OFFSET[0] + singing_man_im.shape[0],
        SINGING_MAN_OFFSET[1] : SINGING_MAN_OFFSET[1] + singing_man_im.shape[1],
    ] = singing_man_im

    data = img2binvis.img_to_binary(np_img, data, clrschm=img2binvis.ByteDetail)

    img = Image.fromarray(np_img)
    img.save("./temp/imgwsing_binvis.png")
    img = img.crop(
        (
            SINGING_MAN_OFFSET[1] - 2,
            SINGING_MAN_OFFSET[0] - 2,
            SINGING_MAN_OFFSET[1] + singing_man_im.shape[1] + 2,
            SINGING_MAN_OFFSET[0] + singing_man_im.shape[0] + 2,
        )
    )
    img = img.resize((img.width * 5, img.height * 5), Image.NEAREST)
    img.save("../writeup/img/singing_man.png")
    with open("./temp/imgwsing." + EXT, "wb") as f:
        f.write(data)

    # zoom into sus pixel data and add qr code
    np_img = img2binvis.binary_to_img(
        data,
        SUS_PIXEL_DATA_OFFSET[0],
        SUS_PIXEL_DATA_OFFSET[1],
        img2binvis.ByteMagnitude,
    )

    Image.fromarray(np_img).save("./temp/sus_pixel_binvis.png")

    temp = np_img[
        FLAG_QR_OFFSET[0] : FLAG_QR_OFFSET[0] + flag_qr_im.shape[0],
        FLAG_QR_OFFSET[1] : FLAG_QR_OFFSET[1] + flag_qr_im.shape[1],
    ]
    temp = temp * (1 - QR_OPACITY) + flag_qr_im * QR_OPACITY
    np_img[
        FLAG_QR_OFFSET[0] : FLAG_QR_OFFSET[0] + flag_qr_im.shape[0],
        FLAG_QR_OFFSET[1] : FLAG_QR_OFFSET[1] + flag_qr_im.shape[1],
    ] = temp

    data = img2binvis.img_to_binary(
        np_img,
        data,
        SUS_PIXEL_DATA_OFFSET[0],
        SUS_PIXEL_DATA_OFFSET[1],
        img2binvis.ByteMagnitude,
        True,
    )

    with open("../public/MtEverest." + EXT, "wb") as f:
        f.write(data)

    np_img = img2binvis.binary_to_img(
        data,
        SUS_PIXEL_DATA_OFFSET[0],
        SUS_PIXEL_DATA_OFFSET[1],
        img2binvis.ByteMagnitude,
    )

    img = Image.fromarray(np_img)
    img.save("./temp/sus_pixel_qr_binvis.png")
    img = img.crop(
        (
            FLAG_QR_OFFSET[1] - 2,
            FLAG_QR_OFFSET[0] - 2,
            FLAG_QR_OFFSET[1] + flag_qr_im.shape[1] + 2,
            FLAG_QR_OFFSET[0] + flag_qr_im.shape[0] + 2,
        )
    )
    img = img.resize((img.width * 6, img.height * 6), Image.NEAREST)
    img.save("../writeup/img/qr_code.png")

    img = img.point(lambda p: 255 if p > 150 else 0)  # type: ignore

    img.save("../writeup/img/qr_code_edited.png")
