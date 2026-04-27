# Live Auction/Bidding

## Problem Summary

Design a live auction where bids must be strictly increasing and updates are broadcast efficiently to many viewers.

## Why This Problem Is Asked

Live auction bidding combines two concurrency challenges: atomically enforcing a strictly-increasing bid invariant under concurrent submissions, and fan-out broadcasting to potentially thousands of viewers without holding the auction lock during dispatch.

The classic mistake is holding the auction lock while calling each observer’s `on_bid()` callback, which can cause the dispatch to block if any observer is slow. A strong design copies the subscriber list under the lock, then releases the lock before iterating.

## Functional Requirements

1. Register auction items.
2. Subscribe viewers to receive real-time bid updates.
3. Place a bid that must strictly exceed the current highest bid.
4. Reject bids equal to or lower than the current highest.
5. Broadcast each accepted bid to all subscribed viewers without holding the bid lock.

## ASCII UML

```text
+-------------------+
| Bid               |
+-------------------+
| bidder_id         |
| amount            |
+-------------------+

+-------------------+
| Auction           |
+-------------------+
| current_bid       |
| viewers           |
| lock              |
+-------------------+
| place_bid()       |
| subscribe()       |
+-------------------+
```

## Concurrency Checklist

- Shared state: current highest bid and subscriber list.
- Deadlock risk: do not notify viewers while holding the bid lock.
- Lock granularity: one lock per auction item.
- Lock-free alternative: append-only bid streams with pub/sub fanout.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Auction` owns the current bid and the subscriber registry. `BidValidator` validates bid preconditions. `AuctionService` orchestrates validation, commit, and fan-out. |
| **OCP**   | Adding a reserve-price rule means a new `BidValidator` subclass; `AuctionService` composes validators without modification.                                            |
| **LSP**   | All viewer subscriber types (in-app, WebSocket, email) satisfy `on_bid(auction_id, bid_amount)`; the service never branches on subscriber type.                        |
| **ISP**   | `Subscriber` declares only `on_bid()`. Viewers do not implement auction administration methods.                                                                        |
| **DIP**   | `AuctionService` dispatches to `Subscriber` abstractions; it never imports concrete notifier classes directly.                                                         |

## Key Edge Cases

- A bid equal to the current highest must be rejected, not accepted.
- Viewer notifications must not be sent while the bid lock is held to avoid blocking on slow observers.
- Subscribing after bids have already been placed must still work correctly.

## Follow-up Questions

1. How would you add a reserve price below which the auction cannot close?
2. How would you support a countdown timer that auto-closes the auction when it expires?
3. How would you provide a full bid history replay for a closed auction?
