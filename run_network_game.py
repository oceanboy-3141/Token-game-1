#!/usr/bin/env python3
"""
Network version of Token Quest Flask App
Allows other devices on your WiFi to play the game
"""
import socket
from main import app

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def print_network_info(ip, port):
    """Print network connection information"""
    print("🎮 Token Quest - Network Edition")
    print("=" * 50)
    print(f"🌐 Server running on: {ip}:{port}")
    print(f"📱 Share this URL with players on your WiFi:")
    print(f"   http://{ip}:{port}")
    print("=" * 50)
    print("✨ Each player gets their own game session!")
    print("🔗 Players can access from any device with a web browser")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    
    print_network_info(local_ip, port)
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for playing Token Quest!")
    except Exception as e:
        print(f"\n❌ Error running server: {e}")
        print("Make sure port 5000 is not already in use!") 