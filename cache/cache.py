from collections import deque
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

        # Contadores de estadísticas
        self.hits = 0
        self.misses = 0

        self._init_SRAM()
       
    def _init_SRAM(self) -> None:
        self.SRAM = {i: deque(maxlen=self.N) for i in range(self.S)}

    def access(self, addr:int) -> bool:

        HIT = True
        MISS = False

        tag_bits = self._get_tag_bits(addr)
        set_bits = self._get_set_bits(addr)

        cache_set = self.SRAM[set_bits]
        if tag_bits in cache_set:
            cache_set.remove(tag_bits)
            cache_set.append(tag_bits) # Mueve el tag a MRU
            self.hits += 1             # Incrementa el contador de estadísticas
            return HIT
        
        if len(cache_set) == self.S:
            cache_set.popleft()

        cache_set.append(tag_bits)
        self.misses += 1               # Incrementa el contador de estadísticas 
        return MISS



    def _get_tag_bits(self, addr:int) -> int:
        set_bits = math.log2(self.S)
        block_bits = math.log2(self.b)

        tag_bits = Cache.MEMORY_ADDR_LEN - Cache.BYTE_OFFSET - set_bits - block_bits
        tag_start = Cache.BYTE_OFFSET + set_bits + block_bits

        return self._bitsel(addr,tag_start,tag_bits)

    def _get_set_bits(self, addr:int) -> int:
        set_bits = math.log2(self.S)
        block_bits = math.log2(self.b)

        set_start = Cache.BYTE_OFFSET + block_bits

        return self._bitsel(addr,set_start,set_bits)

    def _get_block_bits(self, addr:int) -> int:
        block_bits = math.log2(self.b)
        block_start = Cache.BYTE_OFFSET

        return self._bitsel(addr,block_start,block_bits)
        

    def _bitsel(self, word:int, start:int, bits:int) -> int:
        mask = (1 << int(bits)) - 1
        return (int(word) >> int(start)) & mask
    
    def reportar_estadisticas(self):
        print(f"Hits: {self.hits}")
        print(f"Misses: {self.misses}")