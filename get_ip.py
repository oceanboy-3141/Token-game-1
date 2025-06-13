"""
Simple script to find your computer's IP address for sharing Token Quest
"""
import socket
import subprocess
import sys

def get_local_ip():
    """Get the local IP address of this computer."""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return None

def get_all_ips():
    """Get all network interfaces and their IPs."""
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            return result.stdout
        else:
            # Linux/Mac
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            return result.stdout
    except Exception:
        return "Could not retrieve network information"

if __name__ == "__main__":
    print("🌐 Token Quest - Network Information")
    print("=" * 50)
    
    local_ip = get_local_ip()
    if local_ip:
        print(f"✅ Your computer's IP address: {local_ip}")
        print(f"🚀 Share this URL with others: http://{local_ip}:5000")
        print()
        print("📝 Instructions:")
        print("1. Make sure your Flask app is running")
        print("2. Share the URL above with your mom")
        print("3. Make sure you're both on the same WiFi network")
        print()
        print("⚠️  Note: This only works if you're on the same network (same WiFi)")
    else:
        print("❌ Could not determine your IP address")
    
    print("\n🔍 All Network Information:")
    print("-" * 30)
    print(get_all_ips()) 