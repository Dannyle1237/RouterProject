import sys
import json
import distance_vector as dv
import router as r#Import for router set up funcs 
import threading

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
    routing_table = routers[router]['routing_table']
    message = {"routing_table": routing_table}
    json_message = json.dumps(message)
    for neighbor in routers[router]['connected']:
        #print(str(router) + " Sending routing table to " + str(neighbor))
        sockets[router].sendto(json_message.encode(), (neighbor, port))

#Receiving Function to update routing tables
def receive_messages(router):
    while True:
        global routers
        response, addr = sockets[router].recvfrom(4096)
        #print(f"{router} Received from {addr}: {response}")
        response = json.loads(response.decode())
        if "routing_table" in response:
            routing_table = routers[router]['routing_table']
            neighbor_rt = response['routing_table']
            neighbor_ip = addr[0]
            routing_table = dv.calculate_dv(routing_table, neighbor_ip, neighbor_rt)
            routers[router]['routing_table'] = routing_table

def start_receiver_threads():
    threads = []
    for router in sockets:
        thread = threading.Thread(target=receive_messages, args=(router,))
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
print(routers)
#bind socket to each router
sockets = r.setup_sockets(routers, port)


# Start receiver threads to listen for incoming messages
receiver_threads = start_receiver_threads()

while True:
    # Send updated routing tables to neighbors
    for router in sockets:
        update_neighbors(router)
    print_topology_table(routers) 