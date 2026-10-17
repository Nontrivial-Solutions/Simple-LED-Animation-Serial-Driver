/**
 * \file arduino_src.ino
 * \brief Arduino project for basic control of a string/array of LED.
 */

#include "FastLED.h"
#include <CRC32.h>
#include <stdio.h>

/*************************************************************************************************/
/************************** Defines **************************************************************/
/*************************************************************************************************/


/**
 * \brief The size the LED array. Bounded by memory size of the uc in relation to serial buffer
 *needs.
 */
#define MAX_NUM_LEDS (1000u)

/**
 * \brief Physical pin the LED are connected to.
 */
#define DATA_PIN (6u)

/**
 * \brief Specify the ringbuffer size for the hardware monitor. The arduino default is 64bytes.
 */
#define SERIAL_BUFFER_SIZE (64u)

/**
 * \brief The baudrate to use for the serial connection.  
 */
#define SERIAL_BAUDRATE (115200u)

/**
 * \brief Specify the string to send as acknowledgement to a message with no explicit reply.
 */
#define ACK_STR ("ACK")

/**
 * \brief Return status when a command is processed correctly.
 */
#define RET_STA_VALID (0u)

/**
 * \brief Return status when a command is processed incorrectly.
 */
#define RET_STA_INVALID (1u)

/*************************************************************************************************/
/*************************************************************************************************/
/*************************************************************************************************/

/**
 * \typedef cmd_handler_funptr_t
 * \brief Function pointer type for a command handler callback function.
 */
typedef uint8_t (*cmdHandlerFunptr_t)();

/**
 * \struct cmdDic_t
 * \brief The storage type for a serial command.
 *
 */
typedef struct cmdDic_t {
  char *charClass;           /**< The class of char that indicate a command.*/
  cmdHandlerFunptr_t funptr; /**< The callback used to process the command.*/
} cmdDic_t;

/*************************************************************************************************/
/************************** Private Function Declarations ****************************************/
/*************************************************************************************************/

/* Documentation in declaration.*/
uint8_t setLedStateCmd();

/* Documentation in declaration.*/
uint8_t setLedOffCmd();

/* Documentation in declaration.*/
uint8_t setLedCountCmd();

/* Documentation in declaration.*/
uint8_t procShowCmd();

/* Documentation in declaration.*/
uint8_t getCrcCmd();

/* Documentation in declaration.*/
bool cmdCheckCharset(const char *validChars, const char strChar);

/* Documentation in declaration.*/
uint32_t getChecksum(uint16_t count);

/*************************************************************************************************/
/************************** Local Variables ******************************************************/
/*************************************************************************************************/

/**
 * \brief The collection of LED objects.
 */
CRGB leds[MAX_NUM_LEDS];

/**
 * \brief The collection of LED objects.
 */
char serialBuffer[SERIAL_BUFFER_SIZE];

/**
 * \brief The collection of LED objects.
 */
unsigned long int ledCount = 0;

/**
 * \brief The checksum for the LED array. Global so it can be computed in the main loop.
 */
uint32_t ledArrayCsum = 0;

/**
 * \brief The state command template.
 */
cmdDic_t setState = { "Ss", &setLedStateCmd };

/**
 * \brief The count command template.
 */
cmdDic_t setCount = { "Cc", &setLedCountCmd };

/**
 * \brief The show command template.
 */
cmdDic_t procShow = { "Hh", &procShowCmd };

/**
 * \brief The get CRC command template.
 */
cmdDic_t getCrc = { "Rr", &getCrcCmd };

/**
 * \brief The off command template.
 */
cmdDic_t setOff = { "Oo", &setLedOffCmd };

/**
 * \brief The collection of commands. Must be NULL terminated.
 */
const cmdDic_t *charcheck_dict[] = { &setState, &setOff, &setCount, &procShow, &getCrc, NULL };


/*************************************************************************************************/
/************************** Primary Arduino Event Loop *******************************************/
/*************************************************************************************************/
void setup() {
  /* initialize serial: */
  Serial.begin(SERIAL_BAUDRATE);
  Serial.setTimeout(10);
  while (!Serial) {
    ;
  }
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, MAX_NUM_LEDS);
  ledCount = 0u;
  setLedOffCmd();
  Serial.println(ACK_STR);
  Serial.flush();
}

void loop() {
  if (Serial.available() > 0) {
    size_t i;
    /* Read until newline, leaving room for the null-terminator */
    int bytesRead = Serial.readBytesUntil('\n', serialBuffer, SERIAL_BUFFER_SIZE - 1);

    /* Error Handling: Check for buffer overflow */
    if (bytesRead == SERIAL_BUFFER_SIZE - 1) {
      Serial.println(F("ERROR: Buffer overflow. Input exceeded 63 chars."));
      Serial.flush();
      /* Flush the remaining garbage out of the hardware buffer */
      while (Serial.available() > 0) {
        Serial.read();
      }
      return;
    } else {
      /* Null-terminate the string so standard C string functions work safely */
      serialBuffer[bytesRead] = '\0';

      /* Strip trailing carriage returns (Windows Serial Monitor sends \r\n) */
      if (bytesRead > 0 && serialBuffer[bytesRead - 1] == '\r') {
        serialBuffer[bytesRead - 1] = '\0';
      }

      /* Process the validated input */
      for (i = 0; charcheck_dict[i] != NULL; i++) {
        const cmdDic_t *dic_p = charcheck_dict[i];
        if (cmdCheckCharset(dic_p->charClass, serialBuffer[0])) {
          if (dic_p->funptr != NULL) {
            dic_p->funptr();
          }
          break;
        }
      }
    }
    ledArrayCsum = getChecksum(ledCount);
  }
}

/*************************************************************************************************/
/************************** Private Function Definitions *****************************************/
/*************************************************************************************************/

/**
 * \brief Callback function for the state command.
 *
 * Set the state of an individual LED in the array.
 *
 * \return The status of the command processing.
 */
uint8_t setLedStateCmd() {
  unsigned long int idx = 0;
  unsigned long int r = 0;
  unsigned long int g = 0;
  unsigned long int b = 0;

  int res = sscanf(serialBuffer, "S%ld:%ld:%ld:%ld\n", &idx, &r, &g, &b);

  if ((r > 0xff) || (g > 0xff) || (b > 0xff) || (res != 4) || (idx >= ledCount)) {
    Serial.print("ERROR: while setting LED state -- red: ");
    Serial.print(r);
    Serial.print(" -- green: ");
    Serial.print(g);
    Serial.print(" -- blue: ");
    Serial.print(b);
    Serial.print(" -- idx: ");
    Serial.print(idx);
    Serial.print(" -- sscanf: ");
    Serial.print(res);
    Serial.print(" -- buffer: ");
    Serial.print(serialBuffer);
    Serial.print(" -- count: ");
    Serial.println(ledCount);
    Serial.flush();
    return RET_STA_INVALID;
  }
  leds[idx].red = (uint8_t)r;
  leds[idx].green = (uint8_t)g;
  leds[idx].blue = (uint8_t)b;
  Serial.println(ACK_STR);
  Serial.flush();
  return RET_STA_VALID;
}

/**
 * \brief Callback function for the LED count command.
 *
 * Set the number of LED in the array.
 *
 * \return The status of the command processing.
 */
uint8_t setLedCountCmd() {
  unsigned long int tcount;

  int res = sscanf(serialBuffer, "C%ld", &tcount);

  if ((res != 1) || (tcount > MAX_NUM_LEDS)) {
    Serial.print("ERROR: while setting LED count -- sscanf: ");
    Serial.print(res);
    Serial.print(" -- temp count: ");
    Serial.print(tcount);
    Serial.print(" -- count: ");
    Serial.println(ledCount);
    Serial.flush();
    return RET_STA_INVALID;
  }
  ledCount = tcount;
  Serial.println(ACK_STR);
  Serial.flush();
  return RET_STA_VALID;
}

/**
 * \brief Callback function for the off command.
 *
 * Set the entire array off.
 *
 * \return The status of the command processing.
 */
uint8_t setLedOffCmd() {
  size_t i;

  for (i = 0; i < MAX_NUM_LEDS; i++) {
    leds[i].r = (uint8_t)0u;
    leds[i].g = (uint8_t)0u;
    leds[i].b = (uint8_t)0u;
  }
  Serial.println(ACK_STR);
  Serial.flush();
  return RET_STA_VALID;
}

/**
 * \brief Callback function for the LED array show command.
 *
 * Command the array to update to show the current state.
 *
 * \return The status of the command processing.
 */
uint8_t procShowCmd() {
  FastLED.show();
  Serial.println(ACK_STR);
  Serial.flush();
  return RET_STA_VALID;
}

/**
 * \brief Callback function for the CRC command.
 *
 * Get the array CRC from the device.
 *
 * \return The status of the command processing.
 */
uint8_t getCrcCmd() {
  Serial.println(ledArrayCsum);
  Serial.flush();
  return RET_STA_VALID;
}

/**
 * \brief Identify if the buffered message is a valid command.
 *
 * \param valid_chars The set of valid command indicators.
 * \param str_char The char indicating what command to process.
 * \return True when command is found. False otherwise.
 */
bool cmdCheckCharset(const char *valid_chars, const char str_char) {
  bool retval = false;
  size_t i;

  for (i = 0; i < strlen(valid_chars); i++) {
    if (str_char == valid_chars[i]) {
      retval = true;
      break;
    }
  }
  return retval;
}

/**
 * \brief Compute the CRC32 for the color byte values of the LED array.
 *
 * \return The current CRC32 for the LED array.
 */
uint32_t getChecksum(uint16_t count) {
  CRC32 crc;
  size_t i;

  for (i = 0; i < count; i++) {
    crc.add(leds[i].red);
    crc.add(leds[i].green);
    crc.add(leds[i].blue);
  }
  return crc.calc();
}
