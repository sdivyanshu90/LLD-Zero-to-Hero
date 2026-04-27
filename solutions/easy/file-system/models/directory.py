from models.node import FileSystemNode


class DirectoryNode(FileSystemNode):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.children: list[FileSystemNode] = []

    def add_child(self, child: FileSystemNode) -> None:
        self.children.append(child)

    def total_size(self) -> int:
        return sum(child.total_size() for child in self.children)