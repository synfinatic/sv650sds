
From [ECU Hacking Board](http://ecuhacking.activeboard.com/t22573776/sds-protocol/?sort=oldestFirst&page=5#comment-50643196)

I can't tell if this is old news or not so I'll throw it out on the off chance that it is of interest.

I've been studying the pds file saved by the SDS software. It seems like there's a good chance that the saved values are the same as in the K-line data stream. The relationship between those values and engineering units is as follows:


 * RPM = Value*100/255
 * Throttle position (°) = Value*125/255
 * Manifold pressure = (Value*5 - 153)*133/4/255
 * Temperature (C) = Value*160/255 - 30
 * Temperature (F) = Value*288/255 - 22
 * Voltage = Value*20/255
 * Secondary throttle position (%) = Value*100/255
 * EXCVA sensor = Value*100/255
