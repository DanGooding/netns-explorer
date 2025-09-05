from typing import Iterable

import graphviz
import model

def interface_id_node_name(interface_id: model.InterfaceId) -> str:
    return f'if{interface_id}'

def interface_node_name(interface: model.Interface) -> str:
    return interface_id_node_name(interface.id)

def render(namespaces: Iterable[model.Namespace]) -> graphviz.Digraph:
    dot = graphviz.Digraph()

    interfaces_by_namespace_and_name = {}
    for namespace in namespaces:
        interfaces_by_namespace_and_name[namespace.metadata.path] = {}
        for interface in namespace.interfaces:
            interfaces_by_namespace_and_name[namespace.metadata.path][interface.name] = interface

    for namespace in namespaces:
        if namespace.is_default():
            subgraph_name = ''
        else:
            subgraph_name = f'cluster:{namespace.metadata.path}'
        with dot.subgraph(None, subgraph_name) as ns_graph:
            for interface in namespace.interfaces:
                ns_graph.node(interface_node_name(interface), interface.name)
                ns_graph.attr(color='grey')

                if interface.veth_pair_id:
                    # undirected veth pair edge
                    dot.edge(
                        interface_node_name(interface),
                        interface_id_node_name(interface.veth_pair_id))

                if interface.bridge_name:
                    # directed bridge switch->interface edge

                    bridge_interface = interfaces_by_namespace_and_name[namespace.metadata.path][interface.bridge_name]
                    dot.edge(
                        interface_node_name(bridge_interface),
                        interface_node_name(interface))

    return dot