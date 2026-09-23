/**
 * \file arduino_src.ino
 * \brief Arduino project for basic control of a string of LED.
 */


#include "FastLED.h"

/*************************************************************************************************/
/************************** Defines **************************************************************/
/*************************************************************************************************/


/**
 * \brief The size the LED array. Bounded by memory size of the uc in relation to serial buffer
 *needs.
 */
#define MAX_NUM_LEDS 1200

/**
 * \brief The size the serial buffer array. Bounded by memory size of the uc.
 */
#define MAX_SERIAL_BUFFER ((3 * MAX_NUM_LEDS) + 2)

/**
 * \brief Physical pin the LED are connected to.
 */
#define DATA_PIN 6

/*************************************************************************************************/
/************************** Private Function Declarations ****************************************/
/*************************************************************************************************/

uint8_t set_led_state_cmd(uint8_t *buff, size_t count);
uint8_t set_led_off_cmd(uint8_t *buff, size_t count);
bool cmd_check_charset(const char *valid_chars, const char str_char);
void log(char *msg);

/*************************************************************************************************/
/*************************************************************************************************/
/*************************************************************************************************/

/**
 * \typedef cmd_handler_funptr_t
 * \brief Function pointer type for a command handler callback function.
 */
typedef uint8_t (*cmd_handler_funptr_t)(uint8_t *buff, size_t count);

/**
 * \struct cmd_dic_t
 * \brief The storage type for a serial command.
 *
 */
typedef struct cmd_dic_t {
  char *char_class;            /**< The class of char that indicate a command.*/
  cmd_handler_funptr_t funptr; /**< The callback used to process the command.*/
} cmd_dic_t;

/*************************************************************************************************/
/************************** Local Variables ******************************************************/
/*************************************************************************************************/

/**
 * \brief The collection of LED objects.
 */
CRGB leds[MAX_NUM_LEDS];

/**
 * \brief The serial buffer.
 */
uint8_t serial_buffer[MAX_SERIAL_BUFFER];


/**
 * \brief The state command template.
 */
cmd_dic_t setState = { "Ss", &set_led_state_cmd };

/**
 * \brief The off command template.
 */
cmd_dic_t setOff = { "oO", &set_led_off_cmd };

/**
 * \brief The collection of commands. Must be NULL terminated.
 */
const cmd_dic_t *charcheck_dict[] = { &setState, &setOff, NULL };

/*************************************************************************************************/
/************************** Primary Arduino Event Loop *******************************************/
/*************************************************************************************************/

void setup() {
  /* initialize serial: */
  Serial.begin(115200);
  FastLED.addLeds< NEOPIXEL, DATA_PIN >(leds, MAX_NUM_LEDS);
}

void loop() {
  FastLED.show();
}

void clearBuffer() {
  size_t i;

  for (i = 0; i < MAX_SERIAL_BUFFER - 1; i++) {
    serial_buffer[i] = '\0';
  }
}

void serialEvent() {
  /*Initialize the character checking dictionary*/
  const cmd_dic_t *dic_p;

  if (Serial.available()) {
    size_t inCnt =
      (size_t)Serial.readBytes(serial_buffer, MAX_SERIAL_BUFFER - 1);

    if (inCnt == 0) {
      log("ERROR: Issue with reading bytes from serial");
    }

    if (serial_buffer[inCnt] != '\n') {
      log("ERROR: Issue with reading bytes from serial");
    }

    serial_buffer[inCnt] = '\0';
    for (dic_p = charcheck_dict[0]; dic_p != NULL; dic_p++) {
      if (cmd_check_charset(dic_p->char_class, serial_buffer[0])) {
        (void)dic_p->funptr(serial_buffer, inCnt);
        break;
      }
    }
    if (dic_p == NULL) {
      log("ERROR: Issue with processing command from serial.");
    }
  }
  clearBuffer();
}

/*************************************************************************************************/
/************************** Private Function Definitions *****************************************/
/*************************************************************************************************/

/**
 * \brief Callback function for the state command.
 *
 * \param buff buffer to process.
 * \param count Number of bytes in the buffer.
 * \return not used
 */
uint8_t set_led_state_cmd(uint8_t *buff, size_t count) {
  if ((count <= 2) || ((count - 2) % 3)) {
    log("ERROR: Issue with state command");
  } else {
    size_t i;
    buff++;
    count -= 2;

    for (i = 0; i * 3 < count; i++) {
      leds[i].r = buff[i * 3];
      leds[i].g = buff[i * 3 + 1];
      leds[i].b = buff[i * 3 + 2];
    }
    for (; i < MAX_NUM_LEDS; i++) {
      leds[i].r = 0;
      leds[i].g = 0;
      leds[i].b = 0;
    }
  }
  return 0;
}

/**
 * \brief Callback function for the state command.
 *
 * \param buff buffer to process.
 * \param count Number of bytes in the buffer.
 * \return not used
 */
uint8_t set_led_off_cmd(uint8_t *buff, size_t count) {
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

/**
 * \brief Send a serial response with a payload.
 *
 * \param msg The message to send.
 */
void log(char *msg) {
  Serial.write(msg);
}