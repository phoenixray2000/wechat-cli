"""Local privacy helpers for state files and logs."""

import json
import os
import shutil
import tempfile


def mask_secret(value, prefix=8, suffix=4):
    """Return a stable, non-sensitive representation of a secret."""
    if not value:
        return "<hidden>"
    text = str(value)
    if len(text) <= prefix + suffix:
        return "<hidden>"
    return f"{text[:prefix]}...{text[-suffix:]} (hidden)"


def ensure_private_dir(path):
    """Create a directory and make it owner-only on POSIX platforms."""
    os.makedirs(path, exist_ok=True)
    if os.name != "nt":
        try:
            os.chmod(path, 0o700)
        except OSError:
            pass


def ensure_private_file(path):
    """Make a file owner-readable/writable on POSIX platforms."""
    if os.name != "nt":
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass


def write_private_json(path, data, **dump_kwargs):
    ensure_private_dir(os.path.dirname(os.path.abspath(path)))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, **dump_kwargs)
    ensure_private_file(path)


def remove_path(path):
    """Remove a file or directory if it exists."""
    if not path or not os.path.exists(path):
        return False
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
    return True


def legacy_temp_cache_dir():
    return os.path.join(tempfile.gettempdir(), "wechat_cli_cache")
