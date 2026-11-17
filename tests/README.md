# A brief explanation about how to test PyQt5

### How to install
pip install pytest pytest-qt

## Exemple of some basic generic tests
### ui/HMI.py
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, backend=None):
        super().__init__()
        self.backend = backend
        # ... construction de l'UI (boutons, labels, etc.)

### ARCA.py
import sys
from PyQt5.QtWidgets import QApplication
from ui.HMI import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

### tests/test_hmi.py
import pytest
from PyQt5.QtCore import Qt
from ui.HMI import MainWindow

@pytest.fixture
def window(qtbot):
    w = MainWindow()
    qtbot.addWidget(w)   # fermeture et nettoyage automatiques
    w.show()
    return w

def test_titre(window):
    assert window.windowTitle() == "Mon App"

def test_clic_bouton(qtbot, window):
    qtbot.mouseClick(window.btn_start, Qt.LeftButton)
    assert window.label_status.text() == "Running"

def test_saisie(qtbot, window):
    qtbot.keyClicks(window.line_edit, "hello")
    assert window.line_edit.text() == "hello"

def test_signal_emis(qtbot, window):
    with qtbot.waitSignal(window.worker.finished, timeout=2000):
        window.btn_start.click()

def test_mise_a_jour_asynchrone(qtbot, window):
    window.btn_start.click()
    qtbot.waitUntil(lambda: window.label_status.text() == "Done", timeout=3000)

## Isoler l’UI du reste

Pour des tests rapides et fiables, remplacez le matériel, le réseau ou les threads par des mocks :

python
from unittest.mock import MagicMock

def test_bouton_appelle_backend(qtbot):
    backend = MagicMock()
    w = MainWindow(backend=backend)
    qtbot.addWidget(w)

    w.btn_start.click()

    backend.start.assert_called_once()

## Test de fumée de l’app complète

Pour vérifier que l’application démarre sans crash :

python
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

def test_smoke(qtbot):
    w = MainWindow()
    qtbot.addWidget(w)
    w.show()
    QTimer.singleShot(500, w.close)
    qtbot.waitExposed(w)