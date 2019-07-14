<?php
function get_mp3($postdata, $file_name){
$api_key = '0bf528396c8146268c5eb01bf1f51bd8';
$voice = 'female';
$speed = 0;
$prosody = 1;

$postdata = str_replace('&nbsp;', '', $postdata);

$url = 'http://api.openfpt.vn/text2speech/v4?api_key='.$api_key.'&voice='.$voice.'&speed='.$speed.'&prosody='.$prosody;

//The data you want to send via POST
$fields = [$postdata];

//url-ify the data for the POST
$fields_string = http_build_query($fields);

//open connection
$ch = curl_init();

//set the url, number of POST vars, POST data
curl_setopt($ch,CURLOPT_URL, $url);
curl_setopt($ch,CURLOPT_POST, true);
curl_setopt($ch,CURLOPT_POSTFIELDS, $postdata);

//So that curl_exec returns the contents of the cURL; rather than echoing it
curl_setopt($ch,CURLOPT_RETURNTRANSFER, true); 

//execute post
$result = curl_exec($ch);
curl_close($ch);

//json parse 
$json = json_decode($result);

//download mp3 file
$file_url = $json->async;

if (!file_exists('audio')) {
    mkdir('audio', 0777, true);
}
if (!file_exists('audio/title')) {
    mkdir('audio/title', 0777, true);
}
$ch = curl_init($file_url);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_NOBODY, 0);
curl_setopt($ch, CURLOPT_TIMEOUT, 5);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
$output = curl_exec($ch);
$status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);
if ($status == 200) {
    file_put_contents('audio/'. $file_name .'.mp3', $output);
}
}
?>
