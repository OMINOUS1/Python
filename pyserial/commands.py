"""
 commands.py

    Author : Paul Farrell (@OMINOUS1) (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.14.2

    ~~~~~~~~~~Control Commands
    A0  Start belt with communication timer (close loop speed operation)
    A1  Start belt, communcation timer disabled
    A2  Disengage belt
    A3  Set target speed, MSB 0 is forward, 3 is reverse
    A4  Set target inclination / elevation
    A6  Set maximum elevation
    A7  Set zero offset for belt creep
    A8  OpenLoopGrade
    A9  Start belt, communication timer disabled (closed loop)
    AA  Auto stop
    AB  Sets min grade at power up
    AD  Set belt control type and linear elevation
    88  Brake setting command in amps

    ~~~~~~~~~~Control Command Responsese
    B0  Acknowledge start belt command A0
    B1  Acknowledge start belt command A1
    B2  Acknowledge disengage belt command A2
    B3  Acknowledgeset speed command A3
    B4  Acknowledge sets elevation command A4
    B6  Acknowledge set max elevation command A6
    B7  Acknowledge belt creep command A7
    B9  Acknowledge start belt command A9
    BA  Acknowledge auto stop command AA
    BD
    BE  Invalid data
    BF  Invalid command
    89  Acknowledge set brake setting

    ~~~~~~~~~~Status Query
    C0  Communcation Test
    C1  Transmit previous speed measurment
    C2  Transmit previous inclination measurment
    C3  Transmit sooftware revision
    C4  Transmit time since last start belt command

    ~~~~~~~~~~Status Query Respponse
    D0  0x31 belt stopped, 0x32 belt started, 0x33 belt is running
    D1  Speed measurment
    D2  incline measurment4
    D3  Software revision
    D4  Time response

    """

#~~~~~Imports~~~~
import config

def ctrl(command, value):
    
    cmd = command + value

    config.serCfg.write(cmd)
    print(f'Sending Command: {cmd}')

    response = config.serCfg.readline()
    hex_response = response.hex()
    if response:
        print(f"Received Val: {response}")      # ascii
        print(f"Received Hex: {hex_response}")  # hex
    else:
        print("No response received")

def ctrl_start_belt_wd():
    
    cmd = bytes.fromhex('A0')
    val =bytes.fromhex('')

    ctrl(cmd,val)

def ctrl_start_belt():
    
    cmd = bytes.fromhex('A1')
    val = bytes.fromhex('')

    ctrl(cmd,val)

def ctrl_disengage_belt():
    
    cmd = bytes.fromhex('A2')
    val = bytes.fromhex('')

    ctrl(cmd,val)

def ctrl_belt_speed():
    
    cmd = bytes.fromhex('A3')
    user_input = input("\n>>Enter Speed (0-12.5): ").strip()
    val = bytes.fromhex(user_input)

    ctrl(cmd,val)

def ctrl_belt_elevation():
    
    cmd = bytes.fromhex('A4')
    user_input = input("\n>>Enter Elevation (0-12.5): ").strip()
    val = bytes.fromhex(user_input)

    ctrl(cmd,val)

def ctrl_belt_engage():
    
    cmd = bytes.fromhex('A9')
    val = bytes.fromhex('')

    ctrl(cmd,val)

def ctrl_belt_stop():
    
    cmd = bytes.fromhex('AA')
    val = bytes.fromhex('')

    ctrl(cmd,val)
