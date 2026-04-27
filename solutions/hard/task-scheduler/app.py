import threading

from services.scheduler import TaskScheduler


def main() -> None:
    results: list[str] = []
    done = threading.Event()

    def record(label: str) -> None:
        results.append(label)
        if len(results) == 2:
            done.set()

    scheduler = TaskScheduler(worker_count=2)
    try:
        scheduler.schedule("t1", 0.0, record, "first")
        scheduler.schedule("t2", 0.01, record, "second")
        done.wait(1)
        print(results)
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    main()