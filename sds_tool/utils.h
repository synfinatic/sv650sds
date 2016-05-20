#include <Arduino.h>

#ifndef __UTILS_H__
#define __UTILS_H__

uint8_t calc_checksum(uint8_t *data, uint8_t len);
void toggle_led();
char *ftoa(char *a, double f, int precision);
const char * bytes2str(uint8_t *bytes, uint8_t len);
void console_printf(const char *fmt, ... );

#endif
