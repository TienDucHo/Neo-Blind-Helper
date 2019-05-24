<?php
include 'simple_html_dom.php';

$lnk = $_POST["link"];
$html = file_get_html($lnk);

foreach($html->find('h1.title_news') as $title)
{
	$href = $title->find('a');
	echo $href[0]->href;
	echo '<br>';
	echo $title -> plaintext;
	echo '<br>';
}

foreach($html->find('h4.title_news') as $title)
{
	$href = $title->find('a');
	echo $href[0]->href;
	echo '<br>';
	echo $title -> plaintext;
	echo '<br>';
}

?>