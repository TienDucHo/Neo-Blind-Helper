<?php
include 'simple_html_dom.php';
include 'text_to_speech.php';
//File get content cua bai bao.
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
	get_mp3($node->plaintext,'news');
} 
echo '<br>';
//for content
$id=0;
$part = 'part';

foreach($html->find('p.Normal') as $norm)
{
	if (!($norm->find('strong'))) 
	{
		echo (($norm->plaintext)); 
		$id = $id+1;
		get_mp3($norm->plaintext,$part.$id);
		
		echo '<br>';
	}
}
?>
