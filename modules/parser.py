from .models import *
from .block import Block


class Parser:
    def __init__(self):
        self.scaling = 1

    def __set_format(self, block_format):
        if block_format == 'hex':
            self.scaling = 2
        else:
            raise Exception("Format not available")

    def __format_size(self, size):
        return self.scaling*size

    def parse(self, content, block_format='hex'):
        self.__set_format(block_format)
        current = 0
        #Parse header
        header_items = Header.get_items()
        block_items = []
        for item in header_items:
            start = self.__format_size(current)
            end = self.__format_size(current+item.size)

            retrieved = content[start:end]
            parsed_item = AbstractTypeFactory.from_hex(retrieved, item.type, start, end)
            block_items.append(parsed_item)
            print(parsed_item)
            current += item.size
        block = Block.from_parsed_items(block_items)
        
        print("done parsing")

