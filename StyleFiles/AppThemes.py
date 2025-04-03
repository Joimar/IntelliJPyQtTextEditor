from enum import Enum


class AppTheme(Enum):
    DARK = '''
    QWidget {
        background-color: #212121;
        color: #FFFFFF;
    }

    QPlainTextEdit {
        background-color: #2E2E2E;
        color: #E0E0E0;
        border: 1px solid #555555;
    }

    QPushButton {
        background-color: #424242;
        color: #FFFFFF;
        border: 1px solid #555555;
        
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #616161;
    }

    QMenuBar {
        background-color: #333333;
    }

    QMenuBar::item {
        background: transparent;
        color: #FFFFFF;
        
    }
    QMenuBar::item:selected {
        background: #555555;
    }

    QMenu {
        background-color: #333;
        color: white;
        border: 1px solid #444;
        padding: 5px; 
        margin: 2px; 
    }
    
    QMenu::item {
        padding: 4px 20px; 
    }
    
    QMenu::item:selected {
        background-color: #555555;
    }

    QScrollBar:vertical {
        background: #2E2E2E;
        width: 10px;
    }
    QScrollBar::handle:vertical {
        background: #555555;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
    }

    QToolTip {
        background-color: #555555;
        color: #FFFFFF;
        border: 1px solid #777777;
    }
    '''

    LIGHT = ""
