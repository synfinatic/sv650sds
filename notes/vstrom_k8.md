Partial decode for Suzuki VStrom 2008

80
F1
12
34
61.....
8
9
16
56
E0
1
5
E0
FF
FF
FF
FF //Speed = byte 17 * 2 in km/h
0 // RPM high
FF // RPM low
0 // TPS  trottle position 
FF// IAP sensor 1 - pression air admission 1
0 // CLT
36  // IAT temperature admission air
FF //AP ??? 
0 //BATT
FF //H02
5 // Gears
FF // IAP sensor 2 - pression air admission 2
6B // Desired Idle Speed
2 // ISC Valve Position
FF 
0 // Fuel Hi1
0 // Fuel Lo1
0 // Fuel Hi2
0 // Fuel Lo2
FF // Fuel Hi3
FF // Fuel Lo3
FF // Fuel Hi4
FF // Fuel Lo4
FF
FF
47
47
FF
FF
FF 
0 // STP second trottle valve
FF
FF
FF
FF // mode ABC
8 // PAIR
5 // retour interrupteur poignée embrayage MS/clutch
22 // neutral switch  if not connected : 22 if connected : 20 NT/HOX_on
FF
FF
A7 // checksum


### Formulas 

 * ECT = k_inByte * 160 / 255; 
 * TPS = (k_inByte * 125 / 255);
 * BAT = k_inByte * 20.0 / 255;
 * SPEED = (byte24 * 2 );
 * RPM1 = Byte25 * 100;
 * RPM = (byte26 * 100 / 255) + RPM1;


http://ecuhacking.activeboard.com/t22573776/sds-protocol/?sort=oldestFirst&page=5#comment-49610241

Note that 57 bytes is the same as the SV650!!!!
 62 http://ecuhacking.activeboard.com/t22573776/sds-protocol/?sort=oldestFirst&page=5#comment-49610241
