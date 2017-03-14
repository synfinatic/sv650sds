#include <Arduino.h>
#include "utils.h"
#include "sds_decode.h"

/**
 * \brief calc_checksum(*data, len)
 *
 * Calculates the checksum for <len> bytes of *data
 */
uint8_t
calc_checksum(uint8_t *data, uint8_t len) {
    uint8_t crc = 0;
    uint8_t i = 0;

    for (i = 0; i < len; i++) {
        crc += data[i];
    }
    return crc;
}


/**
 * \brief toggle_led(pin)
 *
 * Toggeles the led on <pin>
 */
void
toggle_led() {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
}

/*
 * Float to ascii
 * Since the sprintf() of the Arduino doesn't support floating point
 * converstion, #include <stdlib.h> for itoa() and then use this function
 * to do the conversion manually
 */
char *
ftoa(char *a, double f, int precision) {
    long p[] = { 0,10,100,1000,10000,100000,1000000,10000000,100000000 };
    char *ret = a;
    long heiltal = (long)f;
    long desimal;

    itoa(heiltal, a, 10);
    while (*a != '\0') {
        a++;
    }
    *a++ = '.';
    desimal = abs((long)((f - heiltal) * p[precision]));
    itoa(desimal, a, 10);
    return ret;
}

/*
 * printf to the HW serial port, useful for debugging.  Note 128char limit!
 */
void
console_printf(const char *fmt, ...) {
    char tmp[255];
    va_list args;
    va_start(args, fmt);
    vsnprintf(tmp, 254, fmt, args);
    va_end(args);
    Console.print(tmp);
}

void 
console_printf(const __FlashStringHelper *fmt, ... ) {
    char buf[128]; // resulting string limited to 128 chars
    va_list args;
    va_start (args, fmt);
#ifdef __AVR__
    vsnprintf_P(buf, sizeof(buf), (const char *)fmt, args); // progmem for AVR
#else
    vsnprintf(buf, sizeof(buf), (const char *)fmt, args); // for the rest of the world
#endif
    va_end(args);
    Console.print(buf);
}
