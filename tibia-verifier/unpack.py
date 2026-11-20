"""Unpack application source from the self-contained archive during Render builds."""
from pathlib import Path
import base64
import io
import tarfile

root = Path(__file__).resolve().parent
source = base64.b64decode((root / "source.tar.xz.b64").read_text().strip())
with tarfile.open(fileobj=io.BytesIO(source), mode="r:xz") as tar:
    for member in tar.getmembers():
        dest = (root / member.name).resolve()
        if not dest.is_relative_to(root):
            raise RuntimeError("Unsafe archive path")
    tar.extractall(root, filter="data")
print("Tibia verifier source extracted")
