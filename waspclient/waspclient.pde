#include <WaspXBee802.h>
#include <time.h>

#include "definitions.h"

int FLAG_SERVER_AVAILABLE = 0;
char* SERVER_ADDR; 

int DEEPTIME = 0;

int cycle = 0;

void setup_acc()
{
  ACC.ON();
  detect_shake();

  clearINT();
  
  USB.OFF();
}

void send_status()
{
  
  char timestr[31];
  
  strncpy(timestr, RTC.getTime(), sizeof(timestr));
  float batteryLevel = PWR.getBatteryLevel();
  int x_acc = ACC.getX();
  int y_acc = ACC.getY();
  int z_acc = ACC.getZ();
  unsigned long ep = RTC.getEpochTime();
  
  int cause = 0;
  if(intFlag & ACC_INT) {
    cause = 1;
  } else if(intFlag & RTC_INT) {
    cause = 2;
  }
  
  // Send data message
  char msg[MAX_LENGTH + 1];
  generate_status_packet(msg, ep, x_acc, y_acc, z_acc, batteryLevel, cause);
  
  USB.println(msg);
  
  int err = sendTextPacket(SERVER_ADDR, msg);
  delay(1500);
  
  if(err == 0) {
    USB.println("\n\n *** Waspmote send status *** ");
    USB.println(timestr);
    USB.print("(X,Y,Z) = ("); USB.print(", "); USB.print(x_acc); USB.print(", "); USB.print(y_acc); USB.print(", "); USB.print(z_acc); USB.println(")");
    USB.print("Battery level = "); USB.print(batteryLevel); USB.println(" %");

    USB.print("Waspmote wakes up | Caused by : ");
    if(intFlag & ACC_INT) {
      USB.println("Device was moved");
    } else if(intFlag & RTC_INT) {
      USB.println("Time expired");
    } else {
      USB.println("Unknown");
    }

    USB.println("\n\n");
  }
  
}

/////////////

void detect_shake()
{
  ACC.setIWU();
}

void setup()
{
  int8_t err;
  
  USB.ON();
  RTC.ON();
  
  // Activate the XBee radio
  if (err = commInit(0))
  {
    USB.println(F("Radio failed. Exiting ..."));
    exit(0);
  }
  USB.println(("\nRadio initialized"));
}


void loop()
{
  if(FLAG_SERVER_AVAILABLE == 0) {
    int8_t err;
    char data[MAX_LENGTH + 1];
    char from[17];
    static uint16_t np = 0;
    
    err = receiveTextPacket(from, data, RECEIVER_TIMEOUT);
    if (err == 0) // Espera a que el servidor envíe un mensaje de inicio de comunicación
    {
      FLAG_SERVER_AVAILABLE = 1;
      SERVER_ADDR = from;
      
      unsigned long unixtime;
      if(parse_start_packet(data, &unixtime, &DEEPTIME)) {
        
        set_unixtime(unixtime);
        
        // ACK mensaje de inicio de comunicación
        char response[MAX_LENGTH + 1] = "OK\0";
        
        err = sendTextPacket(from, response);
        
        delay(1500);
        
        if(err == 0) {
          FLAG_SERVER_AVAILABLE = 1;
          SERVER_ADDR = from;
          
          setup_acc();
        }
        
      }
      
    }
  } else {
      
    // Re-init modules
    // This is necessary if we use ALL_OFF in PWR.deepSleep
    USB.ON();
    
    if(cycle > 0) {
      
      send_status();
      
    }

    clearINT();

    cycle++;
    
    // Switch all modules off and deep sleep for five seconds
    char deepstr[12];
    sprintf(deepstr, "00:00:00:%02d", DEEPTIME);
    
    PWR.deepSleep(deepstr, RTC_OFFSET, RTC_ALM1_MODE2, ALL_OFF);
    
    USB.println("Reconnects XBee");
    commInit(0);
  }
}

