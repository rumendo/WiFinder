import subprocess
import time

while True:

    p1 = subprocess.Popen(['netstat', '-lan'], stdout=subprocess.PIPE)

    # Run the command
    output = p1.communicate()[0]

    print(output)

    time.sleep(5)
