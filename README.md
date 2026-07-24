# 📖 Bible Alias — Database Editor

**Редактор баз даних для гри "Біблійний Аліас"** | *Database editor for the Bible Alias word game*

---

## Про програму | About

**Bible Alias Database Editor** — це самодостатній застосунок на Python/Streamlit для керування словниками гри "Біблійний Аліас". Програма працює як єдиний `.exe` файл без потреби у встановленому Python чи будь-яких залежностях.

*A standalone Python/Streamlit application for managing Bible Alias game word databases. Runs as a single `.exe` file with no external dependencies.*

### Можливості | Features

- 📂 **Робота з папкою БД** — завантаження всіх `.json` файлів з обраної папки
- 🔍 **Пошук та фільтрація** — пошук за словом/описом, фільтр за складністю
- ✏️ **CRUD-операції** — додавання, редагування, видалення слів
- 📁 **Створення нових БД** — створення порожніх файлів баз даних
- 🗑️ **Видалення БД** — видалення непотрібних файлів баз даних
- 💾 **Збереження** — збереження окремого файлу або всіх файлів одразу
- 📋 **Рівні складності** — Легко, середній, експерт
- 🏷️ **Категорії** — підтримка категорій: Люди, Міста, Події, Книги, Предмети, Притчі, Свята, Місця
- 🎨 **Сучасний інтерфейс** — темна тема, кольорове маркування рівнів складності

### Технології | Tech Stack

- **Python 3.14+**
- **Streamlit** — веб-інтерфейс
- **PyInstaller** — збірка самодостатнього `.exe`
- **JSON** — формат зберігання даних

---

## Встановлення | Installation

### Варіант 1: Готовий `.exe` (рекомендовано)

1. Завантажте останній реліз зі сторінки [Releases](https://github.com/zeroprotocolx86/bible-alias-editor/releases)
2. Розпакуйте та запустіть `BibleAliasEditor.exe`
3. Програма відкриє браузер з інтерфейсом редактора

### Варіант 2: Інсталятор (Windows)

1. Завантажте `BibleAliasEditor_Setup.exe` зі сторінки [Releases](https://github.com/zeroprotocolx86/bible-alias-editor/releases)
2. Запустіть інсталятор та дотримуйтесь інструкцій
3. Програма буде доступна в меню "Пуск" та на робочому столі
4. Для видалення використовуйте "Програми та засоби" панелі керування

### Варіант 3: З вихідного коду

```bash
git clone https://github.com/zeroprotocolx86/bible-alias-editor.git
cd bible-alias-editor
pip install -r requirements.txt
streamlit run app.py
```

---

## Використання | Usage

1. **Вибір папки**: натисніть "Огляд" або введіть шлях до папки з `.json` файлами
2. **Натисніть "Завантажити"**
3. **Виберіть файл** зі списку ліворуч для редагування
4. **Редагуйте**: клікніть ✏️ біля слова, щоб відкрити форму редагування
5. **Додавайте**: використовуйте форму "➕ Додати слово" в сайдбарі
6. **Шукайте**: використовуйте панель "🔍 Пошук" для фільтрації слів
7. **Зберігайте**: натисніть "💾 Зберегти" після внесення змін

---

## Структура БД | Database Structure

Кожен файл `.json` містить масив об'єктів з наступними полями:
*Each `.json` file contains an array of objects with these fields:*

```json
{
  "id": "люди_42",
  "word": "Авраам",
  "category": "Люди",
  "difficulty": "середній",
  "description": "Батько віруючих, якому Бог обіцяв землю Ханаанську",
  "enabled": true
}
```

| Поле | Опис | Description |
|------|------|-------------|
| `id` | Унікальний ідентифікатор | Unique identifier |
| `word` | Слово/фраза | Word/phrase |
| `category` | Категорія | Category |
| `difficulty` | Рівень складності (Легко/середній/експерт) | Difficulty level |
| `description` | Опис або підказка | Description or hint |
| `enabled` | Чи активне слово | Whether the word is active |

---

## Збірка | Building

Для створення самодостатнього `.exe`:

```bat
build.bat
```

Або вручну:

```bat
pyinstaller --onefile --name "BibleAliasEditor" --icon icon.ico ^
  --add-data "data;data" --add-data "app.py;." launcher.py
```

---

## Ліцензія | License

MIT License. Ви можете вільно використовувати, модифікувати та поширювати цю програму.
*MIT License. You are free to use, modify, and distribute this software.*
