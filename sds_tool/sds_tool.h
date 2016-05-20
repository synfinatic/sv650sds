#ifndef __SDS_TOOL_H__
#define __SDS_TOOL_H__

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

#define MAX_MSG_LEN 255          // maximum number of bytes in a single message

#define ECU_ID 0x12              // ECU ID
#define SDT_ID 0xf1              // SDS Test Tool ID


/*
const byte K_START_COMMS[] PROGMEM = {
    0x81, 0x12, 0xF1, 0x81, 0x05
};

const byte K_READ_ALL_SENSORS[] PROGMEM = {
    0x80, 0x12, 0xF1, 0x02, 0x21, 0x08, 0xAE
};
*/
#endif
