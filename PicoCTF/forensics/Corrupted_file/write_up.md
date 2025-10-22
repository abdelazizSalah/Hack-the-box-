- any file should have a type, and usually each type has specific header. 
    > xxd -l 64 file # to check the header
- So, here we can just check the header of the file, and then we will see that it has 5c78 ffe0. 
- This is similar to the jpg header which is: ffd8 ffe0
- so, what we can do, is to modify the first 2 bytes to be ffd8 using this command: 
    > printf '\xFF\xD8' | dd of=file bs=1 count=2 conv=notrunc
- then convert the extension of the file to .jpg, and you will manage to see the flag
    > picoCTF{r3st0r1ng_th3_by73s_752d2c00}
