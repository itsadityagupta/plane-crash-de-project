import config
from process_data import ProcessData

if __name__ == "__main__":
    """
    Initializes a ProcessData object and initiates the processing of files.
    """
    process_data = ProcessData(config.folder_path)
    process_data.process_files()
