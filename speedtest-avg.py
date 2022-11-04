import subprocess
import re
from progressbar import progressbar
from datetime import datetime

# Enter number of tests to perform
TESTS = 30

# Set True for a file output in the logs directory
file_output = False


def run_speedtest():

	output = subprocess.check_output("speedtest", shell=True)
	output_decoded = output.decode("utf-8").split("\n")

	result = {
			"download": 0.00,
			"upload": 0.00
	}

	for line in output_decoded:

		if not (re.search("download", line.lower()) or re.search("upload", line.lower())):
			continue

		if re.search("download", line.lower()):
			dspeed = re.findall("[0-9]{2,3}\.[0-9]{2} [A-Z]{1}bps",line)
			result["download"] = float(dspeed[0][0: -5])


		if re.search("upload", line.lower()):
			uspeed = re.findall("[0-9]{2,3}\.[0-9]{2} [A-Z]{1}bps",line)
			result["upload"] = float(uspeed[0][0: -5])

	return result


def output_results(results):

	result_count = len(results)
	dtotal = 0
	utotal = 0

	for result in results:
		dtotal += result["download"]
		utotal += result["upload"]

	davg = dtotal / result_count
	uavg = utotal / result_count

	print("----------------------------")
	print("        Test Results        ")
	print("----------------------------")

	print(f"Average Download: {round(davg, 2)} Mbps")
	print(f"  Average Upload: {round(uavg, 2)} Mbps\n")

	current_time = datetime.now().strftime("%d-%m-%Y_%H%M%S")
	file_name= f"{current_time}.txt"

	with open(file_name, "w") as fp:
		fp.write(f"""----------------------------\n        Test Results        \n----------------------------\nAverage Download: {round(davg, 2)} Mbps\n  Average Upload: {round(uavg, 2)} Mbps
			""")



def main():
	test_results = []

	print("Running tests...")

	for i in progressbar(range(TESTS), redirect_stdout=True):
		test_results.append(run_speedtest())
		print(f"Test {i+1} complete")

	if file_output:
		output_results(test_results)



if __name__ == "__main__":
	main()
