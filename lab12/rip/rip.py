import json

ITERATIONS = 5

def update(routing_table, routes):
    for destination, cost_and_ip in routes.items():
        cost, source_ip = cost_and_ip
        if destination not in routing_table or routing_table[destination][0] > cost + 1:
            routing_table[destination] = (cost + 1, source_ip)

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        network_config = json.load(config_file)

    routers = {}

    for router_ip in network_config['routers']:
        routers[router_ip] = {}
        for connected_router, cost in network_config['routers'][router_ip].items():
            update(routers[router_ip], {connected_router: (cost, router_ip)})

    for _ in range(ITERATIONS):
        for router_ip in routers:
            for neighbor_ip, neighbor_routes in network_config['routers'][router_ip].items():
                if neighbor_ip in routers:
                    update(routers[router_ip], routers[neighbor_ip])

    for router_ip, router in routers.items():
        print(f"Router {router_ip} table:")
        print("Destination; Cost; Next Hop")
        for destination, (cost, next_hop) in router.items():
            print(f"{destination}; {cost}; {next_hop}")
        print()