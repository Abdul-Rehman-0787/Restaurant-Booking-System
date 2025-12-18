######################################################
# Abdul-Rehman-0787
######################################################

######################################################
#                     Admin Credentials
######################################################
# Admin User Name : admin
# Admin Password  : HotelManager
######################################################
import socket
import threading
import time
import datetime

HOST = 'localhost'
PORT = 10000

######################################################
# Create server socket
######################################################
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("\033[92m" + "=" * 50)
print("     Restaurant Booking Server Started")
print("=" * 50 + "\033[0m")
print("Waiting For Clients...\n")

######################################################
# Store data
######################################################
active_clients = []
waiting_queue = []
reservations = []

######################################################
# Days of week
######################################################
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
time_slots = {
    "hi-tea": ["11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM"],
    "dinner": ["6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM"]
}

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
# Check day availability (max 2 reservations per slot per day)
######################################################
def check_availability(day, buffet_type, time_slot):
    count = 0
    for res in reservations:
        if res['day'] == day and res['buffet'] == buffet_type and res['time'] == time_slot:
            count = count + 1
    if count < 2:
        return True
    else:
        return False

######################################################
# Handle client connection
######################################################
def handle_client(connection, client_address):
    client_id = str(client_address[0]) + ":" + str(client_address[1])
    print(COLORS['green'] + "[+] Client Connected: " + client_id + COLORS['reset'])
    
    ######################################################
    # Check if server is full
    ######################################################
    if len(active_clients) >= 5:
        if len(waiting_queue) < 10:
            waiting_queue.append((connection, client_address))
            msg = "[CLEAR_SCREEN]" + COLORS['yellow'] + "\n" + "="*50 + "\n"
            msg = msg + "     Server Status\n"
            msg = msg + "="*50 + COLORS['reset'] + "\n\n"
            msg = msg + COLORS['yellow'] + "Server Is Full. You Are In Queue.\n"
            msg = msg + "Position: #" + str(len(waiting_queue)) + "\n"
            msg = msg + "Please Wait..." + COLORS['reset'] + "\n[WAIT_THEN_CLEAR]"
            connection.send(msg.encode())
            return
        else:
            msg = "[CLEAR_SCREEN]" + COLORS['red'] + "\n" + "="*50 + "\n"
            msg = msg + "     Server Status\n"
            msg = msg + "="*50 + COLORS['reset'] + "\n\n"
            msg = msg + COLORS['red'] + "Server And Queue Are Full.\n"
            msg = msg + "Please Try Again Later." + COLORS['reset'] + "\n[ERROR_WAIT]"
            connection.send(msg.encode())
            connection.close()
            return
    
    ######################################################
    # Add to active clients
    ######################################################
    active_clients.append((connection, client_address))
    print(COLORS['blue'] + "[*] Active Clients: " + str(len(active_clients)) + COLORS['reset'])
    
    try:
        ######################################################
        # Welcome message
        ######################################################
        welcome = "[CLEAR_SCREEN]" + COLORS['bold'] + COLORS['green'] + "\n" + "="*50
        welcome = welcome + "\n      Welcome To Restaurant Booking System\n"
        welcome = welcome + "="*50 + COLORS['reset'] + "\n\n[SHORT_WAIT]"
        connection.send(welcome.encode())
        
        ######################################################
        # Main menu loop
        ######################################################
        while True:
            ######################################################
            # Display menu
            ######################################################
            menu = "[CLEAR_SCREEN]" + COLORS['cyan'] + "\n" + "="*40 + "\n"
            menu = menu + COLORS['bold'] + "    Restaurant Booking System\n"
            menu = menu + COLORS['cyan'] + "="*40 + COLORS['reset'] + "\n"
            menu = menu + COLORS['yellow'] + "[1]" + COLORS['reset'] + " View Time Slots\n"
            menu = menu + COLORS['yellow'] + "[2]" + COLORS['reset'] + " Make Reservation\n"
            menu = menu + COLORS['yellow'] + "[3]" + COLORS['reset'] + " View My Bookings\n"
            menu = menu + COLORS['yellow'] + "[4]" + COLORS['reset'] + " Admin Login\n"
            menu = menu + COLORS['yellow'] + "[5]" + COLORS['reset'] + " Exit\n"
            menu = menu + COLORS['green'] + "\nEnter Choice (1-5): " + COLORS['reset']
            connection.send(menu.encode())
            
            choice = connection.recv(1024).decode().strip()
            
            if choice == "1":
                ######################################################
                # Show time slots
                ######################################################
                slots_msg = "[CLEAR_SCREEN]" + COLORS['cyan'] + "\n" + "-"*40 + "\n"
                slots_msg = slots_msg + COLORS['bold'] + "     Available Time Slots\n"
                slots_msg = slots_msg + COLORS['cyan'] + "-"*40 + COLORS['reset'] + "\n\n"
                
                slots_msg = slots_msg + COLORS['yellow'] + "Hi-Tea Buffet:\n" + COLORS['reset']
                for i in range(1, 5):
                    slots_msg = slots_msg + "  " + str(i) + ". " + time_slots["hi-tea"][i-1] + "\n"
                
                slots_msg = slots_msg + "\n" + COLORS['yellow'] + "Dinner Buffet:\n" + COLORS['reset']
                for i in range(1, 5):
                    slots_msg = slots_msg + "  " + str(i) + ". " + time_slots["dinner"][i-1] + "\n"
                
                slots_msg = slots_msg + "\n" + COLORS['green'] + "Note: Max 2 Bookings Per Time Slot Per Day" + COLORS['reset'] + "\n"
                slots_msg = slots_msg + "[WAIT_THEN_CLEAR]"
                connection.send(slots_msg.encode())
                
            elif choice == "2":
                ######################################################
                # Make reservation
                ######################################################
                connection.send(("[CLEAR_SCREEN]" + COLORS['cyan'] + "Enter Your Name: " + COLORS['reset']).encode())
                name = connection.recv(1024).decode().strip()
                
                connection.send(("[CLEAR_SCREEN]" + COLORS['cyan'] + "Enter Day (E.G., Monday, Tuesday): " + COLORS['reset']).encode())
                day = connection.recv(1024).decode().strip()
                
                if day not in days:
                    msg = COLORS['red'] + "\nInvalid Day. Use Full Day Name." + COLORS['reset'] + "\n[ERROR_WAIT]"
                    connection.send(msg.encode())
                    continue
                
                connection.send(("[CLEAR_SCREEN]" + COLORS['cyan'] + "Select Buffet Type (1 For Hi-Tea, 2 For Dinner): " + COLORS['reset']).encode())
                buffet_choice = connection.recv(1024).decode().strip()
                
                if buffet_choice == "1":
                    buffet = "hi-tea"
                    slots = time_slots["hi-tea"]
                    slot_msg = "[CLEAR_SCREEN]" + COLORS['cyan'] + "Select Time Slot (1-4):" + COLORS['reset'] + "\n"
                    for i in range(1, 5):
                        slot_msg = slot_msg + "  " + str(i) + ". " + slots[i-1] + "\n"
                    slot_msg = slot_msg + "\nYour choice: "
                    connection.send(slot_msg.encode())
                elif buffet_choice == "2":
                    buffet = "dinner"
                    slots = time_slots["dinner"]
                    slot_msg = "[CLEAR_SCREEN]" + COLORS['cyan'] + "Select Time Slot (1-4):" + COLORS['reset'] + "\n"
                    for i in range(1, 5):
                        slot_msg = slot_msg + "  " + str(i) + ". " + slots[i-1] + "\n"
                    slot_msg = slot_msg + "\nYour choice: "
                    connection.send(slot_msg.encode())
                else:
                    msg = COLORS['red'] + "\nInvalid Choice." + COLORS['reset'] + "\n[ERROR_WAIT]"
                    connection.send(msg.encode())
                    continue
                
                slot_input = connection.recv(1024).decode().strip()
                if slot_input.isdigit():
                    slot_num = int(slot_input)
                    if 1 <= slot_num <= 4:
                        time_chosen = slots[slot_num-1]
                    else:
                        msg = COLORS['red'] + "\nInvalid Slot Number." + COLORS['reset'] + "\n[ERROR_WAIT]"
                        connection.send(msg.encode())
                        continue
                else:
                    msg = COLORS['red'] + "\nInvalid Input." + COLORS['reset'] + "\n[ERROR_WAIT]"
                    connection.send(msg.encode())
                    continue
                
                ######################################################
                # Check availability
                ######################################################
                if check_availability(day, buffet, time_chosen):
                    ######################################################
                    # Save reservation
                    ######################################################
                    reservation = {
                        'name': name,
                        'day': day,
                        'buffet': buffet,
                        'time': time_chosen,
                        'client': client_id,
                        'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    reservations.append(reservation)
                    
                    ######################################################
                    # Save to file
                    ######################################################
                    with open("bookings.txt", "a") as f:
                        f.write(name + "," + day + "," + buffet + "," + time_chosen + "," + reservation['date'] + "\n")
                    
                    msg = "[CLEAR_SCREEN]" + COLORS['green'] + "\n" + "*"*50 + "\n"
                    msg = msg + "      Reservation Confirmed!\n"
                    msg = msg + "*"*50 + COLORS['reset'] + "\n\n"
                    msg = msg + COLORS['bold'] + "Name:" + COLORS['reset'] + " " + name + "\n"
                    msg = msg + COLORS['bold'] + "Day:" + COLORS['reset'] + " " + day + "\n"
                    msg = msg + COLORS['bold'] + "Time:" + COLORS['reset'] + " " + time_chosen + "\n"
                    msg = msg + COLORS['bold'] + "Buffet:" + COLORS['reset'] + " " + buffet + "\n"
                    msg = msg + COLORS['bold'] + "Booking Time:" + COLORS['reset'] + " " + reservation['date'] + "\n\n"
                    msg = msg + "[WAIT_THEN_CLEAR]"
                    connection.send(msg.encode())
                else:
                    msg = "[CLEAR_SCREEN]" + COLORS['red'] + "\nSorry! This Time Slot For " + day + " Is Fully Booked.\n"
                    msg = msg + "Please Choose Another Time Or Day." + COLORS['reset'] + "\n[ERROR_WAIT]"
                    connection.send(msg.encode())
                    
            elif choice == "3":
                ######################################################
                # View client's bookings
                ######################################################
                client_res = []
                for res in reservations:
                    if res['client'] == client_id:
                        client_res.append(res)
                
                if len(client_res) > 0:
                    msg = "[CLEAR_SCREEN]" + COLORS['cyan'] + "\n" + "-"*40 + "\n"
                    msg = msg + "     Your Bookings\n"
                    msg = msg + "-"*40 + COLORS['reset'] + "\n\n"
                    for i in range(1, len(client_res) + 1):
                        msg = msg + COLORS['yellow'] + str(i) + "." + COLORS['reset'] + " " + client_res[i-1]['name'] + " - " + client_res[i-1]['day'] + " " + client_res[i-1]['time'] + " (" + client_res[i-1]['buffet'] + ")\n"
                    msg = msg + "\n" + COLORS['green'] + "Total: " + str(len(client_res)) + " Booking(s)" + COLORS['reset'] + "\n"
                    msg = msg + "[WAIT_THEN_CLEAR]"
                    connection.send(msg.encode())
                else:
                    msg = "[CLEAR_SCREEN]" + COLORS['yellow'] + "\nNo Bookings Found For You." + COLORS['reset'] + "\n[ERROR_WAIT]"
                    connection.send(msg.encode())
                    
            elif choice == "4":
                ######################################################
                # Admin login
                ######################################################
                connection.send(("[CLEAR_SCREEN]" + COLORS['cyan'] + "Admin Username: " + COLORS['reset']).encode())
                username = connection.recv(1024).decode().strip()
                
                connection.send(("[CLEAR_SCREEN]" + COLORS['cyan'] + "Admin Password: " + COLORS['reset']).encode())
                password = connection.recv(1024).decode().strip()
                
                if username == "admin" and password == "HotelManager":
                    admin_menu(connection)
                else:
                    msg = "[CLEAR_SCREEN]" + COLORS['red'] + "\nAccess Denied! Invalid Credentials." + COLORS['reset'] + "\n[ERROR_WAIT]"
                    connection.send(msg.encode())
                    
            elif choice == "5":
                msg = "[CLEAR_SCREEN]" + COLORS['green'] + "\nThank You For Using Our Service!\nGoodbye!" + COLORS['reset'] + "\n[SHORT_WAIT]"
                connection.send(msg.encode())
                break
            else:
                msg = COLORS['red'] + "\nInvalid Choice! Please Enter 1-5." + COLORS['reset'] + "\n[ERROR_WAIT]"
                connection.send(msg.encode())
                
    except:
        pass
    
    finally:
        ######################################################
        # Clean up
        ######################################################
        if (connection, client_address) in active_clients:
            active_clients.remove((connection, client_address))
        connection.close()
        print(COLORS['yellow'] + "[-] Client Disconnected: " + client_id + COLORS['reset'])
        print(COLORS['blue'] + "[*] Active Clients: " + str(len(active_clients)) + COLORS['reset'])
        
        ######################################################
        # Move from queue if space available
        ######################################################
        if len(waiting_queue) > 0 and len(active_clients) < 5:
            next_client = waiting_queue.pop(0)
            threading.Thread(target=handle_client, args=next_client).start()

######################################################
# Admin menu function
######################################################
def admin_menu(connection):
    while True:
        menu = "[CLEAR_SCREEN]" + COLORS['magenta'] + "\n" + "="*40 + "\n"
        menu = menu + "      Admin Panel\n"
        menu = menu + "="*40 + COLORS['reset'] + "\n"
        menu = menu + COLORS['yellow'] + "[1]" + COLORS['reset'] + " View All Reservations\n"
        menu = menu + COLORS['yellow'] + "[2]" + COLORS['reset'] + " View Active Clients\n"
        menu = menu + COLORS['yellow'] + "[3]" + COLORS['reset'] + " View Queue Status\n"
        menu = menu + COLORS['yellow'] + "[4]" + COLORS['reset'] + " Check Day Availability\n"
        menu = menu + COLORS['yellow'] + "[5]" + COLORS['reset'] + " Back To Main Menu\n"
        menu = menu + COLORS['cyan'] + "\nAdmin Choice (1-5): " + COLORS['reset']
        
        connection.send(menu.encode())
        choice = connection.recv(1024).decode().strip()
        
        if choice == "1":
            if len(reservations) > 0:
                msg = "[CLEAR_SCREEN]" + COLORS['cyan'] + "\n" + "-"*50 + "\n"
                msg = msg + "        All Reservations\n"
                msg = msg + "-"*50 + COLORS['reset'] + "\n\n"
                for i in range(1, len(reservations) + 1):
                    msg = msg + str(i) + ". " + reservations[i-1]['name'] + " - " + reservations[i-1]['day'] + " " + reservations[i-1]['time'] + " (" + reservations[i-1]['buffet'] + ")\n"
                    msg = msg + "   Client: " + reservations[i-1]['client'] + " | Booked: " + reservations[i-1]['date'] + "\n\n"
                msg = msg + COLORS['green'] + "Total Reservations: " + str(len(reservations)) + COLORS['reset'] + "\n"
                msg = msg + "[WAIT_THEN_CLEAR]"
                connection.send(msg.encode())
            else:
                msg = "[CLEAR_SCREEN]" + COLORS['yellow'] + "\nNo Reservations Yet." + COLORS['reset'] + "\n[ERROR_WAIT]"
                connection.send(msg.encode())
                
        elif choice == "2":
            msg = "[CLEAR_SCREEN]" + COLORS['cyan'] + "\n" + "-"*40 + "\n"
            msg = msg + "     Active Clients\n"
            msg = msg + "-"*40 + COLORS['reset'] + "\n\n"
            msg = msg + COLORS['green'] + "Active: " + str(len(active_clients)) + "/5" + COLORS['reset'] + "\n\n"
            for i in range(1, len(active_clients) + 1):
                msg = msg + str(i) + ". " + active_clients[i-1][1][0] + ":" + str(active_clients[i-1][1][1]) + "\n"
            msg = msg + "[WAIT_THEN_CLEAR]"
            connection.send(msg.encode())
            
        elif choice == "3":
            msg = "[CLEAR_SCREEN]" + COLORS['cyan'] + "\n" + "-"*40 + "\n"
            msg = msg + "     Queue Status\n"
            msg = msg + "-"*40 + COLORS['reset'] + "\n\n"
            msg = msg + COLORS['yellow'] + "In Queue: " + str(len(waiting_queue)) + "/10" + COLORS['reset'] + "\n\n"
            if len(waiting_queue) > 0:
                for i in range(1, len(waiting_queue) + 1):
                    msg = msg + str(i) + ". " + waiting_queue[i-1][1][0] + ":" + str(waiting_queue[i-1][1][1]) + "\n"
            else:
                msg = msg + "Queue Is Empty\n"
            msg = msg + "[WAIT_THEN_CLEAR]"
            connection.send(msg.encode())
            
        elif choice == "4":
            connection.send(("[CLEAR_SCREEN]" + COLORS['cyan'] + "Enter Day To Check (E.G., Monday): " + COLORS['reset']).encode())
            day = connection.recv(1024).decode().strip()
            
            if day not in days:
                msg = COLORS['red'] + "Invalid Day. Use Full Day Name." + COLORS['reset'] + "\n[ERROR_WAIT]"
                connection.send(msg.encode())
                continue
            
            msg = "[CLEAR_SCREEN]" + COLORS['cyan'] + "\n" + "-"*50 + "\n"
            msg = msg + "     Availability For " + day.upper() + "\n"
            msg = msg + "-"*50 + COLORS['reset'] + "\n\n"
            
            msg = msg + COLORS['yellow'] + "Hi-Tea Buffet:" + COLORS['reset'] + "\n"
            for slot in time_slots["hi-tea"]:
                count = 0
                for r in reservations:
                    if r['day'] == day and r['buffet'] == "hi-tea" and r['time'] == slot:
                        count = count + 1
                available = 2 - count
                if available > 0:
                    status = COLORS['green'] + "Available (" + str(available) + " Slots)" + COLORS['reset']
                else:
                    status = COLORS['red'] + "Full" + COLORS['reset']
                msg = msg + "  " + slot + ": " + status + "\n"
            
            msg = msg + "\n" + COLORS['yellow'] + "Dinner Buffet:" + COLORS['reset'] + "\n"
            for slot in time_slots["dinner"]:
                count = 0
                for r in reservations:
                    if r['day'] == day and r['buffet'] == "dinner" and r['time'] == slot:
                        count = count + 1
                available = 2 - count
                if available > 0:
                    status = COLORS['green'] + "Available (" + str(available) + " Slots)" + COLORS['reset']
                else:
                    status = COLORS['red'] + "Full" + COLORS['reset']
                msg = msg + "  " + slot + ": " + status + "\n"
            
            msg = msg + "[WAIT_THEN_CLEAR]"
            connection.send(msg.encode())
            
        elif choice == "5":
            msg = "[CLEAR_SCREEN]" + COLORS['green'] + "\nReturning To Main Menu..." + COLORS['reset'] + "\n[SHORT_WAIT]"
            connection.send(msg.encode())
            break
        else:
            msg = COLORS['red'] + "\nInvalid Admin Choice!" + COLORS['reset'] + "\n[ERROR_WAIT]"
            connection.send(msg.encode())

######################################################
# Check for inactive clients every 60 seconds
######################################################
def check_inactive():
    while True:
        time.sleep(60)
        print(COLORS['blue'] + "[*] Status Check: " + str(len(active_clients)) + " Active, " + str(len(waiting_queue)) + " Waiting" + COLORS['reset'])

######################################################
# Start timeout checker
######################################################
timeout_thread = threading.Thread(target=check_inactive)
timeout_thread.daemon = True
timeout_thread.start()

######################################################
# Main server loop
######################################################
while True:
    connection, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()
