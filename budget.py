import better_exceptions

from gui import MainWindow

DATA_FILE_NAME = "budget.csv"

if __name__ == "__main__":

    better_exceptions.hook()
    print("Welcome to simplistic personal budget")

    window = MainWindow(DATA_FILE_NAME)

    window.mainloop()
