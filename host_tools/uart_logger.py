#!/usr/bin/env python3
"""
UART logger for PSoC6 -> CSV.

Expected incoming line format (CSV):
timestamp_iso,device_id,moisture_raw,nitrate_raw,temp_c,battery_v

Example:
2026-03-07T10:41:12Z,PSOC6_01,512,823,22.6,3.92
"""

import argparse
import csv
import os
from datetime import datetime, timezone

import serial


HEADER = ["timestamp_iso", "device_id", "moisture_raw", "nitrate_raw", "temp_c", "battery_v"]


def utc_iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def parse_line(line: str, default_device_id: str) -> dict | None:
    """
    Returns a dict matching HEADER, or None if line is not usable.
    """
    s = line.strip()
    if not s:
        return None

    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 6:
        # Not the format we expect (you can expand later if needed)
        return None

    ts, dev, moisture, nitrate, temp, batt = parts

    if not ts or ts.lower() == "none":
        ts = utc_iso_now()

    if not dev:
        dev = default_device_id

    try:
        return {
            "timestamp_iso": ts,
            "device_id": dev,
            "moisture_raw": int(float(moisture)),
            "nitrate_raw": int(float(nitrate)),
            "temp_c": float(temp),
            "battery_v": float(batt),
        }
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", required=True, help="Serial port, e.g. /dev/cu.usbmodemXXXX")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--device-id", default="PSOC6_01")
    ap.add_argument("--out", default=None, help="Output CSV path (default: data/device_logs/psoc_log_<timestamp>.csv)")
    args = ap.parse_args()

    if args.out is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.out = f"data/device_logs/psoc_log_{ts}.csv"

    ensure_parent_dir(args.out)

    file_exists = os.path.exists(args.out) and os.path.getsize(args.out) > 0

    print(f"[INFO] Listening on {args.port} @ {args.baud}")
    print(f"[INFO] Writing to: {args.out}")
    print("[INFO] Press CTRL+C to stop.\n")

    with serial.Serial(args.port, args.baud, timeout=1) as ser, open(args.out, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)

        if not file_exists:
            writer.writeheader()
            f.flush()

        try:
            while True:
                raw = ser.readline()
                if not raw:
                    continue

                line = raw.decode("utf-8", errors="ignore")
                row = parse_line(line, args.device_id)
                if row is None:
                    continue

                writer.writerow(row)
                f.flush()
                print(row)
        except KeyboardInterrupt:
            print("\n[INFO] Stopped.")


if __name__ == "__main__":
    main()
