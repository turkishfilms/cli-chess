# Copyright (C) 2021-2022 Trevor Bayless <trevorbayless1@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from cli_chess.game.board import BoardModel
from cli_chess.utils import Event
from chess import piece_symbol, WHITE, BLACK
from typing import List


class MoveListModel:
    def __init__(self, board_model: BoardModel) -> None:
        self.board_model = board_model
        self.board_model.e_board_model_updated.add_listener(self.update)

        # The move replay board is used to generate the move list output
        # by replaying the move stack of the actual game on the replay board
        self.move_replay_board = self.board_model.board.copy()

        self.initial_fen = self.move_replay_board.fen()
        self.move_list_data = []

        self.e_move_list_model_updated = Event()
        self.update()

    def _move_list_model_updated(self) -> None:
        """Notifies listeners of move list model updates"""
        self.e_move_list_model_updated.notify()

    def update(self) -> None:
        """Updates the move list data using the latest move stack"""
        self.move_list_data.clear()
        self.move_replay_board.set_fen(self.initial_fen)

        for move in self.board_model.get_move_stack():
            if not move:
                raise ValueError(f"Invalid move ({move}) retrieved from move stack")

            color = WHITE if self.move_replay_board.turn == WHITE else BLACK

            # Use the drop piece type if this is a crazyhouse drop
            if move.drop is None:
                piece_type = self.move_replay_board.piece_type_at(move.from_square)
            else:
                piece_type = move.drop

            symbol = piece_symbol(piece_type)
            is_castling = self.move_replay_board.is_castling(move)
            san_move = self.move_replay_board.san_and_push(move)

            move_data = {
                'turn': color,
                'move': san_move,
                'piece_type': piece_type,
                'piece_symbol': symbol,
                'is_castling': is_castling,
                'is_promotion': True if move.promotion else False
            }

            self.move_list_data.append(move_data)

        self._move_list_model_updated()

    def get_move_list_data(self) -> List[dict]:
        """Returns the move list data"""
        return self.move_list_data
