## [forens] Secret Menu

Usually, you can find some header information at the beginning of the file

1. SOI (Start of Image): <br>
    Hex: FF D8 <br>
    This marker indicates the beginning of the JPEG file. <br>

2. APP0 (Application Segment):<br>
    Typically follows SOI and contains metadata about the image.<br>
    Hex: FF E0 (for APP0)<br>
    This segment can contain information such as the JFIF (JPEG File Interchange Format) version, density, and thumbnail data.<br>

3. DQT (Define Quantization Table):<br>
    Hex: FF DB<br>
    This segment defines the quantization tables used for compressing the image. It specifies how the image's colors are quantized.<br>

4. SOF0 (Start of Frame - Baseline DCT):<br>
    Hex: FF C0<br>
    This segment describes the image dimensions and color components (like YCbCr) used.<br>

5. DHT (Define Huffman Table):<br>
    Hex: FF C4<br>
    This segment contains the Huffman tables used for encoding the image data.<br>

6. SOS (Start of Scan):<br>
    Hex: FF DA<br>
    Marks the beginning of the image data (the actual compressed pixel data).<br>

10. EOI (End of Image)(Usually at the end of the file):<br>
    Hex: FF D9<br>
    This marker indicates the end of the image file<br>

You can see that the plate under the burger looks weird, seem like chopped.<br>
![](sample1.jpg)That indicate you to think of is the Height of the image get changed?

Put the secret_menu.jpg in a hex editer(hexed.it used here)
![](sample2.png)
You will find that no SOF0(FF CO) found. Instead, you find FF C2<br>
![](sample3.png)
Actually it also represent SOF but it is SOF2

Structure of SOF2
1. Marker:

    Value: FF C2<br>
    This indicates that the following data pertains to the SOF2 segment.

2. Length:

    Size: 2 bytes<br>
    This field specifies the total length of the SOF2 segment, excluding the marker itself.

3. Precision:

    Size: 1 byte<br>
    This field indicates the number of bits per sample, usually set to 08 for 8 bits per channel.

4. Height:

    Size: 2 bytes<br>
    This field specifies the height of the image in pixels.

5. Width:

    Size: 2 bytes<br>
    This field specifies the width of the image in pixels.

In this challenge, we have 04 57 04 74 as our height and width
![](sample4.png)
04 57 is the height <br>
04 74 is the width


Increase the height and the flag will come out
![](secret_menu_original.jpg)

flag: cuhk24ctf{Is_Hoi_Luk_Hung_Bou}
