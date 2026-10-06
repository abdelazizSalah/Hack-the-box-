- Examining the file property
    > file disko-3.d
    > fdisk -l disko-2.dd
    - fdisk is a disk partitioning tool, allows us to view, create, delete or modify disk partition on storage devices.
    - with -l, it lists to you all available partitions.
    - since the problem mentioned that we need to target the linux, so we should focus on the first partition. 
- Extracting the partition into .img format
- > sudo mkdir /mnt/part2
- > sudo mount -o loop disko-3.dd /mnt/part2
- > cd /mnt/part2
- you will find a log folder
- go inside it, and list all files.
- you will find a file called flag.gz
- unzip it
- > gzip -d flag.gz
- cat the flag
- picoCTF{n3v3r_z1p_2_h1d3_26d4f233}