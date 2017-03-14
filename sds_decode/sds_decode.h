#ifndef __SDS_DECODE_H__
#define __SDS_DECODE_H__

#include <avr/pgmspace.h>

#define TEENSY20  // Use Teensy 2.0 hardware

#ifdef TEENSY20
// Teensy 2.0 config
#define SDSSerial Serial1
#define Console Serial
#define CONSOLE_BAUD 9600
#define TX_PIN 8
#define RX_PIN 7
#define LED_PIN 11
#endif

#define SDS_BAUD 10400
#define FAST_START_WAIT 1000
#define FAST_START_PULSE 25

// Timings
#define MAXSENDTIME 2000         // 2 second timeout on KDS comms.
#define ISO_REQUEST_BYTE_DELAY 10
#define ISO_REQUEST_DELAY 40     // Time between requests.
#define MINIMUM_MESSAGE_GAP 20

#define MAX_MSG_LEN 100          // maximum number of bytes in a single message
#define TEMP_STR_LEN 15

#define ECU_ID 0x12              // ECU ID
#define SDT_ID 0xf1              // SDS Test Tool ID

typedef char *(*EcuCodeFmt)(char *, int, uint8_t, uint8_t);

/*
 * Data struct to store all the ECU code & meanings
 */
typedef struct
{
    int16_t a_index;             // index to a's value
    int16_t b_index;             // index to b's value or -1 for not used
    char name[15];               // name of sensor
    EcuCodeFmt formatter;        // pointer to formatter function
} ECU_CODE;


/*
Here are a bunch of messages that we may need to send some day.
I think there is one message missing: a keep alive, although it's possible
that UKNOWN_1 or 2 are actually the keepalives? 

No ideal right now what UKNOWN_1 & 2 actually are for.  They're sent by the SDS Tool
after start, but before K_READ_ALL_SENSORS.


const byte K_START_COMMS[] PROGMEM = {
    0x81, ECU_ID, SDT_ID, 0x81, 0x05
};

const byte K_START_RESPONSE[] PROGMEM = {
    0x80, SDT_ID, ECU_ID, 0x03, 0xc1, 0xea, 0x8f, 0xc0
};

const byte K_READ_ALL_SENSORS[] PROGMEM = {
    0x80, ECU_ID, SDT_ID, 0x02, 0x21, 0x08, 0xAE
};

const byte K_END_COMMS[] PROGMEM = {
    0x80, ECU_ID, SDT_ID, 0x01, 0x82, 0x06
};

const byte K_END_RESPONSE[] PROGMEM = {
    0x80, SDT_ID, ECU_ID, 0x01, 0xc2, 0x46
};

const byte K_UNNKNOWN_1[] PROGMEM = {
    0x80, ECU_ID, SDT_ID, 0x02, 0x1a, 0x91, 0x30 
};
// Response looks like: 
// 80,f1,12,12,5a,91,33,32,39,32,30,2d,31,37,47,32,2a,00,00,00,00,00,b8


const byte K_UNNKNOWN_2[] PROGMEM = {
    0x80, ECU_ID, SDT_ID, 0x02, 0x1a, 0x9a, 0x39 
};
// Response looks like:
// 80,f1,12,12,5a,9a,33,32,39,32,30,2d,31,37,47,30,00,00,00,00,00,00,95

*/
#endif
