import mainwindow as mw
import vars


def main():
    vars.mainwindow = mw.Mainwindow()
    vars.mainwindow.mainloop()


if __name__ == '__main__':
    main()
