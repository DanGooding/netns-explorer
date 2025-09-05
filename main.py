import click
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network
from fabric import Connection
import re
from typing import Optional, Generator

type InterfaceId = int
type InterfaceName = str

@dataclass
class Interface:
    id: int
    """ the global identifier - e.g. 123 for `if123`  """
    name: str
    """ the human-readable name - meaningful within the namespace """

    address: Optional[IPv4Address]
    state: str
    """ UP/DOWN etc. """

    bridge_name: Optional[InterfaceName]
    """ For an interface connected to a bridge (virtual switch).
        The bridge will be in the same namespace. 
    """
    veth_pair_id: Optional[InterfaceId]
    """ the paired interface, if this is a veth """

@dataclass
class Gateway:
    """ a router - provides routing beyond this subnet """
    address: IPv4Address

@dataclass
class Route:
    """ an `ip route` entry """
    destination: IPv4Network
    interface_name: InterfaceName
    gateway: Optional[Gateway]

@dataclass
class Namespace:
    name: str
    interfaces: list[Interface]
    routing_table: list[Route]

def command_lines(conn: Connection, command: str) -> list[str]:
    links_result = conn.run(command, hide='both')
    if links_result.failed:
        raise RuntimeError(links_result)

    return links_result.stdout.splitlines()

ip_link_pattern = re.compile(r'^(?P<id>\d+): (?P<name>[\w_]+)(?:@if(?P<pair_id>\d+))?: .*?(?: master (?P<bridge_name>[\w_]+))? state (?P<state>[A-Z]+)')
def parse_ip_links(lines: list[str]) -> dict[int, Interface]:
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

        interfaces_by_id[interface_id] = Interface(
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
def parse_ip_routes(lines: list[str]) -> list[Route]:
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
            gateway = Gateway(IPv4Address(groups['gateway']))

        routes.append(Route(
            destination=destination,
            interface_name=str(groups['if_name']),
            gateway=gateway))

    return routes



@click.command()
@click.argument('ssh_host')
def main(ssh_host: str):
    conn = Connection(ssh_host)

    interfaces_by_id = parse_ip_links(
        command_lines(conn, 'ip -detail -oneline link'))
    for interface_id, ip_addr in parse_ip_addrs(command_lines(conn, 'ip -oneline address')).items():
        interfaces_by_id[interface_id].address = ip_addr

    routes = parse_ip_routes(command_lines(conn, 'ip -detail -oneline route'))

    for interface in interfaces_by_id.values():
        print(interface)
    for route in routes:
        print(route)


if __name__ == '__main__':
    main()