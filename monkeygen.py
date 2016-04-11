import sys
import random
import time
import os

TEST_SUITE_DIR = "testsuites"
AUT_PACKAGE_NAME = "org.tomdroid"
SDK_PATH = "/home/davidadamojr/Android/Sdk" 

def print_usage():
    print "Usage: python monkeygen.py generate [no_of_testcases] [no_of_events]\n python monkeygen.py replay [path_to_suite]"
    
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
            
            suite_name = time.time() + "_suite.monkey"
            suite_path = os.path.join(TEST_SUITE_DIR, suite_name)
            if not os.path.isfile(suite_path):
                os.makedirs(suite_path)
            
            existing_nums = set([])
            with open(suite_path) as suite_file:
                rand_num = random.randint(0, no_of_testcases)
                while rand_num in existing_nums:
                    rand_num = random.randint(0, no_of_testcases*2)
                
                existing_nums.add(rand_num)
                adb_path = SDK_PATH + "/platform-tools/adb"
                monkey_options = "-p " + AUT_PACKAGE_NAME + " -v " + no_of_events + " -s " + rand_num
                monkey_command = adb_path + " shell monkey " + monkey_options
            
            
            
        
            
        
    elif task == "replay":
        pass
    else:
        print_usage()