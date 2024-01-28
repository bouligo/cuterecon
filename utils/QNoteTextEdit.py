from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QTextEdit


class QNoteTextEdit(QTextEdit):
    def insertImage(self, image: QImage):
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, 'PNG')
        image_encoded = byte_array.toBase64().data().decode()
        cursor = self.textCursor()
        cursor.insertHtml(f'<img src="data:image/png;base64, {image_encoded}" alt="" />')

    def canInsertFromMimeData(self, source):
        if source.hasImage() or source.hasUrls():
            return True
        else:
            return QTextEdit.canInsertFromMimeData(self, source)

    def insertFromMimeData(self, source):
        if source.hasImage():
            image = QImage(source.imageData())
            self.insertImage(image)
        elif source.hasUrls():
            for resource in source.urls():
                if resource.isLocalFile():
                    image = QImage(resource.toLocalFile())
                    self.insertImage(image)
        else:
            QTextEdit.insertFromMimeData(self, source)