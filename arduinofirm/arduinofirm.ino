/*
	https://github.com/therealdreg/autobuspirateupgrade
	MIT LICENSE
	David Reguera Garcia aka Dreg @therealdreg
	dreg@fr33project.org
	
	bullshit crappies code in the world
*/

#define POWER_USB_PIN   12
#define PGD_PGC_PIN     11


#define CONNECT_USB_POWER() digitalWrite(POWER_USB_PIN, LOW);
#define DISCONNECT_USB_POWER() digitalWrite(POWER_USB_PIN, HIGH);
#define CONNECT_PGD_PGC() digitalWrite(PGD_PGC_PIN, LOW);
#define DISCONNECT_PGD_PGC() digitalWrite(PGD_PGC_PIN, HIGH);

#define CONNECT_USB_POWER_CHAR      '0'
#define DISCONNECT_USB_POWER_CHAR   '1'
#define CONNECT_PGD_PGC_CHAR        '2'
#define DISCONNECT_PGD_PGC_CHAR     '3'


void setup() 
{
  pinMode(POWER_USB_PIN, OUTPUT);
  DISCONNECT_USB_POWER();
  pinMode(PGD_PGC_PIN, OUTPUT);
  DISCONNECT_PGD_PGC();

  
  Serial.begin(9600);
}

void printhelp(void)
{
       Serial.println("Write one of the following numbers:\n"
              "CONNECT_USB_POWER_CHAR      = '0'\r\n"
              "DISCONNECT_USB_POWER_CHAR   = '1'\r\n"
              "CONNECT_PGD_PGC_CHAR        = '2'\r\n"
			        "DISCONNECT_PGD_PGC_CHAR     = '3'\r\n");
              
}


void loop() 
{

  printhelp();
  delay(500);

  if (Serial.available() > 0) 
  {
    unsigned char byte = Serial.read();
    if (byte >= '0' && byte <= '3')
    {
      switch(byte)
      {
        case CONNECT_USB_POWER_CHAR:
          CONNECT_USB_POWER();
        break;

        case DISCONNECT_USB_POWER_CHAR:
          DISCONNECT_USB_POWER();
        break;

        case CONNECT_PGD_PGC_CHAR:
          CONNECT_PGD_PGC();
        break;

        case DISCONNECT_PGD_PGC_CHAR:
          DISCONNECT_PGD_PGC();
        break;
      }
    }
  }

}
