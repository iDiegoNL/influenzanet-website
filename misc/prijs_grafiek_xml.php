<?

session_start();

require_once('../includes/config.php');
require_once('../includes/contentbasis.php');

$today=date("Y-m-d");
// session ----------------------


// wie is deze meter, is ie ingelogd.
include ('../includes/check_login_inc.php');

$begindatum="2010-11-01";
$einddatum="2011-05-01";
$interval=7;


$sql="SELECT 
datum,
klacht,
aantal,
percentage
FROM 
prijsvraag_grafiek
ORDER by datum";
$result = mmmcms_q($sql);
if (mysql_num_rows($result)>0) {

	while ($row = mysql_fetch_object($result)) {
		$datum[]=$row->datum;
		$klacht[]=$row->klacht;
		$percentage[]=$row->percentage;
	}
}


// begin xml
print "<grafiekinput>";
print "<meter_id>".$meter_id."</meter_id>";
print "<naam>".$_SESSION['naam']."</naam>";

if (ereg ("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", $begindatum, $regs)) {
	$fjaar=intval($regs[1]);
	$fmaand=intval($regs[2]);
	$fdag=intval($regs[3]);
}
if (ereg ("([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})", $einddatum, $regs)) {
	$eijaar=intval($regs[1]);
	$eifmaand=intval($regs[2]);
	$eifdag=intval($regs[3]);
}
$days=(int)((mktime(0,0,0,$eifmaand,$eifdag,$eijaar)-mktime(0,0,0,$month,$day,$year))/86400);

$weeknr=1;
for ($i=0;$i<$days;$i++) {	
		$dy=date("Y-m-d", mktime(0,0,0,$fmaand,$fdag+$i,$fjaar));	
		for ($ti=0;$ti<count($datum);$ti++) {
			if ($datum[$ti]==$dy) { 
					if ($klacht[$ti]=="griep") {
	
						print "<week nr=\"".$weeknr."\">".$percentage[$ti]."</week>";

						$totperc_griep=$totperc_griep+$percentage[$ti];
						$a_griep++;
						$weeknr++;
					}	
			}
		}
}	
print "</grafiekinput>";
// eind xml

mysql_free_result($result);
?>
