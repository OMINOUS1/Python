"""
fnc.py

    API to hold functions for the hipot tests

    Author : Paul Farrell (@OMINOUS1) (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.14.2

"""

#~~~~~ Imports ~~~~~
import time
import config

#~~~~~ Functions ~~~~~
def run():

    print("\nEnter Serial Number of DUT")
    serial_number = input(">>Serial Number: ")

    # ascii commands 
    # Need to be terminated by Line Feed (\n) or Carriage return (\r)
    run = 'RUN\n'
    stat = 'STAT?\n'
    rslt = 'RSLT?\n'
    stprslt1 = 'STEPRSLT?,1\n'
    stprslt2 = 'STEPRSLT?,2\n'

    # convering ascii commands into bytes to send
    run_cmd = run.encode('utf-8')
    stat_cmd = stat.encode('utf-8')
    rslt_cmd = rslt.encode('utf-8')
    stprslt1_cmd = stprslt1.encode('utf-8')
    stprslt2_cmd = stprslt2.encode('utf-8')

    # run command
    print("\n**********RUNNING HIPOT TEST SEQUENCE**********")
    print("*********HIGH VOLTAGE DO NOT TOUCH DUT*********")
    config.serCfg.write(run_cmd)
    time.sleep(20)  # delay in secounds for test period
    print("\nTest Complete\n")

    print(f'Device Serial Number: {serial_number}')

    # status inquery
    config.serCfg.write(stat_cmd)
    stat_response = config.serCfg.readline()
    str_stat = stat_response.decode('ascii')
    stat = read_stat_flag(str_stat)
    print(f'Test Status: {stat}')

    # results inquery
    config.serCfg.write(rslt_cmd)
    rslt_response = config.serCfg.readline()
    str_rslt = rslt_response.decode('ascii')
    rslt = read_rslt_flag(str_rslt)
    print(f'Test Result: {rslt}')

    # test sequence 1 inquery
    config.serCfg.write(stprslt1_cmd)
    stp_rslt1 = config.serCfg.readline()
    str_stp_rslt1 = stp_rslt1.decode('ascii').replace('\n', '').replace('\r', '')
    print(f'Ground Bond (GB) Test Results: {str_stp_rslt1}')

    # test sequence 2 inquery
    config.serCfg.write(stprslt2_cmd)
    stp_rslt2 = config.serCfg.readline()
    str_stp_rslt2 = stp_rslt2.decode('ascii').replace('\n', '').replace('\r', '')
    print(f'AC Voltage Withstand (ACW) Test Results: {str_stp_rslt2}')

def read_stat_flag(val):
    stat_flag = 'DEADBEEF'

    match val:

        case 'PP\r\n':
            stat_flag = 'PASS'
        case 'F-\r\n':
            stat_flag = 'FAILURE'
        case '--\r\n':
            stat_flag = 'Not Performed'
        case '??\r\n':
            stat_flag = 'In Process'

    return stat_flag


def read_rslt_flag(val):
    rslt_flag = 'DEADBEEF'

    match val:

        case '0\r\n':
            rslt_flag = 'No Failure'
        case '1\r\n':
            rslt_flag = 'V74 Internal Fault'
        case '2\r\n':
            rslt_flag = 'Over Voltage output'
        case '4\r\n':
            rslt_flag = 'Line too low to implement configued voltage/current'
        case '8\r\n':
            rslt_flag = 'DUT Breakdown detected'
        case '16\r\n':
            rslt_flag = 'HOLD step timeout occured'
        case '32\r\n':
            rslt_flag = 'User aborted the sequence'
        case '64\r\n':
            rslt_flag = 'Ground Bond (GB) step was over-compliance'
        case '128\r\n':
            rslt_flag = 'Arc detected'
        case '256\r\n':
            rslt_flag = 'Below Maximum Limit'
        case '512\r\n':
            rslt_flag = 'Above Maximum Limit'
        case '1024\r\n':
            rslt_flag = 'IR Failure - WRONG TEST'
        case '2048\r\n':
            rslt_flag = 'INTERLOCK Failure'
        case '4096\r\n':
            rslt_flag = 'Switch Matrix Error'
        case '8192\r\n':
            rslt_flag = 'V74 Overheated'
        case '16384\r\n':
            rslt_flag = 'DUT voltage or current could not be controlled'
        case '32768\r\n':
            rslt_flag = 'Wiring error detected in Ground Bond (GB) step'
        case '65536\r\n':
            rslt_flag = 'Unstable ramp voltage or rapid varying of leakage current'

    return rslt_flag
