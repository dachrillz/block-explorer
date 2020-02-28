from enum import Enum

class Type(Enum):
    int32_t = 1
    char32 = 2
    uint8_t = 3
    uint16_t = 4
    uint32_t = 5
    uint64_t = 6

###
# Pre parse models
###


class ParseItem:
    """[summary]
    """
    def __init__(self, size, _type):
        """Init
        Arguments:
            size {[Integer]} -- [size in bytes of item]
            type {[Type]} -- [Type enum]
        """
        self.size = size
        self.type = _type



class Header:
    version = ParseItem(4, Type.int32_t)
    previous_block_header_hash = ParseItem(32, Type.char32)
    merkle_root_hash = ParseItem(32, Type.char32)
    time = ParseItem(4, Type.uint32_t)
    nBits = ParseItem(4, Type.uint32_t)
    nonce = ParseItem(4, Type.uint32_t)

    @staticmethod
    def get_items():
        return iter([
            Header.version,
            Header.previous_block_header_hash,
            Header.merkle_root_hash,
            Header.time,
            Header.nBits,
            Header.nonce])

class Transactions:
    def __init__(self, block_without_headers):
        self.transaction_stream_raw = block_without_headers
        self.current = 0


###
# Post parse models
###

class AbstractTypeFactory:

    @staticmethod
    def from_hex(hex_string, item_type, start_location, end_location):
        if(item_type == Type.int32_t):
            return Signed32Int(hex_string, start_location, end_location)
        elif(item_type == Type.uint32_t):
            return Unsigned32Int(hex_string, start_location, end_location)
        elif(item_type == Type.char32):
            return Char32(hex_string, start_location, end_location)
        else:
            raise Exception(f"Parsed Item Factory could not find match for type: {item_type}")


class ParsedItem:
    def __init__(self, value_as_string, start_location=None, end_location=None):
        self.start = start_location
        self.end = end_location
        self.raw_hex_as_string = value_as_string
        self.value_as_string = self._from_little_endian(value_as_string)

    def _from_little_endian(self, s):
        return ''.join([c[1] + c[0] for c in zip(s[::2], s[1::2])])[::-1]

    def _from_hex_to_uint(self, value, size_in_bits=32):
        hex_size = int(size_in_bits/2)
        a = int(value, 16)
        fs = int('f'*hex_size, 16)
        return a & fs

    def __repr__(self):
        if (self.start is None) or (self.end is None):
            return self.value_as_string
        else:
            return f"{self.value_as_string} -- from {self.start} to {self.end}. Size: {self.end - self.start} "

class CompactSizeUnsignedInteger(ParsedItem):
    def __init__(self, value_as_string, start, end):
        super().__init__(value_as_string, start, end)
        self.value_item = self.__parse_compact_unsigned_integer(self.raw_hex_as_string)

    def __parse_compact_unsigned_integer(self, value):
        prefix = value[0:2]
        if(prefix == 'fd'):
            value = value[2:6]
            value = Unsigned16Int(value, None, None)
        elif(prefix == 'fe'):
            value = value[2:10]
            value = Unsigned32Int(value, None, None)
        elif(prefix == 'ff'):
            value = value[2:18]
            value = Unsigned64Int(value, None, None)
        else:
            value = Unsigned8Int(value, None, None)
        return value

    def get_value(self):
        return self.value_item.value
            

class Char32(ParsedItem):
    def __init__(self, value_as_string, start, end):
        super().__init__(value_as_string, start, end)
        self.value_as_string = self.__hex_to_string(self.value_as_string)

    def __hex_to_string(self, value):
        return value
        # return value.decode('hex')

class Signed32Int(ParsedItem):
    def __init__(self, value_as_string, start, end):
        super().__init__(value_as_string, start, end)
        self.value_as_string = self.__parse_32_uint(self.value_as_string)

    def __parse_32_uint(self, value):
        # @TODO: Change name and fix this, it calculates it wrong!
        a = int(value, 16)
        return a & 0xffffffffffffffff

class Unsigned8Int(ParsedItem):
    def __init__(self, value_as_string, start, end):
        super().__init__(value_as_string, start, end)
        self.value = super()._from_hex_to_uint(self.value_as_string, 8)

class Unsigned16Int(ParsedItem):
    def __init__(self, value_as_string, start, end):
        super().__init__(value_as_string, start, end)
        self.value = super()._from_hex_to_uint(self.value_as_string, 16)


class Unsigned32Int(ParsedItem):
    def __init__(self, value_as_string, start, end):
        super().__init__(value_as_string, start, end)
        self.value = super()._from_hex_to_uint(self.value_as_string, 32)

class Unsigned64Int(ParsedItem):
    def __init__(self, value_as_string, start, end):
        super().__init__(value_as_string, start, end)
        self.value = super()._from_hex_to_uint(self.value_as_string, 16)
