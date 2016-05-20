#include <Arduino.h>
#include "sds_tool.h"
#include "utils.h"


void process_message(uint8_t *message, uint8_t msglen, uint32_t delay);

void
setup() {
    uint32_t last = 0, now;

    // Init the pins
    pinMode(LED_PIN, OUTPUT);
    pinMode(TX_PIN, OUTPUT);
    pinMode(RX_PIN, INPUT);
    Console.begin(CONSOLE_BAUD);
    digitalWrite(LED_PIN, HIGH);

    // Wait until we see some indication that someone is talking.
    Console.printf("Waiting for someone to talk (RX goes low).\n");
    while (digitalRead(RX_PIN) == HIGH) {
        now = millis();
        if (last + 500 > now) {
            last = now;
            toggle_led();
        }
    }
    SDSSerial.begin(SDS_BAUD);
}


uint32_t lastms = 0;
uint32_t force_blink = 0;

void
loop() {
    static uint8_t msglen = 0;
    static uint8_t message[MAX_MSG_LEN];
    uint8_t byte;
    uint32_t currentms, deltams;

    currentms = millis();
    if (SDSSerial.available()) {
        byte = SDSSerial.read();
        toggle_led();
        deltams = currentms - lastms;
        lastms = currentms;

        if (deltams > MINIMUM_MESSAGE_GAP) {
            process_message(message, msglen, deltams);
            msglen = 0;
        }

        message[msglen] = byte;
        msglen++;
    } else {
        if (force_blink + 1000 < currentms) {
            toggle_led();
            force_blink = currentms;
            Console.printf("Waiting...\n");
        }
    }
}


/*
 * Processes & prints a message to the console
 */
void
process_message(uint8_t *message, uint8_t msglen, uint32_t delay) {
    uint8_t i, csum;
    uint8_t verify = 0;

    if (msglen < 2) {
        Console.printf("Wow!  Short message.  %d bytes long\n", msglen);
        return;
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
            Console.printf("OK ToECU [%03lums] %d: ", delay, msglen);
            break;
        case (SDT_ID + 1):
            Console.printf("OK FromECU [%03lums] %d: ", delay, msglen);
            break;
        case (ECU_ID + 2):
            Console.printf("BAD ToECU [%03lums] %d: ", delay, msglen);
            break;
        case (SDT_ID + 2):
            Console.printf("BAD FromECU [%03lums] %d: ", delay, msglen);
            break;
        default:
            Console.printf("Uknown message [%03lums] %d\n", delay, msglen);
            return;
    }

    // print the message
    for (i = 0; i < (msglen - 1); i++) {
        Console.printf("%02x,", message[i]);
    }
    // last/checksum byte has a newline instead of a comma after it
    Console.printf("%02x\n", message[i]);
}
