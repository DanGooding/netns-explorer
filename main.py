import click
from fabric import Connection
import ip_command
import namespace_command
import model

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
def main(ssh_host: str):
    conn = Connection(ssh_host)

    namespace_metadata = namespace_command.list_namespaces(conn)

    for metadata in namespace_metadata:
        namespace = discover_namespace(conn, metadata)

        print(namespace)

if __name__ == '__main__':
    main()