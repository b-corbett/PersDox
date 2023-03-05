<!DOCTYPE html>

<html>
  <head lang="en">
    <?php require("head.php"); ?>
  </head>

  <body>
    <?php include("navbar.php"); ?>
    <h1>Manual tests</h1>

    <!-- BE ABLE TO ADD A SOLVER IN THE INPUTS TO MAKE A SORT OF MANUAL TESTING SUITE CREATED AT ONCE -->
    <div id="manual_page_content">
      <form id="manual_test_form" action="manual.php" method="post">
        <div id="solver_input">
          <label>Solver name:</label>
          <input type="text" id="solver_name" autocomplete="off" />
        </div>

        <div id="test_item_input_titles">
          <span>Question:</span>
          <span>Expected:</span>
        </div>

        <div id="test_item_input_container">
          <div class="test_item_input_field">
            <textarea name="question1" form="manual_test_form" rows="1"></textarea>
            <textarea name="expected1" form="manual_test_form" rows="1"></textarea>
          </div>
        </div>

        <div id="test_item_form_control">
          <button type="button" onclick="addTestInput()">Add test item</button>
          <button type="button" onclick="addManualTest()">Add solver test to suite</button>
        </div>
      </form>

      <div id="manual_tests_display">
        <?php
          $manualTests = array_slice(get_all_manual_tests(), 2);
          foreach($manualTests as $testName):
            $parsedTestName = explode(' ', $testName);
            $solver = $parsedTestName[0];
            $createDate = $parsedTestName[1];
            $createTime = $parsedTestName[2]; ?>
            <div class="test_display_card">
              <button type="button" class="dlt_card_btn" onclick="deleteManualTest('<?= $testName ?>')">Delete</button>
              <p>
                <span class="prefix">test for </span>
                <span class="data"><?= $solver ?></span>
              </p>
              <p>
                <span class="prefix">created on </span>
                <span class="data"><?= $createDate; ?></span>
                <span class="prefix"> at </span>
                <span class="data"><?= $createTime; ?></span>
              </p>
            </div>
          <?php endforeach;
        ?>
      </div>
    </div>

    <script type="text/javascript">
      function addManualTest() {
        let testPairs = [];
        $("#test_item_input_container").children().each(function() {
          let question = $(this).children()[0].value;
          let expected = $(this).children()[1].value;
          testPairs.push([question, expected]);
        });
        let solver = $("#solver_name").val();
        let requestData = {reqSolver: solver, reqTestPairs: JSON.stringify(testPairs)};
        $.post("php_scripts/create_manual_solver_test.php", requestData, () => {
          $('textarea').val('');
          location.reload();
        });
      }

      function deleteManualTest(test_name) {
        let requestData = {reqTestName: test_name};
        $.post("php_scripts/delete_manual_test.php", requestData, () => location.reload())
      }

      let i = 2;
      function addTestInput() {
        let newQuestionTextarea = $("<textarea></textarea>").attr({
          name: `question${i}`,
          form: 'manual_test_form',
          rows: '1'
        });
        let newExpectedTextarea = $("<textarea></textarea>").attr({
          name: `expected${i}`,
          form: 'manual_test_form',
          rows: '1'
        });
        let newInputFieldDiv = $("<div></div>").addClass("test_item_input_field").append(newQuestionTextarea, newExpectedTextarea);
        $("#test_item_input_container").append(newInputFieldDiv);
        newQuestionTextarea.focus();
      }
    </script>
  </body>
</html>
