import serial
import json
import re
import sqlite3
from datetime import datetime

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

conn = sqlite3.connect("airgradient.db")
cur = conn.cursor()

def insert(data):
	cur.execute("""
		INSERT INTO measurements (
		timestamp, rco2, atmp, rhum,
		tvocIndex, noxIndex,
		pm01, pm02, pm10
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
	""", (
		datetime.now().isoformat(),
		data.get("rco2"),
		data.get("atmp"),
		data.get("rhum"),
		data.get("tvocIndex"),
		data.get("noxIndex"),
		data.get("pm01"),
		data.get("pm02"),
		data.get("pm10")
		))
		conn.commit()

while True:
	line = ser.readline().decode("utf-8", errors="ignore").strip()

	m = re.search(r'(\{.*\})', line)
	if not m:
		continue

	try:
		data = json.loads(m.group(1))
		insert(data)

		print(
			f"CO2={data.get('rco2')} "
			f"T={data.get('atmp')} "
			f"RH={data.get('rhum')}"
		)

	except Exception as e:
		print(e)
