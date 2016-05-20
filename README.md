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
capture the initial 25ms handshake between the SDT and ~12 seconds worth of data.

By using the UART Analyser built in to [OLS](http://ols.lxtreme.nl/), I was 
able to generate a simple CSV file with all the communications.  Next step is 
to build a suite of tools to clean up the data (OLS puts some binary characters 
in the CSV) and to do some basic decoding of the messages to figure out:

 - Decode header to determine if sender is ECU or SDT 
 - Decode payload bytes
 - Build a lookup table to map payload values to something meaningful
 - Convert payload to useful messages


Teensy + STL9637D
=================

Using a simplified version of the code from here: https://github.com/o5i/Datalogger
I was able to validate that the Teensy/STL9637D can communicate to the bike.
Connecting the two is pretty straight forward (just need +12V, GND and the K-Line 
off the bike), but you need to remember a 500-1k pull up resistor on the K-Line.

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
