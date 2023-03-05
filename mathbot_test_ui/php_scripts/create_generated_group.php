<?php
chdir("../..");
exec("python createGeneratedGroup.py");


/*



you can add a parameter to the url:

example:

function.php?g=1

now, on the serverside check for the get parameter:

if($_GET['g']==1)
{
    echo date();
}
else
{
    echo time();
}



*/
?>
