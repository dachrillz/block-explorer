import hashlib
import codecs
import binascii

class Block:
    def __init__(self, version, hash_prev, hash_merkle_root, time, bits, nonce, tx_list=None):
        self.version = version
        self.hash_prev = hash_prev
        self.hash_merkle_root = hash_merkle_root
        self.time = time
        self.bits = bits
        self.nonce = nonce
        self.tx_list = tx_list

        self.hash = self.__hash_of_block()

    @staticmethod
    def from_parsed_items(list_of_parsed_items):
        return Block(*list_of_parsed_items)

    def __hash_of_block(self):
        header_hex = (self.version.raw_hex_as_string +
                        self.hash_prev.raw_hex_as_string +
                        self.hash_merkle_root.raw_hex_as_string +
                        self.time.raw_hex_as_string +
                        self.bits.raw_hex_as_string +
                        self.nonce.raw_hex_as_string)
        header_bin = binascii.unhexlify(header_hex)
        # header_bin = header_hex.decode('hex')
        hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest()
        h = str(codecs.encode(hash[::-1], 'hex_codec'), 'utf-8')
        print(h)
        return h

    def get_hash_little_endian(self):
        return self.hash[::-1]



    