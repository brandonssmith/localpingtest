# PingTest

A Python network ping monitoring application that sends pings to multiple IP addresses at set intervals and logs the results to a file. Features a modern GUI configuration editor for easy setup and management.

## Features

- **Network Monitoring**: Continuous ping monitoring with configurable intervals
- **IP Address Management**: Add, remove, and reorder IP addresses with optional names
- **GUI Configuration Editor**: User-friendly interface for managing all settings
- **Timestamped Logging**: Automatic log file timestamping for each session
- **Cross-Platform Support**: Windows, Linux, and macOS compatibility
- **JSON Configuration**: Flexible configuration file format
- **Command-Line Interface**: Full CLI support with all options
- **Packet Loss Monitoring**: Track network reliability metrics
- **Response Time Tracking**: Monitor network performance
- **IP Reordering**: Drag-and-drop style reordering of IP addresses
- **IP Naming**: Optional descriptive names for IP addresses

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)
- No external dependencies (uses only Python standard library)
- Network access to target IP addresses

## Installation

1. Clone or download the application files to `C:\Code\pingtest`
2. Ensure Python 3.6+ is installed on your system
3. Copy the batch files to your home directory (`C:\Users\brand\`):
   - `pingtest.bat` - Launches the main ping monitoring application
   - `pingtest_config.bat` - Launches the GUI configuration editor

## Quick Start

### Windows Users

1. **Launch Configuration Editor**: Double-click `pingtest_config.bat` in your home directory
2. **Configure IP Addresses**: Add your target IP addresses with optional names
3. **Adjust Settings**: Click the ⚙️ Settings button to configure ping parameters
4. **Save Configuration**: Click 💾 SAVE CONFIGURATION to save your settings
5. **Run Monitoring**: Double-click `pingtest.bat` to start ping monitoring

### Command Line Users

```bash
# Start continuous monitoring
python pingtest.py

# Run single test
python pingtest.py --single

# Use custom configuration
python pingtest.py --config myconfig.json
```

## Configuration

The application uses a `config.json` file for configuration. The GUI editor automatically manages this file, or you can edit it manually.

### Configuration Structure

```json
{
    "ip_addresses": {
        "8.8.8.8": "Google DNS",
        "1.1.1.1": "Cloudflare DNS",
        "192.168.1.1": "Router",
        "192.168.1.9": "Local Device 1"
    },
    "ping_interval": 20,
    "ping_count": 2,
    "timeout": 5,
    "log_file": "pingtest.log",
    "total_runtime": 0
}
```

### Configuration Options

- **ip_addresses**: Dictionary mapping IP addresses to optional names
- **ping_interval**: Time between ping tests in seconds
- **ping_count**: Number of pings per IP address per test
- **timeout**: Ping timeout in seconds
- **log_file**: Base name for log files (timestamped automatically)
- **total_runtime**: Total runtime in seconds (0 = run indefinitely)

## GUI Configuration Editor

The configuration editor provides an intuitive interface for managing all PingTest settings.

### Main Interface

- **IP Address List**: Shows all configured IP addresses with names
- **Add IP**: Enter IP address and optional name
- **Remove IP**: Select and remove unwanted IP addresses
- **Edit Name**: Modify names for existing IP addresses
- **Reorder IPs**: Use ▲▼ buttons or Ctrl+↑↓ to reorder IP addresses
- **Clear All**: Remove all IP addresses at once

### Settings Dialog

Access via the ⚙️ Settings button to configure:
- Ping interval and count
- Timeout values
- Total runtime
- Log file location
- Automatic timestamping information

### Keyboard Shortcuts

- **Ctrl+S**: Save configuration quickly
- **Ctrl+↑**: Move selected IP up
- **Ctrl+↓**: Move selected IP down
- **Enter**: Save in dialogs
- **Escape**: Cancel operations

## Usage

### Continuous Monitoring

Run the application in continuous mode (default):

```bash
python pingtest.py
```

### Single Test

Run a single ping test and exit:

```bash
python pingtest.py --single
```

### Custom Configuration

Use a custom configuration file:

```bash
python pingtest.py --config myconfig.json
```

### Command Line Options

- `--config, -c`: Specify configuration file path (default: config.json)
- `--single, -s`: Run single test and exit
- `--interval, -i`: Override ping interval from config
- `--runtime, -r`: Override total runtime from config (in seconds)
- `--help, -h`: Show help message

## Logging

The application automatically creates timestamped log files for each session.

### Log File Naming

Log files are automatically named with timestamps:
- Base name: `pingtest.log` (from config)
- Timestamped: `pingtest_20250119_143022.log`
- Format: `{basename}_{YYYYMMDD_HHMMSS}.{extension}`

### Log Format

```
2025-01-19 14:30:22,123 - INFO - PingTest session started - Log file: pingtest_20250119_143022.log
2025-01-19 14:30:22,456 - INFO - Pinging Google DNS (8.8.8.8)...
2025-01-19 14:30:22,789 - INFO - Ping to Google DNS (8.8.8.8): SUCCESS - Response time: 15.23ms, Packet loss: 0.0%
2025-01-19 14:30:23,012 - INFO - Pinging Router (192.168.1.1)...
2025-01-19 14:30:23,345 - INFO - Ping to Router (192.168.1.1): SUCCESS - Response time: 2.45ms, Packet loss: 0.0%
```

### Log Information

Each log entry includes:
- Timestamp
- IP address with name (if configured)
- Success/failure status
- Response time (if successful)
- Packet loss percentage
- Error details (if failed)

## Examples

### Basic Usage

```bash
# Start continuous monitoring with default settings
python pingtest.py
```

### Custom Configuration

```bash
# Use custom config and run single test
python pingtest.py --config production.json --single
```

### Quick Test

```bash
# Test all IPs once with 30-second interval
python pingtest.py --interval 30 --single

# Run for 5 minutes (300 seconds)
python pingtest.py --runtime 300

# Run for 6 hours (21600 seconds)
python pingtest.py --runtime 21600
```

## File Structure

```
C:\Code\pingtest\                    # Application directory
├── pingtest.py                      # Main ping monitoring application
├── config_editor.py                 # GUI configuration editor
├── config.json                      # Configuration file
├── requirements.txt                 # Dependencies (none required)
├── README.md                        # This file
└── pingtest_*.log                  # Timestamped log files

C:\Users\brand\                      # User home directory
├── pingtest.bat                     # Launches main application
└── pingtest_config.bat              # Launches configuration editor
```

## Stopping the Application

To stop continuous monitoring, press `Ctrl+C` in the terminal.

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure you have network access and appropriate permissions
2. **IP Address Unreachable**: Check if the target IP addresses are valid and reachable
3. **High Packet Loss**: May indicate network congestion or connectivity issues
4. **Timeout Errors**: Increase the timeout value in the settings dialog
5. **Configuration Not Saving**: Ensure you click the 💾 SAVE CONFIGURATION button

### Windows-Specific Notes

- The application automatically detects Windows and uses appropriate ping command syntax
- Windows ping uses `-n` for count and `-w` for timeout (in milliseconds)
- Batch files use `cd /d` to ensure proper working directory

### Linux/macOS Notes

- Uses standard ping command with `-c` for count and `-W` for timeout
- May require root privileges for some network operations

### GUI Issues

- **Settings Not Visible**: Click the ⚙️ Settings button to access ping parameters
- **IP Names Not Saving**: Ensure you save after making changes
- **Reorder Not Working**: Select an IP first, then use ▲▼ buttons or Ctrl+↑↓

## Features in Detail

### IP Address Management

- **Add IPs**: Enter IP address and optional descriptive name
- **Remove IPs**: Select and remove individual IP addresses
- **Edit Names**: Modify names without removing IP addresses
- **Reorder**: Change the sequence of IP addresses using visual controls
- **Validation**: Basic IP address format validation

### Configuration Persistence

- **Auto-save**: All changes are saved to `config.json`
- **Backup**: Original configuration is preserved during updates
- **Validation**: Input validation prevents invalid configurations
- **Confirmation**: Save confirmation dialog shows all changes

### Enhanced Logging

- **Session-based**: Each run creates a new timestamped log file
- **Named IPs**: Log entries include IP names when configured
- **Comprehensive**: All ping attempts and results are logged
- **Readable**: Clear, structured log format for easy analysis

## License

This application is provided as-is for educational and monitoring purposes.

## Contributing

Feel free to modify and improve the application according to your needs. The modular design makes it easy to add new features or modify existing functionality. 