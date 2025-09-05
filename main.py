import click
from fabric import Connection
import model
import parse

def command_lines(conn: Connection, command: str) -> list[str]:
    links_result = conn.run(command, hide='both')
    if links_result.failed:
        raise RuntimeError(links_result)

    return links_result.stdout.splitlines()

def discover_namespace(conn: Connection, name: str) -> model.Namespace:
    interfaces_by_id = parse.parse_ip_links(
        command_lines(conn, 'ip -detail -oneline link'))
    for interface_id, ip_addr in parse.parse_ip_addrs(command_lines(conn, 'ip -oneline address')).items():
        interfaces_by_id[interface_id].address = ip_addr

    routes = parse.parse_ip_routes(command_lines(conn, 'ip -detail -oneline route'))

    return model.Namespace(
        name=name,
        interfaces=list(interfaces_by_id.values()),
        routing_table=routes)

@click.command()
@click.argument('ssh_host')
def main(ssh_host: str):
    conn = Connection(ssh_host)

    default_namespace = discover_namespace(conn, 'default')
    print(default_namespace)


if __name__ == '__main__':
    main()