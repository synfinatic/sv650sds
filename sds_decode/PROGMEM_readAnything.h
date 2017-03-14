/*
 * Simple template to read from PROGMEM 
 * http://arduino.stackexchange.com/questions/13545/using-progmem-to-store-array-of-structs
 */

#ifndef __READANYTHING_H__
#define __READANYTHING_H__

#include <Arduino.h>  // for type definitions

template <typename T> void PROGMEM_readAnything (const T * sce, T& dest)
{
    memcpy_P (&dest, sce, sizeof (T));
}

template <typename T> T PROGMEM_getAnything (const T * sce)
{
    static T temp;
    memcpy_P (&temp, sce, sizeof (T));
    return temp;
}

#endif
