#Danny Le, Raunak Kunwar
#1001794802, 1001742301
#CSE 4344
def calculate_dv(router_table, neighbor, neighbor_table):
    updated_table = {}
    for dest in router_table:
        if router_table[dest] == 0:
            updated_table[dest] = 0
        elif neighbor_table[dest] == "INF":
            updated_table[dest] = router_table[dest]
        else:
            curr_cost = router_table[dest]
            new_cost = router_table[neighbor] + neighbor_table[dest]
            if( curr_cost == 'INF'):
                updated_table[dest] = new_cost
            else:
                updated_table[dest] = min (curr_cost, new_cost)
    return updated_table