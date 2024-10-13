import sys
import random

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor


class Tetris(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()
        self.tboard.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.tboard.start()

        self.resize(180, 380)
        self.center()
        self.setWindowTitle('Tetris')
        self.show()


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))


class Board(QFrame):

    msg2statusbar = pyqtSignal(str)

    BOARD_WIDTH = 10
    BOARD_HEIGHT = 22
    SPEED = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.init_board()


    def init_board(self):
        self.timer = QBasicTimer()
        self.is_waiting_after_line = False
        self.cur_x = 0
        self.cur_y = 0
        self.num_lines_removed = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.is_started = False
        self.isPaused = False
        self.clear_board()


    def shape_at(self, x, y):
        return self.board[(y * Board.BOARD_WIDTH) + x]


    def set_shape_at(self, x, y, shape):
        self.board[(y * Board.BOARD_WIDTH) + x] = shape


    def square_width(self):
        return self.contents_rect().width() // Board.BOARD_WIDTH


    def square_height(self):
        return self.contents_rect().height() // Board.BOARD_HEIGHT


    def start(self):
        if self.isPaused:
            return

        self.is_started = True
        self.is_waiting_after_line = False
        self.num_lines_removed = 0
        self.clear_board()

        self.msg2statusbar.emit(str(self.num_lines_removed))
        self.new_piece()
        self.timer.start(Board.SPEED, self)


    def pause(self):
        if not self.is_started:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2statusbar.emit("paused")
        else:
            self.timer.start(Board.SPEED, self)
            self.msg2statusbar.emit(str(self.num_lines_removed))

        self.update()


    def paint_event(self, event):
        painter = QPainter(self)
        rect = self.contents_rect()
        boardTop = rect.bottom() - Board.BOARD_HEIGHT * self.square_height()

        for i in range(Board.BOARD_HEIGHT):
            for j in range(Board.BOARD_WIDTH):
                shape = self.shape_at(j,
                                      Board.BOARD_HEIGHT - i - 1)

                if shape != Tetrominoe.NO_SHAPE:
                    self.draw_square(painter,
                                     rect.left() + j * self.square_width(),
                                     boardTop + i * self.square_height(), shape)

        if self.cur_piece.shape() != Tetrominoe.NO_SHAPE:
            for i in range(4):
                x = self.cur_x + self.cur_piece.x(i)
                y = self.cur_y - self.cur_piece.y(i)
                self.draw_square(painter,
                                 rect.left() + x * self.square_width(),
                                 boardTop + (Board.BOARD_HEIGHT - y - 1) * self.square_height(),
                                 self.cur_piece.shape())


    def key_press_event(self, event):
        if not self.is_started or self.cur_piece.shape() == Tetrominoe.NO_SHAPE:
            super(Board, self).key_press_event(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.try_move(self.cur_piece,
                          self.cur_x - 1,
                          self.cur_y)

        elif key == Qt.Key_Right:
            self.try_move(self.cur_piece,
                          self.cur_x + 1,
                          self.cur_y)

        elif key == Qt.Key_Down:
            self.try_move(self.cur_piece.rotate_right(),
                          self.cur_x,
                          self.cur_y)

        elif key == Qt.Key_Up:
            self.try_move(self.cur_piece.rotate_left(),
                          self.cur_x,
                          self.cur_y)

        elif key == Qt.Key_Space:
            self.drop_down()

        elif key == Qt.Key_D:
            self.one_line_down()

        else:
            super(Board, self).key_press_event(event)


    def timer_event(self, event):
        if event.timerId() == self.timer.timerId():
            if self.is_waiting_after_line:
                self.is_waiting_after_line = False
                self.new_piece()
            else:
                self.one_line_down()
        else:
            super(Board, self).timer_event(event)


    def clear_board(self):
        self.board = [Tetrominoe.NO_SHAPE] * (Board.BOARD_HEIGHT * Board.BOARD_WIDTH)


    def drop_down(self):
        new_y = self.cur_y

        while new_y > 0:
            if not self.try_move(self.cur_piece, self.cur_x, new_y - 1):
                break
            new_y -= 1

        self.piece_dropped()


    def one_line_down(self):
        if not self.try_move(self.cur_piece, self.cur_x, self.cur_y - 1):
            self.piece_dropped()


    def piece_dropped(self):
        for i in range(4):
            x = self.cur_x + self.cur_piece.x(i)
            y = self.cur_y - self.cur_piece.y(i)
            self.set_shape_at(x, y, self.cur_piece.shape())

        self.remove_full_lines()

        if not self.is_waiting_after_line:
            self.new_piece()


    def remove_full_lines(self):
        rows_to_remove = []

        for i in range(Board.BOARD_HEIGHT):
            if all(self.shape_at(j, i) != Tetrominoe.NO_SHAPE for j in range(Board.BOARD_WIDTH)):
                rows_to_remove.append(i)

        for row in rows_to_remove:
            for i in range(row, Board.BOARD_HEIGHT - 1):
                for j in range(Board.BOARD_WIDTH):
                    self.set_shape_at(j, i, self.shape_at(j, i + 1))

        if rows_to_remove:
            self.num_lines_removed += len(rows_to_remove)
            self.msg2statusbar.emit(str(self.num_lines_removed))
            self.is_waiting_after_line = True
            self.cur_piece.set_shape(Tetrominoe.NO_SHAPE)
            self.update()


    def new_piece(self):
        self.cur_piece = Shape()
        self.cur_piece.set_random_shape()
        self.cur_x = Board.BOARD_WIDTH // 2 + 1
        self.cur_y = Board.BOARD_HEIGHT - 1 + self.cur_piece.min_y()

        if not self.try_move(self.cur_piece,
                             self.cur_x,
                             self.cur_y):
            self.cur_piece.set_shape(Tetrominoe.NO_SHAPE)
            self.timer.stop()
            self.is_started = False
            self.msg2statusbar.emit("Game over")


    def try_move(self, new_piece, new_x, new_y):
        for i in range(4):
            x = new_x + new_piece.x(i)
            y = new_y - new_piece.y(i)

            if x < 0 or x >= Board.BOARD_WIDTH or y < 0 or y >= Board.BOARD_HEIGHT:
                return False

            if self.shape_at(x, y) != Tetrominoe.NO_SHAPE:
                return False

        self.cur_piece = new_piece
        self.cur_x = new_x
        self.cur_y = new_y
        self.update()

        return True


    def draw_square(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fill_rect(x + 1,
                          y + 1,
                          self.square_width() - 2,
                          self.square_height() - 2,
                          color)

        painter.set_pen(color.lighter())
        painter.draw_line(x,
                          y + self.square_height() - 1,
                          x,
                          y)
        painter.draw_line(x,
                          y,
                          x + self.square_width() - 1,
                          y)

        painter.set_pen(color.darker())
        painter.draw_line(x + 1,
                          y + self.square_height() - 1,
                          x + self.square_width() - 1,
                          y + self.square_height() - 1)
        painter.draw_line(x + self.square_width() - 1,
                          y + self.square_height() - 1,
                          x + self.square_width() -1,
                          y + 1)


class Tetrominoe:
    NO_SHAPE = 0
    Z_SHAPE = 1
    S_SHAPE = 2
    LINE_SHAPE = 3
    T_SHAPE = 4
    SQUARE_SHAPE = 5
    L_SHAPE = 6
    MIRRORED_L_SHAPE = 7


class Shape:
    COORDS_TABLE = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1))
    )

    def __init__(self):
        self.coords = [[0, 0] for _ in range(4)]
        self.piece_shape = Tetrominoe.no_shape
        self.set_shape(Tetrominoe.no_shape)


    def shape(self):
        return self.piece_shape


    def set_shape(self, shape):
        table = Shape.COORDS_TABLE[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]
        self.piece_shape = shape


    def set_random_shape(self):
        self.set_shape(random.randint(1, 7))


    def x(self, index):
        return self.coords[index][0]


    def y(self, index):
        return self.coords[index][1]


    def set_x(self, index, x):
        self.coords[index][0] = x


    def set_y(self, index, y):
        self.coords[index][1] = y


    def min_x(self):
        return min(self.coords[i][0] for i in range(4))


    def min_y(self):
        return min(self.coords[i][1] for i in range(4))


    def rotate_left(self):
        if self.piece_shape == Tetrominoe.SQUARE_SHAPE:
            return self

        result = Shape()
        result.piece_shape = self.piece_shape
        for i in range(4):
            result.set_x(i,
                         self.y(i))
            result.set_y(i,
                         -self.x(i))
        return result


    def rotate_right(self):
        if self.piece_shape == Tetrominoe.SQUARE_SHAPE:
            return self

        result = Shape()
        result.piece_shape = self.piece_shape
        for i in range(4):
            result.set_x(i, -self.y(i))
            result.set_y(i, self.x(i))
        return result


if __name__ == '__main__':
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())