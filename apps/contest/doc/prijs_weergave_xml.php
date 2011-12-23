<?
session_start();

require_once('../includes/config.php');
require_once('../includes/contentbasis.php');

$today=date("Y-m-d");


// wie is deze meter, is ie ingelogd.
include ('../includes/check_login_inc.php');

// zie ook tijdlijn_pagina.php
// ------------------------------------------------------------------------------


// begin xml
print "<voorspelling>\n";
print "<meter_id>".$meter_id."</meter_id>\n";
print "<naam>".$_SESSION['naam']."</naam>\n";

$sql="SELECT 
*
FROM 
prijsvraag WHERE meter_id=".$meter_id;
$result = mmmcms_q($sql);
if (mysql_num_rows($result)>0) {

	while ($row = mysql_fetch_object($result)) {
		print "<datum>".$row->datum."</datum>\n";

				
		print "<week nr=\"1\">".$row->week1."</week>\n";
		print "<week nr=\"2\">".$row->week2."</week>\n";
		print "<week nr=\"3\">".$row->week3."</week>\n";		
		print "<week nr=\"4\">".$row->week4."</week>\n";
		print "<week nr=\"5\">".$row->week5."</week>\n";				
		print "<week nr=\"6\">".$row->week6."</week>\n";
		print "<week nr=\"7\">".$row->week7."</week>\n";				
		print "<week nr=\"8\">".$row->week8."</week>\n";
		print "<week nr=\"9\">".$row->week9."</week>\n";			
		print "<week nr=\"10\">".$row->week10."</week>\n";
		print "<week nr=\"11\">".$row->week11."</week>\n";			
		print "<week nr=\"12\">".$row->week12."</week>\n";
		print "<week nr=\"13\">".$row->week13."</week>\n";		
		print "<week nr=\"14\">".$row->week14."</week>\n";
		print "<week nr=\"15\">".$row->week15."</week>\n";		
		print "<week nr=\"16\">".$row->week16."</week>\n";
		print "<week nr=\"17\">".$row->week17."</week>\n";		
		print "<week nr=\"18\">".$row->week18."</week>\n";
		print "<week nr=\"19\">".$row->week19."</week>\n";		
		print "<week nr=\"20\">".$row->week20."</week>\n";
		print "<week nr=\"21\">".$row->week21."</week>";		
		print "<week nr=\"22\">".$row->week22."</week>";
		print "<week nr=\"23\">".$row->week23."</week>";
		print "<week nr=\"24\">".$row->week24."</week>\n";		
		print "<week nr=\"25\">".$row->week25."</week>\n";
		print "<week nr=\"26\">".$row->week26."</week>\n";		
		print "<week nr=\"27\">".$row->week27."</week>\n";
		print "<week nr=\"28\">".$row->week28."</week>\n";		
		print "<week nr=\"29\">".$row->week29."</week>\n";
		print "<week nr=\"30\">".$row->week30."</week>";		
		print "<week nr=\"31\">".$row->week31."</week>\n";
		//print "<week nr=\"32\">".$row->week32."</week>\n";		
		//print "<week nr=\"33\">".$row->week33."</week>\n";

		
		
		
		
		
		
	}
}

print "</voorspelling>\n";

mysql_free_result($result);
?>