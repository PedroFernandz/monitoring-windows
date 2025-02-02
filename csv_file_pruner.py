import os
import glob
import logging
from datetime import datetime

# Directory path where the CSV files are stored
csv_dir = r"C:\Program Files\OpenHardwareMonitor"

# Log file path
log_file = os.path.expanduser(r"~\Documents\limpiar_csv.log")

# Ensure the log directory exists
log_dir = os.path.dirname(log_file)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create the log file if it does not exist
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("=== CSV Cleanup Log ===\n")

# Configure logging settings
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def limpiar_csv():
    """
    Cleans up old CSV files in the specified directory.
    Retains only the two most recent files and deletes the rest.
    Logs the deletion process, including any errors encountered.
    """
    try:
        # Retrieve the list of CSV files matching the pattern in the directory
        csv_files = glob.glob(os.path.join(csv_dir, "OpenHardwareMonitorLog-*.csv"))

        # Sort the files by modification date (newest first)
        csv_files.sort(key=os.path.getmtime, reverse=True)

        # Keep only the two most recent files and delete the rest
        if len(csv_files) > 2:
            deleted_files = []
            for file in csv_files[2:]:  # Start from the third file onward
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
            logging.info("Less than two CSV files present, no deletion performed.")

    except Exception as e:
        logging.error(f"General error during CSV cleanup: {e}")

# Execute the cleanup process
if __name__ == "__main__":
    logging.info("Starting CSV cleanup process.")
    limpiar_csv()
    logging.info("CSV cleanup process completed.\n")
