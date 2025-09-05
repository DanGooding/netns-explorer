from fabric import Connection
from ipaddress import IPv4Address
from pathlib import Path
from typing import Optional
import model
import parse

def command_lines(conn: Connection, command: str) -> list[str]:
    links_result = conn.run(command, hide='both')
    if links_result.failed:
        raise RuntimeError(links_result)

    return links_result.stdout.splitlines()

def in_namespace(namespace_file: Optional[Path], command: str) -> str:
    if namespace_file is None:
        return command
    else:
        return f"nsenter --net='{namespace_file}' -- {command}"

def ip_link(conn: Connection, namespace_file: Optional[Path]) \
        -> dict[model.InterfaceId, model.Interface]:
    command = in_namespace(namespace_file, 'ip -detail -oneline link')

    return parse.parse_ip_links(command_lines(conn, command))

def ip_addr(conn: Connection, namespace_file: Optional[Path]) \
        -> dict[model.InterfaceId, IPv4Address]:
    command = in_namespace(namespace_file, 'ip -oneline address')

    return parse.parse_ip_addrs(command_lines(conn, command))


def ip_route(conn: Connection, namespace_file: Optional[Path]) -> list[model.Route]:
    command = in_namespace(namespace_file, 'ip -detail -oneline route')

    return parse.parse_ip_routes(command_lines(conn, command))
