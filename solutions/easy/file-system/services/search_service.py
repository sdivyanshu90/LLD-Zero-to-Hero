from __future__ import annotations

from collections import deque

from models.directory import DirectoryNode
from models.file import FileNode
from models.node import FileSystemNode


class FileSystemSearchService:
    def dfs_by_extension(self, root: FileSystemNode, extension: str) -> list[FileNode]:
        matches: list[FileNode] = []
        self._dfs(root, extension, matches)
        return matches

    def bfs_by_min_size(self, root: FileSystemNode, minimum_size: int) -> list[FileSystemNode]:
        queue = deque([root])
        matches: list[FileSystemNode] = []

        while queue:
            node = queue.popleft()
            if node.total_size() >= minimum_size:
                matches.append(node)
            if isinstance(node, DirectoryNode):
                queue.extend(node.children)

        return matches

    def _dfs(self, node: FileSystemNode, extension: str, matches: list[FileNode]) -> None:
        if isinstance(node, FileNode):
            if node.extension() == extension:
                matches.append(node)
            return

        if isinstance(node, DirectoryNode):
            for child in node.children:
                self._dfs(child, extension, matches)