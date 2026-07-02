import serial
import re
import sqlite3
from datetime import datetime
import logging

#Configure logging
logging.basicConfig(
    filename="/tmp/AirGradient/zmqServer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

conn = sqlite3.connect("/var/lib/airgradient/AirGradient.db")
cur = conn.cursor()


def insert(data, timestamp):

    cur.execute("""
        INSERT INTO measurements (
            timestamp,
            rco2, atmp, rhum,
            tvocIndex, tvocRaw,
            noxIndex, noxRaw,
            atm_pm01, atm_pm02, atm_pm10,
            std_pm01, std_pm02, std_pm10,
            count_03, count_05, count_10,
            count_25, count_50, count_100
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,

        data.get("rco2"),
        data.get("atmp"),
        data.get("rhum"),

        data.get("tvocIndex"),
        data.get("tvocRaw"),

        data.get("noxIndex"),
        data.get("noxRaw"),

        data.get("atm_pm01"),
        data.get("atm_pm02"),
        data.get("atm_pm10"),

        data.get("std_pm01"),
        data.get("std_pm02"),
        data.get("std_pm10"),

        data.get("count_03"),
        data.get("count_05"),
        data.get("count_10"),
        data.get("count_25"),
        data.get("count_50"),
        data.get("count_100")
    ))

    conn.commit()


data = {}

while True:

    line = ser.readline().decode("utf-8", errors="ignore").strip()

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

        timestamp = datetime.now().isoformat()

        # end of measurement frame
        insert(data, timestamp)

        logger.info(
            f"{timestamp} "
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

#        print(
#            f"{timestamp} "
#            f"CO2={data.get('rco2')} "
#            f"T={data.get('atmp')} "
#            f"RH={data.get('rhum')} "
#            f"TVOC={data.get('tvocIndex')} "
#            f"TVOC_Raw={data.get('tvocRaw')} "
#            f"NOx={data.get('noxIndex')} "
#            f"NOx_Raw={data.get('noxRaw')} "
#            f"AtmPM1.0={data.get('atm_pm01')} "
#            f"AtmPM2.5={data.get('atm_pm02')} "
#            f"AtmPM10={data.get('atm_pm10')} "
#            f"StdPM1.0={data.get('std_pm01')} "
#            f"StdPM2.5={data.get('std_pm02')} "
#            f"StdPM10={data.get('std_pm10')} "
#            f"CntPM0.3={data.get('count_03')} "
#            f"CntPM0.5={data.get('count_05')} "
#            f"CntPM1.0={data.get('count_10')} "
#            f"CntPM2.5={data.get('count_25')} "
#            f"CntPM5.0={data.get('count_50')} "
#            f"CntPM10={data.get('count_100')}"
#        )

        data = {} 
