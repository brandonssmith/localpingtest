#!/usr/bin/env python3
"""
PingTest - A network ping monitoring application
Sends pings to multiple IP addresses at set intervals and logs results
"""

import subprocess
import time
import datetime
import logging
import json
import os
import sys
from typing import List, Dict, Optional
import platform


class PingTest:
    def __init__(self, config_file: str = "config.json"):
        """Initialize PingTest with configuration"""
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_logging()
        
    def load_config(self) -> Dict:
        """Load configuration from JSON file"""
        default_config = {
            "ip_addresses": {
                "8.8.8.8": "Google DNS",
                "1.1.1.1": "Cloudflare DNS",
                "208.67.222.222": "OpenDNS"
            },
            "ping_interval": 60,  # seconds
            "ping_count": 4,      # number of pings per check
            "timeout": 5,         # timeout in seconds
            "log_file": "pingtest.log",
            "total_runtime": 0    # total runtime in seconds (0 = run indefinitely)
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    
                    # Handle legacy config format (convert list of IPs to dict format)
                    if "ip_addresses" in config and isinstance(config["ip_addresses"], list):
                        # Convert old format to new format
                        old_ips = config["ip_addresses"]
                        config["ip_addresses"] = {}
                        for ip in old_ips:
                            config["ip_addresses"][ip] = ""
                    
                    # Merge with defaults for any missing keys
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            else:
                # Create default config file
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config
    
    def setup_logging(self):
        """Setup logging configuration"""
        # Generate timestamped log filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_log_file = self.config['log_file']
        
        # Split filename and extension
        if '.' in base_log_file:
            name_part, ext_part = base_log_file.rsplit('.', 1)
            timestamped_log_file = f"{name_part}_{timestamp}.{ext_part}"
        else:
            timestamped_log_file = f"{base_log_file}_{timestamp}"
        
        # Update config with timestamped filename
        self.config['log_file'] = timestamped_log_file
        
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(timestamped_log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Log the start of the session
        self.logger.info(f"PingTest session started - Log file: {timestamped_log_file}")
    
    def ping_host(self, ip_address: str) -> Dict:
        """Ping a single host and return results"""
        result = {
            'ip': ip_address,
            'timestamp': datetime.datetime.now().isoformat(),
            'success': False,
            'response_time': None,
            'packet_loss': 100,
            'error': None
        }
        
        try:
            # Determine ping command based on OS
            if platform.system().lower() == "windows":
                cmd = ['ping', '-n', str(self.config['ping_count']), '-w', str(self.config['timeout'] * 1000), ip_address]
            else:
                cmd = ['ping', '-c', str(self.config['ping_count']), '-W', str(self.config['timeout']), ip_address]
            
            # Execute ping command
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config['timeout'] + 5
            )
            
            if process.returncode == 0:
                # Parse ping output
                output = process.stdout
                
                # Extract response time (average) - this is required for success
                response_time_extracted = False
                if platform.system().lower() == "windows":
                    # Windows ping output parsing
                    lines = output.split('\n')
                    for line in lines:
                        if 'Average =' in line:
                            try:
                                # Handle different Windows ping output formats
                                if 'Average =' in line:
                                    avg_time = line.split('Average =')[1].split('ms')[0].strip()
                                    result['response_time'] = float(avg_time)
                                    response_time_extracted = True
                                elif 'Average=' in line:  # No space after equals
                                    avg_time = line.split('Average=')[1].split('ms')[0].strip()
                                    result['response_time'] = float(avg_time)
                                    response_time_extracted = True
                            except (ValueError, IndexError):
                                # Try alternative parsing if the first method fails
                                try:
                                    # Look for time pattern like "Average = 5.00ms"
                                    import re
                                    time_match = re.search(r'Average\s*=\s*(\d+\.?\d*)ms', line)
                                    if time_match:
                                        result['response_time'] = float(time_match.group(1))
                                        response_time_extracted = True
                                except:
                                    pass
                        elif 'Lost =' in line:
                            try:
                                lost_info = line.split('Lost =')[1].split('(')[0].strip()
                                sent_info = line.split('Sent =')[1].split(',')[0].strip()
                                lost = int(lost_info)
                                sent = int(sent_info)
                                if sent > 0:
                                    result['packet_loss'] = (lost / sent) * 100
                            except:
                                pass
                else:
                    # Linux/Mac ping output parsing
                    lines = output.split('\n')
                    for line in lines:
                        if 'rtt min/avg/max' in line:
                            try:
                                # Handle different Linux/Mac ping output formats
                                if 'rtt min/avg/max' in line:
                                    avg_time = line.split('avg/')[1].split('/')[0]
                                    result['response_time'] = float(avg_time)
                                    response_time_extracted = True
                                elif 'round-trip' in line:  # Alternative format
                                    import re
                                    time_match = re.search(r'avg\s*=\s*(\d+\.?\d*)', line)
                                    if time_match:
                                        result['response_time'] = float(time_match.group(1))
                                        response_time_extracted = True
                            except (ValueError, IndexError):
                                # Try alternative parsing if the first method fails
                                try:
                                    import re
                                    time_match = re.search(r'avg\s*=\s*(\d+\.?\d*)', line)
                                    if time_match:
                                        result['response_time'] = float(time_match.group(1))
                                        response_time_extracted = True
                                except:
                                    pass
                        elif 'packets transmitted' in line:
                            try:
                                parts = line.split(',')
                                transmitted = int(parts[0].split()[0])
                                received = int(parts[1].split()[0])
                                if transmitted > 0:
                                    result['packet_loss'] = ((transmitted - received) / transmitted) * 100
                            except:
                                pass
                
                # Only mark as successful if we actually got a response time
                if response_time_extracted:
                    result['success'] = True
                else:
                    result['error'] = "Failed to parse response time from ping output"
                    result['success'] = False
            else:
                result['error'] = f"Ping failed with return code: {process.returncode}"
                if process.stderr:
                    result['error'] += f" - {process.stderr.strip()}"
                    
        except subprocess.TimeoutExpired:
            result['error'] = "Ping command timed out"
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def log_ping_result(self, result: Dict):
        """Log ping result to file and console"""
        # Get IP name if available
        ip_name = self.config['ip_addresses'].get(result['ip'], "")
        display_text = f"{ip_name} ({result['ip']})" if ip_name else result['ip']
        
        if result['success']:
            self.logger.info(
                f"Ping to {display_text}: SUCCESS - "
                f"Response time: {result['response_time']:.2f}ms, "
                f"Packet loss: {result['packet_loss']:.1f}%"
            )
        else:
            self.logger.error(
                f"Ping to {display_text}: FAILED - {result['error']}"
            )
    
    def run_ping_test(self):
        """Run ping test for all configured IP addresses"""
        ip_addresses = self.config['ip_addresses']
        
        if not ip_addresses:
            self.logger.error("No IP addresses configured")
            return
        
        # Calculate end time if total_runtime is set
        start_time = datetime.datetime.now()
        end_time = None
        if self.config['total_runtime'] > 0:
            end_time = start_time + datetime.timedelta(seconds=self.config['total_runtime'])
            self.logger.info(f"Starting ping test for {len(ip_addresses)} IP addresses")
            self.logger.info(f"Ping interval: {self.config['ping_interval']} seconds")
            self.logger.info(f"Ping count per check: {self.config['ping_count']}")
            self.logger.info(f"Total runtime: {self.config['total_runtime']} seconds")
            self.logger.info(f"Application will stop at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            self.logger.info(f"Starting ping test for {len(ip_addresses)} IP addresses")
            self.logger.info(f"Ping interval: {self.config['ping_interval']} seconds")
            self.logger.info(f"Ping count per check: {self.config['ping_count']}")
            self.logger.info("Application will run indefinitely (press Ctrl+C to stop)")
        
        try:
            while True:
                # Check if we've reached the total runtime limit
                if end_time and datetime.datetime.now() >= end_time:
                    elapsed_time = datetime.datetime.now() - start_time
                    self.logger.info("-" * 50)
                    self.logger.info(f"Total runtime limit reached: {elapsed_time.total_seconds():.1f} seconds")
                    self.logger.info("Stopping ping test application")
                    break
                
                self.logger.info("-" * 50)
                self.logger.info(f"Ping test started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                for ip, display_name in ip_addresses.items():
                    if display_name:
                        self.logger.info(f"Pinging {display_name} ({ip})...")
                    else:
                        self.logger.info(f"Pinging {ip}...")
                    result = self.ping_host(ip)
                    self.log_ping_result(result)
                    time.sleep(1)  # Small delay between pings
                
                self.logger.info(f"Ping test completed at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Check if we should continue or stop
                if end_time and datetime.datetime.now() >= end_time:
                    elapsed_time = datetime.datetime.now() - start_time
                    self.logger.info(f"Total runtime limit reached: {elapsed_time.total_seconds():.1f} seconds")
                    self.logger.info("Stopping ping test application")
                    break
                
                self.logger.info(f"Next test in {self.config['ping_interval']} seconds...")
                time.sleep(self.config['ping_interval'])
                
        except KeyboardInterrupt:
            elapsed_time = datetime.datetime.now() - start_time
            self.logger.info(f"Ping test stopped by user after {elapsed_time.total_seconds():.1f} seconds")
        except Exception as e:
            elapsed_time = datetime.datetime.now() - start_time
            self.logger.error(f"Unexpected error after {elapsed_time.total_seconds():.1f} seconds: {e}")
    
    def run_single_test(self):
        """Run a single ping test and exit"""
        ip_addresses = self.config['ip_addresses']
        
        if not ip_addresses:
            self.logger.error("No IP addresses configured")
            return
        
        self.logger.info(f"Running single ping test for {len(ip_addresses)} IP addresses")
        
        for ip, display_name in ip_addresses.items():
            if display_name:
                self.logger.info(f"Pinging {display_name} ({ip})...")
            else:
                self.logger.info(f"Pinging {ip}...")
            result = self.ping_host(ip)
            self.log_ping_result(result)
            time.sleep(1)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PingTest - Network ping monitoring application')
    parser.add_argument('--config', '-c', default='config.json', help='Configuration file path')
    parser.add_argument('--single', '-s', action='store_true', help='Run single test and exit')
    parser.add_argument('--interval', '-i', type=int, help='Override ping interval from config')
    parser.add_argument('--runtime', '-r', type=int, help='Override total runtime from config (in seconds)')
    
    args = parser.parse_args()
    
    try:
        pingtest = PingTest(args.config)
        
        # Override interval if specified
        if args.interval:
            pingtest.config['ping_interval'] = args.interval
        
        # Override runtime if specified
        if args.runtime:
            pingtest.config['total_runtime'] = args.runtime
        
        if args.single:
            pingtest.run_single_test()
        else:
            pingtest.run_ping_test()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 