
## Overview
This is a simple text editor made in Python using Pyside6 (Qt Framework) to develop the GUI and qt-linguist to switch application language dinamically.

## Instructions

This how I converted GUI Qt designer files into python files to integrate them in the project

```shell
pyside6-uic UIMainWindow.ui -o UIMainWindow.py
```
This command below opens Qt Linguist
```shell
pyside6-linguist
```
This one creates the `.ts` file

```shell
 pyside6-lupdate UIClasses/Window.py -ts Translations/pt_BR.ts
```

This one creates the `.qm` file based on the `.ts` file

```shell
pyside6-lrelease Translations/pt_BR.ts -qm pt_BR.qm 
```

### How the translation system is working here

The way I was using `.ts` before was not efficient: the `.ts` file needed to know exactly the line of code where I inserted `QCoreApplication.translate(Context, String str)` (`Context` being the name of the class with message and `str` is the message). However, if I need to provide the line of code of the string that needs to switch language, I'd need to update `.ts` every single time I would change anything in MainWindow class (Window.py file).

Well, I've created `AppStrings.py` to be the file with all strings and in `.ts` file it is necessary only the file name `AppStrings.py` to indicate the source from where to get the string and its id like below:

```xml
    <message>
            <location filename="../Utils/AppStrings.py" line="id:menu_edit"/>
            <source>Edit</source>
            <translation>Editar</translation>
    </message>
```

Before, the code in Window.py where I set the Action names was like this

```python
self.ui.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File")) # File is the string content that wil change
```

Now is like:

```python
self.ui.menuFile.setTitle(QCoreApplication.translate(*AppStrings.MENU_FILE))
```

It is better now, 'cause if I change anything in `MainWindow`, I don't need to change `.ts` file, once `.ts` file no longer needs to know the line in `MainWindow` it has to check, now `.ts` gets information from `AppStrings`. Take a look on a example in `AppStrings`:

```python
class AppStrings:
    # MainWindow
    WINDOW_TITLE = ("MainWindow", "Text Editor")
    OPEN_FILE = ("MainWindow", "Open file")
    SAVING_FILE = ("MainWindow", "Saving File")
    EXPORT_PDF = ("MainWindow", "Export PDF")
    EXPORT_COMPLETED = ("MainWindow", "Export Completed")

    # ExportDialog
    FILE_SAVED = ("ExportDialog", "File saved in {0}")
    EXPORT_ERROR = ("ExportDialog", "Error of Exporting")
    EXPORT_ERROR_MESSAGE = ("ExportDialog", "Not possible to export PDF file.\nError: ")

    # Close Event
    PROGRAM_NAME = ("MainWindow", "Text Editor")
    SAVE_CHANGES_QUESTION = ("MainWindow", "Do you want to save the changes?")

    # Menus
    MENU_FILE = ("MainWindow", "File")
    MENU_EDIT = ("MainWindow", "Edit")
    MENU_APPEARANCE = ("MainWindow", "Appearance")
    MENU_LANGUAGE = ("MainWindow", "Language")
```

In this case, if `.ts` needs to work with translation of "Edit Menu", it only needs to indicate `AppStrings.py` file and the id "menu_edit", and then uses the tag `source` to point the text to be translated and then uses the tag `translation`, like in a previous example in this README file. 

In short words: `.ts` uses `AppStrings.py` as indication of the texts that can be translated without needing to know any line number, so `MainWindow` can be changed. See below how `MainWindow` uses `AppStrings.py`:

```python
def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Text Editor"))

        self.Export_pdf = AppStrings.EXPORT_PDF

        self.ui.menuFile.setTitle(QCoreApplication.translate(*AppStrings.MENU_FILE))
        self.ui.actionNew.setText(QCoreApplication.translate(*AppStrings.ACTION_NEW))
```

`AppStrings.py` has the string content, and differently from the way I was doing before, if I make any change that would make any string usage move to another line, `.ts` does not need to change anything in itself. Previously `MainWindow` was using strings created inside the class, and once `.ts` was indicating directly `MainWindow`, every change of line was a nightmare.  

## Class Diagram here: (In Progress)

https://lucid.app/lucidchart/b3bc5f04-7113-4b4d-bba3-53429326a05e/edit?invitationId=inv_cd46ab9e-c2cd-4486-b359-e808e8bd015f&page=HWEp-vi-RSFO#

## PlantUML Code (In Progress)

```shell
@startuml
!theme plain

skinparam class {
    BackgroundColor #F8F8F8
    BorderColor #444
    ArrowColor #666
    FontName Helvetica
}

skinparam defaultTextAlignment center

title Diagrama de Classes - Editor de Texto

' 1. Classes de UI
class Ui_MainWindow {
  + setupUi(MainWindow: QMainWindow)
  + retranslateUi(MainWindow: QMainWindow)
}

class Ui_FontSize {
  + setupUi(MainWindow: QMainWindow)
  + retranslateUi(MainWindow: QMainWindow)
}

class FontSizeWindow {
  - __fontSize: int
  - ui: Ui_FontSize
  + __init__(plainText: QPlainTextEdit, parent: QWidget=None)
  - __updateTextSize(plainText: QPlainTextEdit)
}

' 2. Classes de Serviço
class TextEditorService {
  - _file_path: str
  - _is_modified: bool
  - _saved: bool
  - _is_updating: bool
  + new_file()
  + open_file(file_path: str): str | None
  + save_file(text: str)
  + save_as(text: str, file_path: str)
  + file_exist(): bool
}

class FileManager {
  + {static} checkFile(file_path: str): bool
  + {static} extractFileName(file_path: str): str
  + {static} updatingFile(file_path: str, content: str)
  + {static} read(file_path: str): str | None
  + {static} append(file_path: str, content: str)
}

' 3. Classes de Aparência
enum AppTheme {
  DARK
  LIGHT
}

' 4. Classe Principal
class MainWindow {
  - __fontSizeWindow: FontSizeWindow
  - __service: TextEditorService
  - __is_updating: bool
  - ui: Ui_MainWindow
  + __init__(parent: QWidget=None)
  + press_file_new()
  + pressFileSave()
  + pressFileSaveAs()
  + pressExportPDF()
  - apply_stylesheet(theme: AppTheme)
  + closeEvent(event: QCloseEvent)
}

' 5. Relacionamentos
MainWindow --> Ui_MainWindow : compõe
MainWindow --> TextEditorService : compõe
MainWindow --> FontSizeWindow : associa
MainWindow --> AppTheme : usa

FontSizeWindow --> Ui_FontSize : compõe

TextEditorService ..> FileManager : usa

' 6. Classes Qt (simplificadas)
class QMainWindow <<external>> {
  __
}

class QPlainTextEdit <<external>> {
  __
}

MainWindow --|> QMainWindow
FontSizeWindow --|> QMainWindow

' 7. Notas explicativas
note top of MainWindow
  **Classe Principal**
  Controla toda a aplicação,
  conecta ações de UI com
  a lógica de negócio
end note

note right of TextEditorService
  **Camada de Serviço**
  Gerencia:
  - Estado do documento
  - Operações de arquivo
  - Controle de modificações
end note

note bottom of FileManager
  **Utilitário de Arquivos**
  Operações estáticas de:
  - Leitura/Escrita
  - Verificação
  - Manipulação de paths
end note

@enduml
```

## Image 
![alt text](JLNDRX~1.PNG)

## Issues

Currently the messages in other context windows such as Export PDF are not having their strings' content being changed for some reason.
