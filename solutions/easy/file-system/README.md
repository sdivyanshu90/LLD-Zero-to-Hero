# File System Solution

This implementation uses the Composite Pattern for files and directories, then keeps traversal algorithms in a separate search service.

## Design Notes

- `FileSystemNode` is the shared contract.
- `FileNode` is the leaf.
- `DirectoryNode` is the composite.
- `FileSystemSearchService` holds BFS and DFS traversal logic.

## Complexity Analysis

| Operation            | Time                             | Space                            |
| -------------------- | -------------------------------- | -------------------------------- |
| `directory.size()`   | O(n), n = total nodes in subtree | O(d) stack depth for recursion   |
| `dfs_by_extension()` | O(n)                             | O(d) recursion stack             |
| `bfs_by_min_size()`  | O(n)                             | O(w) queue width at widest level |
| Space (tree)         | —                                | O(n)                             |

## SOLID Compliance

| Principle | Evidence                                                                                                                                 |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | Nodes know their own size and children. `FileSystemSearchService` owns traversal algorithms. Neither leaks into the other.               |
| **OCP**   | Adding a `SymlinkNode` requires one new class implementing `FileSystemNode`; search and size logic are unchanged.                        |
| **LSP**   | Both `FileNode` and `DirectoryNode` satisfy `FileSystemNode`: `size()` returns a non-negative integer; `children()` returns an iterable. |
| **ISP**   | `FileSystemNode` is minimal: `size()` and `children()`. Callers never need to downcast to check if a node is a directory.                |
| **DIP**   | `FileSystemSearchService` accepts a `FileSystemNode` root; it never imports `DirectoryNode` directly.                                    |

## Design Pattern

Composite Pattern: `FileNode` and `DirectoryNode` share the `FileSystemNode` interface, so `size()` and child traversal are uniform at any depth.

## Folder Layout

```text
file-system/
|-- app.py
|-- models/
|   |-- node.py
|   |-- file.py
|   `-- directory.py
`-- services/
    `-- search_service.py
```

## Trade-offs

- Keeping search algorithms in a service (not in the nodes) respects SRP; nodes are pure data.
- This version stores children as a list; swap to `dict[name, node]` if O(1) lookup by name is needed.

## Run

From this directory:

```bash
python app.py
```
