<?php
$solver = $_GET["solverDir"];
chdir("../../json_math_tests/generated/$selectedGroup");
$solverDirs = array_reverse(scandir('.', SCANDIR_SORT_DESCENDING));
$solverTypes = [];
for ($solverDirs as $dir_name) {
  exec("python getSolverType.py $dir_name", $solverTypes);
}
echo json_encode($solverTypes);
?>
