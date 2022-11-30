<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <table>
        <tr>
            <th>Separacion</th>
            <th>Codigo</th>
            <th>Asociado</th>
            <th>Rut</th>
            <th>Glosa</th>
            <th>Valor</th>
            <th>Mes</th>
            <th>x/y</th>
            <th>Pagina</th>
        </tr>
        <?php
        $dir = 'files/procesado/';

        $processed = scandir($dir);
        //[0] -> file 0 | [] ->  page 0
        foreach ($processed as $folder) {
            if ($folder != '.' && $folder != '..') {
                $retrieved = json_decode(file_get_contents($dir . $folder));

                foreach ($retrieved as $page) {
                    foreach ($page as $line) {
                        echo $line[1] . '<br>';
                        if ($line[0] == 'Mensual') {


        ?>
                            <tr>
                                <td><?php echo $line[0] ?></th>
                                <td><?php echo $line[1] ?></th>
                                <td><?php echo $line[2] ?></th>
                                <td><?php echo $line[3] ?></th>
                                <td><?php echo $line[4] ?></th>
                                <td><?php echo $line[5] ?></th>
                                <td><?php echo $line[6] ?></th>
                                <td><?php echo $line[7] ?></th>
                                <td><?php echo $line[8] ?></th>

                            </tr>
        <?php
                        }else {
                            ?>
                                <tr>
                                <td><?php echo $line[0] ?></th>
                                <td><?php echo $line[1] ?></th>
                                <td><?php echo $line[2] ?></th>
                                <td><?php echo $line[3] ?></th>
                                <td><?php echo $line[4] ?></th>
                                <td><?php echo $line[5] ?></th>
                                <td><?php echo $line[6] ?></th>

                            </tr>
                            <?php
                        }
                    }
                }
            }
        }


        ?>
    </table>
</body>

</html>