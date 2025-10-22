- First we need to ensure that this is a correct zipping format:
    > file disko-1.dd.gz
- we should see something like gzip compressed data was "disko-1.dd"
- then we should unzip it using this command: 
    > gzip -d disko-1.dd.gz
- then we should check the file version and details of it
    > file disko-1.dd
- then we can use the strings to read all the strings inside the disk
    > strings disko-1.dd | grep pico
- then we can submit the flag :)
    > picoCTF{1t5_ju5t_4_5tr1n9_be6031da}