Danny Le, Raunak Kunwar
1001794802, 1001742301
CSE 4344

Language used: Python 3.10.1

How to run:
cd to folder containing source files (submitted as dtl4802_DannyLe/RouterApp)

Run command in CLI with following parameters
    python main.py <config file> <port number>

for example:
    python main.py config.json 5000

The program will then output 
    The sockets being created with their relative
    information. (Spec 4c)
    The routers with their current routing tables (Spec4a)
    Updates each router makes as they're receiving neighboring routing tables
On end of program:
    Broadcast messages as each router receives it 
    The final topology table (Each router with their routing tables)

To Modify Program:
    You can change the amount of updates the program runs by changing the
    variable 'n' on line 113
    'n' is considered the sum of the amount of updates(routing table) each router has 
    sent to one of it's neighbors. 

Test Case 2:
    Danny Le,1001794802
    Even: Assume link A/B is broken
        Cost from A/D, A/F, A/C is increased since 
        B made it cheaper for those path

Config file:
    The config file for our program was set up in json since it works easily
    with Python, and set up to replicate the topology graph
    
    We gave it a header ["ROUTERS"] which contained a Python Set,
    the set contained headers 
        "routers", which is a list of ip_addresses
        representing the routers
        "vertices",which is all of the connections between the routers
