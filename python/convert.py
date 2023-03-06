import ipaddress
import socket
import struct


class CidrMaskConvert:
    def cidr_to_mask(self, val):
        host_bits = 32 - int(val)
        buffer = struct.pack("!I", (1 << 32) - (1 << host_bits))
        netmask = socket.inet_ntoa(buffer)
        return netmask

    def mask_to_cidr(self, val):
        cidr = sum(bin(int(x)).count("1") for x in val.split("."))
        return cidr


class IpValidate:
    def ipv4_validation(self, val):
        try:
            ipaddress.ip_address(val)
            return True
        except ValueError:
            pass
        return False
