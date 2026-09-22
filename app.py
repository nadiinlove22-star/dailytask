from datetime import datetime, timedelta
import json
import streamlit as st

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="DayliDo - Daily Todo List", page_icon="📋", layout="centered"
)

# Custom CSS untuk mempercantik tampilan ala Dark Mode Tailwind
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1329;
        color: #f1f5f9;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inisialisasi Session State
if "user_name" not in st.session_state:
  st.session_state.user_name = "Dedi Kurniawan"
if "selected_date" not in st.session_state:
  st.session_state.selected_date = datetime.now().strftime("%Y-%m-%d")
if "tasks" not in st.session_state:
  st.session_state.tasks = [
      {
          "id": "1",
          "title": "Minum Air Putih 2L",
          "target": 2,
          "freq": "daily",
          "extra": None,
      },
      {
          "id": "2",
          "title": "Olahraga / Stretching",
          "target": 1,
          "freq": "daily",
          "extra": None,
      },
      {
          "id": "3",
          "title": "Baca Buku 15 Menit",
          "target": 1,
          "freq": "daily",
          "extra": None,
      },
  ]
if "progress" not in st.session_state:
  st.session_state.progress = {}
if "task_meta" not in st.session_state:
  st.session_state.task_meta = {}

days_indo = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
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
  first_name = st.session_state.user_name.split(" ")[0]
  st.markdown(f"### Hey, {first_name}! 👋")
  selected_dt = datetime.strptime(st.session_state.selected_date, "%Y-%m-%d")
  date_str_display = (
      f"{days_indo[selected_dt.weekday()]}, {selected_dt.day}"
      f" {months_indo[selected_dt.month-1]} {selected_dt.year}"
  )
  st.caption(f"📅 {date_str_display}")
with col2:
  st.markdown(
      f"<div style='text-align: right; background: #1e293b; padding: 8px"
      f" rounded-lg; border: 1px solid #334155;'><b>👤"
      f" {st.session_state.user_name[0]}</b></div>",
      unsafe_allow_html=True,
  )

st.divider()

# --- PILIH TANGGAL (NAVIGASI) ---
col_date1, col_date2 = st.columns([2, 1])
with col_date1:
  chosen_date = st.date_input(
      "Pilih Tanggal Aktif", datetime.strptime(st.session_state.selected_date, "%Y-%m-%d")
  )
  st.session_state.selected_date = chosen_date.strftime("%Y-%m-%d")

# --- HITUNG PROGRESS & FILTER FREKUENSI ---
def is_task_active(task, date_str):
  freq = task.get("freq", "daily")
  if freq == "daily":
    return True
  d = datetime.strptime(date_str, "%Y-%m-%d")
  if freq == "weekly":
    return str(d.weekday() + 1) % 7 == int(
        task.get("extra", 1)
    )  # penyesuaian index hari
  if freq == "monthly":
    return d.day == int(task.get("extra", 1))
  if freq == "specific_date":
    return date_str == task.get("extra")
  return True


active_tasks = [
    t
    for t in st.session_state.tasks
    if is_task_active(t, st.session_state.selected_date)
]
day_prog = st.session_state.progress.get(st.session_state.selected_date, {})

total_target = sum([t.get("target", 1) for t in active_tasks])
total_done = sum(
    [
        min(day_prog.get(t["id"], 0), t.get("target", 1))
        for t in active_tasks
    ]
)
percent = int((total_done / total_target * 100)) if total_target > 0 else 0

# --- KARTU PROGRESS ---
st.markdown(
    f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: bold; color: #34d399;">
            <span>PRODUKTIVITAS HARIAN</span>
            <span>{percent}%</span>
        </div>
        <p style="font-size: 11px; color: #94a3b8; margin-top: 5px;">{total_done} dari {total_target} target selesai</p>
    </div>
""",
    unsafe_allow_html=True,
)
st.progress(percent / 100)

st.markdown("<br>", unsafe_allow_html=True)

# --- NAVIGASI TAB UTAMA ---
tab1, tab2, tab3, tab4 = st.tabs(["📋 Tugas", "📅 Kalender", "📊 Analitik", "⚙️ Pengaturan"])

# --- TAB 1: TUGAS & PENCARIAN ---
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
    st.info("Tidak ada tugas terjadwal atau yang cocok dengan pencarian.")
  else:
    for task in filtered_tasks:
      current_val = day_prog.get(task["id"], 0)
      target_val = task.get("target", 1)
      is_done = current_val >= target_val

      cols = st.columns([0.1, 0.7, 0.2])
      with cols[0]:
        checked = st.checkbox(
            "✓", value=is_done, key=f"chk_{task['id']}_{st.session_state.selected_date}"
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
            "text-decoration: line-through; color: #94a3b8;"
            if is_done
            else "color: #ffffff; font-weight: 500;"
        )
        st.markdown(
            f"<div style='font-size: 13px; {title_style}'>{task['title']}</div>"
            f"<div style='font-size: 10px; color: #64748b;'>Progress:"
            f" {current_val}/{target_val}</div>",
            unsafe_allow_html=True,
        )
      with cols[2]:
        if st.button("🗑️", key=f"del_{task['id']}"):
          st.session_state.tasks = [
              t for t in st.session_state.tasks if t["id"] != task["id"]
          ]
          st.rerun()

  st.divider()

  # Form Tambah Tugas
  with st.expander("➕ Tambah Tugas Baru"):
    with st.form("add_task_form"):
      new_title = st.text_input("Nama Tugas")
      new_target = st.number_input("Target Jumlah", min_value=1, value=1)
      new_freq = st.selectbox(
          "Frekuensi",
          ["daily", "weekly", "monthly", "specific_date"],
          format_func=lambda x: {
              "daily": "Setiap Hari",
              "weekly": "Mingguan",
              "monthly": "Bulanan",
              "specific_date": "Tanggal Spesifik",
          }[x],
      )

      extra_val = None
      if new_freq == "weekly":
        extra_val = st.selectbox(
            "Pilih Hari",
            [1, 2, 3, 4, 5, 6, 0],
            format_func=lambda x: [
                "Minggu",
                "Senin",
                "Selasa",
                "Rabu",
                "Kamis",
                "Jumat",
                "Sabtu",
            ][x],
        )
      elif new_freq == "monthly":
        extra_val = st.number_input("Tanggal (1-31)", min_value=1, max_value=31, value=1)
      elif new_freq == "specific_date":
        extra_val = st.date_input("Tanggal Spesifik").strftime("%Y-%m-%d")

      submitted = st.form_submit_button("Simpan Tugas")
      if submitted and new_title:
        new_task = {
            "id": str(datetime.now().timestamp()),
            "title": new_title,
            "target": new_target,
            "freq": new_freq,
            "extra": str(extra_val) if extra_val else None,
        }
        st.session_state.tasks.append(new_task)
        st.success("Tugas berhasil ditambahkan!")
        st.rerun()

# --- TAB 2: KALENDER ---
with tab2:
  st.subheader("📅 Agenda Kegiatan")
  cal_date = st.date_input("Pilih Tanggal Agenda", datetime.now())
  cal_date_str = cal_date.strftime("%Y-%m-%d")

  cal_tasks = [t for t in st.session_state.tasks if is_task_active(t, cal_date_str)]
  cal_prog = st.session_state.progress.get(cal_date_str, {})

  if not cal_tasks:
    st.info("Tidak ada agenda tugas pada tanggal ini.")
  else:
    for t in cal_tasks:
      cur = cal_prog.get(t["id"], 0)
      tgt = t.get("target", 1)
      done = cur >= tgt
      status_icon = "✅" if done else "⏳"
      st.markdown(
          f"- **{t['title']}** — `{cur}/{tgt}` {status_icon}", unsafe_allow_html=True
      )

# --- TAB 3: ANALITIK ---
with tab3:
  st.subheader("📊 Statistik Produktivitas")
  total_days = len(st.session_state.progress)
  all_done_count = sum(
      [
          sum(1 for k, v in day.items() if v > 0)
          for day in st.session_state.progress.values()
      ]
  )

  col_a, col_b = st.columns(2)
  with col_a:
    st.metric("Total Hari Tercatat", total_days)
  with col_b:
    st.metric("Aksi Selesai", all_done_count)

# --- TAB 4: PENGATURAN ---
with tab4:
  st.subheader("⚙️ Pengaturan Pengguna")
  new_name = st.text_input("Nama Pemilik", value=st.session_state.user_name)
  if st.button("Simpan Nama"):
    st.session_state.user_name = new_name
    st.success("Nama berhasil diperbarui!")
    st.rerun()

  st.divider()
  if st.button("🗑️ Reset Semua Data"):
    st.session_state.clear()
    st.success("Data direset!")
    st.rerun()
    
