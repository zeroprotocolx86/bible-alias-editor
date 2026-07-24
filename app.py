import streamlit as st
import json
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

st.set_page_config(page_title="Біблійний Alias — Редактор БД", page_icon="📖", layout="wide")

DIFFICULTIES = ['Легко', 'середній', 'експерт']

if 'folder_path' not in st.session_state:
    st.session_state.folder_path = ""
if 'files' not in st.session_state:
    st.session_state.files = {}
if 'current_file' not in st.session_state:
    st.session_state.current_file = None
if 'editing_idx' not in st.session_state:
    st.session_state.editing_idx = None
if 'search' not in st.session_state:
    st.session_state.search = ""
if 'filter_diff' not in st.session_state:
    st.session_state.filter_diff = "Всі"
if 'confirm_delete_file' not in st.session_state:
    st.session_state.confirm_delete_file = None


def load_folder(path):
    p = Path(path)
    if not p.is_dir():
        return False
    files = {}
    for f in sorted(p.glob('*.json')):
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            files[f.name] = data
        except Exception:
            files[f.name] = []
    st.session_state.files = files
    st.session_state.folder_path = str(p.resolve())
    st.session_state.current_file = None
    st.session_state.editing_idx = None
    return True


def save_file(filename):
    if filename not in st.session_state.files:
        return False
    path = Path(st.session_state.folder_path) / filename
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.files[filename], f, ensure_ascii=False, indent=2)
    return True


def get_all_categories():
    cats = set()
    for fname, words in st.session_state.files.items():
        for w in words:
            c = w.get('category', '')
            if c:
                cats.add(c)
    return sorted(cats)


def get_next_id(words, cat):
    existing = []
    for w in words:
        wid = w.get('id', '')
        if wid and '_' in wid:
            try:
                existing.append(int(wid.split('_')[-1]))
            except ValueError:
                pass
    nid = max(existing) + 1 if existing else 1
    prefix = cat.lower().replace(' ', '_')[:20]
    return f"{prefix}_{nid}"


def new_word(category):
    return {"id": "", "word": "", "category": category, "difficulty": "середній", "description": "", "enabled": True}


st.sidebar.title("📖 Редактор БД")
st.sidebar.caption("Біблійний Alias — редактор слів")

with st.sidebar.expander("📁 Папка з БД", expanded=True):
    folder_default = st.session_state.folder_path or str(Path("data").resolve())
    folder_input = st.text_input("Шлях до папки", value=folder_default)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📂 Огляд", use_container_width=True):
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            path = filedialog.askdirectory(title="Виберіть папку з БД")
            root.destroy()
            if path:
                st.session_state.folder_path = path
                if load_folder(path):
                    st.rerun()
    with col_b:
        if st.button("📂 Завантажити", use_container_width=True):
            if load_folder(folder_input.strip() or folder_default):
                st.rerun()

if st.session_state.files:
    with st.sidebar.expander("📄 Файли БД", expanded=True):
        for fname in sorted(st.session_state.files.keys()):
            cnt = len(st.session_state.files[fname])
            active = fname == st.session_state.current_file
            cols = st.columns([4, 1])
            with cols[0]:
                if st.button(
                    f"{'📄' if not active else '📝'} {fname}  ({cnt})",
                    key=f"file_{fname}",
                    use_container_width=True,
                    type="primary" if active else "secondary"
                ):
                    st.session_state.current_file = fname
                    st.session_state.editing_idx = None
                    st.rerun()
            with cols[1]:
                if st.button("🗑️", key=f"del_{fname}", help="Видалити цю БД"):
                    st.session_state.confirm_delete_file = fname
                    st.rerun()

    if st.session_state.confirm_delete_file:
        df = st.session_state.confirm_delete_file
        st.sidebar.warning(f"Видалити **{df}**?")
        c1, c2 = st.sidebar.columns(2)
        with c1:
            if c1.button("✅ Так", key="confirm_del_yes", use_container_width=True):
                fpath = Path(st.session_state.folder_path) / df
                if fpath.exists():
                    fpath.unlink()
                st.session_state.files.pop(df, None)
                if st.session_state.current_file == df:
                    st.session_state.current_file = None
                    st.session_state.editing_idx = None
                st.session_state.confirm_delete_file = None
                st.rerun()
        with c2:
            if c2.button("✕ Ні", key="confirm_del_no", use_container_width=True):
                st.session_state.confirm_delete_file = None
                st.rerun()

    with st.sidebar.expander("🔍 Пошук", expanded=True):
        col_s, col_b = st.columns([3, 1])
        with col_s:
            st.text_input("Пошук слова", key="search", placeholder="Введіть слово...")
        with col_b:
            st.write("")
            st.write("")
            if st.button("🔍", key="btn_search", help="Шукати"):
                pass
        diffs = ["Всі"] + DIFFICULTIES
        st.selectbox("Складність", diffs, key="filter_diff")

    with st.sidebar.expander("📁 Створити БД", expanded=True):
        new_db_name = st.text_input("Назва файлу", value="new.json", key="new_db_name")
        if st.button("➕ Створити", use_container_width=True):
            if new_db_name.strip() and new_db_name.strip() not in st.session_state.files:
                st.session_state.files[new_db_name.strip()] = []
                st.session_state.current_file = new_db_name.strip()
                path = Path(st.session_state.folder_path) / new_db_name.strip()
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                st.rerun()

if st.session_state.current_file:
    words = st.session_state.files[st.session_state.current_file]

    if st.sidebar.button("⬅ Назад до списку файлів", use_container_width=True, type="primary"):
        st.session_state.current_file = None
        st.session_state.editing_idx = None
        st.rerun()
    st.sidebar.markdown("---")

    with st.sidebar.expander("➕ Додати слово", expanded=True):
        all_cats = get_all_categories()
        if not all_cats:
            all_cats = ["Загальне"]
        new_cat = st.selectbox("Категорія", all_cats, key="new_cat")
        new_word_val = st.text_input("Слово", key="new_word_text", placeholder="Введіть слово")
        new_desc = st.text_area("Опис", key="new_desc", placeholder="Короткий опис", height=60)
        new_diff = st.selectbox("Складність", DIFFICULTIES, key="new_diff", index=1)
        target_file = st.selectbox("Додати у файл", sorted(st.session_state.files.keys()), key="target_file")
        if st.button("➕ Додати", use_container_width=True, type="primary"):
            if new_word_val.strip() and target_file:
                target_words = st.session_state.files[target_file]
                tmpl = new_word(new_cat)
                tmpl['id'] = f"{new_cat.lower().replace(' ', '_')[:20]}_{get_next_id(target_words, new_cat)}"
                tmpl['word'] = new_word_val.strip()
                tmpl['description'] = new_desc.strip()
                tmpl['difficulty'] = new_diff
                target_words.append(tmpl)
                st.session_state.files[target_file] = target_words
                st.rerun()

    with st.sidebar.expander("💾 Зберегти", expanded=True):
        if st.button("💾 Зберегти цей файл", use_container_width=True):
            save_file(st.session_state.current_file)
            st.success("Збережено!")
        if st.button("💾 Зберегти всі", use_container_width=True):
            for fn in st.session_state.files:
                save_file(fn)
            st.success("Усі файли збережено!")
        if words:
            st.caption(f"Слів: {len(words)}")

if not st.session_state.files:
    st.info("👈 Вкажіть шлях до папки з файлами БД (.json) та натисніть 'Завантажити'")
    st.markdown("---")
    st.markdown("### Як користуватись")
    st.markdown("1. Вкажіть шлях до папки з **.json** файлами бази даних")
    st.markdown("2. Натисніть **Завантажити**")
    st.markdown("3. Оберіть файл зі списку ліворуч")
    st.markdown("4. Редагуйте слова у таблиці")
    st.stop()

if not st.session_state.current_file:
    st.info("👈 Оберіть файл для редагування зі списку ліворуч")
    st.markdown("---")
    st.markdown("### Доступні файли")
    for fname, data in sorted(st.session_state.files.items()):
        cnt = len(data)
        enabled = sum(1 for w in data if w.get('enabled', True))
        cats = len(set(w.get('category', '') for w in data))
        if st.button(
            f"📄 **{fname}** — {cnt} слів, {cats} категорій, ✅ {enabled} активних",
            key=f"sel_{fname}",
            use_container_width=True
        ):
            st.session_state.current_file = fname
            st.rerun()
    st.stop()

fn = st.session_state.current_file
words = st.session_state.files[fn]

filtered = words[:]
q = st.session_state.search.lower().strip()
if q:
    filtered = [w for w in filtered if q in w.get('word', '').lower() or q in w.get('description', '').lower()]
if st.session_state.filter_diff != "Всі":
    filtered = [w for w in filtered if w.get('difficulty') == st.session_state.filter_diff]

st.title(f"📝 {fn}")
col1, col2, col3 = st.columns([1, 5, 1])
col1.metric("Всього", len(words))
col2.metric("Відфільтровано", len(filtered))
with col3:
    if st.button("⬅ Назад до списку", use_container_width=True):
        st.session_state.current_file = None
        st.session_state.editing_idx = None
        st.rerun()

if st.session_state.editing_idx is not None:
    idx = st.session_state.editing_idx
    if idx < len(words):
        w = words[idx]
        st.markdown("---")
        st.subheader(f"✏️ Редагування: {w.get('word', '')}")

        with st.form(key="edit_form"):
            word_val = st.text_input("Слово *", value=w.get('word', ''), key="ew_word")
            cat_val = st.text_input("Категорія", value=w.get('category', ''), key="ew_cat")
            diff_val = st.selectbox("Складність", DIFFICULTIES,
                index=DIFFICULTIES.index(w.get('difficulty', 'середній')) if w.get('difficulty') in DIFFICULTIES else 1,
                key="ew_diff")
            desc_val = st.text_area("Опис", value=w.get('description', ''), key="ew_desc", height=100)
            enabled_val = st.checkbox("Активно", value=w.get('enabled', True), key="ew_enabled")
            btns = st.columns([1, 1, 4])
            with btns[0]:
                saved = st.form_submit_button("💾 Зберегти", type="primary", use_container_width=True)
            with btns[1]:
                deleted = st.form_submit_button("🗑️ Видалити", use_container_width=True)
            with btns[2]:
                cancelled = st.form_submit_button("✕ Скасувати", use_container_width=True)

        if saved:
            w['word'] = word_val
            w['category'] = cat_val
            w['difficulty'] = diff_val
            w['description'] = desc_val
            w['enabled'] = enabled_val
            st.session_state.files[fn] = words
            st.session_state.editing_idx = None
            st.rerun()
        if deleted:
            words.pop(idx)
            st.session_state.files[fn] = words
            st.session_state.editing_idx = None
            st.rerun()
        if cancelled:
            st.session_state.editing_idx = None
            st.rerun()
    else:
        st.session_state.editing_idx = None
        st.rerun()
else:
    st.markdown("---")
    if not filtered:
        st.warning("Немає слів за вибраним фільтром")
    else:
        for i, w in enumerate(filtered):
            idx = words.index(w)
            cols = st.columns([2.5, 1.5, 1.2, 5, 0.8, 0.8])
            dc = {"Легко": "green", "середній": "orange", "експерт": "red"}.get(w.get('difficulty', ''), 'grey')
            cols[0].markdown(f"**{w.get('word', '')}**")
            cols[1].caption(w.get('category', ''))
            cols[2].markdown(f":{dc}[{w.get('difficulty', '')}]")
            cols[3].caption(w.get('description', '')[:80])
            enabled = w.get('enabled', True)
            cols[4].markdown("✅" if enabled else "❌")
            if cols[5].button("✏️", key=f"edit_{i}"):
                st.session_state.editing_idx = idx
                st.rerun()
