from ppadb.client import Client
import socket
from PIL import Image
from Visitor import Visitor
import asyncio

class Communication:
    message_code = {
        ## sending message
        "presentation_start": 1,
        "presentation_end": 2,
        "rating_start": 3,

        ## recieving message
        "wrong_data": 4,
        "progress": 5,
        "signature": 6,
        "rating": 7,
        "error": 8
    }


    def __init__(self):
        ##self.device_ip_adress = "127.0.0.1"
        self.device_ip_adress =self.get_android_device_ip()
        self.port_out = 5013
        self.port_in = 5014
        ##self.initialize_android_debbuging_connection()

    def get_android_device_ip(self):
        # Create a connection to the ADB server
        adb = Client(host='127.0.0.1', port=5037)
        
        # Get the list of connected devices
        devices = adb.devices()
        if not devices:
            raise Exception("No Android devices connected to computer.")
        
        # Assuming only one device is connected, you can access it directly
        device = devices[0]

        # Run 'adb shell ip route' command to get the device IP addresss
        result = device.shell('ip route')
    
        # Extract the IP address from the result
        ip_address = result.split('src ')[1].split(' ')[0]

        return ip_address

    def initialize_android_debbuging_connection(self):
        # Create a connection to the ADB server
        adb = Client(host='127.0.0.1', port=5037)
        
        # Get the list of connected devices
        devices = adb.devices()
        if not devices:
            raise Exception("No Android devices connected to computer.")
        
        # Assuming only one device is connected, you can access it directly
        device = devices[0]

        # Run 'adb shell ip route' command to get the device IP addresss
        result = device.shell(f"forward tcp:{self.port_out} tcp:{self.port_out}")
        print(result)
        result = device.shell(f"reverse tcp:{self.port_in} tcp:{self.port_in}")
        print(result)
        
    def send_start_presentation(self, visitor: Visitor):
        ## Sends message to start presentation for given visitor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            message_code = Communication.message_code["presentation_start"].to_bytes(1)
            visitor_string = visitor.getDataToWrite().encode('utf-8')
            data_lenght = len(visitor_string).to_bytes(1)

            message = message_code + data_lenght + visitor_string
            s.connect((self.device_ip_adress, self.port_out))
            s.sendall(message)
            s.close()
            print("Presentation started...")
        return Communication.message_code["progress"], None
    
    def send_start_review(self, visitor: Visitor):
        ## Sends message to start review for given visitor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            message_code = Communication.message_code["rating_start"].to_bytes(1)
            visitor_string = visitor.getDataToWrite().encode('utf-8')
            data_lenght = len(visitor_string).to_bytes(1)

            message = message_code + data_lenght + visitor_string
            s.connect((self.device_ip_adress, self.port_out))
            s.sendall(message)
            s.close()
            print("Review started...")
        return Communication.message_code["progress"], None

    def send_end_presentation(self):
        ## Sends message to end presentation
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            message = Communication.message_code["presentation_end"].to_bytes(1)
            s.connect((self.device_ip_adress, self.port_out))
            s.sendall(message)
        return Communication.message_code["presentation_end"]

    def recieve(self):
        print("---- Waiting for some message ---- ")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ##s.bind((self.device_ip_adress, self.port_in))
            s.bind(("0.0.0.0", self.port_in))
            s.listen()
            
            # Accept a single incoming connection
            client_socket, client_address = s.accept()

            # Receive data from the client
            message_code = int.from_bytes(client_socket.recv(1))
            
            if message_code == Communication.message_code["wrong_data"]:
                client_socket.close()
                print("Zle data")
                return message_code, None
        
            if message_code == Communication.message_code["progress"]:
                progres_percentage = int.from_bytes(client_socket.recv(4))
                client_socket.close()
                print(f"Progress ... {progres_percentage}")
                return message_code, progres_percentage
            
            if message_code == Communication.message_code["signature"]:
                width = int.from_bytes(client_socket.recv(4))
                height = int.from_bytes(client_socket.recv(4))

                print(width)
                print(height)
                signature = Image.new('RGB', (width, height), color='white')
                for y in range(height):
                    for x in range(width):
                        pixel_color = int.from_bytes(client_socket.recv(1))
                        if pixel_color == 0:
                            signature.putpixel((x, y), (0, 0, 0))
                
                client_socket.close()
                print("Signature")
                return message_code, signature
            
            if message_code == Communication.message_code["error"]:
                message_lenght = int.from_bytes(client_socket.recv(4))
                error_message = client_socket.recv(message_lenght).decode('utf-8')
                client_socket.close()
                print(f"Error: {error_message}")
                return message_code, error_message
            
            if message_code == Communication.message_code["rating"]:
                rating = int.from_bytes(client_socket.recv(4))
                client_socket.close()
                print(f"Rating ... {rating}")
                return message_code, rating


            # Close the client socket
            print("zla sprava")
            client_socket.close()

             

        
        return None, None

    
    
    

if __name__ == "__main__":
    communication = Communication()
    visitor = Visitor(15, "Jožko", "Mrkvička", 1, "AB-123-CD", "Matfyz", 0, "Musim")
    
    state, data = communication.send_start_presentation(visitor)
    ##state, data = communication.send_start_review(visitor)
    while state == Communication.message_code["progress"]:
        state, data = communication.recieve()
    
    print(state)
    print(data)
    

        
    


    
    

