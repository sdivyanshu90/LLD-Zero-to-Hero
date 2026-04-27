# File System

## Problem Summary

Design a simple in-memory file system using the Composite Pattern.

The system should support files and directories, compute directory sizes recursively, and search using both DFS and BFS strategies.

## Why This Problem Is Asked

The Composite Pattern question tests whether a candidate can model tree-structured data with a uniform interface. Real file systems, UI component trees, and org charts all share this structure.

The secondary test is algorithm placement: a weak design puts `search()` inside `DirectoryNode`, entangling traversal strategy with node data. A strong design keeps nodes as pure data holders and extracts search into a service that can swap DFS for BFS without touching any node class.

## Functional Requirements

1. Model files and directories.
2. Allow directories to contain both files and directories.
3. Compute recursive size.
4. Search by file extension using DFS.
5. Search by minimum size using BFS.

## Constraints

- Files and directories should share a common interface.
- Search behavior should stay outside the node classes when possible.
- Directory size should be derived recursively.

## ASCII UML

```text
+-------------------+
| FileSystemNode    | <<abstract>>
+-------------------+
| name              |
+-------------------+
| size()            |
| children()        |
+-------------------+
        ^
        |
+-------+-------+
|               |
+---------------+   +-------------------+
| FileNode      |   | DirectoryNode     |
+---------------+   +-------------------+
| _size         |   | _children         |
+---------------+   +-------------------+
                    | add_child()       |
                    +-------------------+

+----------------------------+
| FileSystemSearchService    |
+----------------------------+
| dfs_by_extension()         |
| bfs_by_min_size()          |
+----------------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `FileNode` and `DirectoryNode` know their own size and children. `FileSystemSearchService` owns all traversal logic.                  |
| **OCP**   | Adding a symbolic link node type only requires a new class implementing `FileSystemNode` — search and size logic are unaffected.      |
| **LSP**   | `FileNode` and `DirectoryNode` are interchangeable everywhere `FileSystemNode` is expected; both implement `size()` and `children()`. |
| **ISP**   | `FileSystemNode` exposes only `size()` and `children()` — callers never need to downcast.                                             |
| **DIP**   | `FileSystemSearchService` accepts any `FileSystemNode` root, not a concrete `DirectoryNode`.                                          |

## Key Edge Cases

- Empty directories.
- Nested directories several levels deep.
- Searching when no match exists.

## Follow-up Questions

1. How would you add delete and move operations?
2. How would you represent permissions?
3. How would you support pattern-based search?
