<?php 
echo isset($_POST['submit']);
if(isset($_POST['submit'])){
 
    // Count total files
    $countfiles = count($_FILES['formFileMultiple']['name']);

    // Looping all files
    for($i=0;$i<$countfiles;$i++){
        $filename = $_FILES['formFileMultiple']['name'][$i];
 
        // Upload file
        
        if (!file_exists('../files/por_procesar/' . $filename)){
            
            move_uploaded_file($_FILES['formFileMultiple']['tmp_name'][$i],'../files/por_procesar/'.$filename);
        }
        
 
    }
    header('Location: ../exec.php');
} 
?>