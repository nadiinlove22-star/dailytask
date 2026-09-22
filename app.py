from datetime import datetime, timedelta
import streamlit as st

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="DailyTask", page_icon="📋", layout="centered"
)

# Custom CSS untuk membuat UI benar-benar mirip aplikasi mobile (Dark Mode & Card Style)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1329;
        color: #f1f5f9;
    }
    /* Sembunyikan elemen bawaan Streamlit yang mengganggu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Kartu Utama & Kontainer */
    .metric-card {
        background-color: #121c38;
        border: 1px solid #1e293b;
        padding: 15px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .task-card {
        background-color: #131c38;
        border: 1px solid #1e293b;
        padding: 10px 14px;
        border-radius: 12px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inisialisasi Session State
if "user_name" not in st.session_state:
  st.session_state.user_name = "DK"
if "selected_date" not in st.session_state:
  st.session_state.selected_date = datetime.now().strftime("%Y-%m-%d")
if "tasks" not in st.session_state:
  st.session_state.tasks = [
      {
          "id": "1",
          "title": "Kasih Makan Ikan",
          "target": 1,
          "freq": "daily",
          "extra": None,
      },
      {
          "id": "2",
          "title": "Up Vid Berkahlangit.id",
          "target": 2,
          "freq": "daily",
          "extra": None,
      },
      {
          "id": "3",
          "title": "Upload Shopee Video",
          "target": 2,
          "freq": "daily",
          "extra": None,
      },
      {
          "id": "4",
          "title": "Share link shopee",
          "target": 50,
          "freq": "daily",
          "extra": None,
      },
      {
          "id": "5",
          "title": "Generate AI Video",
          "target": 2,
          "freq": "daily",
          "extra": None,
      },
  ]
if "progress" not in st.session_state:
  st.session_state.progress = {}

days_indo = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
days_full = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
months_indo = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "Mei",
    "Jun",
    "Jul",
    "Ags",
    "Sep",
    "Okt",
    "Nov",
    "Des",
]

# --- HEADER PROFIL ---
col1, col2 = st.columns([3, 1])
with col1:
  st.markdown(f"### Hey, {st.session_state.user_name}! ✏️")
  selected_dt = datetime.strptime(st.session_state.selected_date, "%Y-%m-%d")
  day_idx = selected_dt.weekday()  # 0=Senin, 6=Minggu
  day_name = days_full[
      (day_idx + 1) % 7
      if day_idx < 6
      else 0  # penyesuaian index ke format minggu sbg awal/akhir
  ]
  date_str_display = (
      f"{days_full[selected_dt.weekday()]}, {selected_dt.day}"
      f" {months_indo[selected_dt.month-1]} {selected_dt.year}"
  )
  st.caption(f"📅 {date_str_display}")
with col2:
  day_of_year = selected_dt.timetuple().tm_yday
  st.markdown(
      f"<div style='text-align: right; background: #131c38; padding: 6px"
      f" 10px; border-radius: 8px; border: 1px solid #1e293b; font-size: 11px;"
      f" color: #94a3b8;'>Hari ke-{day_of_year} dari 365</div>",
      unsafe_allow_html=True,
  )

st.divider()

# --- HITUNG PROGRESS & FILTER ---
active_tasks = st.session_state.tasks
day_prog = st.session_state.progress.get(st.session_state.selected_date, {})

total_target = sum([t.get("target", 1) for t in active_tasks])
total_done = sum(
    [
        min(day_prog.get(t["id"], 0), t.get("target", 1))
        for t in active_tasks
    ]
)
percent = int((total_done / total_target * 100)) if total_target > 0 else 0

# --- KARTU PRODUKTIVITAS ---
st.markdown(
    f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; color: #34d399;">
            <span>PRODUKTIVITAS {days_full[selected_dt.weekday()].upper()}</span>
            <span>{percent}%</span>
        </div>
        <p style="font-size: 11px; color: #94a3b8; margin-top: 5px;">{total_done} dari {total_target} tugas selesai</p>
    </div>
""",
    unsafe_allow_html=True,
)
st.progress(percent / 100)

# --- NAVIGASI HARI CEPAT (PILL BUTTONS) ---
st.markdown("<br>", unsafe_allow_html=True)
day_cols = st.columns(7)
today_obj = datetime.now()
for i, d_label in enumerate(days_indo):
  # Hitung tanggal relatif minggu ini
  current_weekday = today_obj.weekday()
  # sesuaikan selisih hari
  target_date_obj = today_obj + timedelta(
      days=(i - (current_weekday if current_weekday != 6 else 6))
  )
  t_str = target_date_obj.strftime("%Y-%m-%d")

  is_selected = t_str == st.session_state.selected_date
  btn_type = "primary" if is_selected else "secondary"

  with day_cols[i]:
    if st.button(
        d_label, key=f"day_btn_{i}", use_container_width=True, type=btn_type
    ):
      st.session_state.selected_date = t_str
      st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVIGASI TAB UTAMA ---
tab1, tab2, tab3, tab4 = st.tabs(["📋 Tugas", "📅 Kalender", "📊 Analitik", "⚙️ Pengaturan"])

# --- TAB 1: DAFTAR TUGAS ---
with tab1:
  search_query = st.text_input(
      "🔍 Cari tugas...", placeholder="Ketik nama tugas..."
  ).lower()
  filtered_tasks = (
      [t for t in active_tasks if search_query in t["title"].lower()]
      if search_query
      else active_tasks
  )

  if not filtered_tasks:
    st.info("Tidak ada tugas ditemukan.")
  else:
    for task in filtered_tasks:
      current_val = day_prog.get(task["id"], 0)
      target_val = task.get("target", 1)
      is_done = current_val >= target_val

      cols = st.columns([0.4, 2.3, 1.2, 0.4, 0.4])

      with cols[0]:
        checked = st.checkbox(
            "✓",
            value=is_done,
            key=f"chk_{task['id']}_{st.session_state.selected_date}",
            label_visibility="collapsed",
        )
        if checked != is_done:
          if not st.session_state.progress.get(st.session_state.selected_date):
            st.session_state.progress[st.session_state.selected_date] = {}
          st.session_state.progress[st.session_state.selected_date][
              task["id"]
          ] = (target_val if checked else 0)
          st.rerun()

      with cols[1]:
        title_style = (
            "text-decoration: line-through; color: #94a3b8; font-size: 13px;"
            if is_done
            else "color: #ffffff; font-weight: 500; font-size: 13px;"
        )
        st.markdown(f"<div style='{title_style}'>{task['title']}</div>", unsafe_allow_html=True)

      with cols[2]:
        sub_c1, sub_c2, sub_c3 = st.columns(3)
        with sub_c1:
          if st.button("➖", key=f"min_{task['id']}"):
            if current_val > 0:
              st.session_state.progress[st.session_state.selected_date][
                  task["id"]
              ] = (current_val - 1)
              st.rerun()
        with sub_c2:
          st.markdown(
              f"<div style='text-align:center; font-size:11px;"
              f" color:#94a3b8; padding-top:4px;'>{current_val}/{target_val}</div>",
              unsafe_allow_html=True,
          )
        with sub_c3:
          if st.button("➕", key=f"plus_{task['id']}"):
            if current_val < target_val:
              st.session_state.progress[st.session_state.selected_date][
                  task["id"]
              ] = (current_val + 1)
              st.rerun()

      with cols[3]:
        if st.button("✏️", key=f"edit_{task['id']}"):
          st.toast(f"Edit: {task['title']}")

      with cols[4]:
        if st.button("🗑️", key=f"del_{task['id']}"):
          st.session_state.tasks = [
              t for t in st.session_state.tasks if t["id"] != task["id"]
          ]
          st.rerun()

  st.divider()

  # Form Tambah Tugas Baru
  with st.expander("➕ Tambah Tugas Baru"):
    with st.form("add_task_form"):
      new_title = st.text_input("Nama Tugas")
      new_target = st.number_input("Target Jumlah", min_value=1, value=1)
      submitted = st.form_submit_button("Simpan Tugas")
      if submitted and new_title:
        new_task = {
            "id": str(datetime.now().timestamp()),
            "title": new_title,
            "target": new_target,
            "freq": "daily",
            "extra": None,
        }
        st.session_state.tasks.append(new_task)
        st.success("Tugas berhasil ditambahkan!")
        st.rerun()

# --- TAB 2: KALENDER ---
with tab2:
  st.subheader("📅 Kalender & Riwayat")
  chosen_cal = st.date_input("Pilih Tanggal Agenda", datetime.now())
  cal_str = chosen_cal.strftime("%Y-%m-%d")
  st.write(f"Menampilkan aktivitas untuk tanggal: {cal_str}")

# --- TAB 3: ANALITIK ---
with tab3:
  st.subheader("📊 Statistik Produktivitas")
  col_m1, col_m2 = st.columns(2)
  with col_m1:
    st.metric("Total Hari Tercatat", len(st.session_state.progress))
  with col_m2:
    total_actions_done = sum(
        sum(1 for v in day.items() if v[1] > 0)
        for day in st.session_state.progress.values()
    )
    st.metric("Total Aksi Selesai", total_actions_done)

# --- TAB 4: PENGATURAN ---
with tab4:
  st.subheader("⚙️ Pengaturan Aplikasi")
  new_name = st.text_input("Nama Panggilan", value=st.session_state.user_name)
  if st.button("Simpan Nama"):
    st.session_state.user_name = new_name
    st.success("Nama berhasil diperbarui!")
    st.rerun()

  st.divider()
  if st.button("🗑️ Reset Semua Data"):
    st.session_state.clear()
    st.success("Data direset!")
    st.rerun()
          
