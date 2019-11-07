import sys, traceback
from app import Application


def main():
    print('Started')
    app = Application()
    try:
        app.init(sys.argv)
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_last()
        exit(-1)

    # Output result.
    print(f'Time-weighted average highest price of orders: {app.average_highest_price()}')
    print('Done')
    return 0


if __name__ == "__main__":
    main()