class DummyDB:
    def __init__(self):
        self.data = {}
        self._index_count = 0
    
    def index_forward(self) -> int:
        self._index_count += 1
        return self._index_count
    
    def create(self, key: str, value: str) -> bool:
        self.data.setdefault(key, value)
        return True
    
    def read(self, key: str) -> str:
        return self.data.get(key)
    
    def read_all(self) -> list[str]:
        return [v for v in self.data.values()]
    
    def update(self, key: str, value: str) -> bool:
        if not key in self.data:
            return False

        self.data[key] = value
        return True
    
    def delete(self, key: str) -> bool:
        return True if self.data.pop(key, None) else False
