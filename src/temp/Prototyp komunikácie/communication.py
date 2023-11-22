from ppadb.client import Client
import socket

def get_android_device_ip():
    try:
        # Create a connection to the ADB server
        adb = Client(host='127.0.0.1', port=5037)
        
        # Get the list of connected devices
        devices = adb.devices()
        
        if not devices:
            print("No Android devices connected.")
            return None

        # Assuming only one device is connected, you can access it directly
        device = devices[0]

        # Run 'adb shell ip route' command to get the device IP address
        result = device.shell('ip route')

        # Extract the IP address from the result
        ip_address = result.split('src ')[1].split(' ')[0]

        return ip_address
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_message(message, host, port=5555):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))


if __name__ == "__main__":
    device_ip = get_android_device_ip()
    message_to_send = "Hello from Python"
    
    if device_ip:
        send_message(message_to_send, device_ip)
        print("Message send")
    else:
        print("Couln't send message")
