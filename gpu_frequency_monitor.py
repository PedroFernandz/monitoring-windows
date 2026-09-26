"""Print the latest GPU core clock reported by Open Hardware Monitor.

Reads the most recent Open Hardware Monitor CSV log and prints the last
recorded GPU core clock, in MHz, as a single value. Intended for use as a
Zabbix Agent UserParameter script.
"""

import argparse
import os
from datetime import datetime

import pandas as pd

DEFAULT_LOG_DIR = r"C:\Program Files\OpenHardwareMonitor"
DEFAULT_LOG_PREFIX = "OpenHardwareMonitorLog-"


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--log-dir",
        default=os.environ.get("OHM_LOG_DIR", DEFAULT_LOG_DIR),
        help="Directory containing the Open Hardware Monitor CSV logs "
             "(env: OHM_LOG_DIR, default: %(default)s).",
    )
    parser.add_argument(
        "--log-prefix",
        default=os.environ.get("OHM_LOG_PREFIX", DEFAULT_LOG_PREFIX),
        help="Filename prefix of the Open Hardware Monitor CSV logs, before "
             "the date (env: OHM_LOG_PREFIX, default: %(default)s).",
    )
    return parser.parse_args()


def find_latest_csv(log_dir, log_prefix):
    """Return the path to today's Open Hardware Monitor CSV log, falling
    back to the most recent one available in `log_dir`."""
    today_date = datetime.now().strftime("%Y-%m-%d")
    csv_path = os.path.join(log_dir, f"{log_prefix}{today_date}.csv")

    if not os.path.exists(csv_path):
        csv_files = [
            f for f in os.listdir(log_dir)
            if f.startswith(log_prefix) and f.endswith(".csv")
        ]
        if csv_files:
            csv_files.sort(reverse=True)  # Sort by filename (assumed to be date-based)
            csv_path = os.path.join(log_dir, csv_files[0])

    return csv_path


def main():
    args = parse_args()

    try:
        csv_path = find_latest_csv(args.log_dir, args.log_prefix)
        if not os.path.exists(csv_path):
            print("0")  # Return 0 if no valid CSV file is found
            return

        # Load the CSV into a DataFrame
        df = pd.read_csv(csv_path, low_memory=False)

        # The raw column headers are the sensor identifiers OHM writes on the
        # first line (e.g. "/nvidiagpu/0/clock/0", "/atigpu/0/clock/0"); the
        # first data row holds the human-readable sensor names (e.g.
        # "GPU Core"). Keep the identifiers before they get overwritten below.
        sensor_identifiers = df.columns

        # Use the sensor names row as the actual header and remove it from the data
        df.columns = df.iloc[0]  # Assign first row as column names
        df = df[1:].reset_index(drop=True)  # Remove the duplicate header row

        # Prefer selecting the column by its sensor identifier: a GPU core
        # clock identifier contains "/clock/" together with "nvidiagpu" or
        # "atigpu". This is unambiguous, unlike the "GPU Core" name, which
        # OHM reuses for the clock, the temperature and the load sensors.
        gpu_clock_index = None
        for i, identifier in enumerate(sensor_identifiers):
            identifier_str = str(identifier).lower()
            if "/clock/" in identifier_str and ("nvidiagpu" in identifier_str or "atigpu" in identifier_str):
                gpu_clock_index = i
                break  # Stop at the first match (the GPU core clock)

        # Fall back to the name-based choice only if the identifier row isn't
        # usable (e.g. a CSV export without sensor-path identifiers): OHM
        # groups sensors by type in clock/temperature/load order, so among
        # the "GPU Core" columns the first occurrence is the clock.
        if gpu_clock_index is None:
            gpu_core_indices = [i for i, col in enumerate(df.columns) if "GPU Core" in str(col)]
            if gpu_core_indices:
                gpu_clock_index = gpu_core_indices[0]  # First occurrence is the clock

        if gpu_clock_index is None:
            print("0")  # Return 0 if no GPU core clock column is found
            return

        # Extract the column based on the identified index
        gpu_clock_values = df.iloc[:, gpu_clock_index]

        # Convert values to numeric, handling conversion errors
        gpu_clock_values = pd.to_numeric(gpu_clock_values, errors="coerce")

        # Get the last valid GPU core clock value (MHz)
        gpu_clock = gpu_clock_values.dropna().iloc[-1]

        # Print only the numeric value (for integration with Zabbix)
        print(gpu_clock)

    except Exception:
        print("0")  # Return 0 in case of processing errors


if __name__ == "__main__":
    main()
