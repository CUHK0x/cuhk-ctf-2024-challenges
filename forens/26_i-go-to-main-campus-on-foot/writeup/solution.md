## [forens] I go to main campus on foot

For this challenge, I embedded another JPG file in the given PNG file using OpenStego with a password.
![](sample1.png)

The password is hide in the metadata, "Author" tag.<br>
![](sample2.png)

After extraction, you should get Night_of_university_mall.JPG
![](Night_of_university_mall.jpg)

Open it in a Hex editor(I use HexEd.it), scroll down.
You should see some number at the end.
![](sample3.png)

Put the number in Hex to ASCII converter
![](sample4.png)

flag: cuhk24ctf{Main_CamPus_@9}

