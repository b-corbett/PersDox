<?php
$solver = $_POST['reqSolver'];
$testPairs = $_POST['reqTestPairs'];
chdir("../..");
exec("python createManualSolverTest.py $solver '$testPairs'");
chdir("mathbot_test_ui/php_scripts");
?>
