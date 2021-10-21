#!/usr/bin/env python
from pynetdicom import AE
from pynetdicom import debug_logger


def main() -> int:

    debug_logger()

    ae = AE()
    ae.add_requested_context("1.2.840.10008.1.1")

    # association is a Thread subclass
    assoc = ae.associate("localhost", 11112)

    if assoc.is_established:
        print("Association established with Echo SCP!")

        # response is a Dataset object
        resp = assoc.send_c_echo()
        assert resp["Status"].value == 0, "Expected 0 for success"

        assoc.release()
    else:
        # Association rejected, aborted or never connected
        print("Failed to associate")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
