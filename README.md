# AI-aircraft-FS92P3Dv4
Conversion of FS9/FSX library of AI aircraft to FSX/P3Dv4 library

This minor project was completed to help convert my old FS9 library of AI aircraft to P3Dv4 compatible. Many aircraft models in FS9 will not show, or only partially work as they are of a SCASM format that is not supported in P3Dv4. Luckily, FSX aircraft are modelled differently and hence work in P3Dv4. Whilst I will not explain the full description of how you install a new aircraft into the P3Dv4/FSX library as this is not the place for this (It can be easily googled), this code will help show what is needed to build a library of aircraft given that you have the correct FSX/P3Dv4 model installed. My code works specifically for my library and maybe yours will containe different models, names of models, .air files, and aircraft.cfgs. Mine supports the basic ones such as The Fruit Stand, AIA, FAIB, UTT, and HTAI. Ultimately, if anything offer a guide to how it could work for your library!

You will need to download the livery for a given airline which are to be installed in the library. These can be found at various websites (for example, www.avsim.com, www.flightsim.com, www.juergenbaumbusch.de). You can either download them indiviudally, or use a more sophisticated method, such as webscraping using, for example, beautufilsoup for python (which I used).

Before starting, it might be worth getting familiar with how each zip file is packed. Over the years therehas been a general format to which everyone has kind of followed and this code is based on that. Unfortunaly, not everyone packs their files the same way or differs slightly from the format and this will mean that code will return that that particlar livery is not installed and will have to be installed manually. In time, I might try and look at solving this, but for now, it is what it is. It took me 7 years to produce the FS9 library as slowly newer liveries came out, but using this code I rebuilt the library in 3 weeks given what time I had available.

Mandatory changes when running code:

my_park="atc_parking_codes=DHK,DHL" <----------------------- Change parking code \n
my_type="atc_parking_types=CARGO"   <------------------------ Change parking type \n
airline='dhl'                       <------------------------ Change airline code used in path setup \n

zippath = 'C:/Users/w9641432/Desktop/fsx/downloads/'+ airline +'/' < --------------- Path where zips are held \n
z_out_path = 'C:/Users/w9641432/Desktop/fsx/temp/'                 <---------------- Output folder where zip contents will reside \n
dst_ai = 'C:/Users/w9641432/Desktop/fsx/new_AI_Aircraft/'          <---------------- Destination folder of livery \n


It should also be noted that the code will report if an existing livery is present incase you happend to try and install it again, at which point the livery is not added. 
