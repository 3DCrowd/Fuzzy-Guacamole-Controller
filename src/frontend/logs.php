<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Fuzzy Guacamole Logs</title>
    <link rel="stylesheet" href="/css/styles.css">
    <link rel="stylesheet" href="/css/logs.css">
  </head>
  <body>
    <div class="head">
      <h2>Fuzzy Guacamole Dashboard</h2>
      <div class="settingsImg" onclick="document.getElementById('navigation').classList.toggle('hidden');">
        <img src="/img/settings.png" alt="">
      </div>

    </div>

    <div id="navigation" class="navigation hidden">
      <ul>
        <li><a href="/">Dashboard</a></li>
        <li><a href="/logs.php">Logs</a></li>
      </ul>
    </div>

    <div class="logs-wrapper">
      <div class="container log">
        <h2>printer.log</h2>
        <?php
          $printerLog = file_get_contents("/var/www/html/printer.log");
          $printerLog = explode("\n", $printerLog);

          for ($i = count($printerLog); $i > 0; $i--)  {
            echo $printerLog[$i] ."<br />";
          }
        ?>
      </div>
    </div>
  </body>
</html>
