import os
import subprocess
from subprocess import PIPE


def cmd(args, capture_output=True):
    if capture_output:
        ret = subprocess.run(args.split(" "), stdout=PIPE, stderr=PIPE)
        ret.stdout = ret.stdout.decode("utf-8")
        ret.stderr = ret.stderr.decode("utf-8")
        return ret
    else:
        return subprocess.run(args.split(" "))


def start_paasta_api():
    print("Starting Paasta API Server")
    p = subprocess.Popen(
        f'python -m paasta_tools.api.api -D -c {os.environ["KIND_CLUSTER"]} {os.environ["PAASTA_API_PORT"]}'.split(
            " "
        )
    )
    return p


def paasta_apply():
    print("Applying SOA configurations")
    service_instances = cmd(
        f'python -m paasta_tools.list_kubernetes_service_instances -d {os.environ["SOA_DIR"]}',
    )
    cmd(
        f'python -m paasta_tools.setup_kubernetes_job {service_instances.stdout.strip()} -v -d {os.environ["SOA_DIR"]}',
        False,
    )


def init_all():
    paasta_apply()
    return start_paasta_api()
