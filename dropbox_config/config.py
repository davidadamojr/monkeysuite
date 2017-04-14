import os

HOME_FOLDER = os.path.expanduser("~")
MONKEY_CMD = "python monkeygen.py generate 2 193"
DESTINATION_FOLDER = os.path.join(HOME_FOLDER, "Dropbox", "TestSuitesInputDomain", "MoneyBalance_1", "Monkey")
AUT_PACKAGE = "ivl.android.moneybalance"
TAR_PREFIX = "ivl.android.moneybalance_768_1280_444"
STRATEGY_TAG = "monkey"
MACHINE_NAME = "SELL"
GENYMOTION_PATH = os.path.join(HOME_FOLDER, "genymotion", "player")
VM_NAME = "7eb76928-3531-41b4-8ad9-1344d11087ef"
