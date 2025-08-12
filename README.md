# PingTest

A Python network ping monitoring application that sends pings to multiple IP addresses at set intervals and logs the results to a file.

## Features

- Ping up to 10 IP addresses simultaneously
- Configurable ping intervals
- Comprehensive logging with timestamps
- Cross-platform support (Windows, Linux, macOS)
- JSON configuration file
- Command-line interface
- Packet loss monitoring
- Response time tracking

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)
- Network access to target IP addresses

## Installation

1. Clone or download the application files
2. Ensure Python 3.6+ is installed on your system
3. No additional package installation required

## Configuration

The application uses a `config.json` file for configuration. You can modify this file to customize:

- **ip_addresses**: List of IP addresses to ping (maximum 10)
- **ping_interval**: Time between ping tests in seconds
- **ping_count**: Number of pings per IP address per test
- **timeout**: Ping timeout in seconds
- **log_file**: Name of the log file
- **max_ips**: Maximum number of IP addresses (hardcoded to 10)
- **total_runtime**: Total runtime in seconds (0 = run indefinitely)

### Example Configuration

```json
{
    "ip_addresses": [
        "8.8.8.8",
        "1.1.1.1",
        "208.67.222.222"
    ],
    "ping_interval": 60,
    "ping_count": 4,
    "timeout": 5,
    "log_file": "pingtest.log",
    "max_ips": 10,
    "total_runtime": 0
}
```

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

### Override Interval

Override the ping interval from the command line:

```bash
python pingtest.py --interval 30
```

### Override Runtime

Override the total runtime from the command line:

```bash
python pingtest.py --runtime 300
```

### Help

Display help information:

```bash
python pingtest.py --help
```

## Command Line Options

- `--config, -c`: Specify configuration file path (default: config.json)
- `--single, -s`: Run single test and exit
- `--interval, -i`: Override ping interval from config
- `--runtime, -r`: Override total runtime from config (in seconds)
- `--help, -h`: Show help message

## Logging

The application logs all ping results to both:
- Console output (real-time)
- Log file (persistent storage)

### Log Format

```
2024-01-15 10:30:00,123 - INFO - Ping to 8.8.8.8: SUCCESS - Response time: 15.23ms, Packet loss: 0.0%
2024-01-15 10:30:01,456 - INFO - Ping to 1.1.1.1: SUCCESS - Response time: 12.45ms, Packet loss: 0.0%
2024-01-15 10:30:02,789 - ERROR - Ping to 192.168.1.1: FAILED - Ping command timed out
```

### Log Information

Each log entry includes:
- Timestamp
- IP address
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

## Stopping the Application

To stop continuous monitoring, press `Ctrl+C` in the terminal.

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure you have network access and appropriate permissions
2. **IP Address Unreachable**: Check if the target IP addresses are valid and reachable
3. **High Packet Loss**: May indicate network congestion or connectivity issues
4. **Timeout Errors**: Increase the timeout value in config.json if needed

### Windows-Specific Notes

- The application automatically detects Windows and uses appropriate ping command syntax
- Windows ping uses `-n` for count and `-w` for timeout (in milliseconds)

### Linux/macOS Notes

- Uses standard ping command with `-c` for count and `-W` for timeout
- May require root privileges for some network operations

## File Structure

```
pingtest/
├── pingtest.py      # Main application
├── config.json      # Configuration file
├── requirements.txt # Dependencies (none required)
├── README.md        # This file
└── pingtest.log     # Log file (created when running)
```

## License

This application is provided as-is for educational and monitoring purposes.

## Contributing

Feel free to modify and improve the application according to your needs. 