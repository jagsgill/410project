<html>
<head></head>
<body>
Result for: <?php echo $_POST["url"] . "<br>";?>
<?php
$command = escapeshellcmd('./env/bin/python ./main.py auto' . ' ' . $_POST["url"]);
$output = shell_exec($command);
echo "<pre>$output</pre>";
?>
</body>
</html>
