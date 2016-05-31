<html>
<head></head>
<body>
Processing repo at <?php echo $_POST["url"] . "<br>";?>
<?php
$command = escapeshellcmd('./env/bin/python ./main.py auto' . ' ' . $_POST["url"]);
$output = shell_exec($command);
echo "<pre>$output</pre>";
?>
<!-- Progress bar holder -->
<div id="progress" style="width:500px;border:1px solid #ccc;"></div>
<!-- Progress information -->
<div id="information" style="width"></div>

<!-- Progress bar code from http://w3shaman.com/article/php-progress-bar-script -->
<?php
$script = './env/bin/python ./main.py ';
$cmd = array('getRepo ' . $_POST["url"],
             'GenerateJSON',
             'GenerateGraph');
$progress_top = array('Downloading repo ... ',
                      'Analyzing ... ',
                      'Loading animation ... ');
// Total processes
$total = 3;
// Loop through process
for($i=0; $i<$total; $i++){
    echo $progress_top[$i];
    #echo $script . $cmd[$i] . "<br>";
    // Calculate the percentation
    $percent = intval(($i+1)/$total * 100)."%";
    
    echo '<script language="javascript">
    document.getElementById("progress").innerHTML="<div style=\"width:'.$percent.';background-color:#ddd;\">&nbsp;</div>";
    document.getElementById("information").innerHTML="'.$percent.'";
    </script>';
    

// This is for the buffer achieve the minimum size in order to flush data
    echo str_repeat(' ',1024*64);
    

// Send output to browser immediately
    flush();
    

// Sleep one second so we can see the delay
    sleep(1);
        
    echo "done <br>";
}
// Tell user that the process is completed
echo '<script language="javascript">document.getElementById("information").innerHTML="*** Process completed ***"</script>';
?>
</body>
</html>
