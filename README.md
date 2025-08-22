# SQLite GUI App
A simple GUI-based SQLite database manager built with Python, Tkinter, ttkbootstrap, and Tabulate.
This app allows you to create, open, and manage SQLite databases easily without writing commands manually.

## Features
- Create and open SQLite databases
- Run SQL queries directly from the editor
- View results in a styled table format
- Save and open .nbdb notebook files
- Built-in notepad for SQL scripts
- Multiple themes (light/dark modes with ttkbootstrap)
- Portable mode support (--portable)
  ```bash
  python sqlite.py --portable
  ```
- Exportable results with tabulate

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/KCoder-programming/sqlite-gui-app.git
   cd sqlite-gui-app
   ```

2. Install dependencies:
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
- Python 3.8+
- Pillow
- Tabulate
- ttkbootstrap
(Already listed in [requirements.txt](https://github.com/KCoder-programming/sqlite-gui-app/blob/main/requirements.txt))

## Screenshot:
<img width="952" height="592" alt="Screenshot 2025-08-22 183943" src="https://github.com/user-attachments/assets/55325f74-434b-40a2-bf96-72ba7b115aa0" />

---

## License
Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

Copyright © 2025 KCoder-programming

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms:
- Attribution — You must give appropriate credit , provide a link to the license, and indicate if changes were made . You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- NonCommercial — You may not use the material for commercial purposes .

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

Notices:
- You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation .
- No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.

See [LICENSE](https://github.com/KCoder-programming/sqlite-gui-app/blob/main/LICENSE.txt) for details.
