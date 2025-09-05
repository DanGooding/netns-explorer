from fabric import Connection
import json
from pathlib import Path
import model

def list_namespaces(conn: Connection) -> list[model.NamespaceMetadata]:
    result = conn.run('lsns --type=net --json', hide='both')
    if result.failed:
        raise RuntimeError(result)

    result_json = json.loads(result.stdout)

    namespaces = []
    for namespace_json in result_json['namespaces']:
        namespace_path = None
        if (nsfs := namespace_json['nsfs']) is not None:
            namespace_path = Path(nsfs)

        running_process_command = namespace_json['command']

        namespaces.append(
            model.NamespaceMetadata(
                path=namespace_path,
                running_process_command=running_process_command))

    return namespaces
