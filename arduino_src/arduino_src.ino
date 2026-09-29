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
#define MAX_NUM_LEDS 1200

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
uint16_t readUint16();
color_t readColor();

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
uint16_t ledCount;

/**
 * \brief The state command template.
 */
cmd_dic_t setState = { "Ss", &set_led_state_cmd };

cmd_dic_t setCount = { "Cc", &set_led_count_cmd };

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
  FastLED.addLeds< NEOPIXEL, DATA_PIN >(leds, MAX_NUM_LEDS);
  ledCount = 0u;
  set_led_off_cmd();
  Serial.println("READY!");
}
void loop() {
  const cmd_dic_t *dic_p;
  if (Serial.available()) {
    uint8_t curChar = Serial.read();
    for (dic_p = charcheck_dict[0]; dic_p != NULL; dic_p++) {
      if (cmd_check_charset(dic_p->char_class, curChar)) {
        if (dic_p->funptr != NULL) {
          (void)dic_p->funptr();
        }
        break;
      }
    }
  }
  FastLED.show();
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
  uint16_t idx = readUint16();
  Serial.println(idx);
  Serial.println(ledCount);
  if (idx > ledCount) {
    Serial.println("ERROR: idx out of range");
  }
  color_t color = readColor();
  leds[idx].r = color.red;
  leds[idx].g = color.green;
  leds[idx].b = color.blue;
  Serial.println(checksum(ledCount));
  return 0;
}

/**
 * \brief Callback function for the state command.
 *
 * \return not used
 */
uint8_t set_led_count_cmd() {
  ledCount = readUint16();
  if (ledCount > MAX_NUM_LEDS) {
    Serial.println("ERROR: to many LED");
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

color_t readColor() {
  color_t color;
  color.red = Serial.read();
  color.green = Serial.read();
  color.blue = Serial.read();
  return color;
}

uint16_t readUint16() {
  uint8_t lower = Serial.read();
  uint8_t upper = Serial.read();
  uint16_t retval = 0;
  retval = upper;
  retval <<= 8;
  retval |= lower;
  return retval;
}

uint32_t checksum(uint16_t count) {
  CRC32 crc;
  size_t i;
  // Here we add each byte to the checksum, caclulating the checksum as we go.
  for (i = 0; i < count; i++) {
    crc.update(leds[i].r);
    crc.update(leds[i].g);
    crc.update(leds[i].b);
  }
  return crc.finalize();
}