/**
 * \file arduino_src.ino
 * \brief Arduino project for basic control of a string of LED.
 */


#include "FastLED.h"
#include <CRC32.h>

/*************************************************************************************************/
/************************** Defines **************************************************************/
/*************************************************************************************************/


/**
 * \brief The size the LED array. Bounded by memory size of the uc in relation to serial buffer
 *needs.
 */
#define MAX_NUM_LEDS 1000u

/**
 * \brief Physical pin the LED are connected to.
 */
#define DATA_PIN 6

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
uint32_t checksum(uint16_t count);
bool readUint16(uint16_t *val);
bool readColor(color_t *color);
void clearIBuff();

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
uint16_t ledCount = 0;

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
const cmd_dic_t *charcheck_dict[] = { &setState, &setOff, &setCount, NULL };

/*************************************************************************************************/
/************************** Primary Arduino Event Loop *******************************************/
/*************************************************************************************************/
uint8_t pinstate = HIGH;
void setup() {
  /* initialize serial: */
  Serial.begin(9600);
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
    uint8_t curChar = Serial.read();
    size_t i;
    for (i = 0; charcheck_dict[i] != NULL; i++) {
      const cmd_dic_t *dic_p = charcheck_dict[i];
      if (cmd_check_charset(dic_p->char_class, curChar)) {
        if (dic_p->funptr != NULL) {
          dic_p->funptr();
        }
        break;
      }
    }
  }
  delay(100);
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
  uint16_t idx;
  color_t color;
  readUint16(&idx);
  if (idx >= ledCount) {
    Serial.print("ERROR: idx out of range");
    Serial.println(ledCount);
  }
  readColor(&color);
  leds[idx].red = color.red;
  leds[idx].green = color.green;
  leds[idx].blue = color.blue;
  return 0;
}

/**
 * \brief Callback function for the state command.
 *
 * \return not used
 */
uint8_t set_led_count_cmd() {
  readUint16(&ledCount);
  if (MAX_NUM_LEDS < ledCount) {
    Serial.print(" ERROR: to many LED ");
    Serial.println(ledCount);
  }
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
  }
  return 0;
}

uint8_t set_show() {
  FastLED.show();
  return 0;
}

uint8_t get_crc() {
  Serial.println(checksum(ledCount));
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

bool readColor(color_t *color) {
  bool retval = false;
  if (3 <= Serial.available()) {
    color->red = Serial.read();
    color->green = Serial.read();
    color->blue = Serial.read();
    retval = true;
  }
  return retval;
}

bool readUint16(uint16_t *val) {
  bool retval = false;

  if (2 <= Serial.available()) {
    uint8_t lower = Serial.read();
    uint8_t upper = Serial.read();
    *val = upper;
    *val <<= 8;
    *val |= lower;
    retval = true;
  }

  return retval;
}

uint32_t checksum(uint16_t count) {
  CRC32 crc;
  size_t i;
  for (i = 0; i < count; i++) {
    crc.add(leds[i].r);
    crc.add(leds[i].g);
    crc.add(leds[i].b);
  }
  return crc.calc();
}


void clearIBuff() {
  while (Serial.available() > 0) {
    Serial.read();
  }
}