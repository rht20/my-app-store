<?php

list($key, $val) = explode('=', $argv[1]);
  //var_dump(array($key=>$val));
echo $val;

   
error_reporting(E_ALL);
ini_set('display_errors', 1);


// Your Access Key ID, as taken from the Your Account page
$access_key_id = "AKIAJGPVHL4AUW3DAYSQ";

// Your Secret Key corresponding to the above ID, as taken from the Your Account page
$secret_key = "6IdtDciYOYRW+Qh0UUhAN46OynCCFjJ46lE08Pnc";

// The region you are interested in
$endpoint = "webservices.amazon.co.uk";

$uri = "/onca/xml";

$params = array(
    "Service" => "AWSECommerceService",
    "Operation" => "ItemSearch",
    "AWSAccessKeyId" => "AKIAJGPVHL4AUW3DAYSQ",
    "AssociateTag" => "myplaystore03-21",
    "SearchIndex" => "MobileApps",
    "Keywords" => $val,
    "ResponseGroup" => "Images,ItemAttributes,Offers"
);

// Set current timestamp if not set
if (!isset($params["Timestamp"])) {
    $params["Timestamp"] = gmdate('Y-m-d\TH:i:s\Z');
}

// Sort the parameters by key
ksort($params);

$pairs = array();

foreach ($params as $key => $value) {
    array_push($pairs, rawurlencode($key)."=".rawurlencode($value));
}

// Generate the canonical query
$canonical_query_string = join("&", $pairs);

// Generate the string to be signed
$string_to_sign = "GET\n".$endpoint."\n".$uri."\n".$canonical_query_string;

// Generate the signature required by the Product Advertising API
$signature = base64_encode(hash_hmac("sha256", $string_to_sign, $secret_key, true));

// Generate the signed URL
$request_url = 'http://'.$endpoint.$uri.'?'.$canonical_query_string.'&Signature='.rawurlencode($signature);

//**echo "Signed URL: \"".$request_url."\"";


//$file = file_get_contents("http://webservices.amazon.co.uk/onca/xml?AWSAccessKeyId=AKIAJGPVHL4AUW3DAYSQ&AssociateTag=myplaystore03-21&Keywords=Ninja&Operation=ItemSearch&ResponseGroup=Images%2CItemAttributes%2COffers&SearchIndex=MobileApps&Service=AWSECommerceService&Timestamp=2018-04-20T21%3A10%3A21.000Z&Signature=M8uGoF%2BeG8SNKOBkKAtpeivA3LoG4IM%2FluMQnl34bBI%3D");
$file = file_get_contents($request_url);
$xml = new DOMDocument();
$xml->loadXML($file);
$items = $xml->getElementsByTagName("Items")[0];

if (!empty($items)) 
{
	 echo "data found";
}else {
	 echo "No data found";
}


$l1= 'https://www.amazon.com/gp/product/';
$l2= '/ref=sr_1_1?s=mobile-apps&ie=UTF8&sr=1-1&keywords='.$val;
$l3= 'ASIN=';

$f1 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/FTitle.txt';
$f2 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/FImage.txt';
$f3 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/FASIN.txt';
$f4 = '/home/user/Documents/NO/Amazon-review-extractor/amazon_review_analyzer/templates/search_text/FRating.txt';
$current1 ="";
$current2 ="";
$current3 ="";
$current4 ="";
foreach ( $items->getElementsByTagName("Item") as $item )    {
	
	 $ASIN=$item->getElementsByTagName("ASIN")[0]->nodeValue.PHP_EOL;
	 $t1= $item->getElementsByTagName("ItemAttributes")[0];
	 $Title= $t1->getElementsByTagName("Title")[0]->nodeValue.PHP_EOL;
	 $ASIN = preg_replace('/\n$/','',$ASIN);
	 $applink= $l1.$ASIN.$l2."\n"; //.$l3.$ASIN;
	 $img = $item->getElementsByTagName("MediumImage")[0];  
	 $image= $img->getElementsByTagName("URL")[0]->nodeValue.PHP_EOL;
	 
		
	
	
	 //$current1 = file_get_contents($f1);
	 //$current2 = file_get_contents($f2);
	 //$current3 = file_get_contents($f3);
	
	 
	 $current1 .= $Title;
	 $current2 .= $image;
	 $current3 .= $applink;
	 $current4 .="selected\n"."selected\n"."selected\n"."selected\n"."selected\n";
	 
	 #echo $current;
	
	 
	 //echo "ASIN:".$Title;
	 //echo "link:".$applink;
     //echo "image:".$image;
}

	 file_put_contents($f1, $current1);
	 file_put_contents($f2, $current2);
	 file_put_contents($f3, $current3);
	 file_put_contents($f4, $current4);

