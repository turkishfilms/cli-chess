from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit import HTML

class BoardView:
    def __init__(self, presenter, initial_board="Initial board not set"):
        self.board_presenter = presenter
        self.board_output = FormattedTextControl(HTML(initial_board))
        self.container = Window(self.board_output, width = 20)

    def update_board_output(self, board_output : str):
        """Updates the board output with the passed in text"""
        self.board_output.text = HTML(board_output)


    def get_container(self) -> Window:
        return self.container


    def __pt_container__(self) -> Window:
        """Returns the game_view container"""
        return self.container
