- Always start by opening the image, and check it.
- If you found nothing, then go and check its meta data. 
    > exiftool red.png
- you will find a poem like this: 
    Crimson heart, vibrant and bold,.
    Hearts flutter at your sight..
    Evenings glow softly red,.
    Cherries burst with sweet life..
    Kisses linger with your warmth..
    Love deep as merlot..
    Scarlet leaves falling softly,.Bold in every stroke.
- So checking the capital letters we can see: Check LSB. 
- We should use a tool called zsteg is specifically made to detect LSB steganography in .png and .bmp files
- then you should use this command:
    > zsteg red.png
- you will find this base64 encoded text, go to cyberchef, and decode it, and you will get this key :)

- picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}