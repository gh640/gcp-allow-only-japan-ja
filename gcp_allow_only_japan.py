"""Google Cloud Platform で日本以外からのアクセスをブロックするルールを作成するためのスクリプト

`jp.txt` の内容のイメージ:

1.0.16.0/20
1.0.64.0/18
1.1.64.0/18
1.5.0.0/16
"""
import argparse
import subprocess
from pathlib import Path
from typing import List

ADDRESS_FILE = Path(__file__).parent / 'jp.txt'
GCP_PROJECT = '__GCP_PROJECT_NAME__'
PRIORITY_ALLOW = 10
PRIORITY_DENY = 20
CHUNK_SIZE = 256


def main():
    """メイン関数"""
    args = get_args()
    dry_run = args.dry_run

    addresses = get_addresses(ADDRESS_FILE)
    name_prefix = 'allow-japan-'

    print('IP 範囲の数: {}'.format(len(addresses)))

    create_deny_rule(dry_run=dry_run)
    create_allow_rules(name_prefix, addresses, dry_run=dry_run)


def get_args():
    """コマンドライン引数を取得する"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='ドライラン')
    return parser.parse_args()


def create_allow_rules(name_prefix: str, addresses: List[str], *, dry_run: bool):
    """ファイヤウォールルールを複数件まとめて作成する"""
    n = 0
    while True:
        start = n * CHUNK_SIZE
        stop = start + CHUNK_SIZE
        chunk_addresses = addresses[start:stop]
        if not chunk_addresses:
            break
        name = '{}{}'.format(name_prefix, n)
        create_allow_rule(name, chunk_addresses, dry_run=dry_run)
        n += 1


def create_allow_rule(name: str, addresses: List[str], *, dry_run: bool):
    """特定のレンジを許可するルールを 1 件作成する"""
    args = [
        'gcloud',
        'compute',
        'firewall-rules',
        'create',
        name,
        '--project={}'.format(GCP_PROJECT),
        '--action=ALLOW',
        '--rules=tcp:80,tcp:443',
        '--direction=INGRESS',
        '--priority={}'.format(PRIORITY_ALLOW),
        '--no-enable-logging',
        '--source-ranges={}'.format(','.join(addresses)),
    ]
    if dry_run:
        print('実行:', ' '.join(args))
        return
    return subprocess.run(args, check=True)


def create_deny_rule(*, dry_run: bool):
    """すべてを拒否するルールを 1 件作成する"""
    args = [
        'gcloud',
        'compute',
        'firewall-rules',
        'create',
        'deny-all',
        '--project={}'.format(GCP_PROJECT),
        '--action=DENY',
        '--rules=tcp:80,tcp:443',
        '--direction=INGRESS',
        '--priority={}'.format(PRIORITY_DENY),
        '--no-enable-logging',
        '--source-ranges=0.0.0.0/0',
    ]
    if dry_run:
        print('実行:', ' '.join(args))
        return
    return subprocess.run(args, check=True)


def get_addresses(path):
    """アドレス一覧を取得する"""
    def is_valid(line):
        return line.strip() and not line.startswith('#')

    with open(path) as f:
        addresses = [line.strip() for line in f.readlines() if is_valid(line)]

    return addresses


if __name__ == '__main__':
    main()
