from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network
from pathlib import Path
from typing import Optional

type InterfaceId = int
type InterfaceName = str
type NamespacePath = Optional[Path]
""" None indicates the default namespace """

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
class NamespaceMetadata:
    path: NamespacePath
    running_process_command: Optional[str]

@dataclass
class Namespace:
    metadata: NamespaceMetadata
    interfaces: list[Interface]
    routing_table: list[Route]
