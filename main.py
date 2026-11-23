#!/usr/bin/env python3
"""Entry for the make.fun bounty "Sum up 23 November's world news in one image".

Copies the entry image (entry.png, held in this repo) to the output location
and verifies the copy is byte-identical to the source.

Python 3.13, standard library only. Deterministic: no network, no clock,
no randomness. Two runs write identical bytes.

Output location: $MAKEFUN_OUTPUT if set, otherwise /output/entry.png.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT = Path("/output") / SOURCE_NAME
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1_048_576  # 1 MiB cap

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path: Path) -> tuple[int, int]:
    """Read the width/height from a PNG file's IHDR chunk (stdlib only)."""
    with path.open("rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        raise ValueError(f"{path} is not a PNG file")
    if header[12:16] != b"IHDR":
        raise ValueError(f"{path} has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def verify_image(path: Path) -> str | None:
    """Return an error message if the image breaks any entry rule, else None."""
    size = path.stat().st_size
    if size > MAX_BYTES:
        return f"{path} is {size} bytes, over the {MAX_BYTES}-byte cap"
    try:
        width, height = png_dimensions(path)
    except (OSError, ValueError) as exc:
        return f"cannot read PNG dimensions of {path}: {exc}"
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        return (f"{path} is {width}x{height}, expected "
                f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}")
    return None


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_output(repo_dir: Path) -> Path:
    """Pick the output path, falling back to a repo-local dir if needed.

    $MAKEFUN_OUTPUT wins when set. Otherwise the default is /output/entry.png;
    if /output cannot be created (e.g. read-only filesystem), fall back to
    <repo>/output/entry.png instead of failing outright.
    """
    override = os.environ.get("MAKEFUN_OUTPUT")
    if override:
        return Path(override)
    try:
        DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        fallback = repo_dir / "output" / SOURCE_NAME
        print(f"warning: cannot create {DEFAULT_OUTPUT.parent} ({exc}); "
              f"falling back to {fallback}", file=sys.stderr)
        return fallback
    return DEFAULT_OUTPUT


def main() -> int:
    repo_dir = Path(__file__).resolve().parent
    source = repo_dir / SOURCE_NAME
    if not source.is_file():
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    problem = verify_image(source)
    if problem is not None:
        print(f"error: source image failed verification: {problem}",
              file=sys.stderr)
        return 1

    output = resolve_output(repo_dir)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory {output.parent}: {exc}",
              file=sys.stderr)
        return 1

    try:
        shutil.copyfile(source, output)
    except OSError as exc:
        if output == DEFAULT_OUTPUT:
            # /output looked writable but the copy failed; try the fallback.
            fallback = repo_dir / "output" / SOURCE_NAME
            print(f"warning: cannot write {output} ({exc}); "
                  f"falling back to {fallback}", file=sys.stderr)
            try:
                fallback.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, fallback)
            except OSError as fallback_exc:
                print(f"error: fallback write also failed: {fallback_exc}",
                      file=sys.stderr)
                return 1
            output = fallback
        else:
            print(f"error: cannot write output image {output}: {exc}",
                  file=sys.stderr)
            return 1

    if sha256_of(output) != sha256_of(source):
        print("error: output copy is not byte-identical to the source image",
              file=sys.stderr)
        return 1

    problem = verify_image(output)
    if problem is not None:
        print(f"error: output image failed verification: {problem}",
              file=sys.stderr)
        return 1

    print(f"wrote {output} ({output.stat().st_size} bytes, "
          f"sha256 {sha256_of(output)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
