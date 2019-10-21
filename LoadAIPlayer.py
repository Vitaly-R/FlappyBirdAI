from FlappyBirdPlayer import FlappyBirdPlayer
from AIPlayer import AIPlayer
import os


def main():
    path = ''
    player = FlappyBirdPlayer(True)
    if os.path.exists(path):
        ai = AIPlayer.load_from_weights(path, player.get_width(), player.get_height())
        player.set_players([ai])
    player.play()


if __name__ == '__main__':
    main()
