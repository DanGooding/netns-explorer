from fabric import Connection
from ipaddress import IPv4Address
import model
import parse

def command_lines(conn: Connection, command: str) -> list[str]:
    links_result = conn.run(command, hide='both')
    if links_result.failed:
        raise RuntimeError(links_result)

    return links_result.stdout.splitlines()

def in_namespace(namespace_path: model.NamespacePath, command: str) -> str:
    if namespace_path is None:
        return command
    else:
        return f"nsenter --net='{namespace_path}' -- {command}"

def ip_link(conn: Connection, namespace_path: model.NamespacePath) \
        -> dict[model.InterfaceId, model.Interface]:
    command = in_namespace(namespace_path, 'ip -detail -oneline link')

    return parse.parse_ip_links(command_lines(conn, command))

def ip_addr(conn: Connection, namespace_path: model.NamespacePath) \
        -> dict[model.InterfaceId, IPv4Address]:
    command = in_namespace(namespace_path, 'ip -oneline address')

    return parse.parse_ip_addrs(command_lines(conn, command))


def ip_route(conn: Connection, namespace_path: model.NamespacePath) -> list[model.Route]:
    command = in_namespace(namespace_path, 'ip -detail -oneline route')

    return parse.parse_ip_routes(command_lines(conn, command))
