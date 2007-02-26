import sys
import unittest
from PyQt4.QtGui import QApplication, QWidget, QGraphicsScene, QGraphicsView, QGraphicsTextItem
from PyQt4.QtSvg import QGraphicsSvgItem
from PyQt4.QtOpenGL import QGLWidget, QGLFormat, QGL

def card2SvgElement(card):
    if card == None:
        return "back"
    cardsuit2svg = {"d" : "diamond", "c" : "club", "s" : "spade", "h" : "heart"}
    cardvalue2svg = {"Q" : "queen", "K" : "king", "J" : "jack", "T" : "10", "A" : "1"}
    return (cardvalue2svg.has_key(card[0]) and cardvalue2svg[card[0]] or card[0]) + "_" + cardsuit2svg[card[1]]

class QPokerWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.scene = QGraphicsScene()
        self.chat = QGraphicsTextItem()
        self.chat.setFlag(QGraphicsTextItem.ItemIsMovable, True)
        self.table = QGraphicsSvgItem("table.svg")
        self.table.setFlag(QGraphicsSvgItem.ItemIsMovable, True)
        self.board = []
        for i in range(5):
            card = QGraphicsSvgItem("svg-cards.svg", self.table)
            card.setElementId("back")
            card.setFlag(QGraphicsSvgItem.ItemIsMovable, True)
            card.scale(0.5, 0.5)
            self.board.append(card)
        self.scene.addItem(self.chat)
        self.scene.addItem(self.table)
        self.view = QGraphicsView(self)
        self.view.setScene(self.scene)
        self.view.resize(800, 600)
    def renderChat(self, message):
        self.chat.setPlainText(message)
    def renderBoard(self, cards):
        map(lambda card, svgItem: svgItem.setElementId(card2SvgElement(card)), cards, self.board)
    def renderStart(self):
        map(lambda svgItem: svgItem.setElementId("back"), self.board)
    def keyPressEvent(self, event):
        if event.text() == "q":
            self.view.scale(1.1, 1.1)
        elif event.text() == "a":
            self.view.scale(0.9, 0.9)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QPokerWidget()
    widget.show()
    sys.exit(app.exec_())

