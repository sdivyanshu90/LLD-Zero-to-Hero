from models.node import FileSystemNode


class FileNode(FileSystemNode):
    def __init__(self, name: str, size_bytes: int) -> None:
        super().__init__(name)
        self.size_bytes = size_bytes

    def total_size(self) -> int:
        return self.size_bytes

    def extension(self) -> str:
        if "." not in self.name:
            return ""
        return "." + self.name.rsplit(".", 1)[1]