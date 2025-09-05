from typing import Iterable
from colorhash import ColorHash
import graphviz
import model

def interface_id_node_name(interface_id: model.InterfaceId, namespace: model.Namespace) -> str:
    return f'if{interface_id}'

def interface_node_name(interface: model.Interface, namespace: model.Namespace) -> str:
    return interface_id_node_name(interface.id, namespace)

def route_node_name(route: model.Route, namespace: model.Namespace) -> str:
    return f'{namespace.metadata.path} {route.destination} {route.interface_name}'

def wrap_command(command: str | None) -> str:
    if not command:
        return ''

    target_width = 40
    break_at = ' -'

    lines = []
    while len(command) > target_width:
        break_index = command.rfind(break_at, 0, target_width)
        if break_index == -1:
            break
        lines.append(command[:break_index])
        command = command[break_index + 1:]

    lines.append(command)
    return '\n'.join(lines)

def render(namespaces: Iterable[model.Namespace]) -> graphviz.Digraph:
    dot = graphviz.Digraph()
    dot.attr(ranksep='2.0')

    interfaces_by_namespace_and_name = {}
    interfaces_by_id = {}
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
            subgraph_color = ColorHash(subgraph_name)

            ns_graph.attr(fontcolor=subgraph_color.hex)
            ns_graph.attr(label=wrap_command(namespace.metadata.running_process_command))

            for interface in namespace.interfaces:
                ns_graph.node(interface_node_name(interface, namespace), interface.name,
                              style='filled',
                              fillcolor=subgraph_color.hex,
                              fontcolor='white')

                if interface.veth_pair_id:
                    # undirected veth pair edge

                    my_name = interface_node_name(interface, namespace)
                    other_name = interface_id_node_name(interface.veth_pair_id, None)
                    if my_name < other_name:
                        dot.edge(
                            my_name,
                            other_name,
                            dir='none',
                            rank='same')

                if interface.bridge_name:
                    # directed bridge switch->interface edge

                    bridge_interface = interfaces_by_namespace_and_name[namespace.metadata.path][interface.bridge_name]
                    dot.edge(
                        interface_node_name(bridge_interface, namespace),
                        interface_node_name(interface, namespace),
                        style='dashed',
                    rank='same')

            for route in namespace.routing_table:
                route_name = route_node_name(route, namespace)
                ns_graph.node(route_name, str(route.destination),
                              shape='plaintext',
                              fontcolor=subgraph_color.hex)

                interface = interfaces_by_namespace_and_name[namespace.metadata.path][route.interface_name]
                ns_graph.edge(
                    interface_node_name(interface, namespace),
                    route_name,
                    dir='back',
                    rank='same')

    return dot