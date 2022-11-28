<?php 


shell_exec(escapeshellcmd('env/Scrips/activate'));
$command = escapeshellcmd('lector.py');
$output = shell_exec($command);
echo $output;
header('Location: display.php')

?>