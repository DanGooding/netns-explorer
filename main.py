import click
from fabric import Connection
import ip_command
import model

def discover_namespace(conn: Connection, namespace_path: model.NamespacePath) -> model.Namespace:
    interfaces_by_id = ip_command.ip_link(conn, namespace_path)
    for interface_id, ip_addr in ip_command.ip_addr(conn, namespace_path).items():
        interfaces_by_id[interface_id].address = ip_addr

    routes = ip_command.ip_route(conn, namespace_path)

    return model.Namespace(
        path=namespace_path,
        interfaces=list(interfaces_by_id.values()),
        routing_table=routes)

@click.command()
@click.argument('ssh_host')
def main(ssh_host: str):
    conn = Connection(ssh_host)

    default_namespace = discover_namespace(conn, None)
    print(default_namespace)


if __name__ == '__main__':
    main()