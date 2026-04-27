import threading

from services.broker import MessageBroker


def main() -> None:
    broker = MessageBroker()
    broker.create_topic("orders")

    def publish_range(prefix: str, count: int) -> None:
        for index in range(count):
            broker.publish("orders", f"{prefix}-{index}")

    threads = [
        threading.Thread(target=publish_range, args=("A", 2)),
        threading.Thread(target=publish_range, args=("B", 2)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    batch = broker.poll("orders", "consumer-1", batch_size=2)
    print([(message.offset, message.payload) for message in batch])
    broker.ack("orders", "consumer-1", batch[-1].offset)
    replay = broker.poll("orders", "consumer-1", batch_size=10)
    print([(message.offset, message.payload) for message in replay])


if __name__ == "__main__":
    main()