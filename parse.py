from ipaddress import IPv4Address, IPv4Network
import re
import model

ip_link_pattern = re.compile(r'^(?P<id>\d+): (?P<name>[\w_]+)(?:@if(?P<pair_id>\d+))?: .*?(?: master (?P<bridge_name>[\w_]+))? state (?P<state>[A-Z]+)')
def parse_ip_links(lines: list[str]) -> dict[int, model.Interface]:
    interfaces_by_id = {}
    for line in lines:
        match = ip_link_pattern.match(line.strip())
        if not match:
            continue

        groups = match.groupdict()
        interface_id = int(groups['id'])
        veth_pair_id = None
        if groups['pair_id']:
            veth_pair_id = int(groups['pair_id'])

        interfaces_by_id[interface_id] = model.Interface(
            id=interface_id,
            name=groups['name'],
            state=groups['state'],
            bridge_name=groups['bridge_name'],
            veth_pair_id=veth_pair_id,
            address=None)

    return interfaces_by_id

ip_addr_pattern = re.compile(r'^(?P<id>\d+): [\w_]+ +(?:inet (?P<ipv4>[\d.]+)/\d+)?(?:inet6 (?P<ipv6>[:0-9]+)/\d+)?')
""" parses a the output from `ip addr`
    returns a dict { interface_id: ipv4addr }
"""
def parse_ip_addrs(lines: list[str]) -> dict[int, IPv4Address]:
    addrs_by_interface_name = {}
    for line in lines:
        match = ip_addr_pattern.match(line.strip())
        if not match:
            continue

        groups = match.groupdict()
        if not groups['ipv4']:
            # ignore ipv6 for now
            continue
        addrs_by_interface_name[int(groups['id'])] = IPv4Address(groups['ipv4'])

    return addrs_by_interface_name

ip_route_pattern = re.compile(r'^unicast (?P<destination>default|[\d.]+(/\d+)?)( via (?P<gateway>[\d.]+))? dev (?P<if_name>[\w_]+)')
def parse_ip_routes(lines: list[str]) -> list[model.Route]:
    routes = []
    for line in lines:
        match = ip_route_pattern.match(line.strip())
        if not match:
            continue
        groups = match.groupdict()

        destination = groups['destination']
        if destination == 'default':
            destination = IPv4Network('0.0.0.0/0')
        else:
            destination = IPv4Network(destination)

        gateway = None
        if groups['gateway']:
            gateway = model.Gateway(IPv4Address(groups['gateway']))

        routes.append(model.Route(
            destination=destination,
            interface_name=str(groups['if_name']),
            gateway=gateway))

    return routes