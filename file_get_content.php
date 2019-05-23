<?php
include 'simple_html_dom.php';

$lnk = $_POST["link"];
$homepage = file_get_contents($lnk);
//echo $homepage;
//$st = strpos($homepage, "<title>");
//$en = strpos($homepage, "</title>");
//$tt = substr($homepage, $st + 7, $en - $st - 7);
//echo $tt;
$doc = new DOMDocument();
libxml_use_internal_errors(true);
$doc->loadHTML($homepage);
libxml_use_internal_errors(false);
//for title
$result = $doc->getElementsByTagName('h1');

foreach($result as $node) {
    echo (utf8_decode($node->nodeValue)); 
} 
echo '<br>';
//for content
$html = file_get_html($lnk);

foreach($html->find('p.Normal') as $norm)
{
	if (!($norm->find('strong'))) 
	{
		echo (($norm->plaintext)); 
		echo '<br>';
	}
}
?>