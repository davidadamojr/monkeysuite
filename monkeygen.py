import sys
import random
import time
import os
import subprocess

TEST_SUITE_DIR = "testsuites"
APK_FILE = "org.tomdroid_072_aligned.apk"
AUT_PACKAGE_NAME = "org.tomdroid"
SDK_PATH = os.path.join(os.path.expanduser('~'), "Android", "Sdk") 
INSTRUMENTATION_CLASS = "com.davidadamojr.tester.EmmaInstrumentation"
DEVICE_COV_PATH = "/mnt/sdcard/" + AUT_PACKAGE_NAME + "/coverage.ec"
DROPBOX_DIR = os.path.join("Dropbox", "TestSuitesInputDomain", )

def print_usage():
    print "Usage: python monkeygen.py generate [time_in_hours] [no_of_events]\n python monkeygen.py replay [path_to_suite]"

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
        
def generate_testcases(paths, test_gen_time, num_of_events):
    suite_path = paths[0]
    cov_path = paths[1]
    # log_path = paths[2]
    current_milli_time = lambda: int(round(time.time() * 1000))
    test_gen_time = test_gen_time * 3600 * 1000 # convert hours to milliseconds
    adb_path = os.path.join(SDK_PATH, "platform-tools", "adb")
    
    # install APK
    install_cmd = adb_path + " install " + os.path.join("apps", APK_FILE)
    subprocess.call(install_cmd, shell=True)
    
    with open(os.path.join(suite_path, "suite.monkey"), 'w') as suite_file:
        existing_nums = set([])
        clear_cache_cmd = adb_path + " shell pm clear " + AUT_PACKAGE_NAME
        # clear_logs_cmd = adb_path + " logcat -c"
        clear_sdcard_cmd = adb_path + " shell rm -rf /mnt/sdcard/*"
        uninstall_app_cmd = adb_path + " uninstall " + AUT_PACKAGE_NAME
        test_suite_start_time = current_milli_time()
        
        test_case_num = 1
        while current_milli_time() < test_gen_time:
            # clear package data
            subprocess.call(clear_cache_cmd, shell=True)
                
            # clear adb logs
            # subprocess.call(clear_logs_cmd, shell=True)
            
            rand_num = random.randint(0, 1000000)
            while rand_num in existing_nums:
                rand_num = random.randint(0, 1000000)
            existing_nums.add(rand_num)
            
            # launch app with instrumentation
            app_launch_cmd = adb_path + " shell am instrument -e coverage true " + \
                            "-w " + AUT_PACKAGE_NAME + "/" + INSTRUMENTATION_CLASS
            subprocess.Popen(app_launch_cmd, shell=True)
    
            monkey_options = "-p " + AUT_PACKAGE_NAME + " -v " + str(num_of_events) + \
                            " -s " + str(rand_num) + " --throttle 2000 --ignore-crashes --ignore-timeouts"   
            monkey_cmd = adb_path + " shell monkey " + monkey_options
            subprocess.call(monkey_cmd, shell=True)     # waits for command to complete
            suite_file.write(str(rand_num) + os.linesep)
            test_case_end_time = current_milli_time() - test_suite_start_time
            
            collect_code_coverage(adb_path, test_case_num, cov_path, test_case_end_time)
            
            # collect_logs(adb_path, test_case_num, cov_path, test_case_end_time)
                
            test_case_num = test_case_num + 1
            
        subprocess.call(clear_sdcard_cmd, shell=True)
        subprocess.call(uninstall_app_cmd, shell=True)

def collect_code_coverage(adb_path, test_case_num, cov_path, test_case_end_time):
    # collect code coverage info
    end_broadcast_cmd = adb_path + " shell am broadcast -a com.davidadamojr.tester.finishtesting"
    subprocess.call(end_broadcast_cmd, shell=True)
    
    cov_filename = "coverage" + str(test_case_num).zfill(5) + "_" + str(test_case_end_time) + ".ec"
    renamed_local_cov_path = os.path.join(cov_path, cov_filename)
    file_pull_cmd = adb_path + " pull " + DEVICE_COV_PATH + " " + cov_path
    subprocess.call(file_pull_cmd, shell=True)
    
    rename_cmd = "mv " + os.path.join(cov_path, "coverage.ec") + " " + renamed_local_cov_path
    subprocess.call(rename_cmd, shell=True) 

# def collect_logs(adb_path, log_path, test_case_num, test_case_end_time):
#     log_filename = "log{}".format(str(test_case_num).zfill(5))
#     retrieve_logs_cmd = adb_path + " logcat -d *:W > {}".format(os.path.join(log_path, log_filename))
#     subprocess.call(retrieve_logs_cmd, shell=True)
       
if len(sys.argv) < 3:
    print_usage()
else:
    task = sys.argv[1]
    if task == "generate":
        if len(sys.argv) != 4:
            print_usage()
        else:
            try:
                test_gen_time = int(sys.argv[2])
                num_of_events =  int(sys.argv[3])
            except ValueError:
                print_usage()
                sys.exit(0)
            
            paths = create_folders()
            generate_testcases(paths, test_gen_time, num_of_events)
    elif task == "replay":
        pass
    else:
        print_usage()
