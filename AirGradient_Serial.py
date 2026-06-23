import serial
import json
import csv
import re
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

with open('airgradient.csv', 'a', newline='') as f:
	writer = csv.writer(f)

	while True:
		line = ser.readline().decode('utf-8', errors='ignore').strip()

		if "PAYLOAD" in line:
			continue

		m = re.search(r'(\{.*\})', line)

		if not m:
			continue

		try:
			data = json.loads(m.group(1))

			timestamp = datetime.now().isoformat()

			writer.writerow([
				timestamp,
				data.get('rco2'),
				data.get('atmp'),
				data.get('rhum'),
				data.get('tvocIndex'),
                		data.get('noxIndex'),
                		data.get('pm02')
            		])

			f.flush()
			print("\n")
			print(data)
			print("\n")
			print(
				f"{timestamp} "
				f"CO2={data.get('rco2')} "
				f"T={data.get('atmp')} "
				f"RH={data.get('rhum')}"
			)
			print("\n")
			
		except Exception as e:
			print(e)
