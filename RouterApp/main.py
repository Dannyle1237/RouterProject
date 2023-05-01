#Danny Le, Raunak Kunwar
#1001794802, ##########
#CSE 4344
import sys
import json
import distance_vector as dv
import router as r#Import for router set up funcs 
import threading
import datetime
import select

def close_sockets(sockets):
    for sock in sockets.values():
        sock.close()

#Print Statement for "Topology table"
def print_topology_table(routers):
    print("Router\t\tOther Routers with costs")
    for cur_router in routers:
        string = ""
        for router in routers[cur_router]['routing_table']:
            string += router + ":" + str(routers[cur_router]['routing_table'][router]) + "\t"
        print(f'{cur_router}\t{string}')

#Sending function for sending data
def update_neighbors(router):
    global sent_updates, run_threads
    routing_table = routers[router]['routing_table']
    message = {"routing_table": routing_table}
    json_message = json.dumps(message)
    for neighbor in routers[router]['connected']:
        sockets[router].sendto(json_message.encode(), (neighbor, port))
        #print(f'\nUPDATES SENT:{sent_updates}')
        sent_updates += 1
        if(sent_updates == n):
            break


#Receiving Function to update routing tables
def receive_messages_threads(router):
    global run_threads
    while run_threads:
        global routers
        response, addr = sockets[router].recvfrom(4096)
        #print(f"{router} Received from {addr}: {response}")
        response = json.loads(response.decode())
        if "routing_table" in response:
            routing_table = routers[router]['routing_table']
            neighbor_rt = response['routing_table']
            neighbor_ip = addr[0]
            prev_RT = routing_table
            routing_table = dv.calculate_dv(routing_table, neighbor_ip, neighbor_rt)
            routers[router]['routing_table'] = routing_table
            print(f'\nUPDATE\nSource IP: {router}\tNeighbor IP: {neighbor_ip}\nPrev Routing Table:{prev_RT}\nUpdated Table:{routing_table}')
        if "broadcast" in response:
            message =  response['broadcast']
            print(f'\nTest Case 1:\nRouter {router} received broadcast message\n{message}')

#Receiving Function to update routing tables
def receive_message(router):
    global routers
    response, addr = sockets[router].recvfrom(4096)
    #print(f"{router} Received from {addr}: {response}")
    response = json.loads(response.decode())
    if "routing_table" in response:
        routing_table = routers[router]['routing_table']
        neighbor_rt = response['routing_table']
        neighbor_ip = addr[0]
        prev_RT = routing_table
        routing_table = dv.calculate_dv(routing_table, neighbor_ip, neighbor_rt)
        routers[router]['routing_table'] = routing_table
        print(f'\nUPDATE\nSource IP: {router}\tNeighbor IP: {neighbor_ip}\nPrev Routing Table:{prev_RT}\nUpdated Table:{routing_table}')
    if "broadcast" in response:
        message =  response['broadcast']
        print(f'\nTest Case 1:\nRouter {router} received broadcast message\n{message}')

def start_receiver_threads():
    threads = []
    for router in sockets:
        thread = threading.Thread(target=receive_messages_threads, args=(router,), name = router)
        thread.start()
        threads.append(thread)
    return threads


#Main
if len(sys.argv) < 3:
    print("Error: Type command in CLI python main.py <config_file> <port number>")
    sys.exit(1)
#Grab config file and port from sys.argv
port = int(sys.argv[2])
config_file = sys.argv[1]
fp = open(config_file)
config = json.load(fp)

#set up routers given config file in CLI
routers = r.setup_routers(config)

#bind socket to each router
sockets = r.setup_sockets(routers, port)

#print topology table before any DV Calcuatlions happen
print("\nSpecification 4a")
print_topology_table(routers) 

# Start receiver threads to listen for incoming messages
#flag to stop threads
run_threads = True
receiver_threads = start_receiver_threads()

#Code to run code/update_neighbors of each router n times
#Number of times to send update
n = 50
#Counter for number of updates sent
sent_updates = 0

#Code to run program continuously 
while True:
    # Send updated routing tables to neighbors
    for router in sockets:
        update_neighbors(router)
        # Check if n updates have been sent
        # If so then terminate sockets, threads, and program
        if sent_updates == n:
            run_threads = False
            # Broadcast message and terminate program
            message = f"Message from Router {router}, IP address {router}, Port No. {port}\nUTA-ID: 1001794802\nDate and Time (UTC): {datetime.datetime.utcnow()}\nTotal number of updates value (n): {n}\nPayload size exclusively for this last broadcast:"
            message += str(len(message))
            message = json.dumps({'broadcast':message})
            for sock in sockets:
                sockets[router].sendto(message.encode(), sockets[sock].getsockname())

            #Check through each router for any messages still incoming
            while True:
                # Loop through all sockets
                for sock in sockets:
                    # Check if there are any messages to receive on this socket
                    ready_to_read, _, _ = select.select([sockets[sock]], [], [], 0)
                    if sockets[sock] in ready_to_read:
                        receive_message(sock)
                
                # Check if there are no more messages to receive on any socket
                all_done = all(not select.select([sockets[sock]], [], [], 0)[0] for sock in sockets)
                if all_done:
                    break
                
            #close sockets
            for sock in sockets:
                sockets[sock].close()
            print(f"\nSockets closed after {n} updates")
            print("\nFinal Topology Table:")
            print_topology_table(routers)
            sys.exit(0)

    #print_topology_table(routers) 