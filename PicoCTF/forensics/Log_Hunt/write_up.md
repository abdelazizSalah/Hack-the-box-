- All you need to do is to use awk along with filters to be able to find the parts of the flag. 
- When you open the log,you will see that there are flag info marked as INFO FLAGPART: 

- So we can use the awk to search for all entries with such start, and collect the flag

``` bash
 awk '/INFO FLAGPART/ {print $5 }' server.log | uniq   

output: 

picoCTF{us3_
y0urlinux_
sk1lls_
cedfa5fb}

```