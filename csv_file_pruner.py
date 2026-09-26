"""Delete old Open Hardware Monitor CSV logs, keeping only the most recent ones.

Intended to run periodically (e.g. via Windows Task Scheduler) to prevent
the Open Hardware Monitor log directory from growing unbounded.
"""

import argparse
import glob
import logging
import os

DEFAULT_LOG_DIR = r"C:\Program Files\OpenHardwareMonitor"
DEFAULT_LOG_PREFIX = "OpenHardwareMonitorLog-"
DEFAULT_RETENTION = 2
DEFAULT_PRUNER_LOG_FILE = os.path.expanduser(r"~\Documents\limpiar_csv.log")


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
    parser.add_argument(
        "--retention",
        type=int,
        default=os.environ.get("OHM_LOG_RETENTION", str(DEFAULT_RETENTION)),
        help="Number of most recent CSV logs to keep; older files are "
             "deleted (env: OHM_LOG_RETENTION, default: %(default)s).",
    )
    parser.add_argument(
        "--log-file",
        default=os.environ.get("OHM_PRUNER_LOG_FILE", DEFAULT_PRUNER_LOG_FILE),
        help="Path to this script's own activity log "
             "(env: OHM_PRUNER_LOG_FILE, default: %(default)s).",
    )
    return parser.parse_args()


def configure_logging(log_file):
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("=== CSV Cleanup Log ===\n")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def limpiar_csv(log_dir, log_prefix, retention):
    """
    Cleans up old CSV files in the specified directory.
    Retains only the `retention` most recent files and deletes the rest.
    Logs the deletion process, including any errors encountered.
    """
    try:
        # Retrieve the list of CSV files matching the pattern in the directory
        csv_files = glob.glob(os.path.join(log_dir, f"{log_prefix}*.csv"))

        # Sort the files by modification date (newest first)
        csv_files.sort(key=os.path.getmtime, reverse=True)

        # Keep only the `retention` most recent files and delete the rest
        if len(csv_files) > retention:
            deleted_files = []
            for file in csv_files[retention:]:  # Start after the kept files
                try:
                    os.remove(file)
                    deleted_files.append(file)
                except Exception as e:
                    logging.error(f"Failed to delete {file}: {e}")

            # Log the deleted files or indicate if no extra files were found
            if deleted_files:
                logging.info(f"Deleted files: {', '.join(deleted_files)}")
            else:
                logging.info("No extra files were available for deletion.")
        else:
            logging.info(f"{len(csv_files)} CSV file(s) present, no deletion performed.")

    except Exception as e:
        logging.error(f"General error during CSV cleanup: {e}")


def main():
    args = parse_args()
    configure_logging(args.log_file)

    logging.info("Starting CSV cleanup process.")
    limpiar_csv(args.log_dir, args.log_prefix, args.retention)
    logging.info("CSV cleanup process completed.\n")


if __name__ == "__main__":
    main()
