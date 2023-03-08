import ipaddress
import socket
import struct


def get_mask_from_cidr(cidr):
    try:
        host_bits = 32 - int(cidr)
    except ValueError:
        return "Invalid cidr provided"

    buffer = struct.pack("!I", (1 << 32) - (1 << host_bits))
    mask = socket.inet_ntoa(buffer)
    return mask if mask != "0.0.0.0" else "Invalid cidr provided"


def get_cidr_from_mask(mask):
    try:
        if ipaddress.ip_address(mask):
            cidr = sum(bin(int(x)).count("1") for x in mask.split("."))
            return cidr if cidr != 0 else "Invalid mask provided"
    except ValueError:
        return "Invalid mask provided"
