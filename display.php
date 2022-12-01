<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carpetas tributarias</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.6.3/css/all.min.css" />
    <link rel="stylesheet" href="style/display.css">
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="background-color: #170963 !important">
        <div class="container-fluid">
            <a class="navbar-brand" style="color: white !important;" href="#">Carpetas Tributarias</a>
            <div class="container-fluid">
                <form class="d-flex">
                    <input id="search" class="form-control me-2" type="search" placeholder="Search" aria-label="Search" onkeyup="buscar()">
                </form>
            </div>

        </div>
    </nav>
    <div class="container">
        <div class="card">
            <div class="card-title text-center">Mensual</div>
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
                $mensual = array();
                $anual = array();
                foreach ($processed as $folder) {
                    if ($folder != '.' && $folder != '..') {
                        $retrieved = json_decode(file_get_contents($dir . $folder));

                        foreach ($retrieved as $page) {
                            foreach ($page as $line) {
                                if ($line[0] == 'MENSUAL') {
                                    $mensual[] = $line;
                                } else {
                                    $anual[] = $line;
                                }
                            }
                        }
                    }
                }

                foreach ($mensual as $line) {
                ?>
                    <tbody>
                        <tr>
                            <td>
                                <?php echo $line[0] ?>
                            </td>
                            <td>
                                <?php echo $line[1] ?>
                            </td>
                            <td>
                                <?php echo $line[2] ?>
                            </td>
                            <td>
                                <?php echo $line[3] ?>
                            </td>
                            <td>
                                <?php echo $line[4] ?>
                            </td>
                            <td>
                                <?php echo $line[5] ?>
                            </td>
                            <td>
                                <?php echo $line[6] ?>
                            </td>
                            <td>
                                <?php echo $line[7] ?>
                            </td>
                            <td>
                                <?php echo $line[8] ?>
                            </td>
                        </tr>
                    </tbody>
                <?php
                }


                ?>
            </table>
        </div>

        <div class="container">
            <div class="card">
                <div class="card-title text-center">
                    Anual
                </div>
                <table>
                    <tr>
                        <th>Separacion</th>
                        <th>Linea</th>
                        <th>Nombre</th>
                        <th>Rut</th>
                        <th>Año</th>
                        <th>Quota</th>
                        <th>Pagina en doc</th>
                    </tr>
                    <?php
                    foreach ($anual as $line) {
                    ?>
                        <tbody>
                            <tr>
                                <td>
                                    <?php echo $line[0] ?>
                                </td>
                                <td>
                                    <?php echo $line[1] ?>
                                </td>
                                <td>
                                    <?php echo $line[2] ?>
                                </td>
                                <td>
                                    <?php echo $line[3] ?>
                                </td>
                                <td>
                                    <?php echo $line[4] ?>
                                </td>
                                <td>
                                    <?php echo $line[5] ?>
                                </td>
                                <td>
                                    <?php echo $line[6] ?>
                                </td>
                            </tr>
                        </tbody>
                    <?php

                    }
                    ?>
                </table>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <script src="js/home.js" type="text/javascript"></script>
</body>

</html>