from ppadb.client import Client
import socket
from PIL import Image
from Visitor import Visitor

class Communication:
    message_type = {
        "start": 1,
        "end": 2,
        "prograss": 3,
        "signature": 4
    }

    def __init__(self):
        self.device_ip_adress = self.get_android_device_ip()
        self.device_ip_adress = "localhost" ## for debugging
        self.port = 5555


    def get_android_device_ip(self):
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


    def start_presentation(self, visitor: Visitor):
        ## Sends message to start presentation for given visitor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            message_type = Communication.message_type["start"].to_bytes(1)
            visitor_string = visitor.getDataToWrite().encode('utf-8')
            data_lenght = len(visitor_string).to_bytes(1)

            message = message_type + data_lenght + visitor_string
            s.connect((self.device_ip_adress, self.port))
            s.sendall(message)

    def end_presentation(self):
        ## Sends message to end presentation
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            message = Communication.message_type["end"].to_bytes(1)
            s.connect((self.device_ip_adress, self.port))
            s.sendall(message)

    def recieve(self):
        ...
  

    
    
    

if __name__ == "__main__":
    communication = Communication()
    visitor = Visitor(15, "Jožko", "Mrkvička", 1, "AB-123-CD", "Matfyz", 0, "Musim")

    communication.start_presentation(visitor)
    
    communication.end_presentation()

    
    

