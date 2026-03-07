# PSoC 6 BLE Sensor Integration (In Progress)
## Goal
Stream soil moisture (Watermark) + nitrate interface readings from a PSoC 6 BLE device, log them with timestamps, then run the same normalization + anomaly detection pipeline.
## Planned Data Packet (CSV over UART or BLE notify)
timestamp_iso, device_id, moisture_raw, nitrate_raw, temp_c, battery_v
Example:
2026-03-07T10:41:12Z,PSOC6_01,512,823,22.6,3.92
## Status
- ✅ Analysis pipeline exists (normalization, rolling avg, z-score, EPA MCL checks)
- ✅ Repo supports clean input CSV + generated plots
- 🔜 Add firmware to read ADC values and transmit packets
- 🔜 Add logger script to capture packets into `data/device_logs/`
