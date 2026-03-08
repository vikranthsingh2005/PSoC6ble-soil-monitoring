# PSoC 6 BLE Sensor Integration (In Progress)

## Goal
Stream soil moisture (Watermark) + nitrate interface readings from a PSoC 6 BLE device, log them with timestamps, then run the same normalization + anomaly detection pipeline.

## Planned Data Packet (CSV over UART or BLE notify)
```text
timestamp_iso,device_id,moisture_raw,nitrate_raw,temp_c,battery_v
2026-03-07T10:41:12Z,PSOC6_01,512,823,22.6,3.92
Status

✅ Repo structure created (firmware / host tools / logs)

✅ UART logger script added (host_tools/uart_logger.py)

🔜 Add firmware to read ADC values and transmit packets

🔜 Add analysis scripts/notebook to normalize + detect anomalies

Repo Structure

host_tools/ → host-side scripts (UART logger)

firmware/ → PSoC project (to be added)

data/device_logs/ → captured device logs (CSV)

docs/ → wiring notes, diagrams

Setup (Mac)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Capture logs from PSoC (UART)

Plug in the PSoC and find the serial port:

ls /dev/cu.*

Run the logger (replace the port with your actual one):

python3 host_tools/uart_logger.py --port /dev/cu.usbmodemXXXX --baud 115200 --out data/device_logs/device_log.csv
