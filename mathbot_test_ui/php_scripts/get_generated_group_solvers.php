<?php
$selectedGroup = $_POST["reqSelectedGroup"];
chdir("../../json_math_tests/generated/$selectedGroup");
$solverDirs = array_reverse(scandir('.', SCANDIR_SORT_DESCENDING));
echo json_encode($solverDirs);
?>
