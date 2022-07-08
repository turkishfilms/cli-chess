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

from __future__ import annotations
from questionary import Question, select
from cli_chess.utils.common import clear_screen


class MenuViewBase:
    def __init__(self, presenter: MenuPresenterBase):
        self.presenter = presenter

    def show(self, title: str = "") -> Question:
        clear_screen()
        return select(title,
                      choices=[option for option in self.presenter.get_menu_options()],
                      qmark="*",
                      instruction=" ",
                      use_shortcuts=True).ask()
