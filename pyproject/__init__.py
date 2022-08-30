import argparse
import json
import sys

from .api import PyProject


def main():
    parser = argparse.ArgumentParser(description='Query a thing.')
    parser.add_argument('--url', type=str, required=True, help='URL of the instance.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--redis_up', action='store_true', help='Check if redis is up.')
    args = parser.parse_args()

    client = PyProject(args.url)

    if not client.is_up:
        print(f'Unable to reach {client.root_url}. Is the server up?')
        sys.exit(1)
    if args.redis_up:
        response = client.redis_up()
    print(json.dumps(response, indent=2))
