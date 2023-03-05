<!DOCTYPE html>

<!-- https://www.google.com/search?channel=fs&client=ubuntu&q=start+sessions+and+cookies+in+php
          this link is for sessions & cookies, need these for persisting values,
            use session to see what select option is currently selected in the table
            dropdown and if changes will update the table-->

<!-- made py_scripts folder for python scripts so rearrange next time -->

<html>
  <head lang="en">
    <?php require("head.php") ?>
  </head>

  <body>
    <?php include("navbar.php");?>
    <h1>Navigate tests</h1>

    <label for="table_group_select">Suite:
      <select id="table_group_select" name="table_group_select">
        <?php
          $generatedGroups = array_reverse(array_slice(get_all_generated_groups(), 2));
          foreach ($generatedGroups as $group):
            if (array_search($group, $generatedGroups) == 0): ?>
              <option selected><?= $group; ?></option>
            <?php else: ?>
              <option><?= $group; ?></option>
            <?php endif;
          endforeach;
        ?>
      </select>
    </label>

    <table id="suite_table">
      <thead>
        <tr>
          <th>Solver</th>
          <th>Type</th>
          <th>Test</th>
          <th>Expected</th>
          <th>Actual</th>
          <th>JSON</th>
        </tr>
      </thead>
      <tbody>

      </tbody>
    </table>

    <script type="text/javascript">
      $(document).ready(function() { changeDisplayedGroup(); });

      $("#table_group_select").change(function() { changeDisplayedGroup(); });

      function changeDisplayedGroup() {
        let selectedGroup = $("#table_group_select").children(":selected").val();
        let requestData = {reqSelectedGroup: selectedGroup};
        $.post("php_scripts/get_generated_group_solvers.php", requestData, (data) => {
          let selectedGroupTests = data.slice(2);
          console.log(selectedGroupTests);
          for (let groupTest of selectedGroupTests) {
            //
          }
        }, "json");
      }

      // $.ajax({
      //   url: `php_scripts/get_generated_group_test_types.php?solverDir=${selectedGroup}`,
      //   type: 'post',
      //   dataType: 'json',
      //   success: function(data) {
      //     $("#suite_table tbody").empty();
      //     selectedGroupTests.map(testName => {
      //       let solverTd   = $("<td></td>").text(testName);
      //       let typeTd     = $("<td></td>");
      //       let expectedTd = $("<td></td>");
      //       let actualTd   = $("<td></td>");
      //       let jsonTd     = $("<td></td>");
      //       let newRow     = $("<tr></tr>").append(solverTd, typeTd, expectedTd, actualTd, jsonTd);
      //       $("#suite_table tbody").append(newRow);
      //     });
      //   }
      // });

    </script>
  </body>
</html>
