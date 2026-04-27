from models.core import Viewer
from services.auction import Auction


def main() -> None:
    auction = Auction(item_id="ITEM-1")
    viewer = Viewer(viewer_id="V1")
    auction.subscribe(viewer)

    print(auction.place_bid("B1", 100))
    print(auction.place_bid("B2", 150))
    print(viewer.notifications)


if __name__ == "__main__":
    main()