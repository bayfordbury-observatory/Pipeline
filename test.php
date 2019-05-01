<?php


$name="M82-1";
echo " - Starting\n";

//Make jpeg from original image
passthru("an-fitstopnm -L 10 -H 99.7 -m 50 -i \"".$name.".fit\" -o \"".$name.".pnm\""); 
passthru("pnmtojpeg --quality=95 \"".$name.".pnm\" > \"".$name.".jpg\"");
unlink($name.".pnm");
copy($name.".jpg",  "/var/www/M82/".$name.".jpg");

$time = microtime(true);
echo " - Removing hot pixels\n";
exec("python hotpix.py \"".$name."\"", $out);
echo $out[12]."\n";
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";

$flength=$out[8];
$pxsize=$out[7];

if($out[9]<720){
	$solved=true;
}else{
	$solved=false;
}
$scale=round(($pxsize/$flength)*206,3);

echo " - Scale guess: $scale \"/pix\n";

$scalelow=round($scale/1.1,5);
$scalehigh=round($scale*1.1,5);

/*
$name=$name.".hpf";#


//Make jpeg from filtered image
passthru("an-fitstopnm -L 10 -H 99.7 -m 50 -i \"".$name.".fit\" -o \"".$name.".pnm\""); 
passthru("pnmtojpeg --quality=95 \"".$name.".pnm\" > \"".$name.".jpg\"");
unlink($name.".pnm");


//Extract stars
echo" - Extracting stars\n";
$time = microtime(true);
passthru("image2xy \"".$name.".fit\" -O -o \"".$name.".xy2.fit\" -w 1.5 -p 8 -a 6 -s 100 -v");
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";

 
//Sort star list by flux
echo" - Sorting list\n";
$time = microtime(true);
passthru("tabsort -d FLUX \"".$name.".xy2.fit\" \"".$name.".xy.fit\"");
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";


//Make jpeg from image
echo" - Making jpeg\n";
$time = microtime(true);
passthru("an-fitstopnm -H 99 -L 5 -i \"".$name.".fit\" -o \"".$name.".pnm\""); 
passthru("pnmtojpeg --quality=95 \"".$name.".pnm\" > \"".$name.".jpg\"");
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";

if(!$solved){
	//Solve field
	echo" - Solving field\n";
	$time = microtime(true);
	passthru("solve-field --no-fits2fits --overwrite --scale-units app --scale-low $scalelow --scale-high $scalehigh --depth 20,40 --solved none -M none -R none -B none -W \"".$name.".wcs\" --no-verify --new-fits none --parity neg --cpulimit 30 --crpix-center --tweak-order 1 --no-plots \"".$name.".xy.fit\""); #--plot-bg \"".$name.".jpg\" 
	echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";
}else{
	echo " - Alreading solved\n";
}


//Convert source list xy to rd 
echo" - Converting xy to rd\n";
$time = microtime(true);
if($solved){
	passthru("wcs-xy2rd -w \"".$name.".fit\" -i \"".$name.".xy.fit\" -o \"".$name.".rd.fit\" ");
}else{
	passthru("wcs-xy2rd -w \"".$name.".wcs\" -i \"".$name.".xy.fit\" -o \"".$name.".rd.fit\" ");
}
 echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";
 
 
//Merge columns
echo" - Merging columns\n";
$time = microtime(true);
passthru("column-merge \"".$name.".xy.fit\" \"".$name.".rd.fit\" \"".$name.".all.fit\"");
 echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";


//passthru("tabsort -d FLUX \"".$name.".all.fit\" \"".$name.".sorted.fit\"");

//Printe wcs details 
$out="";
$time = microtime(true);
if($solved){
	exec("wcsinfo \"".$name.".fit\"", $out);
}else{
	exec("wcsinfo \"".$name.".wcs\"", $out);
}

//print_r($out);
 
$rac=substr($out[18],10);
$decc=substr($out[19],11);
if($decc>0){$decc="+".$decc;}
 
$fovw=substr($out[33],7);
$fovh=substr($out[34], 7);
echo" - rac:$rac\n - decc:$decc\n - fovw:$fovw\n - fovh:$fovh\n";


 echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";
 
 
echo" - Converting lists\n";
$time = microtime(true);
passthru("python list.py \"".$name."\"");
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";

 
//Download nomad source list
echo" - Downloading nomad fit\n";
$time = microtime(true);
$url="http://vizier.u-strasbg.fr/viz-bin/asu-binfits?-source=NOMAD&-c=".$rac.$decc."&-c.bm=".($fovw*1.1)."x".($fovh*1.1)."&-out=NOMAD1%20RAJ2000%20DEJ2000%20pmRA%20pmDE%20Bmag%20Vmag%20Rmag";

copy($url, "nomad.rd.fit"); #&Rmag=%3C".$maglim
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";

//plot extracted sources
echo" - Plotting extracted sources\n";
$time = microtime(true);
passthru("plotxy -i \"".$name.".xy.fit\" -I \"".$name.".pnm\" -o \"".$name.".plot.png\" -C red -r 10 -w 2");
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";

echo" - Converting rd to xy\n";
$time = microtime(true);
//Convert nomad sources from rd to xy
if($solved){
	passthru("wcs-rd2xy -w \"".$name.".fit\" -i \"nomad.rd.fit\" -o \"nomad.xy.fit\" -R RAJ2000 -D DEJ2000");
}else{
	passthru("wcs-rd2xy -w \"".$name.".wcs\" -i \"nomad.rd.fit\" -o \"nomad.xy.fit\" -R RAJ2000 -D DEJ2000");
}
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";

//Merge columns
echo" - Merging lists\n";
$time = microtime(true);
passthru("column-merge \"nomad.xy.fit\" \"nomad.rd.fit\" \"nomad.all.fit\"");
 echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";


//Plot nomad sources
//echo"Plotting nomad sources\n";
//passthru("plotxy -i \"nomad.xy.fit\" -I \"".$name.".pnm\" -o \"nomad.plot.png\" -C red -r 10 -w 1");
 
//extracted source plot to pnm
passthru("pngtopnm \"".$name.".plot.png\" > \"".$name.".plot.pnm\"");
 
//Plot nomad sources (in green) on extracted sources
echo" - Plotting nomad sources\n";
$time = microtime(true);
passthru("plotxy -i \"nomad.xy.fit\" -I \"".$name.".plot.pnm\" -o \"nomad.plot2.png\" -C green -r 10 -w 1");
  echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";




//Calculated fwhm of extracted source list and print file with 
echo" - Calculating fwhm\n";
$time = microtime(true);
passthru("python gauss.py \"".$name."\"");
echo " - Took  ".round((microtime(true) - $time)*1000,4) . "ms\n";

passthru("pngtopnm \"nomad.plot2.png\" > \"nomad.plot2.pnm\"");
//Convert reject list to fits

echo" - Converting reject list\n";
passthru("xylist2fits \"rejects.csv\" \"rejects.xy.fit\"");


//Plot rejects in blue
passthru("plotxy -i \"rejects.xy.fit\" -I \"nomad.plot2.pnm\" -o \"final.plot.png\" -C blue -r 10 -w 1");
echo" - Plotting final image\n";
//passthru("plotxy -i \"rejects.xy.fit\" -I \"".$name.".plot.pnm\" -o \"final.plot.png\" -C blue -r 10 -w 1");

*/

copy("final.plot.png", "/var/www/M82/final.plot.png");

copy($name.".jpg",  "/var/www/M82/".$name.".jpg");
   /**/
?>
