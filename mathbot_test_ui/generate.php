<!DOCTYPE html>

<html>
  <head lang="en">
    <?php require("head.php"); ?>
  </head>

  <body>
    <?php include("navbar.php"); ?>
    <h1>Generate group</h1>

    <button id="generate_group_btn" onclick="createGeneratedGroup()">
      Generate new
    </button>

    <button type="button" id="recent_group_info">
      <span class="material-symbols-outlined">keyboard_double_arrow_down</span>
      <div id="recent_group_info_text">
        <?php
          $recentGroup = get_recent_generated_group();
          if ($recentGroup) {
            $recentGroupDate = explode(' ', $recentGroup)[0];
            $recentGroupTime = explode(' ', $recentGroup)[1];
            $recentGroupTestItemCount = get_recent_generated_group_test_item_count();
            echo "Last generation on $recentGroupDate at $recentGroupTime <br/>
                  Generated $recentGroupTestItemCount tests";
          } else {
            echo "No generated groups exist";
          }
        ?>
      </div>
      <span class="material-symbols-outlined">keyboard_double_arrow_down</span>
    </button>

    <div id="group_display_container">
      <div id="group_display">
        <?php
          $recentGeneratedTests = array_slice(get_recent_generated_group_tests(), 2);
          if ($recentGeneratedTests) {
            foreach($recentGeneratedTests as $testName): ?>
              <span><?= $testName; ?></span>
            <?php endforeach;
          }
        ?>
      </div>
    </div>

    <script type="text/javascript">
      $('#recent_group_info').click(function() {
        var groupDisplayContainer = $(this).next();
        groupDisplayContainer.css("display", (groupDisplayContainer.css("display") === "block") ? "none" : "block");
      });

      function createGeneratedGroup() {
        $.post("php_scripts/create_generated_group.php", () => location.reload());
      }
    </script>
  </body>
</html>
