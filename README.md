Overview
========

SDS (Suzuki Diagnostics System) is a KWP-2000 (sometimes known as K-Line or 
ISO-14230) protocol running at 10,400 baud/8n1.  While the ISO spec covers the 
physical signaling and general protocol, the actual messages and their meaning 
are left up to the manufacturer to define and impliment.

The result is that different manufacturers end up writing incompatible protocols
and that even for a given manufacturer, the protocol may differ for different 
vehicles.

The result is that while AiM can decode the SDS protocol for the Suzuki GSXR, it
can only do a medicore job of doing so for the 03-05 SV650.  The goal of this 
project is to reverse engineer and document the 03-05 SV650 protocol and develop
some tools to make reverse engineering other vehicles easier.

Tools
=====

I have the following tools available to me:

 - Cheap chinese clone of the "HealTech" Suzuki Diagnostic Tool (SDT) off eBay
 - Teensy 2.0 + STL9637D K-Line interface 
 - OpenBench Logic Sniffer + OLS

Logic Sniffer
=============

By using a simple voltage divider using a 33k and 10k resistor, I was able to
drop the 12V signal of the K-Line to something the 
[OpenBench Logic Sniffer](http://dangerousprototypes.com/blog/open-logic-sniffer/) 
was able to process.

Using 50kHz sampling rate and setting a trigger to look for 0x80, I'm able to
capture the initial 25ms handshake between the SDT and 
[~12 seconds worth of data](https://github.com/synfinatic/sv650sds/blob/master/data/sds_tool_output.txt).

By using the UART Analyser built in to [OLS](http://ols.lxtreme.nl/), I was 
able to generate a 
[simple CSV file](https://github.com/synfinatic/sv650sds/blob/master/data/001-basic.csv)
with all the communications.  Next step is to build a suite of tools to clean up the 
data (OLS puts some binary characters in the CSV) and to do some basic decoding of 
the messages to figure out:

 - Decode header to determine if sender is ECU or SDT 
 - Decode payload bytes
 - Build a lookup table to map payload values to something meaningful
 - Convert payload to useful messages

Ended up abandoning this method as the small capture window made things too difficult.

Teensy + STL9637D
=================

Using a simplified version of the code from here: https://github.com/o5i/Datalogger
I was able to validate that the Teensy/STL9637D can communicate to the bike.
Connecting the two is pretty straight forward (just need +12V, GND and the K-Line 
off the bike), but you need to remember a 500-1k pull up resistor on the K-Line.

Ended up abandoning this method because doing all the decoding on the Teensy using
Processing was not efficient enough.

Teensy + Python
===============

After a while, I realized that trying to iterate over decoding the protocol directly
on the Teensy was really painful.  I wanted a way to:

 - Write code in a higher level language like Python
 - Easily save the raw data to disk and use that for apples-to-apples comparison of 
    different versions of the protocol decoder

The result is dumbing down the Teensy code so it just handles the framing 
([sds_print](https://github.com/synfinatic/sv650sds/tree/master/sds_print))
and a new Python script 
([read_serial.py](https://github.com/synfinatic/sv650sds/blob/master/tools/read_serial.py)) 
to process the messages.  This has turned out to be much more powerful and easier 
to iterate over then writing in Processing and reprogramming the Teensy each 
time (duh!).

The only challenge really is that the commercial SDS tool won't export timestamped 
records.  This means I have to *manually* align messages which *sucks*.  I'm probably
going to have to come up with a way to insert my own marks into the data stream for
alignment purposes- probably using the gear position sensor since that is easy to locate
in the data stream, written raw and should be easy to manipulate/create a test harness
for.

External References
===================

Most of these links provide background to the KWP-2000 protocol and should help
understand what is actually going on in the wire.

 - https://github.com/HerrRiebmann/KDS2Bluetooth
 - http://ecuhacking.activeboard.com/t56234221/kds-protocol/
 - http://ecuhacking.activeboard.com/t22573776/sds-protocol/
   - http://ecuhacking.activeboard.com/t22573776/sds-protocol/?sort=oldestFirst&page=5#comment-49610241
   - http://ecuhacking.activeboard.com/t22573776/sds-protocol/?sort=oldestFirst&page=5#comment-50643196
 - https://bitbucket.org/tomnz/kawaduino/
 - https://github.com/o5i/Datalogger
 - https://en.wikipedia.org/wiki/Keyword_Protocol_2000
