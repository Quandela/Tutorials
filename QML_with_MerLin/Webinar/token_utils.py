"""
token_utils.py
--------------
Utility for loading the Quandela cloud token from a .env file or
from the environment.

Supported .env variable names (checked in this order):
    CLOUD_TOKEN
    PCVL_CLOUD_TOKEN
    QUANDELA_CLOUD_TOKEN
    QUANDELA_TOKEN

Fallback: if none of those keys are found, the file is scanned for a
raw token line (i.e. a non-empty line that contains no '=' sign and
is not a comment).

Recommended .env format:
    CLOUD_TOKEN=your_token_here
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# Paths to search for a .env file, tried in order.
_ENV_SEARCH_PATHS = [
    Path(".env"),
    Path("Quantum_Machine_Learning-MerLin/.env"),
]


def load_cloud_token() -> str:
    """Return the Quandela cloud token as a string (empty string if not found).

    The function:
    1. Loads every .env file it can find into the process environment.
    2. Checks standard environment-variable names for the token.
    3. Falls back to reading a raw (key-less) token line from the .env file.
    """
    # Step 1 – load all .env files that exist on disk.
    found_env_files = []
    for path in _ENV_SEARCH_PATHS:
        if path.exists():
            load_dotenv(dotenv_path=path, override=False)
            found_env_files.append(str(path))

    # Step 2 – check well-known environment-variable names.
    token = (
        os.getenv("CLOUD_TOKEN")
        or os.getenv("PCVL_CLOUD_TOKEN")
        or os.getenv("QUANDELA_CLOUD_TOKEN")
        or os.getenv("QUANDELA_TOKEN")
        or ""
    ).strip()

    # Step 3 – fallback for .env files that contain only a bare token string.
    if not token:
        for path in _ENV_SEARCH_PATHS:
            if not path.exists():
                continue
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                stripped = line.strip()
                # Skip blank lines and comment lines.
                if not stripped or stripped.startswith("#"):
                    continue
                # A line with no '=' is treated as a raw token.
                if "=" not in stripped:
                    token = stripped
                    break
            if token:
                break

    if not token:
        searched = found_env_files or [str(p) for p in _ENV_SEARCH_PATHS]
        print("[token_utils] Cloud token not found.")
        print(f"[token_utils] Searched: {searched}")
        print("[token_utils] Expected .env format: CLOUD_TOKEN=your_token_here")

    return token
