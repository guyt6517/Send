from flask import Flask, request, jsonify
import requests
import guinicorn 
app = Flask(__name__)

# Replace with the IP address or URL of the target server
TARGET_SERVER_IP = "http://example.com/endpoint"

# A simple in-memory ban list (extend as needed)
ban_list = set()

@app.route('/report-ip', methods=['POST'])
def report_ip():
    """
    Endpoint that captures the IP address of the client making the request,
    checks if it's banned, and forwards it to the target server.
    """
    # Get the IP address of the client making the request
    client_ip = request.remote_addr

    # Log the IP address for debugging
    print(f"Received request from client IP: {client_ip}")

    # Check if the IP is already in the ban list
    if client_ip in ban_list:
        return jsonify({"status": "banned", "message": "Your IP is banned."}), 403

    # Add the IP to the ban list (for demonstration purposes, assume all IPs are banned)
    ban_list.add(client_ip)
    print(f"Client IP {client_ip} added to the ban list.")

    # Automatically forward the IP address to the target server
    try:
        response = requests.post(TARGET_SERVER_IP, json={"banned_ip": client_ip})
        return jsonify({
            "status": "success",
            "message": "Client IP address forwarded to the target server.",
            "target_server_response": response.json()
        }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/ban-list', methods=['GET'])
def get_ban_list():
    """
    Endpoint to retrieve the current ban list.
    """
    return jsonify({"ban_list": list(ban_list)}), 200

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000)
