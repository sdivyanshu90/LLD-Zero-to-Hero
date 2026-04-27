import threading

from services.database import Table


def main() -> None:
    table = Table()
    table.insert("r1", {"balance": 10})
    table.insert("r2", {"balance": 20})

    t1 = threading.Thread(target=table.update, args=("r1", {"balance": 11}))
    t2 = threading.Thread(target=table.update, args=("r2", {"balance": 21}))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print(table.read("r1"))
    print(table.read("r2"))


if __name__ == "__main__":
    main()