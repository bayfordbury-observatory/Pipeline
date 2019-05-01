<?php
$time_start = microtime(true);
$dbid=1;
$url="M95-1";
$solved=0;
$ra=0;
$dec=0;

//echo "Solving DBID: $dbid\n$url\n";
//passthru("/usr/local/astrometry/bin/solve-field --verbose --no-fits2fits --overwrite --downsample 3 --scale-units amw --scale-low 18 --fits-image --scale-high 27 --depth 20,40 --solved none -M none -R none -B none -W none --no-verify --new-fits ".$dbid.".fits  --parity neg --cpulimit 30 --crpix-center --tweak-order 2 --use-wget --skip-solved --uniformize 0 ".$url, $output);

echo "Solving $url\n\n";
//--downsample 2
passthru("/usr/local/astrometry/bin/solve-field -no-fits2fits --overwrite --downsample 2 --scale-units amw --scale-low 20 --fits-image --scale-high 33 --depth 10,30 --solved none --no-delete-temp -M none -R none -B none -W none --no-verify --new-fits ".$url.".new.fit --parity neg --cpulimit 30 --crpix-center --tweak-order 5 --uniformize 2 --no-plots \"".$url.".fit\"");
//
  
  
echo "|Waiting for solve\n";
$counter=0;
 while(!file_exists($url.".axy") && $counter<=60000){usleep(1000);$counter++;}
 
if(file_exists($url.".axy")){$solved=1;}

$time_end = microtime(true);
$time = round($time_end - $time_start,3);

if($solved){echo "Solved! $ra $dec";}else{echo "Unsolved :(";}
echo "\n Time taken $time seconds\n";
@unlink($url.".axy");
@unlink($url."-indx.xyls");


?>
