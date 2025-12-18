######################################################
# Abdul-Rehman-0787
######################################################
import socket                                      
import threading
import time
import os

HOST = 'localhost'
PORT = 10000

######################################################
# Color codes
######################################################
COLORS = {
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[0m',
    'bold': '\033[1m'
}

######################################################
# Clear terminal screen
######################################################
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    return 0

######################################################
# Global exit flag
######################################################
exit_flag = False


######################################################
# Receive messages from server
######################################################
def receive_messages(sock):
    global exit_flag  
    
    while not exit_flag:  
        data = sock.recv(4096).decode()
        if len(data) == 0:
            print("\n" + COLORS['red'] + "Server Disconnected!" + COLORS['reset'])
            exit_flag = True  
            return 0
        
        
        if "[WAIT_THEN_CLEAR]" in data:
            data = data.replace("[WAIT_THEN_CLEAR]", "")
            if "[CLEAR_SCREEN]" in data:
                data = data.replace("[CLEAR_SCREEN]", "")
            elif "[SHORT_WAIT]" in data:
                data = data.replace("[SHORT_WAIT]", "")
            elif "[ERROR_WAIT]" in data:
                data = data.replace("[ERROR_WAIT]", "")
            elif "[WAIT_INPUT]" in data:
                data = data.replace("[WAIT_INPUT]", "")
            print(data, end='')
            trash = ""
            trash = input("\n" + COLORS['yellow'] + "Press Enter To Continue..." + COLORS['reset'] + " ")
            clear_screen()
            
        elif "[CLEAR_SCREEN]" in data:
            clear_screen()
            data = data.replace("[CLEAR_SCREEN]", "")
            if "[SHORT_WAIT]" in data:
                data = data.replace("[SHORT_WAIT]", "")
            elif "[ERROR_WAIT]" in data:
                data = data.replace("[ERROR_WAIT]", "")
            elif "[WAIT_INPUT]" in data:
                data = data.replace("[WAIT_INPUT]", "")
            print(data, end='')
            
        elif "[SHORT_WAIT]" in data:
            data = data.replace("[SHORT_WAIT]", "")
            if "[ERROR_WAIT]" in data:
                data = data.replace("[ERROR_WAIT]", "")
            elif "[WAIT_INPUT]" in data:
                data = data.replace("[WAIT_INPUT]", "")
            print(data, end='')
            time.sleep(1.5)  
            
        elif "[ERROR_WAIT]" in data:
            data = data.replace("[ERROR_WAIT]", "")
            if "[WAIT_INPUT]" in data:
                data = data.replace("[WAIT_INPUT]", "")
            print(data, end='')
            time.sleep(2)  
            
        elif "[WAIT_INPUT]" in data:
            data = data.replace("[WAIT_INPUT]", "")
            print(data, end='')
            
        else:
            print(data, end='')

######################################################
# Main client function
######################################################
def main():
    global exit_flag  
    
    clear_screen()
    
    ######################################################
    # Title
    ######################################################
    print(COLORS['green'] + "="*50)
    print("     Restaurant Booking Client")
    print("="*50 + COLORS['reset'] + "\n")
    
    ######################################################
    # Connect to server
    ######################################################
    print(COLORS['blue'] + "Connecting To Server..." + COLORS['reset'])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    print(COLORS['green'] + "Connected To Server!" + COLORS['reset'] + "\n")
    
    ######################################################
    # Start receive thread
    ######################################################
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    recv_thread.daemon = True
    recv_thread.start()
    
    ######################################################
    # Send user input
    ######################################################
    while not exit_flag: 
        user_input = ""
        user_input = input()
        client_socket.send(user_input.encode())
        
        if user_input.lower() == 'exit' or user_input == '5':  
            print("\n" + COLORS['yellow'] + "Disconnecting..." + COLORS['reset'])
            exit_flag = True  
            break
    
    client_socket.close()
    clear_screen()
    print(COLORS['green'] + "="*50)
    print("  Thank You For Using Restaurant Booking System!")
    print("="*50 + COLORS['reset'] + "\n")
    return 0

######################################################
# Run main function
######################################################
if __name__ == "__main__":
    main()
