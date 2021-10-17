/* 
 * The sample code requires the ESP8266 v.2.0.0 library for proper operation. 
 * (https://github.com/ubidots/ubidots-esp8266/releases/tag/2.0.0) 
 * However, is strongly recommended to migrate the code to the latest library version.
 * (https://github.com/ubidots/ubidots-esp8266)
 * 
 * Modified by: Augustin Gan.
 * Mod note: All Ubidots connectivity has been removed.
 * Description of sensor: 
 * The MMC5883MA is a complete 3-axis magnetic sensor with on-chip signal processing 
 *   and integrated I2C bus suitable for use in various applications.
 * The device can be connected directly to a microprocessor, 
 *   eliminating the need for A/D converters or timing resources. 
 * It can measure magnetic fields within the full scale range of +-8Gauss(G), 
 *   with 0.25mG per LSB resolution at 16bits operation mode and 0.4mG total RMS noise level, 
 *   enabling heading accuracy of +-1º in electronic compass applications.
 * Contact MEMSIC for access to advanced calibration and tilt-compensation algorithms.
 * An integrated SET/RESET function provides for the elimination of error due 
 *   to Null Field output change with temperature. 
 * Temperature information from the integrated temperature sensor is available over the I2C Interface. 
 * The SET/RESET function can be performed for each measurement, periodically, 
 *   or  when the temperature changes by a predetermined amount as the specific application requires.
 * In addition, the SET/RESET function clears the sensors of any residual magnetic polarization resulting 
 *   from exposure to strong external magnets. 
 * The MMC5883MA is packaged in a low profile LGA package (3.0 x 3.0 x 1.0mm) 
 *   and an operating temperature range from -40C to +85C. 
 * The MMC5883MA provides an I2C digital output with 400 KHz, fast mode operation.
 * 
 * From informal testing:
 * y axis facing North, expect x=-15.9,y=-15.9,z=-15.9
 * y axis facing East , expect x=-15.9,y=-8.0,z=-15.9
 * y axis facing South, expect x=-15.9,y=-0.06,z=-15.9
 * y axis facing West , expect x=-15.9,y=-8.02,z=-15.9
 */

/*
#include "UbidotsMicroESP8266.h"
#define TOKEN  "Your_Token"  // Put here your Ubidots TOKEN
#define WIFISSID "Your_WiFi_SSID" // Put here your Wi-Fi SSID
#define PASSWORD "Your_WiFi_Password" // Put here your Wi-Fi password
Ubidots client(TOKEN);
*/

#include <Wire.h>
/*****************************************************
MMC5883MA Register map
ref: https://media.digikey.com/pdf/Data%20Sheets/MEMSIC%20PDFs/MMC5883MA_RevC_4--28-17.pdf
******************************************************
*/
#define XOUT_LSB    0x00
#define XOUT_MSB    0x01
#define YOUT_LSB    0x02
#define YOUT_MSB    0x03
#define ZOUT_LSB    0x04
#define ZOUT_MSB    0x05
#define TEMPERATURE 0x06      // temperature output
#define STATUS      0x07      // device status
#define INT_CTRL0   0x08      // control register 0
#define INT_CTRL1   0x09
#define INT_CTRL2   0x0A
#define X_THRESHOLD 0x0B      // motion detection threshold of X
#define Y_THRESHOLD 0x0C
#define Z_THRESHOLD 0x0D
#define PROD_ID1    0x2F      // product id

#define MMC5883MA   0x30      // Sensor I2C address
#define MMC5883MA_DYNAMIC_RANGE 16 // Expect readings of 0-16
#define MMC5883MA_RESOLUTION    65536

//*****************************************************
// Functions declaration
//*****************************************************
char read_register(byte REG_ADDR);
void write_register(byte REG_ADDR, byte VALUE);
void wait_meas(void);
void reset_sensor(void);
float parser(char axis_msb, char axis_lsb);

uint8_t count = 0;

//*****************************************************
// Setup
//*****************************************************
void setup() 
{
  Wire.begin();                                   // Join I2C bus (address optional for master)
  Serial.begin(9600);                             // Start USB serial port that Raspi needs to listen to
  //client.wifiConnection(WIFISSID, PASSWORD);
  write_register(INT_CTRL0, 0x04);                // reset internal control - 0x04 is a byte
}  

//*****************************************************
//Main
//*****************************************************
void loop()
{
  Serial.println("---------");                    // To separate each set of readings
  
  // Variables initialization
  char x_lsb, x_msb, y_lsb, y_msb, z_lsb, z_msb;
  float x_val, y_val, z_val;
  uint8_t status_reg = 0;
  uint8_t id = 0;
  uint8_t payload[6] = {};

  reset_sensor(); // Write a byte to ctrl register 1 to forget previous magnetic calibration
  
  write_register(INT_CTRL2, 0x40);                // Enables measurement interrupt
  write_register(STATUS, 0x01);                   // Clean measurement interrupt

  // Check status register before start magnetic field measurement
  status_reg = read_register(STATUS);
  //Serial.print("Status register before: ");
  //Serial.println(status_reg, BIN);
  
  //Serial.println("Starting measurement");
  write_register(INT_CTRL0, 0X01);                // Start magnetic field measurement
  wait_meas();
  
  // Check status register after complete magnetif field measurement
  status_reg = read_register(STATUS);
  //Serial.print("Status register after: ");
  //Serial.println(status_reg, BIN);
  
  x_lsb = read_register(XOUT_LSB);                // Read magnetic field - x lsb
  x_msb = read_register(XOUT_MSB);                // Read magnetic field - x msb
  y_lsb = read_register(YOUT_LSB);                // Read magnetic field - y lsb
  y_msb = read_register(YOUT_MSB);                // Read magnetic field - y msb
  z_lsb = read_register(ZOUT_LSB);                // Read magnetic field - z lsb
  z_msb = read_register(ZOUT_MSB);                // Read magnetic field - z msb

  x_val = parser(x_msb, x_lsb);
  y_val = parser(y_msb, y_lsb);
  z_val = parser(z_msb, z_lsb);

  Serial.print("Xout: ");
  Serial.println(x_val, 7);
  Serial.print("Yout: ");
  Serial.println(y_val, 7);
  Serial.print("Zout: ");
  Serial.println(z_val, 7);

//-------------------------------------------------
  // Ubidots payload
  //client.setDataSourceName("nodemcu_mmc5883ma");
  //client.setDataSourceLabel("nodemcu_mmc5883ma");
  //client.add("x", x_val);
  //client.add("y", y_val);
  //client.add("z", z_val);
  //client.sendAll(true);
//-------------------------------------------------
  delay(6000); //6 sec delay = 1 update/min w window size 10
  //delay(1000); //1 sec delay = 6 update/min w window size 10 //for testing
}

//*****************************************************
// Functions definitions
//*****************************************************
char read_register(byte REG_ADDR)
{
  char reg_value = 0;

  Wire.beginTransmission(byte(MMC5883MA));        // Adress of I2C device
  Wire.write(byte(REG_ADDR));                     // Register address
  Wire.endTransmission();
  
  Wire.requestFrom(byte(MMC5883MA), 1);           // Request 1 byte from I2C slave device
  if (Wire.available() == 1)
  {
    reg_value = Wire.read();                      // Receive a byte as character
  } 
  Wire.endTransmission();
  return reg_value;
}
//-------------------------------------------------
void write_register(byte REG_ADDR, byte VALUE)
{
  Wire.beginTransmission(byte(MMC5883MA));        // Adress of I2C device
  Wire.write(byte(REG_ADDR));                     // Register address
  Wire.write(byte(VALUE));                        // Value to be written
  Wire.endTransmission();
}
//-------------------------------------------------
void reset_sensor()
{
  write_register(INT_CTRL1, 0x80);
  //Serial.println("Sensor reseted");
}
//-------------------------------------------------
void wait_meas()
{
  //Serial.println("Waiting for measurement");
  uint8_t status_reg = 0;
  uint8_t meas_finish = 0;
  byte mask = 1;

  while(meas_finish == 0)
  {
    status_reg = read_register(STATUS);
    meas_finish = status_reg & mask;
  }
  //Serial.println("Measurement finished");
}
//-------------------------------------------------
float parser(char MSB, char LSB)
{
  float ans = (float)(MSB << 8 | LSB) * MMC5883MA_DYNAMIC_RANGE / MMC5883MA_RESOLUTION - (float)MMC5883MA_DYNAMIC_RANGE / 2;
  return ans;
}
