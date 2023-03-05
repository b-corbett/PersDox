<!DOCTYPE html>

<html>
  <head lang="en">
    <?php require("head.php") ?>
  </head>

  <body>
    <?php include("navbar.php");?>

    <h1>Run tests</h1>

    <form method="post">
      <input type="submit" name="run_tests" value="Run" />
    </form>

    <?php
      function runTests() {
        chdir("..");
        $handle = popen('python run_tests.py', 'r');
        $output = fread($handle, 1024);
        echo $output;
        pclose($handle);
        // exec("python run_tests.py");
        chdir("mathbot_test_ui");
      }

      if (isset($_POST['run_tests'])) {
        runTests();
      }
    ?>
  </body>
</html>
