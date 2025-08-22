# SQLite GUI App

A simple GUI-based SQLite database manager built with Python, Tkinter, ttkbootstrap, and Tabulate.
This app allows you to create, open, and manage SQLite databases easily without writing commands manually.

## Features

Create and open SQLite databases

Run SQL queries directly from the editor

View results in a styled table format

Save and open .nbdb notebook files

Built-in notepad for SQL scripts

Multiple themes (light/dark modes with ttkbootstrap)

Portable mode support (--portable)

```bash
python sqlite.py --portable
```

Exportable results with tabulate

## Installation

Clone the repository:
```bash
git clone https://github.com/KCoder-programming/sqlite-gui-app.git
cd sqlite-gui-app
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the app with:
```bash
python sqlite.py
```

Optional:

Run in portable mode:
```bash
python sqlite.py --portable
```

## Requirements

Python 3.8+

Pillow

Tabulate

ttkbootstrap

(Already listed in [requirements.txt](https://github.com/KCoder-programming/sqlite-gui-app/blob/main/requirements.txt))

## License

This project is licensed under Creative Commons BY-NC 4.0.
See [LICENSE](https://creativecommons.org/licenses/by-nc/4.0/) for details.
