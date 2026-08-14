#!/usr/bin/env python3
import zmq
import serial
import json
import re
import sqlite3
import time
from datetime import datetime
import logging

#Configure logging
logging.basicConfig(
    filename="/tmp/AirGradient/AirGradient.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

#Connect to the AirGradient One over USB
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
data = {}

#Name the device
DEVICE = "Apollo-AG1"


#Configure the zmq client for the server
SERVER_IP = "131.225.56.221"
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect(f"tcp://{SERVER_IP}:5555")
print("Socket Connected")

#Read the serial data
while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        data["timestamp"] = datetime.now().isoformat(timespec="seconds")
        data["device"] = DEVICE

        if not line:
                continue

        if m := re.search(r'CO2\s*=\s*([\d.]+)', line):
                data["rco2"] = float(m.group(1))


        elif m := re.search(r'Temperature\s*=\s*([\d.]+)', line):
                data["atmp"] = float(m.group(1))


        elif m := re.search(r'Relative Humidity\s*=\s*([\d.]+)', line):
                data["rhum"] = float(m.group(1))


        elif m := re.search(r'TVOC Index\s*=\s*([\d.]+)', line):
                data["tvocIndex"] = float(m.group(1))


        elif m := re.search(r'TVOC Raw\s*=\s*([\d.]+)', line):
                data["tvocRaw"] = float(m.group(1))

        elif m := re.search(r'NOx Index\s*=\s*([\d.]+)', line):
                data["noxIndex"] = float(m.group(1))

        elif m := re.search(r'NOx Raw\s*=\s*([\d.]+)', line):
                data["noxRaw"] = float(m.group(1))

        # Atmospheric PM
        elif m := re.search(r'Atmospheric PM 1\.0\s*=\s*([\d.]+)', line):
                data["atm_pm01"] = float(m.group(1))

        elif m := re.search(r'Atmospheric PM 2\.5\s*=\s*([\d.]+)', line):
                data["atm_pm02"] = float(m.group(1))

        elif m := re.search(r'Atmospheric PM 10\s*=\s*([\d.]+)', line):
                data["atm_pm10"] = float(m.group(1))

        # Standard PM
        elif m := re.search(r'Standard Particle PM 1\.0\s*=\s*([\d.]+)', line):
                data["std_pm01"] = float(m.group(1))

        elif m := re.search(r'Standard Particle PM 2\.5\s*=\s*([\d.]+)', line):
                data["std_pm02"] = float(m.group(1))

        elif m := re.search(r'Standard Particle PM 10\s*=\s*([\d.]+)', line):
                data["std_pm10"] = float(m.group(1))

        # Particle counts
        elif m := re.search(r'Particle Count 0\.3\s*=\s*([\d.]+)', line):
                data["count_03"] = float(m.group(1))

        elif m := re.search(r'Particle Count 0\.5\s*=\s*([\d.]+)', line):
                data["count_05"] = float(m.group(1))

        elif m := re.search(r'Particle Count 1\.0\s*=\s*([\d.]+)', line):
                data["count_10"] = float(m.group(1))

        elif m := re.search(r'Particle Count 2\.5\s*=\s*([\d.]+)', line):
                data["count_25"] = float(m.group(1))

        elif m := re.search(r'Particle Count 5\.0\s*=\s*([\d.]+)', line):
                data["count_50"] = float(m.group(1))

        elif m := re.search(r'Particle Count 10\s*=\s*([\d.]+)', line):
                data["count_100"] = float(m.group(1))
                logger.info(
                        f"{data['timestamp']} "
                        f"DeviceID: {data['device']} "
                        f"CO2={data.get('rco2')} "
                        f"T={data.get('atmp')} "
                        f"RH={data.get('rhum')} "
                        f"TVOC={data.get('tvocIndex')} "
                        f"TVOC_Raw={data.get('tvocRaw')} "
                        f"NOx={data.get('noxIndex')} "
                        f"NOx_Raw={data.get('noxRaw')} "
                        f"AtmPM1.0={data.get('atm_pm01')} "
                        f"AtmPM2.5={data.get('atm_pm02')} "
                        f"AtmPM10={data.get('atm_pm10')} "
                        f"StdPM1.0={data.get('std_pm01')} "
                        f"StdPM2.5={data.get('std_pm02')} "
                        f"StdPM10={data.get('std_pm10')} "
                        f"CntPM0.3={data.get('count_03')} "
                        f"CntPM0.5={data.get('count_05')} "
                        f"CntPM1.0={data.get('count_10')} "
                        f"CntPM2.5={data.get('count_25')} "
                        f"CntPM5.0={data.get('count_50')} "
                        f"CntPM10={data.get('count_100')}"
                )

# This print statement is for debuggin purposes. The logger captures the output
# and writes it to /tmp/AirGradient/AirGradient.log
#                print(
#                        f"{data['timestamp']} "
#                        f"DeviceID: {data['device']} "
#                        f"CO2={data.get('rco2')} "
#                        f"T={data.get('atmp')} "
#                        f"RH={data.get('rhum')} "
#                        f"TVOC={data.get('tvocIndex')} "
#                        f"TVOC_Raw={data.get('tvocRaw')} "
#                        f"NOx={data.get('noxIndex')} "
#                        f"NOx_Raw={data.get('noxRaw')} "
#                        f"AtmPM1.0={data.get('atm_pm01')} "
#                        f"AtmPM2.5={data.get('atm_pm02')} "
#                        f"AtmPM10={data.get('atm_pm10')} "
#                        f"StdPM1.0={data.get('std_pm01')} "
#                        f"StdPM2.5={data.get('std_pm02')} "
#                        f"StdPM10={data.get('std_pm10')} "
#                        f"CntPM0.3={data.get('count_03')} "
#                        f"CntPM0.5={data.get('count_05')} "
#                        f"CntPM1.0={data.get('count_10')} "
#                        f"CntPM2.5={data.get('count_25')} "
#                        f"CntPM5.0={data.get('count_50')} "
#                        f"CntPM10={data.get('count_100')}"
#                )

                #print(data)
                socket.send_json(data)
                data = {}
