"""cleanup 命令 — 清理本地敏感缓存"""

import os

import click

from ..core.config import CONFIG_FILE, KEYS_FILE, STATE_DIR
from ..core.security import legacy_temp_cache_dir, remove_path


@click.command("cleanup")
@click.option("--all", "include_state", is_flag=True,
              help="同时清理 last_check、decoded_images、decrypted 等临时状态")
@click.option("--include-keys", is_flag=True,
              help="同时删除 config.json 和 all_keys.json（之后需要重新 init）")
def cleanup(include_state, include_keys):
    """清理本地解密数据库缓存。"""
    paths = [
        os.path.join(STATE_DIR, "cache"),
        legacy_temp_cache_dir(),
    ]

    if include_state:
        paths.extend([
            os.path.join(STATE_DIR, "last_check.json"),
            os.path.join(STATE_DIR, "decoded_images"),
            os.path.join(STATE_DIR, "decrypted"),
        ])

    if include_keys:
        paths.extend([KEYS_FILE, CONFIG_FILE])

    removed = []
    for path in paths:
        try:
            if remove_path(path):
                removed.append(path)
        except OSError as e:
            click.echo(f"清理失败: {path}: {e}", err=True)

    if removed:
        click.echo("已清理:")
        for path in removed:
            click.echo(f"  {path}")
    else:
        click.echo("没有可清理的缓存")
