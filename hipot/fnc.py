"""
fnc.py

    API to hold functions for the hipot tests

    Author : Paul Farrell (@OMINOUS1) (Paulf@woodway.com)

    LAST DEVELOPED FOR: Python 3.14.2

"""

#~~~~~ Imports ~~~~~
import time
import config
from decimal import Decimal

#~~~~~ Functions ~~~~~
def run():

    print("\nEnter Serial Number of DUT")
    serial_number = input(">>Serial Number: ")

    # ascii commands 
    # Need to be terminated by Line Feed (\n) or Carriage return (\r)
    run = 'RUN\n'
    run_qry = 'RUN?\n'
    stat = 'STAT?\n'
    rslt = 'RSLT?\n'
    stprslt1 = 'STEPRSLT?,1\n'
    stprslt2 = 'STEPRSLT?,2\n'

    # convering ascii commands into bytes to send
    run_cmd = run.encode('utf-8')
    run_qry_cmd = run_qry.encode('utf-8')
    stat_cmd = stat.encode('utf-8')
    rslt_cmd = rslt.encode('utf-8')
    stprslt1_cmd = stprslt1.encode('utf-8')
    stprslt2_cmd = stprslt2.encode('utf-8')

    # run command
    print("\n********* RUNNING HIPOT TEST SEQUENCE *********")
    print("******** HIGH VOLTAGE DO NOT TOUCH DUT ********")
    config.serCfg.write(run_cmd)
    
    isTestRunning = True
    while isTestRunning:
        
        # poll to see if test is still runnings
        config.serCfg.write(run_qry_cmd)
        testRunningVal = config.serCfg.readline().decode('ascii').replace('\n', '').replace('\r', '')
        
        if testRunningVal == '1':
            time.sleep(0.1)  # delay in secounds for test period

        elif testRunningVal == '0':
            isTestRunning = False
    
    print("\nTest Complete\n")

    print(f'Device Serial Number: {serial_number}')

    # status inquery
    config.serCfg.write(stat_cmd)
    stat_response = config.serCfg.readline()
    str_stat = stat_response.decode('ascii').replace('\n', '').replace('\r', '')
    stat = read_stat_flag(str_stat)
    print(f'Test Status: {stat}')

    # results inquery
    config.serCfg.write(rslt_cmd)
    rslt_response = config.serCfg.readline()
    str_rslt = rslt_response.decode('ascii').replace('\n', '').replace('\r', '')
    rslt = read_rslt_flag(str_rslt)
    print(f'Test Result: {rslt}\n')

    # test sequence 1 inquery
    config.serCfg.write(stprslt1_cmd)
    stp_rslt1 = config.serCfg.readline()
    str_stp_rslt1 = stp_rslt1.decode('ascii').replace('\n', '').replace('\r', '')
    print(f'Ground Bond (GB) Test Results: ')#{str_stp_rslt1}')
    stprslt_split1(str_stp_rslt1)

    # test sequence 2 inquery
    config.serCfg.write(stprslt2_cmd)
    stp_rslt2 = config.serCfg.readline()
    str_stp_rslt2 = stp_rslt2.decode('ascii').replace('\n', '').replace('\r', '')
    print(f'\nAC Voltage Withstand (ACW) Test Results: ')#{str_stp_rslt2}')
    stprslt_split2(str_stp_rslt2)

def stprslt_split1(val):

    array = val.split(',')

    termination = read_termination(array[0])
    time = Decimal(array[1].strip())
    stat = read_rslt_flag(array[2])
    level = Decimal(array[3].strip())
    #breakdown = Decimal(array[4].strip())  #NOT USED
    measurment = Decimal(array[5].strip())
    #arc = Decimal(array[6].strip())        #NOT USED 
    print(f'\tTermination Value: {termination}')
    print(f'\tElapsed Time: {time} seconds')
    print(f'\tStatus Code: {stat}')
    print(f'\tLevel: {level} Amps')
    #print(f'\tBreakdown: {breakdown} Amps')
    print(f'\tMeasurment: {measurment} Ohms')
    #print(f'\tArc Current: {arc} Amps\n')

def stprslt_split2(val):

    array = val.split(',')

    termination = read_termination(array[0])
    time = Decimal(array[1].strip())
    stat = read_rslt_flag(array[2])
    level = Decimal(array[3].strip())
    breakdown = Decimal(array[4].strip())
    measurment = Decimal(array[5].strip())
    #arc = Decimal(array[6].strip())
    print(f'\tTermination Value: {termination}')
    print(f'\tElapsed Time: {time} seconds')
    print(f'\tStatus Code: {stat}')
    print(f'\tLevel: {level} Volts')
    print(f'\tBreakdown: {breakdown} Amps')
    print(f'\tMeasurment: {measurment} Amps')
    #print(f'\tArc Current: {arc} Amps\n')

def read_stat_flag(val):
    stat_flag = 'DEADBEEF'

    match val:

        case 'PP':
            stat_flag = 'PASS'
        case 'F-':
            stat_flag = 'FAILURE'
        case '--':
            stat_flag = 'Not Performed'
        case '??':
            stat_flag = 'In Process'

    return stat_flag

def read_termination(val):
    termination_flag = 'DEADBEEF'

    match val:

        case '0':
            termination_flag = 'Not Executed'
        case '1':
            termination_flag = 'Terminated before fully started'
        case '2':
            termination_flag = 'Terminated during Ramp'
        case '3':
            termination_flag = 'Terminated during Dwell'

    return termination_flag

def read_rslt_flag(val):
    rslt_flag = 'DEADBEEF'

    match val:

        case '0':
            rslt_flag = 'No Failure'
        case '1':
            rslt_flag = 'V74 Internal Fault'
        case '2':
            rslt_flag = 'Over Voltage output'
        case '4':
            rslt_flag = 'Line too low to implement configued voltage/current'
        case '8':
            rslt_flag = 'DUT Breakdown detected'
        case '16':
            rslt_flag = 'HOLD step timeout occured'
        case '32':
            rslt_flag = 'User aborted the sequence'
        case '64':
            rslt_flag = 'Ground Bond (GB) step was over-compliance'
        case '128':
            rslt_flag = 'Arc detected'
        case '256':
            rslt_flag = 'Below Maximum Limit'
        case '512':
            rslt_flag = 'Above Maximum Limit'
        case '1024':
            rslt_flag = 'IR Failure - WRONG TEST'
        case '2048':
            rslt_flag = 'INTERLOCK Failure'
        case '4096':
            rslt_flag = 'Switch Matrix Error'
        case '8192':
            rslt_flag = 'V74 Overheated'
        case '16384':
            rslt_flag = 'DUT voltage or current could not be controlled'
        case '32768':
            rslt_flag = 'Wiring error detected in Ground Bond (GB) step'
        case '65536':
            rslt_flag = 'Unstable ramp voltage or rapid varying of leakage current'

    return rslt_flag
