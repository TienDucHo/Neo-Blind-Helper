<?php
include 'simple_html_dom.php';

$lnk = $_POST["link"];
$homepage = file_get_contents($lnk);
//echo $homepage;
//$st = strpos($homepage, "<title>");
//$en = strpos($homepage, "</title>");
//$tt = substr($homepage, $st + 7, $en - $st - 7);
//echo $tt;
$html = file_get_html($lnk);
$doc = new DOMDocument();
libxml_use_internal_errors(true);
$doc->loadHTML($homepage);
libxml_use_internal_errors(false);
//for title

foreach($html->find('h1') as $node) {
    echo (($node->plaintext)); 
} 
echo '<br>';
//for content

foreach($html->find('p.Normal') as $norm)
{
	if (!($norm->find('strong'))) 
	{
		echo (($norm->plaintext)); 
		echo '<br>';
	}
}
?>
