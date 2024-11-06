import math

class Cache:
    MEMORY_ADDR_LEN = 32
    BYTE_OFFSET = 2
    WORD_LEN = 32
    VALID_BIT = 1
    

    def __init__(self, capacity:int, block_size:int, associativity:int):
        self.C = capacity
        self.b = block_size # Linea de cache
        self.N = associativity
        self.B = int(self.C/self.b) # Número de bloques
        self.S = int(self.B/self.N) # Sets

        self._init_SRAM()
       
       
    def _init_SRAM(self) -> None:    

        block = [[None]*self.B]
        self.TAG_SRAM = {i: [None]*self.N for i in range(self.S)}
        self.DATA_SRAM = {i: block*self.N for i in range(self.S)}
        self.VALID = {i: [None]*self.N for i in range(self.S)}
        self.LRU = {i: [None]*2 for i in range(self.S)}

    def write(self, addr:int):
        pass

    def read(self, addr:int) -> tuple:
        
        HIT = True

        tag_bits = self._get_tag_bits(addr)
        set_bits = self._get_tag_bits(addr)
        block_bits = self._get_block_bits(addr)

        tag_set = self.TAG_SRAM[set_bits]
        data_set = self.DATA_SRAM[set_bits]

        if tag_bits in tag_set:
            way_index = tag_set.index(tag_bits)
            is_valid = self.VALID[set_bits][way_index]

            if is_valid:
                data_block = data_set[way_index]
                data = data_block[block_bits]
                return (HIT, data)
            
        
        return (not HIT, None)
    

    def _update_LRU(self) -> None:
        pass

    def _get_tag_bits(self, addr:int) -> int:
        set_bits = math.log2(self.S)
        block_bits = math.log2(self.b)

        tag_bits = self.MEMORY_ADDR_LEN - self.BYTE_OFFSET - set_bits - block_bits
        tag_start = self.BYTE_OFFSET + set_bits + block_bits

        return self._bitsel(addr,tag_start,tag_bits)

    def _get_set_bits(self, addr:int) -> int:
        set_bits = math.log2(self.S)
        block_bits = math.log2(self.b)

        set_start = self.BYTE_OFFSET + block_bits

        return self._bitsel(addr,set_start,set_bits)

    def _get_block_bits(self, addr:int) -> int:
        block_bits = math.log2(self.b)
        block_start = self.BYTE_OFFSET

        return self._bitsel(addr,block_start,block_bits)
        

    def _bitsel(self, word:int, start:int, bits:int) -> int:
        mask = (1 << bits) - 1
        return (word >> start) & mask


cache = Cache(8, 2, 2)
print(cache.VALID)