import click
from fabric import Connection
from pathlib import Path
import ip_command
import namespace_command
import model
import render

def discover_namespace(conn: Connection, metadata: model.NamespaceMetadata) -> model.Namespace:
    interfaces_by_id = ip_command.ip_link(conn, metadata.path)
    for interface_id, ip_addr in ip_command.ip_addr(conn, metadata.path).items():
        interfaces_by_id[interface_id].address = ip_addr

    routes = ip_command.ip_route(conn, metadata.path)

    return model.Namespace(
        metadata=metadata,
        interfaces=list(interfaces_by_id.values()),
        routing_table=routes)

@click.command()
@click.argument('ssh_host')
@click.option('-o', '--output', type=click.Path(), default='/dev/stdout')
def main(ssh_host: str, output: Path):
    conn = Connection(ssh_host)

    namespace_metadata = namespace_command.list_namespaces(conn)

    namespaces = []
    for metadata in namespace_metadata:
        namespaces.append(discover_namespace(conn, metadata))

    print(*namespaces, sep='\n')

    graph = render.render(namespaces)
    with open(output, 'w') as f:
        f.write(graph.source)


if __name__ == '__main__':
    main()