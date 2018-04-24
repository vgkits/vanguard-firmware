from config import hardwareConfig


def run():
    from ampy import pyboard

    try:

        board = pyboard.Pyboard(hardwareConfig()['port'])

        board.enter_raw_repl()
        board.exec_('from vgkits.wifi import provideInsecureWifi; provideInsecureWifi()')
        board.exit_raw_repl()

    except pyboard.PyboardError:
        print("Is cockle unplugged or in use by another program?")

    finally:
        board.close()


if __name__ == "__main__":
    run()