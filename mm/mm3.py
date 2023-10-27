import logging
from flask import Flask, request, Response
from quality_interface import apply_quality_rules
import os

app = Flask(__name__)

@app.route('/<folder>/master.m3u8')
def serve_m3u8_playlist(folder):
    quality = request.args.get('quality', 'high')

    # Access IP and User Agent directly from the request
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Configure logging with IP and User Agent
    configure_logging(ip, user_agent)

    # Determine the path to the requested M3U8 playlist on the server
    playlist_path = os.path.join('/storage', folder, 'master.m3u8')

    if os.path.isfile(playlist_path):
        # Read the original M3U8 playlist from the server
        with open(playlist_path, 'r') as file:
            m3u8_content = file.read()

        # Apply the quality rules using the common interface
        modified_playlist = apply_quality_rules(m3u8_content, quality)

        response = Response(modified_playlist, content_type='application/vnd.apple.mpegurl')
        return response

    return "Not Found", 404

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
    app.run(host='0.0.0.0', port=5000)

