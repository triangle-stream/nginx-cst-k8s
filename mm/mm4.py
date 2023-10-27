import logging
from flask import Flask, request, Response
from quality_interface import apply_quality_rules
import os
import requests

app = Flask(__name__)

# Define the base URL for the remote server
REMOTE_SERVER_URL = "http://dev.trianglestream.com:6081"

@app.route('/<folder>/master.m3u8')
def serve_m3u8_playlist(folder):
    quality = request.args.get('quality', 'high')

    # Access IP and User Agent directly from the request
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Configure logging with IP and User Agent
    configure_logging(ip, user_agent)

    # Determine the path to the requested M3U8 playlist on the remote server
    remote_playlist_url = f"{REMOTE_SERVER_URL}/{folder}/master.m3u8"

    # Fetch the remote playlist
    try:
        response = requests.get(remote_playlist_url)
        response.raise_for_status()
        m3u8_content = response.text
    except requests.exceptions.RequestException as e:
        return "Error fetching the remote playlist", 500

    # Apply the quality rules using the common interface
    modified_playlist = apply_quality_rules(m3u8_content, quality)

    return Response(modified_playlist, content_type='application/vnd.apple.mpegurl')

def configure_logging(ip, user_agent):
    # Create a custom log formatter
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            return super().format(record).replace('{ip}', ip).replace('{user_agent}', user_agent)

    # Configure the root logger to write logs to the console and 'logs.log'
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - IP: {ip} - User Agent: {user_agent} - %(message)s')        
    log_handler = logging.FileHandler('logs.log')
    log_handler.setFormatter(CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - IP: {ip} - User Agent: {user_agent} - %(message)s'))
    root_logger = logging.getLogger()
    root_logger.addHandler(log_handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)

