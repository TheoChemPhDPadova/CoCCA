

def appendi(self, text):
        cursor = self.pippo.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        cursor.insertText("\n")