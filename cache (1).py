
from collections import deque
import math
import random

class Cache:
    MEMORY_ADDR_LEN = 32
    BYTE_OFFSET = 2
    WORD_LEN = 32
    VALID_BIT = 1
    
    def __init__(self, capacity: int, block_size: int, associativity: int, way_prediction=False):
        """
        Inicializa el caché con la capacidad y configuración especificada.
        
        :param capacity: Tamaño total del caché en bytes (por ejemplo, 32 KB).
        :param block_size: Tamaño de cada línea de caché en bytes (por ejemplo, 64 bytes).
        :param associativity: Número de vías (ways) en el conjunto (por ejemplo, 4, 8, 16).
        :param way_prediction: Activa o desactiva la predicción de sentido.
        """
        self.C = capacity
        self.b = block_size
        self.N = associativity
        self.B = int(self.C / self.b)
        self.S = int(self.B / self.N)
        self.way_prediction = way_prediction

        # Contadores de estadísticas
        self.hits = 0
        self.misses = 0
        self.reemplazos = 0
        self.predictions = 0
        self.correct_predictions = 0

        self._init_SRAM()
       
    def _init_SRAM(self) -> None:
        """
        Inicializa la estructura de datos de la memoria caché.
        Cada conjunto es un deque de tamaño N (ways), para facilitar el reemplazo LRU.
        """
        self.SRAM = {i: deque(maxlen=self.N) for i in range(self.S)}
        self.way_predictions = {i: random.randint(0, self.N - 1) for i in range(self.S)}

    def access(self, addr: int) -> bool:
        HIT = True
        MISS = False

        tag_bits = self._get_tag_bits(addr)
        set_bits = self._get_set_bits(addr)
        cache_set = self.SRAM[set_bits]

        # Predicción de sentido
        if self.way_prediction:
            predicted_way = self.way_predictions[set_bits]
            self.predictions += 1

            if len(cache_set) > predicted_way and cache_set[predicted_way] == tag_bits:
                # Predicción correcta
                self.correct_predictions += 1
                self.hits += 1
                cache_set.remove(tag_bits)
                cache_set.append(tag_bits)
                return HIT

        # Acceso completo si la predicción falla o no se usa predicción
        if tag_bits in cache_set:
            cache_set.remove(tag_bits)
            cache_set.append(tag_bits)
            self.hits += 1
            return HIT
        
        # Manejo de miss con reemplazo LRU
        if len(cache_set) == self.N:
            self.reemplazos += 1
            cache_set.popleft()

        cache_set.append(tag_bits)
        self.misses += 1

        # Actualiza predicción después de un miss
        if self.way_prediction:
            self.way_predictions[set_bits] = cache_set.index(tag_bits)

        return MISS

    def _get_tag_bits(self, addr: int) -> int:
        set_bits = int(math.log2(self.S))
        block_bits = int(math.log2(self.b))
        tag_bits = Cache.MEMORY_ADDR_LEN - Cache.BYTE_OFFSET - set_bits - block_bits
        tag_start = Cache.BYTE_OFFSET + set_bits + block_bits
        return self._bitsel(addr, tag_start, tag_bits)

    def _get_set_bits(self, addr: int) -> int:
        set_bits = int(math.log2(self.S))
        block_bits = int(math.log2(self.b))
        set_start = Cache.BYTE_OFFSET + block_bits
        return self._bitsel(addr, set_start, set_bits)

    def _bitsel(self, word: int, start: int, bits: int) -> int:
        mask = (1 << bits) - 1
        return (word >> start) & mask
    
    def reportar_estadisticas(self):
        total_accesses = self.hits + self.misses
        hit_rate = (self.hits / total_accesses) * 100 if total_accesses > 0 else 0
        prediction_accuracy = (self.correct_predictions / self.predictions) * 100 if self.predictions > 0 else 0
        print(f"Configuración: {self.N} ways, {self.C // 1024} KB, línea de {self.b} bytes")
        print(f"Hits: {self.hits}")
        print(f"Misses: {self.misses}")
        print(f"Reemplazos: {self.reemplazos}")
        print(f"Hit Rate: {hit_rate:.2f}%")
        if self.way_prediction:
            print(f"Predicción de Sentido Activada - Precisión de predicción: {prediction_accuracy:.2f}%")