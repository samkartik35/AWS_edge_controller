from subprocess import check_output
import psutil
#name = "test_client.py"
def get_pid(process_name):
   for proc in psutil.process_iter():
       if proc.name() == process_name:
          return proc.pid

print(get_pid("shangdong_parser.py"))
