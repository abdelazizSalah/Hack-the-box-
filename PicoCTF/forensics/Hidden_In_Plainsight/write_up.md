- First thing to do always is to read the meta data of the given image or file. 
    > exiftool img.jpg
- You will find a comment looks wierd, take it, and use cyberchef to decode it using from base64
- You will see steghide:cEF5evdvmqE=
- this suggests two things:
    - first, they use a tool called steghide, to hide data within the image. 
    - second, there is still encoded text cEF5evdvmqE=
- so decode the text, you will get : pAzzword
- then try to use steghide to extract the hidden data
    > steghide extract -sf your_image.jpg
- it will ask you for a passphrase, and you can know that it will be pAzzword
- then it will write the flag in flag.txt file, you can submit it: picoCTF{h1dd3n_1n_1m4g3_871ba555}
