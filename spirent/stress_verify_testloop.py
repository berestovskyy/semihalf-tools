import glob, os
import time
import random
from StcPython import StcPython

############# AUTOMATED TESTS LOOP ################
### Loop some stress files for some time ##########
### Then run verification tests ###################
### Loop stress files again, etc. #################
###################################################

# NOTE: tests are configured as follows:
#	Port 1/1 default gateway - 192.168.202.2/24
#	Port 1/2 default gateway - 192.168.203.2/24
#	Chassis IP 		 - 10.2.100.6

STRESS_TESTS_DIR = 		'stress_tests'
VERIFICATION_TESTS_DIR = 	'verification_tests'
STRESS_TESTS_TO_RUN = 		6			# how many random stress tests to run in iteration
SAPEE_TEST_LEN = 		45			# SAPEE test duration in minutes

# Collect test files
stress_test_files = glob.glob(os.path.join(STRESS_TESTS_DIR, '*.xml'))
verification_test_files = glob.glob(os.path.join(VERIFICATION_TESTS_DIR, '*.xml'))

# Create Spirent API instance
stc = StcPython()

# Common setup before test
def common_init(test_dir, file_name):
# Create project - the root object
	hProject = stc.create("project")

# Print WARN and ERROR messages
	stc.config("automationoptions", logTo='stdout', logLevel='WARN')

# Load configuration from XML, set results dir, set sequencer to stop on error
	stc.perform('loadfromxml', filename=file_name)
	results_dir = os.path.join(test_dir, os.path.basename(os.path.splitext(testfile)[0]))
	stc.config(hProject + '.testResultSetting', saveResultsRelativeTo='NONE', resultsDirectory=results_dir)
	stc.config('system1.sequencer', errorHandler='STOP_ON_ERROR')


# Attach chassis ports and apply configuration
def attach_and_apply():
# Connect to chassis and try to reserve and map the ports. Set RevokeOwner to TRUE to
# kick out the other user (takes a minute)
	rv = stc.perform('attachPorts', RevokeOwner='FALSE')
	if not rv:
		print("Error: Failed to reserve ports - exiting..\n")
		exit(1)

# Apply configuration (verify and upload to chassis)
	stc.apply()


def run_stress_test(file_name):
	common_init(STRESS_TESTS_DIR, file_name)
	attach_and_apply()

	print("Starting sequencer for test " + file_name + "\n");
	stc.perform('sequencerStart')

# SAPEE tests have indefinite length, run them for a fixed duration and then stop
	if 'sapee' in file_name:
		time.sleep(SAPEE_TEST_LEN * 60) # sleep for given duration
	else:
		rv = stc.waitUntilComplete() #blocking
	stc.perform('sequencerStop')
	stc.perform('devicesStopAll')
	time.sleep(30) #30s
	print("Sequencer stopped\n");


def run_verification_test(file_name):
	common_init(VERIFICATION_TESTS_DIR, file_name)
	attach_and_apply()

	print("Starting sequencer for test " + file_name + "\n");
	stc.perform('sequencerStart')

	rv = stc.waitUntilComplete() #blocking
	stc.perform('devicesStopAll')
	time.sleep(30) #30s
	print("Sequencer stopped\n");

############################################# MAIN LOOP ######################################

iteration = 0

while True:
	random.shuffle(stress_test_files)
# Run some random stress tests
	print("RUNNING STRESS TESTS (iteration %d)\n\n" % iteration)
	for testfile in stress_test_files[0:STRESS_TESTS_TO_RUN]:
		run_stress_test(testfile)

# Run all verification tests in random order
	random.shuffle(verification_test_files)
	print("RUNNING VERIFICATION TESTS (iteration %d)\n\n" % iteration)
	for testfile in verification_test_files:
		run_verification_test(testfile)

	iteration += 1
