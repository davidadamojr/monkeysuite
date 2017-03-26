import sys
import os
import tarfile
import subprocess
import shutil
from dropbox_config import config

START_COUNT = int(sys.argv[2])

# first argument to script is the number of test suites to generate
num_test_suites = int(sys.argv[1])

if START_COUNT < 0:
    test_suites_generated = 0
else:
    test_suites_generated = START_COUNT - 1

while test_suites_generated < (START_COUNT - 1) + num_test_suites:
    
    subprocess.call(config.MONKEY_CMD, shell=True)
    test_suite_dir = os.path.join("testsuites", config.AUT_PACKAGE)
    test_suite_file_names = os.listdir(test_suite_dir)
    tar_file_name = "{}_{}_{}_{}.tar.gz".format(config.TAR_PREFIX, str(test_suites_generated + 1), 
                                                config.STRATEGY_TAG, config.MACHINE_NAME)
    with tarfile.open(os.path.join(test_suite_dir, tar_file_name), "w:gz") as compressed_file:
        for file_name in test_suite_file_names:
            compressed_file.add(os.path.join(test_suite_dir, file_name), file_name)
    
    # copy to dropbox
    print "Copying test suite archive to destination folder..."
    try:
        if not os.path.exists(config.DESTINATION_FOLDER):
            os.makedirs(config.DESTINATION_FOLDER)
        
        shutil.copyfile(os.path.join(test_suite_dir, tar_file_name), 
                        os.path.join(config.DESTINATION_FOLDER, tar_file_name))
    except Exception as e:
        print "Unable to copy archive to destination folder."
        failed = True
    
    # delete all files in test suite directory
    print "Deleting test suite files..."
    test_suite_file_names = os.listdir(test_suite_dir)
    for file_name in test_suite_file_names:
        file_path = os.path.join(test_suite_dir, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print "Unable to delete file: {}".format(file_name)
    
    if failed:
        print "An error occurred. Test suite generation was not completed successfully."
        break

if not failed:
    print "Successfully generated {} test suites.".format(str(test_suites_generated))
    