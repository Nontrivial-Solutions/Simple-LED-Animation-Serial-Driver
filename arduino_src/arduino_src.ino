/**
 * \file arduino_src.ino
 * \brief Arduino project for basic control of a string of LED.
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

#define BUFFER_SIZE (64u)

/*************************************************************************************************/
/*************************************************************************************************/
/*************************************************************************************************/

/**
 * \typedef cmd_handler_funptr_t
 * \brief Function pointer type for a command handler callback function.
 */
typedef uint8_t (*cmd_handler_funptr_t)();

/**
 * \struct cmd_dic_t
 * \brief The storage type for a serial command.
 *
 */
typedef struct cmd_dic_t {
  char *char_class;            /**< The class of char that indicate a command.*/
  cmd_handler_funptr_t funptr; /**< The callback used to process the command.*/
} cmd_dic_t;

/**
 * \struct color_t
 * \brief The storage type for a color tuple.
 *
 */
typedef struct color_t {
  uint8_t red;
  uint8_t green;
  uint8_t blue;
} color_t;
/*************************************************************************************************/
/************************** Private Function Declarations ****************************************/
/*************************************************************************************************/

uint8_t set_led_state_cmd();
uint8_t set_led_off_cmd();
uint8_t set_led_count_cmd();
bool cmd_check_charset(const char *valid_chars, const char str_char);
uint32_t get_checksum(uint16_t count);
void clearIBuff();

/*************************************************************************************************/
/************************** Local Variables ******************************************************/
/*************************************************************************************************/

/**
 * \brief The collection of LED objects.
 */
CRGB leds[MAX_NUM_LEDS];
color_t leds_mirror[MAX_NUM_LEDS];

char serialBuffer[BUFFER_SIZE];

/**
 * \brief The collection of LED objects.
 */
unsigned long int ledCount = 0;

/**
 * \brief The state command template.
 */
cmd_dic_t setState = { "Ss", &set_led_state_cmd };

cmd_dic_t setCount = { "Cc", &set_led_count_cmd };
cmd_dic_t setShow = { "Hh", &set_show };
cmd_dic_t getCrc = { "Rr", &get_crc };

/**
 * \brief The off command template.
 */
cmd_dic_t setOff = { "Oo", &set_led_off_cmd };

/**
 * \brief The collection of commands. Must be NULL terminated.
 */
const cmd_dic_t *charcheck_dict[] = { &setState, &setOff, &setCount, &setShow, &getCrc, NULL };

uint32_t csum = 0;

/*************************************************************************************************/
/************************** Primary Arduino Event Loop *******************************************/
/*************************************************************************************************/
void setup() {
  /* initialize serial: */
  Serial.begin(9600);
  Serial.setTimeout(10);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }
  FastLED.addLeds< NEOPIXEL, DATA_PIN >(leds, MAX_NUM_LEDS);
  ledCount = 0u;
  set_led_off_cmd();
  clearIBuff();
  Serial.println("READY!");
  Serial.flush();
}


void loop() {
  if (Serial.available() > 0) {
    size_t i;
    // Read until newline, leaving room for the null-terminator
    int bytesRead = Serial.readBytesUntil('\n', serialBuffer, BUFFER_SIZE - 1);

    // Error Handling: Check for buffer overflow
    if (bytesRead == BUFFER_SIZE - 1) {
      Serial.println(F("ERROR: Buffer overflow. Input exceeded 63 chars."));
      Serial.flush();
      // Flush the remaining garbage out of the hardware buffer
      while (Serial.available() > 0) {
        Serial.read();
      }
      return;
    } else {

      // Null-terminate the string so standard C string functions work safely
      serialBuffer[bytesRead] = '\0';

      // Strip trailing carriage returns (Windows Serial Monitor sends \r\n)
      if (bytesRead > 0 && serialBuffer[bytesRead - 1] == '\r') {
        serialBuffer[bytesRead - 1] = '\0';
      }

      // Process the validated input
      for (i = 0; charcheck_dict[i] != NULL; i++) {
        const cmd_dic_t *dic_p = charcheck_dict[i];
        if (cmd_check_charset(dic_p->char_class, serialBuffer[0])) {
          if (dic_p->funptr != NULL) {
            dic_p->funptr();
          }
          break;
        }
      }
    }
    csum = get_checksum(ledCount);
  }
}

/*************************************************************************************************/
/************************** Private Function Definitions *****************************************/
/*************************************************************************************************/

/**
 * \brief Callback function for the state command.
 *
 * \return not used
 */
uint8_t set_led_state_cmd() {
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
    return 1;
  }
  leds[idx].red = (uint8_t)r;
  leds[idx].green = (uint8_t)g;
  leds[idx].blue = (uint8_t)b;
  leds_mirror[idx].red = (uint8_t)r;
  leds_mirror[idx].green = (uint8_t)g;
  leds_mirror[idx].blue = (uint8_t)b;
  Serial.println("ack");
  return 0;
}

/**
 * \brief Callback function for the state command.
 *
 * \return not used
 */
uint8_t set_led_count_cmd() {

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
    return 1;
  }
  ledCount = tcount;
  Serial.println("ack");
  return 0;
}

/**
 * \brief Callback function for the state command.
 *
 * \return not used
 */
uint8_t set_led_off_cmd() {
  size_t i;
  for (i = 0; i < MAX_NUM_LEDS; i++) {
    leds[i].r = 0;
    leds[i].g = 0;
    leds[i].b = 0;
    leds_mirror[i].red = (uint8_t)0;
    leds_mirror[i].green = (uint8_t)0;
    leds_mirror[i].blue = (uint8_t)0;
  }
  Serial.println("ack");
  return 0;
}

uint8_t set_show() {
  FastLED.show();
  Serial.println("ack");
  return 0;
}

uint8_t get_crc() {
  Serial.println(csum);
  Serial.flush();
  return 0;
}

/**
 * \brief Identify if the buffered message is a valid command.
 *
 * \param valid_chars The set of valid command indicators.
 * \param str_char The char indicating what command to process.
 * \return True when command is found. False otherwise.
 */
bool cmd_check_charset(const char *valid_chars, const char str_char) {
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

uint32_t get_checksum(uint16_t count) {
  CRC32 crc;
  size_t i;
  for (i = 0; i < count; i++) {
    crc.add(leds_mirror[i].red);
    crc.add(leds_mirror[i].green);
    crc.add(leds_mirror[i].blue);
  }
  return crc.calc();
  ;
}


void clearIBuff() {
  while (Serial.available() > 0) {
    Serial.read();
  }
}