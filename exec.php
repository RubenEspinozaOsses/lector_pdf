<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <div class="loader-1 center"><span>
            <?php


            shell_exec(escapeshellcmd('env/Scripts/activate'));
            $command = escapeshellcmd('python lector.py');
            $output = shell_exec($command);
            echo $output;
            header('refresh:1, url=display.php')

            ?>
        </span></div>
</body>

</html>