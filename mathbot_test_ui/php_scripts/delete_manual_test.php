<?php
$testName = $_POST['reqTestName'];
array_map('unlink', glob("../../json_math_tests/manual/$testName/*"));
rmdir("../../json_math_tests/manual/$testName");
?>
