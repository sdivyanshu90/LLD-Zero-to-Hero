# Live Auction/Bidding Solution

This implementation enforces strictly increasing bids under a per-auction lock and snapshots the viewer list before broadcasting so notifications do not hold the critical section.

## Design Notes

- `Bid` is a frozen dataclass capturing `bidder_id` and `amount`.
- `Viewer` collects notification strings via `notify(message)`.
- `Auction` owns the current highest `Bid`, a list of subscribers, and a `threading.Lock` that protects bid acceptance.
- After accepting a bid, the lock is released; only then are observers notified using the snapshotted list.

## Complexity Analysis

| Operation                   | Time                                              | Space                               |
| --------------------------- | ------------------------------------------------- | ----------------------------------- |
| `place_bid(bidder, amount)` | O(s), s = subscriber count, after O(1) lock check | O(s) snapshot copy                  |
| `subscribe(viewer)`         | O(1) list append                                  | O(1)                                |
| `unsubscribe(viewer)`       | O(s) list remove                                  | O(1)                                |
| Space (total)               | —                                                 | O(b) bid history + O(s) subscribers |

The lock is released before notifying observers, so fan-out latency does not block new bids.

## SOLID Compliance

| Principle | Evidence                                                                                                                                                                |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Bid` is a pure value type. `Viewer` handles notification receipt. `Auction` owns bid validation and subscriber management. `AuctionService` orchestrates the sequence. |
| **OCP**   | Adding a reserve-price or auto-bid rule means a new validator plugged in before `Auction.accept()`; the broadcast logic is unchanged.                                   |
| **LSP**   | All viewer types satisfy `notify(message: str)`; `Auction` never branches on viewer type during fan-out.                                                                |
| **ISP**   | `Viewer` declares only `notify()`. Viewers do not implement bidding or auction management methods.                                                                      |
| **DIP**   | `Auction` dispatches to subscriber references through the `Viewer` interface; it does not import any concrete notifier class.                                           |

## Design Pattern

Observer with lock-release-before-notify: notifying observers while holding the bid lock would block all bidders while slow observers process their messages. Snapshotting the viewer list and releasing the lock first eliminates this liveness hazard.

## Folder Layout

```text
live-auction-bidding/
|-- app.py
|-- models/
|   `-- core.py     # Bid, Viewer
`-- services/
    `-- auction.py  # Auction, AuctionHouse
```

## Trade-offs

- Viewer notification is synchronous; replace with a thread pool or async event loop to avoid slow observers blocking the broadcast loop.
- One `Auction` per item; `AuctionHouse` is a thin registry. Add a closing-time field and a background timer for timed auctions.
- Bids are compared by amount only; add a timestamp tie-breaker for simultaneous equal-amount bids if needed.

## Run

From this directory:

```bash
python3 app.py
```
