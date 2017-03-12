#ifndef __SDS_PRINT_H__
#define __SDS_PRINT_H__

#define SDSSerial Serial1
#define Console Serial
#define CONSOLE_BAUD 9600
#define TX_PIN 8
#define RX_PIN 7
#define LED_PIN 11

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

#endif // __SDS_PRINT_H__
