<?php
function get_recent_generated_group() {
  $generatedGroups = scandir("../json_math_tests/generated", SCANDIR_SORT_DESCENDING);
  return (count($generatedGroups) > 2) ? $generatedGroups[0] : False;
}
function get_recent_generated_group_tests() {
  $recentGroup = get_recent_generated_group();
  $recentGroupTests = scandir("../json_math_tests/generated/$recentGroup", SCANDIR_SORT_ASCENDING);
  return $recentGroupTests;
}
function get_recent_generated_group_test_item_count() {
  $recentGroup = get_recent_generated_group();
  $testItemCount = 0;
  if ($recentGroup) {
    $solverDirs = scandir("../json_math_tests/generated/$recentGroup", SCANDIR_SORT_DESCENDING);
    foreach ($solverDirs as $dir_name) {
      $fileRead = file_get_contents("../json_math_tests/generated/$recentGroup/$dir_name/$dir_name.json");
      $fileData = json_decode($fileRead, true);
      $testItemCount += count($fileData['tests']);
    }
  }
  return $testItemCount;
}
function get_generated_group_test_item_count($group_dir) {
  chdir("../../json_math_tests/generated/$group_dir");
  $testItemCount = 0;
  $solverDirs = scandir('.', SCANDIR_SORT_DESCENDING);
  foreach ($solverDirs as $dir_name) {
    $fileRead = file_get_contents("./$dir_name/$dir_name.json");
    $fileData = json_decode($fileRead, true);
    $testItemCount += count($fileData['tests']);
  }
  return $testItemCount;
}
function get_generated_group_tests($group_dir) {
  chdir("../../json_math_tests/generated/$group_dir");
  $tests = [];
  $solverDirs = scandir('.', SCANDIR_SORT_DESCENDING);
  // foreach ($solverDirs as $dir_name) {
  //   array_push($tests, $dir_name);
  // }
  // return $tests;
  return $solverDirs;
}
function get_all_manual_tests() {
  return scandir("../json_math_tests/manual", SCANDIR_SORT_ASCENDING);
}
function get_all_generated_groups() {
  return scandir("../json_math_tests/generated", SCANDIR_SORT_ASCENDING);
}













?>
