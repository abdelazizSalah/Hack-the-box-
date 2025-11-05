## Identify partitions and Bitlocker volum 
- file bitlocker.dd
- You will get this output:
    -                    
┌──(kali㉿kali)-[~/…/Hack-the-box-/PicoCTF/forensics/Bitlocker-1]
└─$ file bitlocker-1.dd 
bitlocker-1.dd: DOS/MBR boot sector, code offset 0x58+2, OEM-ID "-FVE-FS-", sectors/cluster 8, reserved sectors 0, Media descriptor 0xf8, sectors/track 63, heads 255, hidden sectors 124499968, FAT (32 bit), sectors/FAT 8160, serial number 0, unlabeled; NTFS, sectors/track 63, physical drive 0x1fe0, $MFT start cluster 393217, serial number 02020454d414e204f, checksum 0x41462020
                                        

- This means that you have filesystem is FVE (BitLocker) encrypted.
- Also we have 124499968 hidden sectors

- 
# compute & export offset (you already have 124499968)
OFFSET=$((124499968 * 512))   # -> 63743983616

# create a loop device for the partition (read-only)
sudo losetup --read-only --find --show --offset $OFFSET bitlocker-1.dd
# note the device printed (e.g. /dev/loop0)


# extract crackable hash
sudo bitlocker2john /dev/loop0 > bl.hash


# crack with John or hashcat (example John + rockyou)
john --wordlist=/usr/share/wordlists/rockyou.txt bl.hash
john --show bl.hash

# once you recover PASSWORD, unlock with dislocker and mount decrypted NTFS
sudo mkdir -p /mnt/bitlk /mnt/dec
sudo dislocker -V /dev/loop0 -u"RECOVERED_PASSWORD" -- /mnt/bitlk
sudo mount -o ro,loop /mnt/bitlk/dislocker-file /mnt/dec

# search for flag
grep -R "picoCTF\|flag" -n /mnt/dec 2>/dev/null