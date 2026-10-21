"""Download the source text (not redistributed in this repo; see README)."""
import hashlib
import pathlib
import urllib.request

URL = "https://sanskritdocuments.org/doc_devii/durga700.itx"
SHA256 = "1ea0e4f2e1af0effdba15877e11124d16cb19158b6e7f34c9e19ac56631e476d"  # "Latest update: February 26, 2024"
DEST = pathlib.Path(__file__).resolve().parent.parent / "data" / "durga700.itx"


def fetch(force=False):
    if DEST.exists() and not force:
        data = DEST.read_bytes()
    else:
        DEST.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(URL) as r:
            data = r.read()
        DEST.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    if digest != SHA256:
        print(f"WARNING: {DEST.name} sha256 {digest} differs from the pinned, verified revision.")
    return DEST


if __name__ == "__main__":
    print(fetch())
