from PyQt5.QtWidgets import QFileDialog


def save_to_csv(table):
    file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "CSV Files (*.csv)")

    if file_path:
        with open(file_path, 'w') as f:
            for row in range(table.rowCount()):
                email = table.item(row, 0).text()
                f.write(email + '\n')
