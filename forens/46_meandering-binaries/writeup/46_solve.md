# Meandering Binaries - Writeup

> Author: [FieryRMS](https://github.com/FieryRMS) \
> Difficulty: 3/5

## Given hints

- Meandering = curve, Hilbert = Hilbert curve.
- Looking through the EXIF data you will see:
  - `Artist: Aldo Cortesi`
  - `DateTime: 2011:12:23`

Searching for "Binary hilbert curves" on Google, you will come across the [article](https://corte.si/posts/visualisation/binvis/) (perhaps several if you include his name in the search) by Aldo Cortesi written on 2011-12-23. The article explains how we can visualize binary data using space-filling curves for reverse engineering. He links a demo of the tool he created, [binvis.io](https://binvis.io/).

The very obvious huge QR code is unrelated to the solution and exists only for foreshadowing.

## Solution

1. Upload the given image to [binvis.io](https://binvis.io/).

1. Upon first inspection, you will find an image of a person singing. Changing the `Colorscheme` to `Detail` enhances the colors in the picture.

    ![Singing person](./img/singing_man.png)

1. Clicking on the suspicious violet colored pixel will take you to offsets `(4816304, 10156750)`.

1. Scroll back up to the top to see a QR code. Change to the `Magnitude` cholorscheme to get a better image. The QR code may be hard to scan. Take a screenshot and edit the image to make the QR code more readable.

    ![QR code](./img/qr_code.png)

1. To edit the picture you may use [Photopea](https://www.photopea.com/) -> `Image` -> `Adjustments` -> `Threshold` and use a value between `141` and `157`. Or you may also use a simple python Pillow `point()` threshold filter,

    ```py
    img = img.point(lambda p: 255 if p > 150 else 0)
    ```

    ![Edited QR code](./img/qr_code_edited.png)

1. Scan the QR code to get the flag: \
    `cuhk24ctf{oMg-aRt-uSiNg-bInaRy-vIsuAlIzeRs-nOwAyYyYY}`

## References

- [binvis.io by Aldo Cortesi](https://binvis.io/)
- [Photopea Photo Editor](https://www.photopea.com/)
- [Stock Image from Lorem Picsum](https://picsum.photos/id/29/4000/2670)
- [Singing man pixel art](https://www.pinterest.com/pin/alpha-pattern-144262--525724956515816897/)
- [img2binvis](https://github.com/FieryRMS/img2binvis) - This tool will be made public after the competition ends.
