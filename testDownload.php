<?php
$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, 'https://www.idx.co.id/umbraco/Surface/TradingSummary/DownloadStockSummary?date=20201022');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');

curl_setopt($ch, CURLOPT_ENCODING, 'gzip, deflate');

$headers = array();
$headers[] = 'Connection: keep-alive';
$headers[] = 'Accept: */*';
$headers[] = 'Dnt: 1';
$headers[] = 'X-Requested-With: XMLHttpRequest';
$headers[] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36';
$headers[] = 'Sec-Fetch-Site: same-origin';
$headers[] = 'Sec-Fetch-Mode: cors';
$headers[] = 'Sec-Fetch-Dest: empty';
$headers[] = 'Referer: https://www.idx.co.id/data-pasar/ringkasan-perdagangan/ringkasan-saham/';
$headers[] = 'Accept-Language: en-US,en;q=0.9';
$headers[] = 'Cookie: _ga=GA1.3.904661583.1603279378; __zlcmid=10mjWf7YdGgeKYG; skipFeedback=1; _gid=GA1.3.1666038713.1603513907; _gat_gtag_UA_69243601_3=1';
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

$result = curl_exec($ch);
if (curl_errno($ch)) {
    echo 'Error:' . curl_error($ch);
}
curl_close($ch);

$hasil = json_decode($result);
print_r($hasil->Results);
// echo $result;

?>