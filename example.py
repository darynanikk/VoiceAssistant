from time import sleep

from command.cursor.impl import CursorMovementCommand, CursorClickingCommand
from service.cursor import ClickType

movement: CursorMovementCommand = CursorMovementCommand()

movement.move_to(200, 400)
sleep(1)
movement.move_to(400, 200)
sleep(1)

clicking: CursorClickingCommand = CursorClickingCommand()

clicking.click(ClickType.LEFT)
