import click
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network
from fabric import Connection
import re
from typing import Optional, Generator

@dataclass
class Namespace:
    name: str
    routing_table: list['Route']

@dataclass
class Interface:
    id: int
    """ the global identifier - e.g. 123 for `if123`  """
    namespace: Namespace
    name: str
    """ the human-readable name - meaningful within the namespace """

    address: Optional[IPv4Address]
    state: str
    """ UP/DOWN etc. """

    bridge_name: Optional[str]
    """ For an interface connected to a bridge (virtual switch).
        The bridge will be in the same namespace. 
    """
    veth_pair_id: Optional[int]
    """ the paired interface, if this is a veth """

@dataclass
class Gateway:
    """ a router - provides routing beyond this subnet """
    address: IPv4Address

@dataclass
class Route:
    """ an `ip route` entry """
    destination: IPv4Network
    interface: Interface
    gateway: Optional[Gateway]

def command_lines(conn: Connection, command: str) -> Generator[str, None, None]:
    links_result = conn.run(command, hide='both')
    if links_result.failed:
        raise RuntimeError(links_result)

    for link in links_result.stdout.splitlines():
        link = link.strip()
        if link:
            yield link

@click.command()
@click.argument('ssh_host')
def main(ssh_host: str):
    conn = Connection(ssh_host)

    default_namespace = Namespace(name='', routing_table=[])
    interfaces_by_id = {}
    link_pattern = re.compile(r'(?P<id>\d+): (?P<name>\w+)(?:@if(?P<pair_id>\d+))?: (?:.+ )?(?:master (?P<bridge_name>\w+))?(?: .*)?state (?P<state>[A-Z]+)')
    for link in command_lines(conn, 'ip -detail -oneline link'):
        match = link_pattern.match(link).groupdict()

        id = match['id']
        interface = Interface(
            namespace=default_namespace,
            id=match['id'],
            name=match['name'],
            state=match['state'],
            bridge_name=match['bridge_name'],
            veth_pair_id=match['pair_id'],
            address=None)

        interfaces_by_id[id] = interface

    address_pattern = re.compile(r'(?P<id>\d+): \w+ +(?:inet (?P<ipv4>[\d.]+)/\d+)?(?:inet6 (?P<ipv6>[:0-9]+)/\d+)?')
    for address in command_lines(conn, 'ip -oneline address'):
        match = address_pattern.match(address).groupdict()
        if not match['ipv4']:
            # ignore ipv6 for now
            continue
        interfaces_by_id[match['id']].address = IPv4Address(match['ipv4'])

    for interface in interfaces_by_id.values():
        print(interface)













if __name__ == '__main__':
    main()