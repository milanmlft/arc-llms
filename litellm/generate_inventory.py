#!/usr/bin/env python3
"""Ansible dynamic inventory built from Terraform output."""

import argparse
import json
import subprocess


def terraform_output(name):
    result = subprocess.run(
        ["terraform", "output", "--json", name],
        capture_output=True,
        encoding="UTF-8",
        check=True,
    )
    return json.loads(result.stdout)


def generate_inventory():
    names = terraform_output("vm_names")
    ips = terraform_output("vm_ips")

    hostvars = {}
    for name, ip in zip(names, ips):
        hostvars[name] = {
            "ansible_host": ip,
            "ansible_user": "almalinux",
        }

    return {
        "_meta": {"hostvars": hostvars},
        "all": {"children": ["workers"]},
        "workers": {
            "hosts": list(names),
            "vars": {
                "ansible_ssh_common_args": "-o ProxyJump=condenser",
            },
        },
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Generate an Ansible inventory from Terraform outputs.",
        prog=__file__,
    )
    mo = ap.add_mutually_exclusive_group()
    mo.add_argument(
        "--list", action="store_true", help="Show JSON of all managed hosts"
    )
    mo.add_argument("--host", action="store", help="Display vars related to the host")
    args = ap.parse_args()

    if args.host:
        print(json.dumps({}))
    else:
        print(json.dumps(generate_inventory(), indent=4))
