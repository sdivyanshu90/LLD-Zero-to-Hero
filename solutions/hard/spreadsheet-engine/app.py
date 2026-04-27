from services.spreadsheet import Spreadsheet


def main() -> None:
    sheet = Spreadsheet()
    sheet.set_value("A1", 10)
    sheet.set_value("A2", 5)
    sheet.set_formula("B1", ["A1", "A2"])
    print(sheet.snapshot())
    sheet.set_value("A1", 20)
    print(sheet.snapshot())


if __name__ == "__main__":
    main()