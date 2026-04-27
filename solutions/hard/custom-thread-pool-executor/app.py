import threading

from services.thread_pool import RejectionPolicy, ThreadPoolExecutor


def main() -> None:
    results: list[str] = []
    done = threading.Event()

    def task(label: str) -> None:
        results.append(label)
        if len(results) >= 3:
            done.set()

    pool = ThreadPoolExecutor(worker_count=2, queue_capacity=2, rejection_policy=RejectionPolicy.CALLER_RUNS)
    try:
        pool.submit(task, "a")
        pool.submit(task, "b")
        pool.submit(task, "c")
        done.wait(1)
        print(sorted(results))
    finally:
        pool.shutdown()


if __name__ == "__main__":
    main()