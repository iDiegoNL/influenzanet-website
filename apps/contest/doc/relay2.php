<?
require_once('../includes/config.php');
require_once('../includes/contentbasis.php');
include_once("../vragen/phpxml/xml.php");

$today=date("Y-m-d");
$templatename="persoon_pag";
// session ----------------------
session_start();


// wie is deze meter, is ie ingelogd.
include ('../includes/check_login_inc.php');


// print_r($_POST);
/*
//$arr = get_defined_vars();
//print_r($arr["HTTP_POST_VARS"]);
//$myXMLString =($arr["HTTP_POST_VARS"]);
deze vars checken
    [meter_id] => 2
    [email] => takken@xs4all.nl
    [password] => henk
    [naam] => martin
*/


// checken of deze meter al heeft ingezonden
$sql="SELECT meter_id FROM prijsvraag WHERE meter_id=".$meter_id;
$result = mmmcms_q($sql);
$row = mysql_fetch_object($result);
if ($row->meter_id!="") {
	print "prijsvraag al ingediend";
	exit;
} else {


//deze variabelen opslaan
$sql="INSERT INTO 
	`prijsvraag` ( `prijsvraag_id` , `meter_id` , `datum` , `week1` , `week2` , `week3` , `week4` , `week5` , `week6` , `week7` , `week8` , `week9` , `week10` , 
	`week11` , `week12` , `week13` , `week14` , `week15` , `week16` , `week17` , `week18` , `week19` , `week20`, `week21`, `week22`, `week23` , `week24` , `week25` ,
	`week26` , `week27`, `week28`, `week29`, `week30`, `week31`) 
VALUES (
	'',
	'".$meter_id."', '".$today."', 
	'".$_POST['week1']."', '".$_POST['week2']."', '".$_POST['week3']."', '".$_POST['week4']."', '".$_POST['week5']."', 
	'".$_POST['week6']."', '".$_POST['week7']."', '".$_POST['week8']."', '".$_POST['week9']."', '".$_POST['week10']."', 
	'".$_POST['week11']."', '".$_POST['week12']."', '".$_POST['week13']."', '".$_POST['week14']."', '".$_POST['week15']."', 
	'".$_POST['week16']."', '".$_POST['week17']."', '".$_POST['week18']."', '".$_POST['week19']."', '".$_POST['week20']."', 
	'".$_POST['week21']."', '".$_POST['week22']."',	'".$_POST['week23']."', '".$_POST['week24']."', '".$_POST['week25']."', 
	'".$_POST['week26']."', '".$_POST['week27']."', '".$_POST['week28']."', '".$_POST['week29']."', '".$_POST['week30']."',
	'".$_POST['week31']."'
)";

//print $sql;
//exit;


$result = mmmcms_q($sql);
	//print "prijsvraag is ingediend";
	
	header ("Location: index.php\n\n");
}

?>