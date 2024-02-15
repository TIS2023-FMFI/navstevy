import socket
from PIL import Image
from Visitor import Visitor
from IpConfigParser import ipconfig_all
from threading import Thread
import time


class Communication:
    TIMEOUT_SECONDS = 60
    message_code = {
        ## sending message
        "guardian_angel": 0,
        "presentation_start": 1,
        "presentation_end": 2,
        "rating_start": 3,

        ## recieving message
        "wrong_data": 4,
        "progress": 5,
        "signature": 6,
        "rating": 7,
        "error": 8,

    }

    def __init__(self):
        self.port_out = 5013
        self.port_in = 5014
        self.port_check = 5015

        self.is_device_connected = False
        self.is_application_running = False
        self.device_ip_adress = None

        self.my_angel_alive = True
        self.my_angel = Thread(target=self.guardian_angel)
        self.my_angel.start()
    
    def close(self):
        #print("Koniec komunikacie")
        self.angel_wait_time = 0
        self.my_angel_alive = False
        self.my_angel.join()
        #print("Komunikácia ukončená")

    def stable(self):
        return self.is_device_connected and self.is_application_running

    def guardian_angel(self):
        self.angel_wait_time = 0
        while self.my_angel_alive:
            
            if not self.try_connect_android_device():
                time.sleep(1)
                self.angel_wait_time = 1
                continue
            self.angel_wait_time = 3
            if not self.guardian_angel_check():
                time.sleep(1)
                self.angel_wait_time = 3
                continue
            self.angel_wait_time = 5
            time.sleep(1)
            #print("Komunikácia beží...", end="\r")

    def try_connect_android_device(self):
        try:
            self.device_ip_adress = self.get_android_device_ip()
            self.is_device_connected = True
            return True
        except:
            self.is_device_connected = False
            self.is_application_running = False
            self.device_ip_adress = None
            #print("Device not found...")
            return False
        
    def guardian_angel_check(self):
        try:
            ## Sends message to check connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
                message = Communication.message_code["guardian_angel"].to_bytes(1)
                if self.is_application_running:
                    message += int(0).to_bytes(1)
                else:
                    message += int(1).to_bytes(1)
                s.connect((self.device_ip_adress, self.port_check))
                s.sendall(message)
                
                self.is_application_running = True
                return True
        except:
            #print("App not running ...")
            self.is_application_running = False
            return False



    def get_android_device_ip(self):
        ip_config_result = ipconfig_all()

        for adapter_name, atributes in ip_config_result.items():
            if "Ethernet adapter Ethernet" not in adapter_name:
                continue
            if "Description" not in atributes:
                continue 
            if "UsbNcm Host Device" in atributes["Description"] or "Remote NDIS based Internet Sharing Device" in atributes["Description"]:
                return atributes["Default Gateway"]
        raise Exception("Android device not found")
        
    def send_start_presentation(self, visitor: Visitor):
        try:
            ## Sends message to start presentation for given visitor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                message_code = Communication.message_code["presentation_start"].to_bytes(1)
                visitor_string = visitor.getDataToWrite().encode('utf-8')
                data_lenght = len(visitor_string).to_bytes(1)

                message = message_code + data_lenght + visitor_string
                s.connect((self.device_ip_adress, self.port_out))
                s.sendall(message)
                s.close()
                #print("---> Presentation started...")
            return Communication.message_code["progress"], None
        except Exception as e:
            #print(e)
            return Communication.message_code["error"], "Device not connected properly or application not running"

    
    def send_start_review(self, visitor: Visitor):
        try:
            ## Sends message to start review for given visitor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                message_code = Communication.message_code["rating_start"].to_bytes(1)
                visitor_string = visitor.getDataToWrite().encode('utf-8')
                data_lenght = len(visitor_string).to_bytes(1)

                message = message_code + data_lenght + visitor_string
                s.connect((self.device_ip_adress, self.port_out))
                s.sendall(message)
                s.close()
                #print("---> Review started...")
            return Communication.message_code["progress"], None
        except:
            return Communication.message_code["error"], "Device not connected properly or application not running"

    def send_end_presentation(self):
        try:
            ## Sends message to end presentation
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                message = Communication.message_code["presentation_end"].to_bytes(1)
                s.connect((self.device_ip_adress, self.port_check))
                s.sendall(message)
                #print(f"---> Presentation ended")
            return Communication.message_code["presentation_end"], None
        except:
            return Communication.message_code["error"], "Device not connected properly or application not running"
            

    def recieve(self, array_to_write: list):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ##s.bind((self.device_ip_adress, self.port_in))
            s.bind(("0.0.0.0", self.port_in))
            s.listen()
            s.settimeout(self.TIMEOUT_SECONDS)
            
            try:
                # Accept a single incoming connection
                #print("---- Waiting for some respond ---- ")
                client_socket, client_address = s.accept()

                # Receive data from the client
                message_code = int.from_bytes(client_socket.recv(1))

                if message_code == Communication.message_code["presentation_end"]:
                    client_socket.close()
                    #print("<--- Prezentácia ukončená")
                    array_to_write.append(message_code)
                    array_to_write.append(None)
                    return message_code, None
                
                if message_code == Communication.message_code["wrong_data"]:
                    client_socket.close()
                    #print("<--- Zle zadané dáta")
                    array_to_write.append(message_code)
                    array_to_write.append(None)
                    return message_code, None
            
                if message_code == Communication.message_code["progress"]:
                    progres_percentage = int.from_bytes(client_socket.recv(4))
                    client_socket.close()
                    #print(f"<--- Progress ... {progres_percentage}%")
                    array_to_write.append(message_code)
                    array_to_write.append(progres_percentage)
                    return message_code, progres_percentage
                
                if message_code == Communication.message_code["signature"]:
                    width = int.from_bytes(client_socket.recv(4))
                    height = int.from_bytes(client_socket.recv(4))

                    signature = Image.new('RGB', (width, height), color='white')
                    for y in range(height):
                        for x in range(width):
                            pixel_color = int.from_bytes(client_socket.recv(1))
                            if pixel_color == 0:
                                signature.putpixel((x, y), (0, 0, 0))
                    
                    client_socket.close()
                    #print("<--- Signature")
                    array_to_write.append(message_code)
                    array_to_write.append(signature)
                    return message_code, signature
                
                if message_code == Communication.message_code["error"]:
                    message_lenght = int.from_bytes(client_socket.recv(4))
                    error_message = client_socket.recv(message_lenght).decode('utf-8')
                    client_socket.close()
                    #print(f"<--- Error: {error_message}")
                    array_to_write.append(message_code)
                    array_to_write.append(error_message)
                    return message_code, error_message
                
                if message_code == Communication.message_code["rating"]:
                    rating = int.from_bytes(client_socket.recv(4))
                    client_socket.close()
                    #print(f"<--- Rating ... {rating}")
                    array_to_write.append(message_code)
                    array_to_write.append(rating)
                    return message_code, rating

                #print("<--- Zle formatovaná správa")
                array_to_write.append(Communication.message_code["error"])
                array_to_write.append("Wrong message type")
                client_socket.close()
                return Communication.message_code["error"], "Wrong message type"
            except:
                return Communication.message_code["error"], f"Device didn't respond in {self.TIMEOUT_SECONDS}"
        
if __name__ == "__main__":
    communication = Communication()
    while not communication.stable():
        pass

    visitor = Visitor(15, "Jožko", "Mrkvička", 1, "AB-123-CD", "Matfyz", 0, "Musim")

    state, data = communication.send_start_presentation(visitor)
    ##state, data = communication.send_start_review(visitor)
    while state == Communication.message_code["progress"]:
        state, data = communication.recieve(list())
    
    
    print(state)
    print(data)
    communication.close()