from tic_tac_ohno.game import play_tic


def main():
    play_tic(
        lambda *_: '***\n***\n***',
        lambda *_: False,
        lambda *_: False,
        lambda *_: '***\n*&*\n***',
    )


if __name__ == '__main__':
    main()
