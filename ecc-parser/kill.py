import os
import psutil
# Iterate over all running process
for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        processName = proc.name()
        processID = proc.pid
        #print(processName , ' ::: ', processID)
        if(processName =="python3"):
            os.kill(processID,9)
            print("Killed process:")
            print(processName)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

