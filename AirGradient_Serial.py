import serial
import csv
import re
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

data = {}

with open('airgradient.csv', 'a', newline='') as f:
    writer = csv.writer(f)

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()

        if not line:
            continue

        # print raw data while testing
        # print(line)

        if m := re.search(r'CO2\s*=\s*([\d.]+)', line):
            data['rco2'] = float(m.group(1))

        elif m := re.search(r'Temperature\s*=\s*([\d.]+)', line):
            data['atmp'] = float(m.group(1))

        elif m := re.search(r'Relative Humidity\s*=\s*([\d.]+)', line):
            data['rhum'] = float(m.group(1))

        elif m := re.search(r'TVOC Index\s*=\s*([\d.]+)', line):
            data['tvocIndex'] = float(m.group(1))

        elif m := re.search(r'NOx Index\s*=\s*([\d.]+)', line):
            data['noxIndex'] = float(m.group(1))

        elif m := re.search(r'Atmospheric PM 2\.5\s*=\s*([\d.]+)', line):
            data['pm02'] = float(m.group(1))


            # PM2.5 is the last value in the block, save a sample
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

            print(
                f"{timestamp} "
                f"CO2={data.get('rco2')} "
                f"T={data.get('atmp')} "
                f"RH={data.get('rhum')} "
                f"TVOC={data.get('tvocIndex')} "
                f"NOx={data.get('noxIndex')} "
                f"PM2.5={data.get('pm02')}"
            )

            data = {}
