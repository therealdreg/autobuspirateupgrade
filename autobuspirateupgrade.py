# pip install pyserial

# https://github.com/therealdreg/autobuspirateupgrade
# MIT LICENSE
# David Reguera Garcia aka Dreg @therealdreg
# dreg@fr33project.org
#
# bullshit crappies code in the world

COMNAME_ARDUINO   = 'COM69'
COMNAME_BUSPIRATE = 'COM96'

import serial
import time
import os
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

CONNECT_USB_POWER_CHAR      = b"\x30"
DISCONNECT_USB_POWER_CHAR   = b"\x31"
CONNECT_PGD_PGC_CHAR        = b"\x32"
DISCONNECT_PGD_PGC_CHAR     = b"\x33"


def serial_ports():
    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def yes_bootloader():
    try: 
        bser = serial.Serial(
            port=COMNAME_BUSPIRATE,
            baudrate=115200,
            timeout = 1
        )
    except Exception as e:
        print("error open serial port: ", str(e))
        exit()

    if bser.isOpen():

        try:
            bser.flushInput() #flush input buffer, discarding all its contents
            bser.flushOutput()#flush output buffer, aborting current output 
                     #and discard all that is in buffer

            bser.write(b"\x20")
            print("please wait.. dont close this program!!")
            time.sleep(2)
            response = bser.readlines()
            print("read data: ")
            pp.pprint(response)
            bser.write(b"Yes\r\n")
            print("please wait.. dont close this program!!")
            time.sleep(5)
            response = bser.readlines()
            print("read data: ")
            pp.pprint(response)
            
        except Exception as e1:
            print("error communicating...: ", str(e1))
            exit()

    else:
        print("cannot open serial port ")
        exit()



def self_test():
    try: 
        bser = serial.Serial(
            port=COMNAME_BUSPIRATE,
            baudrate=115200,
            timeout = 1
        )
    except Exception as e:
        print("error open serial port: ", str(e))
        exit()

    if bser.isOpen():

        try:
            bser.flushInput() #flush input buffer, discarding all its contents
            bser.flushOutput()#flush output buffer, aborting current output 
                     #and discard all that is in buffer

            bser.write(b"i\r\n")
            bser.write(b"m\r\n")
            print("please wait.. dont close this program!!")
            time.sleep(2)
            response = bser.readlines()
            print("read data: ")
            pp.pprint(response)
            if str(response).find("Community Firmware v7.1") != -1 and str(response).find("Bootloader v4.5") != -1:
                print("\n\nOK!! installed correctly new firmware (7.1) + new bootloader (4.5)\n\n")
            else:
                print("\n\n\Craap incorrect bootloader+firm")
                exit()
                
            bser.write(b"~\r\n")
            print("please wait.. dont close this program!!")
            time.sleep(5)
            response = bser.readlines()
            print("read data: ")
            pp.pprint(response)
            
            input("\nHey ! Check leds and Press Enter to continue...")
            bser.write(b"\x20")
            print("please wait.. dont close this program!!")
            time.sleep(2)
            response = bser.readlines()
            print("read data: ")
            pp.pprint(response)
            
            if  str(response).find("Found 0 errors") != -1:
                print("\n\nHooorayyyy self_test + new_bootloader + new_firmware works fine!!! bus pirate is ready to use")
                exit()
            
        except Exception as e1:
            print("error communicating...: ", str(e1))
            exit()

    else:
        print("cannot open serial port ")
        exit()


if len(sys.argv) >= 2:
    COMNAME_ARDUINO = sys.argv[1]

print("Arduino PORT: ", COMNAME_ARDUINO)


try: 
    ser = serial.Serial(
        port=COMNAME_ARDUINO,
        baudrate=9600,
        timeout = 1
    )
except Exception as e:
    print("error open serial port: ", str(e))
    exit()

if ser.isOpen():

    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output 
                 #and discard all that is in buffer

        response = ser.readline()
        print("read data: ", str(response))
        
        ser.write(DISCONNECT_USB_POWER_CHAR)
        time.sleep(5)
        print("Serial ports: ")
        old_ports = serial_ports()
        pp.pprint(old_ports)
        print(" - ")
        ser.write(CONNECT_USB_POWER_CHAR)
        time.sleep(5)
        print("New serial ports: ")
        new_ports = serial_ports()
        pp.pprint(new_ports)
        print(" - ")
        new_ports = list(set(new_ports) - set(old_ports))
        pp.pprint(new_ports)

        COMNAME_BUSPIRATE = new_ports[0]
        print("Bus pirate: ", COMNAME_BUSPIRATE)
        time.sleep(1)

        ser.write(DISCONNECT_USB_POWER_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(8)
        ser.write(CONNECT_PGD_PGC_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(2)
        ser.write(CONNECT_USB_POWER_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(10)
        os.system("pirate-loader.exe --dev=" + COMNAME_BUSPIRATE + " --hex=BPv3-bootloader-upgrade-v4xtov4.5.hex")
        print("please wait.. dont close this program!!")
        time.sleep(5)
        ser.write(DISCONNECT_USB_POWER_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(2)
        ser.write(DISCONNECT_PGD_PGC_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(5)
        ser.write(CONNECT_USB_POWER_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(10)
        yes_bootloader()
        ser.write(DISCONNECT_USB_POWER_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(5)
        ser.write(CONNECT_PGD_PGC_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(2)
        ser.write(CONNECT_USB_POWER_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(10)
        os.system("pirate-loader.exe --dev=" + COMNAME_BUSPIRATE + " --hex=busPirate-JTAG_SAFE_1.hex")
        print("please wait.. dont close this program!!")
        time.sleep(5)
        ser.write(DISCONNECT_USB_POWER_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(2)
        ser.write(DISCONNECT_PGD_PGC_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(2)
        ser.write(CONNECT_USB_POWER_CHAR)
        print("please wait.. dont close this program!!")
        time.sleep(10)
        self_test()
          
    except Exception as e1:
        print("error communicating...: ", str(e1))

else:
    print("cannot open serial port ")
    
print("\n\ncraaap dont works, check log")
