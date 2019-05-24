<?php

$api_key = '0bf528396c8146268c5eb01bf1f51bd8';
$voice = 'female';
$speed = 0;
$prosody = 0;
$postdata = 'Hay quá đức ơi';

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
echo $result;
?>