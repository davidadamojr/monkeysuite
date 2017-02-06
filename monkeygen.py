import sys
import random
import time
import os
import subprocess
import datetime

TEST_SUITE_DIR = "testsuites"
AUT_PACKAGE_NAME = "org.tomdroid"
SDK_PATH = "/home/davidadamojr/Android/Sdk" 
INSTRUMENTATION_CLASS = "com.davidadamojr.tester.EmmaInstrumentation"
DEVICE_COV_PATH = "/mnt/sdcard/" + AUT_PACKAGE_NAME + "/coverage.ec"

def print_usage():
    print "Usage: python monkeygen.py generate [no_of_testcases] [no_of_events]\n python monkeygen.py replay [path_to_suite]"

def create_folders():
    current_time = int(round(time.time() * 1000))
    suite_folder = str(current_time) + "_tests"
    coverage_folder = str(current_time) + "_coverage"
    log_folder = str(current_time) + "_logs"
    suite_path = os.path.join(TEST_SUITE_DIR, AUT_PACKAGE_NAME, suite_folder)
    coverage_path = os.path.join(TEST_SUITE_DIR, AUT_PACKAGE_NAME, coverage_folder)
    log_path = os.path.join(TEST_SUITE_DIR, AUT_PACKAGE_NAME, log_folder)
    if not os.path.isfile(suite_path):
        os.makedirs(suite_path)
    
    if not os.path.isfile(suite_path):
        os.makedirs(coverage_path)
        
    if not os.path.isfile(log_path):
        os.makedirs(log_path)
    
    return (suite_path, coverage_path, log_path)

def collect_coverage():
    pass
        
def generate_testcases(paths):
    suite_path = paths[0]
    cov_path = paths[1]
    log_path = paths[2]
    with open(os.path.join(suite_path, "suite.monkey"), 'w') as suite_file:
        existing_nums = set([])
        adb_path = SDK_PATH + "/platform-tools/adb"
        clear_command = adb_path + " shell pm clear " + AUT_PACKAGE_NAME
        clear_logs_cmd = adb_path + " logcat -c"
        for i in range(1, no_of_testcases+1):
            # clear package data
            subprocess.call(clear_command, shell=True)
            
            # clear adb logs
            subprocess.call(clear_logs_cmd, shell=True)
            
            rand_num = random.randint(0, no_of_testcases)
            while rand_num in existing_nums:
                rand_num = random.randint(0, no_of_testcases*2)
            
            existing_nums.add(rand_num)
            
            # launch app with instrumentation
            app_launch_cmd = adb_path + " shell am instrument -e coverage true " + \
                            "-w " + AUT_PACKAGE_NAME + "/" + INSTRUMENTATION_CLASS
            launched_app = subprocess.Popen(app_launch_cmd, shell=True)
            
            """
            monkey_options = "-v " + str(no_of_events) + \
                            " -s " + str(rand_num) + " --throttle 10000"
            """
            monkey_options = "-p " + AUT_PACKAGE_NAME + " -v " + str(no_of_events) + \
                            " -s " + str(rand_num) + " --throttle 4000 --ignore-crashes --ignore-timeouts"   
            monkey_command = adb_path + " shell monkey " + monkey_options
            subprocess.call(monkey_command, shell=True)     # waits for command to complete
            suite_file.write(str(rand_num) + os.linesep)
            
            # end code coverage collection
            end_broadcast_cmd = adb_path + " shell am broadcast -a com.davidadamojr.tester.finishtesting"
            subprocess.call(end_broadcast_cmd, shell=True)
            
            cov_filename = "coverage" + str(i).zfill(5) + ".ec"
            renamed_local_cov_path = os.path.join(cov_path, cov_filename)
            file_pull_cmd = adb_path + " pull " + DEVICE_COV_PATH + " " + cov_path
            subprocess.call(file_pull_cmd, shell=True)
    
            rename_cmd = "mv " + os.path.join(cov_path, "coverage.ec") + " " + renamed_local_cov_path
            subprocess.call(rename_cmd, shell=True) 
            
            # store logs
            log_filename = "log{}".format(str(i).zfill(5))
            retrieve_logs_cmd = "adb logcat -d *:W > {}".format(os.path.join(log_path, log_filename))
            subprocess.call(retrieve_logs_cmd, shell=True)
       
if len(sys.argv) < 3:
    print_usage()
else:
    task = sys.argv[1]
    if task == "generate":
        if len(sys.argv) != 4:
            print_usage()
        else:
            try:
                no_of_testcases = int(sys.argv[2])
                no_of_events =  int(sys.argv[3])
            except ValueError:
                print_usage()
                sys.exit(0)
            
            paths = create_folders()
            generate_testcases(paths)
    elif task == "replay":
        pass
    else:
        print_usage()