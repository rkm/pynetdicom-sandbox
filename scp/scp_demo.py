#!/usr/bin/env python
import os

from pydicom.filewriter import write_file_meta_info
from pynetdicom import AE
from pynetdicom import ALL_TRANSFER_SYNTAXES
from pynetdicom import AllStoragePresentationContexts
from pynetdicom import debug_logger
from pynetdicom import Event
from pynetdicom import evt


def handle_store(event: Event, storage_dir: str) -> int:
    """Handle EVT_C_STORE events."""

    try:
        os.makedirs(storage_dir, exist_ok=True)
    except Exception:
        # Unable to create output dir, return failure status
        return 0xC001

    # We rely on the UID from the C-STORE request instead of decoding
    fname = os.path.join(storage_dir, event.request.AffectedSOPInstanceUID)
    with open(fname, "wb") as f:
        # Write the preamble, prefix and file meta information elements
        f.write(b"\x00" * 128)
        f.write(b"DICM")
        write_file_meta_info(f, event.file_meta)
        # Write the raw encoded dataset
        f.write(event.request.DataSet.getvalue())

    return 0x0000


def main() -> int:

    debug_logger()

    handlers = [(evt.EVT_C_STORE, handle_store, ["out"])]

    ae = AE()
    storage_sop_classes = [cx.abstract_syntax for cx in AllStoragePresentationContexts]
    for uid in storage_sop_classes:
        ae.add_supported_context(uid, ALL_TRANSFER_SYNTAXES)

    ae.start_server(("", 11112), block=True, evt_handlers=handlers)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
