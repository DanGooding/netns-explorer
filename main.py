from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network
from typing import Optional

@dataclass
class Namespace:
    name: str
    routingTable: list['Route']

@dataclass
class Interface:
    id: int
    """ the global identifier - e.g. 123 for `if123`  """
    namespace: Namespace
    name: str
    """ the human-readable name - meaningful within the namespace """

    address: IPv4Address

    kind: str
    """ veth, bridge, vxlan, etc. """
    bridgeId: Optional[int]
    """ for an interface connected to a bridge (virtual switch) """
    vethPairId: Optional[int]
    """ the paired interface, if this is a veth """

@dataclass
class Gateway:
    """ a router - provides routing beyond this network """
    address: IPv4Address

@dataclass
class Route:
    """ an `ip route` entry """
    destination: IPv4Network
    interface: Interface
    gateway: Optional[Gateway]


# fabric for running commands remotely
# + cli library (click)
# + graphviz
# types


# args:
# - ssh host (else run locally)
# - namespace source files (e.g. the docker one)

# rendering the model
# nodes: (style kinds differently)
# - interface
#   - name
#   - ip
# - routing table, html table of
#   - route
#     - cidr
# - gateway
#   - ip
# edges: (style different kinds differently)
# - veth<>veth
# - route->interface
# - bridge->child
# subgraphs:
# - namespace
#   but not the default namespace?


# operation:
# - for each namespace
#   - run and parse each command
#   - update our model with info
# - render our model to a graph

# metadata:
# - link namespaces to docker containers somehow?
