# After I accidentally deleted my super secret stash, I panicked and went ahead to shrink my whole hard drive into a file with Doraemon's minifying torch. ~Hunting treasures with my overpowered forensics skill~
*You know what, I only typed this thing once in the Excel sheet, then I just copied and pasted my way through.*

## TL;DR
A `vhdx` virtual hard disk file that contains a bootable, minimal Alpine Linux distribution. The forensics targets, the *secret stash*, **was** placed in `/home/uwu/` directory, although somewhat irrelevent in the final solving process. The secret stash was `rm`ed from the file system.

## Key Points
1. Running `rm` does not actually delete the file to the hard drive, but rather the *pointer* that refers to the file (the `inode` on an `ext` filesystem). By scanning the contents on the drive it is possible to recover the contents of a file, if you are lucky. You will need raw access to a hard drive, instead of through a file system.
2. **Point 1** is basically it. 

## Solution
### Step 0: Preparing the filesystem
A `vhdx` file is given. We can first look at the disk structure, and then mount the file system to take a quick view of the filesystem. You can checkout the instructions [here](https://gist.github.com/allenyllee/0a4c02952bf695470860b27369bbb60d).
```
Disk /dev/nbd0: 127 GiB, 136365211648 bytes, 266338304 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: BB298484-82C2-4EFC-9ECD-8237895B7711

Device        Start       End   Sectors   Size Type
/dev/nbd0p1    2048   1050623   1048576   512M EFI System
/dev/nbd0p2 1050624   4751359   3700736   1.8G Linux swap
/dev/nbd0p3 4751360 266336255 261584896 124.7G Linux filesystem
```
Looks like a standard linux installation.

OR, if you are using Windows and had Hyper-V installed, you can simply create a machine that boot from this drive. No graphical user interface though, it's high time to learn to use the command line :)
Username & Password:
```
uwu;uwu
root;root
```

### Step 1: Digging in the files
The problem title suggested a *secret stash*, hinting that maybe we need to find some personal data. It maybe a good idea to look at `/home`:
(Assume that you mounted the filesystem at `/mnt/fs`)
```
/mnt/fs$ tree -a home
home
└── uwu
    └── .ash_history

1 directory, 1 file
```
`.*history` files are always cool, let's look at it:
```
/mnt/fs$ cat home/uwu/.ash_history
ls -l /mnt
ls -l /mnt/sdb2
mkdir -p Desktop Pictures/secrets
cp /mnt/*.xcf Desktop
cp /mnt/sdb2/*.xcf Desktop
cp /mnt/sdb2/*.jpg Pictures/secrets
cp funny.txt ~
cp /mnt/sdb2/funny.txt ~
vim funny.txt
vi funny.txt
```
There are `jpg`, `xcf` and `txt` files copied to the home directory. Let's take note of that.

### Step 2: Recovering files
We know that there *was* some files, yet there are nowhere to be seen. As hinted in the description, they should be `rm -rf *`ed away. You can try use `testdisk` (great tool btw), or look at the journal, but you probably won't have much luck. So we'll use brute force techniques, dig through the sea of data to find it. `photorec` does this job, it looks through the *sectors*[^1] for given file signatures and patterns to try and recover files.[^2]
```
$ sudo photorec /dev/nbd0p3
```
It takes quite long to dig through all 127 GiB, so let's limit the file types to speed it up:
```
PhotoRec 7.1, Data Recovery Utility, July 2019
Christophe GRENIER <grenier@cgsecurity.org>
https://www.cgsecurity.org

PhotoRec will try to locate the following files
    Previous
>[X] custom Own custom signatures
 ...
>[X] jpg  JPG picture
 [ ] jsonlz4 Mozilla bookmarks
 [ ] kdb  KeePassX
 [ ] kdbx KeePassX
    Next
Press s to disable all file families, b to save the settings
>[  Quit  ]
                              Return to main menu
```
After running `photorec` it should be able to recover the 9 `jpg` files (*the secret stash*) that was in the disk. Looking through the images we can get two-thirds of the flag: the first part in the bottom left in [an image of a puma](../src/Munster_SdKfz234_2_(dark1).jpg), and the second part in the bottom right in [an image of a T-10m](../src/T-10m-looks-cool.jpg). This is btw an eyesight check as well.
Combining we get:
```
cuhk24ctf{wh0_Said_my_SECret_sTasH
```
Still, the last part is missing. Remember the `xcf` file that was in the history?

Looking up on wikipedia, we find that the magic number for `xcf` files are `gimp xcf `. So maybe try searching for it? (*Yes, it basically just `strings` again.*)

```
$ sudo grep -b -o "gimp xcf" --text /dev/nbd0p3
218103808:gimp xcf
```

Let's skip to that part:
```
$ sudo dd if=/dev/nbd0p3 skip=218103808 bs=1 | less
```
Scrolling down a bit we can get the text object of the `xcf` project file:
```
</metadata>
^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@.<B9>^@^@^@^@^@^@<BB><B8>^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^@^D6^@^@^Aj^@^@^@^A^@^@^@^P_R_aNImE_GirLs}^@^@^@^@^B^@^@^@
^@^@^@^@^F^@^@^@^D^@^@^@<FF>^@^@^@!^@^@^@^D?<80>^@^@^@^@^@^H^@^@^@^D^@^@^@^A^@^@^@      ^@^@^@^D^@^@^@^@^@^@^@"^@^@^@^D^@^@^@^@^@^@^@^\^@^@^@^D^@^@^@^@^@^@^@
^@^@^@^D^@^@^@^@^@^@^@ ^@^@^@^D^@^@^@^@^@^@^@^K^@^@^@^D^@^@^@^@^@^@^@^L^@^@^@^D^@^@^@^@^@^@^@^M^@^@^@^D^@^@^@^@^@^@^@^O^@^@^@^H^@^@^G^G^@^@^F<81>^@^@^@^G^@^@^@^D^@^@^@^\^@^@^@%^@^@^@^D^@^@^@^@^@^@^@$^@^@^@^D<FF><FF><FF><FF>^@^@^@#^@^@^@^D<FF><FF><FF><FF>^@^@^@^T^@^@^@^D^@^@^@^C^@^@^@^Z^@^@^@^D^@^@^@^B^@^@^@^U^@^@^AZ^@^@^@^Pgimp-text-layer^@^@^@^@^A^@^@^A>(text "_R_aNImE_GirLs}")
(font "Noto Sans")
(font-size 62)
(font-size-unit pixels)
(antialias yes)
(language "en-hk")
(base-direction ltr)
(color (color-rgb 0.69019609689712524 0.64705884456634521 0.56862747669219971))
(justify left)
(box-mode fixed)
(box-width 1077)
(box-height 222)
(box-unit pixels)
(hinting yes)
```

Putting the three parts together we get the final flag:
```
cuhk24ctf{wh0_Said_my_SECret_sTasH_R_aNImE_GirLs}
```

## Notes
- When I add `xcf` as a custom file format for `photorec` some reason `photorec` cannot detect the `xcf` file, although `fidentify` returns the right output for an `xcf` file.

## Creation process
*Used Hyper-V*
1. Create a blank VM
2. Install Alpine Linux with `setup-alpine`
3. Reboot and mount a virtual hard disk with the challenge files
4. Copy the challenge files to the virtual hard disk.
5. `rm -rf *` in `~`
6. **Immediately** kill the machine. Do not power off, as it may cause the deleted files to be overwritten.

[^1]: idk if it's the right term
[^2]: Essentially a glorified `grep`
