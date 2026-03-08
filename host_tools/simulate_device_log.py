import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
import random
import time

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = REPO_ROOT / "data" / "device_logs"

def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def simulate_csv(out_path: Path, rows: int = 200, device_id: str = "PSOC6_01", interval_s: float = 1.0):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp_iso","device_id","moisture_raw","nitrate_raw","temp_c","battery_v"])

        moisture = 510
        nitrate = 800
        temp = 22.5
        batt = 3.95

        for _ in range(rows):
            # small random walk
            moisture += random.randint(-3, 6)
            nitrate += random.randint(-10, 60)
            temp += random.uniform(-0.05, 0.08)
            batt += random.uniform(-0.002, 0.000)

            w.writerow([utc_now_iso(), device_id, moisture, nitrate, round(temp,2), round(batt,2)])
            time.sleep(interval_s)

def main():
    p = argparse.ArgumentParser(description="PSoC6 Logger (UART or simulated)")
    p.add_argument("--out", default=str(DEFAULT_OUTDIR / "device_log.csv"), help="Output CSV path")
    p.add_argument("--simulate", action="store_true", help="Generate simulated device CSV (no hardware needed)")
    p.add_argument("--rows", type=int, default=200, help="Sim rows (when --simulate)")
    p.add_argument("--interval", type=float, default=0.0, help="Seconds between rows (when --simulate)")
    p.add_argument("--device-id", default="PSOC6_01", help="Device ID")
    # Real UART args (for later)
    p.add_argument("--port", default=None, help="Serial port (for real UART mode)")
    p.add_argument("--baud", type=int, default=115200, help="Baud rate (for real UART mode)")

    args = p.parse_args()
    out_path = Path(args.out)

    if args.simulate:
        simulate_csv(out_path, rows=args.rows, device_id=args.device_id, interval_s=args.interval)
        print(f"[OK] Wrote simulated device log to: {out_path}")
        return

    # Hardware mode placeholder (for when you have the PSoC)
    raise SystemExit("No hardware connected. Run with --simulate for now.")

if __name__ == "__main__":
    main()
