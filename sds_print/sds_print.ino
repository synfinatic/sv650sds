#include <Arduino.h>
#include "sds_print.h"
#include "utils.h"

uint8_t last_message[MAX_MSG_LEN];
uint8_t message[MAX_MSG_LEN];

bool process_message(uint8_t *message, uint8_t msglen, uint32_t delay);

void
setup() {
    uint32_t last = 0, now;

    // Init the pins
    pinMode(LED_PIN, OUTPUT);
    pinMode(TX_PIN, OUTPUT);
    pinMode(RX_PIN, INPUT);
    Console.begin(CONSOLE_BAUD);
    digitalWrite(LED_PIN, HIGH);
    memset(message, 0, MAX_MSG_LEN);
    memset(last_message, 0, MAX_MSG_LEN);

    // Wait until we see some indication that someone is talking.
    Console.print("Waiting for someone to talk (RX goes low)...\n");
    while (digitalRead(RX_PIN) == HIGH) {
        now = millis();
        if (last + 500 < now) {
            last = now;
            toggle_led();
        }
    }
    SDSSerial.begin(SDS_BAUD);
    Console.print("staring loop()\n");
}

void
loop() {
    static bool overflow = false;
    static uint8_t msglen = 0;
    static uint32_t lastms = 0;
    static uint32_t force_blink = 0;
    uint8_t byte;
    uint32_t currentms, deltams;

    currentms = millis();
    if (SDSSerial.available()) {
        byte = SDSSerial.read();
        toggle_led();
        deltams = currentms - lastms;
        lastms = currentms;


        if (deltams > MINIMUM_MESSAGE_GAP) {
            if (process_message(message, msglen, deltams)) {
                // replace last_message if CSUM is valid
                memcpy(last_message, message, msglen);
            }
            msglen = 0;
            memset(message, 0, MAX_MSG_LEN);
            overflow = false;
        } else if (msglen == MAX_MSG_LEN) {
            // Only print the warning once per read() until we reach the message gap
            if (!overflow) {
                overflow = true;
//                Console.printf("\n******\nERROR: ECU Message is larger then %u"
//                       " bytes! Unable to process!\n******", MAX_MSG_LEN);
            }
            return;  // return now so we don't increment msglen
        }

        message[msglen] = byte;
        msglen++;
    } else {
        if (force_blink + 1000 < currentms) {
            toggle_led();
            force_blink = currentms;
//            Console.printf("Waiting...\n");
        }
    }
}

/*
 * Processes & prints a message to the console 
 * Returns true if message is valid
 */
bool
process_message(uint8_t *message, uint8_t msglen, uint32_t delay) {
    uint8_t i, csum;
    bool unknown = false;
    uint8_t verify = 0;

    if (msglen < 4) {
//        Console.printf("Wow!  Short message.  %d bytes long\n", msglen);
        return false;
    }

    // Figure out if message is from the ECU or Diag tool
    if (message[1] == ECU_ID) {
        verify += ECU_ID;
    } else {
        verify += SDT_ID;
    }

    // Valid checksum?
    csum = calc_checksum(message, msglen - 1);
    if (csum == message[msglen - 1]) {
        verify += 1;
    } else {
        verify += 2;
    }

    // Print the header based on the above checks
    switch (verify) {
        case (ECU_ID + 1):
//            console_printf(F("OK ToECU [%03lums] %db: "), delay, msglen);
            break;
        case (SDT_ID + 1):
            console_printf(F("OK FromECU [%03lums] %db: "), delay, msglen);
            for (i = 0; i < (msglen - 1); i++) {
                Console.printf("%02x,", message[i]);
            }
            // last/checksum byte has a newline instead of a comma after it
            Console.printf("%02x\n", message[i]);
            break;
        case (ECU_ID + 2):
//            console_printf(F("BAD ToECU [%03lums] %db: "), delay, msglen);
            break;
        case (SDT_ID + 2):
//            console_printf(F("BAD FromECU [%03lums] %db: "), delay, msglen);
            break;
        default:
//            console_printf(F("Uknown message [%03lums] %db\n"), delay, msglen);
            unknown = true;
    }

    // print the message

    // Don't diff the sensors if we have an unknown message
    if (unknown)
        return false;

    if (message[1] == SDT_ID) {
        return true;
    }
    return false;
}

