import os
import subprocess
import sys
from collections import defaultdict
import posixpath

sys.dont_write_bytecode = True

DEVICE = os.environ.get("DEVICE", "/dev/ttyACM0")

def run_cmd(args):
    return subprocess.run(args, check=True)

def get_output(args):
    result = subprocess.run(args, check=True, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def run_main():
    run_cmd(["mpremote", "connect", DEVICE, "run", "main.py"])

def push_all():
    run_cmd(["mpremote", "connect", DEVICE, "cp", "-r", ".", ":"])

def clean_all():
    run_cmd(["mpremote", "rm", "-r", "-v", ":"])

def shell():
    run_cmd(["mpremote", "connect", DEVICE, "repl"])

def list_tree():
    tree = defaultdict(list)

    def collect(path):
        output = get_output(["mpremote", "connect", DEVICE, "fs", "ls", path])
        for line in output.splitlines():
            name = line.strip().split()[-1]
            if name == ":" or name == path:
                continue
            clean_name = posixpath.basename(name.rstrip("/"))
            full_path = posixpath.join(path, clean_name)
            tree[path].append((clean_name, full_path))
            if name.endswith("/"):
                collect(full_path)

    def render(path, prefix=""):
        entries = sorted(tree[path], key=lambda x: x[0])
        total = len(entries)
        for i, (name, full_path) in enumerate(entries):
            connector = "└──" if i == total - 1 else "├──"
            print(f"{prefix}{connector} {name}")
            if full_path in tree:
                new_prefix = prefix + ("    " if i == total - 1 else "│   ")
                render(full_path, new_prefix)

    print(":")
    collect(":")
    render(":")

COMMANDS = {
    "run": run_main,
    "sync": push_all,
    "clean": clean_all,
    "list": list_tree,
    "shell": shell,
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Usage: run | sync | clean | list | shell")
        sys.exit(1)
    COMMANDS[sys.argv[1]]()

if __name__ == "__main__":
    main()
