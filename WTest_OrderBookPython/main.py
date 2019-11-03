import App

def main():

    print("Started")

    try:

        app = application()
        app.init()
        app.run()

    except BaseException as e:

        print("Error: ") # << e.what() << endl;
        exit(-1);

    # Output result.
    print("Time-weighted average highest price of orders: ")# << app.average_highest_price() << endl;
    print("Done")
    return 0

if __name__ == "__main__":
    main()