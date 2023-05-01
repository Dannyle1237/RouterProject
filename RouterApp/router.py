#Danny Le, Raunak Kunwar
#1001794802, ##########
#CSE 4344
import socket

#setup routers given config file, returns a set imitating a router structure
def setup_routers(config):
    #'connected' for neighboring nodes with their associated costs
    routing_table = {}
    graph = {node: {'connected': {}} for node in config['ROUTERS']['routers']}
    for node in graph:
        graph[node]['connected'] = config['ROUTERS']['vertices'][node]
        routing_table[node] = "INF"

    #Add routing table to each router
    for router in graph:
        temp_RT = routing_table.copy()
        #Initialize values from neighbors
        for neighbor in graph[router]['connected']:
            temp_RT[neighbor] = graph[router]['connected'][neighbor]
        #Initalize self router as 0
        temp_RT[router] = 0
        graph[router]['routing_table'] = temp_RT
    return graph

#Func to bind sockets given list of routers(ips)
def setup_sockets(routers, port):
    sockets = {}
    print("\nSpecification 4c\n")
    for idx, router in enumerate(routers):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.bind((router, port))
        sockets[router] = sock

        router_ip = router
        router_port = port
        connection_type = 'UDP'
        #specification 4c
        print(f"Router {idx+1} IP: {router_ip}, Port: {router_port}, Connection Type: {connection_type}")
    return sockets
