import docker
from tabulate import tabulate
from termcolor import colored

def get_container_info():
    client = docker.from_env()

    data = []
    for container in client.containers.list(all=True):
        container_info = client.api.inspect_container(container.id)
        networks = container_info['NetworkSettings']['Networks']
        ports = container_info['NetworkSettings']['Ports']

        line_color = 'green' if container.status == 'running' else 'red' if container.status == 'exited' else 'yellow'

        cont = []
        cont.append(colored(container.name, line_color))
        # cont.append(container.status)
        cont.append(colored(container.status, line_color))
        
        port_list = []
        for port, port_data in ports.items():
            if port_data:
                for pd in port_data:
                    port_list.append(colored(pd['HostIp'] + ":" + pd['HostPort'] + " => " + port, line_color))
            else:
                port_list.append(colored(port, line_color))

        cont.append('\n'.join(port_list))

        net_list=[]
        ip_list=[]
        dns_names=[]
        for network_name, network_data in networks.items():
            net_list.append(colored(network_name, line_color))
            ip_list.append(colored(network_data['IPAddress'], line_color))
            name_list = []
            for dn in network_data['DNSNames']:
                if not dn in container_info['Id'] and not dn in container_info['Config']['Hostname']:
                    name_list.append(dn)
            dns_names.append(colored(str(name_list), line_color))

        cont.append('\n'.join(net_list))
        cont.append('\n'.join(ip_list))
        cont.append('\n'.join(dns_names))

        data.append(cont)
    
    data.sort(key=lambda x: x[0])

    headers = ["Container Name\nContainer Hostname", "Container Status", "Container Ports", "Container Networks", "Container IP", "Container DNS Names"]
    print(tabulate(data, headers=headers, tablefmt="grid"))

get_container_info()