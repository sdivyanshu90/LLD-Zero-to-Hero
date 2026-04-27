from models.directory import DirectoryNode
from models.file import FileNode
from services.search_service import FileSystemSearchService


def main() -> None:
    root = DirectoryNode("root")
    docs = DirectoryNode("docs")
    src = DirectoryNode("src")
    docs.add_child(FileNode("readme.md", 1200))
    docs.add_child(FileNode("guide.txt", 800))
    src.add_child(FileNode("main.py", 2400))
    src.add_child(FileNode("utils.py", 1800))
    root.add_child(docs)
    root.add_child(src)

    search = FileSystemSearchService()
    print([node.name for node in search.dfs_by_extension(root, ".py")])
    print([node.name for node in search.bfs_by_min_size(root, 1500)])


if __name__ == "__main__":
    main()