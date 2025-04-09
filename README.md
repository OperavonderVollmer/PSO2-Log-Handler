# PSO2 Log Handler
 
**PSO2 Log Handler** uses my Log-File-Monitor and OPR-Speaks modules to create a robust and responsive log monitoring script that verbalizes in game chat messages, allowing for multi-tasking

## Features

- **Chat Monitoring:** Periodically checks log files for updates.
- **Robust Filtering:** Cleans up chat messages and removes chat commands as well as blacklisted sources and contexts to ensure smooth operations.
- **Text to Speech:** Monitored and sanitized texts are offered to the TTS engine, allowing verbalization in near realtime speeds.
- **Outside Applicability:** The use case does not start and stop at PSO2. PSO2 Log Handler is able to verbalize any log file it is monitoring, even multiple monitors concurrently.

## Installation

### Prerequisites

- Python 3.x
- Required dependencies (install using pip):
  ```sh
  pip install git+https://github.com/OperavonderVollmer/Log-File-Monitor.git@main git+https://github.com/OperavonderVollmer/OPR-Speaks.git@main git+https://github.com/OperavonderVollmer/OperaPowerRelay.git
  ```

### Manual Installation

1. Clone or download the repository.
2. Navigate to the directory containing `setup.py`:
   ```sh
   cd /path/to/PSO2-Log-Handler
   ```
3. Install the package in **editable mode**:
   ```sh
   pip install -e .
   ```

### Installing via pip
```sh
pip install git+https://github.com/OperavonderVollmer/PSO2-Log-Handler
```
