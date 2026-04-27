from services.atm import ATM


def main() -> None:
    atm = ATM(inventory={100: 2, 20: 5, 10: 10})
    print(atm.withdraw(230))
    print(atm.snapshot())


if __name__ == "__main__":
    main()