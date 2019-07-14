<?php
include 'simple_html_dom.php';
include 'text_to_speech.php';
//file get link tu trang chu
$lnk = $_POST["link"];
$html = file_get_html($lnk);
$id = 0;

foreach($html->find('h1.title_news') as $title)
{
	$href = $title->find('a');
	echo $href[0]->href;
	echo '<br>';
	//khúc này để bỏ cái &nbsp ra khỏi text
	$my_str = $title -> plaintext;
	$my_str = htmlentities($my_str);
    $converted = strtr($my_str, array_flip(get_html_translation_table(HTML_ENTITIES, ENT_QUOTES))); 
	trim($converted, chr(0xC2).chr(0xA0));
	echo $converted;
	get_mp3($converted,'title/title'.$id);
	$id = $id + 1; 
	echo '<br>';
}

foreach($html->find('h4.title_news') as $title)
{
	$href = $title->find('a');
	echo $href[0]->href;
	echo '<br>';
	//echo $title -> plaintext;
	$my_str = $title -> plaintext;
	$my_str = htmlentities($my_str);
	$converted = strtr($my_str, array_flip(get_html_translation_table(HTML_ENTITIES, ENT_QUOTES))); 
	trim($converted, chr(0xC2).chr(0xA0));
	echo $converted;
	get_mp3($converted,'title/title'.$id);
	$id = $id + 1;
	echo '<br>';
}

?>
