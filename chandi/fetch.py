"""Download the source text (not redistributed in this repo; see README)."""
import hashlib
import pathlib
import urllib.request

URL = "https://sanskritdocuments.org/doc_devii/durga700.itx"
SHA256 = "1ea0e4f2e1af0effdba15877e11124d16cb19158b6e7f34c9e19ac56631e476d"  # "Latest update: February 26, 2024"
DEST = pathlib.Path(__file__).resolve().parent.parent / "data" / "durga700.itx"


# Rahasya-traya (Bṛhatstotraratnākara via sanskritdocuments.org), recited after the 13 chapters
RAHASYA = {
    "pradhanika": ("prAdhAnikarahasyam", "9ea45aeb0ba0150ad3196a15f01650c2d663e1530a9e78a1776dd866646412d5"),
    "vaikritika": ("vaikRitikarahasyam", "16567b16615ceb463b5bc07636725ef3c3cbba107369c3873ad865b00ae2b61b"),
    "murti": ("mUrtirahasyam", "55496552f88f4bac5ede22076745d36a95921e36072a3c2fbe03461d71b06a0c"),
}


def _get(url, dest, sha, force=False):
    if dest.exists() and not force:
        data = dest.read_bytes()
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        # the site answers 406 to Python's default User-Agent
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (chandi-fetch)"})
        with urllib.request.urlopen(req) as r:
            data = r.read()
        dest.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    if digest != sha:
        print(f"WARNING: {dest.name} sha256 {digest} differs from the pinned, verified revision.")
    return dest


def fetch(force=False):
    return _get(URL, DEST, SHA256, force)


def fetch_rahasya(force=False):
    """{section key: path} for the three Rahasyas."""
    return {key: _get(f"https://sanskritdocuments.org/doc_devii/{name}.itx",
                      DEST.parent / "rahasya" / f"{name}.itx", sha, force)
            for key, (name, sha) in RAHASYA.items()}


if __name__ == "__main__":
    print(fetch(), fetch_rahasya())
