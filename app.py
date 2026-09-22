from datetime import datetime
import json
import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="DailyTask", page_icon="📋", layout="centered"
)

# Sembunyikan Header & Footer Bawaan Streamlit
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: #0b1329;
        padding: 0rem;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inisialisasi Data Default
if "user_name" not in st.session_state:
  st.session_state.user_name = "DK"
if "tasks" not in st.session_state:
  st.session_state.tasks = [
      {"id": "1", "title": "Kasih Makan Ikan", "current": 0, "target": 1},
      {"id": "2", "title": "Up Vid Berkahlangit.id", "current": 0, "target": 2},
      {"id": "3", "title": "Upload Shopee Video", "current": 1, "target": 2},
      {"id": "4", "title": "Share link shopee", "current": 0, "target": 50},
      {"id": "5", "title": "Generate AI Video", "current": 2, "target": 2},
  ]

# HTML & CSS Presisi Mirip Gambar 2
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        body {{
            background-color: #0b1329;
            color: #ffffff;
            padding: 10px;
        }}
        
        /* Top Navigation Bar */
        .top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 5px;
            margin-bottom: 10px;
        }}
        .top-bar h2 {{
            font-size: 18px;
            font-weight: 600;
        }}
        
        /* Profile Header */
        .profile-card {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .user-greeting {{
            font-size: 16px;
            font-weight: 600;
        }}
        .user-date {{
            font-size: 11px;
            color: #64748b;
            margin-top: 2px;
        }}
        .day-tag {{
            background: #1e293b;
            border: 1px solid #334155;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 10px;
            color: #94a3b8;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .avatar {{
            width: 24px;
            height: 24px;
            background: #10b981;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
            color: #000;
        }}
        
        /* Productivity Banner */
        .prod-card {{
            background: #131d35;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 12px 15px;
            margin-bottom: 15px;
        }}
        .prod-header {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            font-weight: 700;
            color: #34d399;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        .progress-bar-bg {{
            background: #1e293b;
            height: 6px;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 8px;
        }}
        .progress-bar-fill {{
            background: #10b981;
            height: 100%;
            width: 20%;
            border-radius: 10px;
        }}
        .prod-sub {{
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #64748b;
        }}
        
        /* Days Navigation */
        .days-nav {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }}
        .day-btn {{
            flex: 1;
            text-align: center;
            padding: 8px 0;
            font-size: 11px;
            color: #64748b;
            border-radius: 8px;
            margin: 0 2px;
        }}
        .day-btn.active {{
            background: #131d35;
            border: 1px solid #10b981;
            color: #10b981;
            font-weight: 600;
        }}
        
        /* Task Item List */
        .task-list {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 15px;
        }}
        .task-item {{
            background: #131d35;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 10px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .task-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .check-circle {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid #334155;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }}
        .check-circle.completed {{
            background: #10b981;
            border-color: #10b981;
            color: #000;
            font-size: 11px;
            font-weight: bold;
        }}
        .task-title {{
            font-size: 12px;
            font-weight: 500;
            color: #e2e8f0;
        }}
        .task-right {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .counter-box {{
            background: #1e293b;
            border-radius: 6px;
            display: flex;
            align-items: center;
            padding: 2px 6px;
            font-size: 11px;
            color: #94a3b8;
            gap: 8px;
        }}
        .btn-action {{
            background: transparent;
            border: none;
            color: #64748b;
            font-size: 12px;
            cursor: pointer;
            padding: 2px 4px;
        }}
        .btn-plus {{
            background: #064e3b;
            color: #34d399;
            border-radius: 4px;
            padding: 2px 6px;
        }}
        
        /* Add Task Button */
        .add-btn {{
            width: 100%;
            background: #131d35;
            border: 1px dashed #10b981;
            color: #10b981;
            padding: 12px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
        }}
    </style>
</head>
<body>

    <!-- Top Bar -->
    <div class="top-bar">
        <h2>DailyTask</h2>
        <span style="font-size:16px;">📋</span>
    </div>

    <!-- Header Profil -->
    <div class="profile-card">
        <div>
            <div class="user-greeting">Hey, {st.session_state.user_name}! ✏️</div>
            <div class="user-date">Rabu, 23 Sep 2026</div>
        </div>
        <div class="day-tag">
            <span>Hari ke-266 dari 365</span>
            <div class="avatar">{st.session_state.user_name[:2]}</div>
        </div>
    </div>

    <!-- Banner Produktivitas -->
    <div class="prod-card">
        <div class="prod-header">
            <span>PRODUKTIVITAS RABU</span>
            <span>20%</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill"></div>
        </div>
        <div class="prod-sub">
            <span>1 dari 5 tugas selesai</span>
            <span style="color: #64748b; text-decoration: underline;">Reset Hari Ini</span>
        </div>
    </div>

    <!-- Navigasi Hari -->
    <div class="days-nav">
        <div class="day-btn">Sen</div>
        <div class="day-btn">Sel</div>
        <div class="day-btn active">Rab</div>
        <div class="day-btn">Kam</div>
        <div class="day-btn">Jum</div>
        <div class="day-btn">Sab</div>
        <div class="day-btn">Min</div>
    </div>

    <!-- Daftar Tugas (Persis Gambar 2) -->
    <div class="task-list">
        <div class="task-item">
            <div class="task-left">
                <div class="check-circle"></div>
                <div class="task-title">Kasih Makan Ikan</div>
            </div>
            <div class="task-right">
                <div class="counter-box">
                    <button class="btn-action">-</button>
                    <span>0/1</span>
                    <button class="btn-action btn-plus">+</button>
                </div>
                <button class="btn-action">✏️</button>
                <button class="btn-action">🗑️</button>
            </div>
        </div>

        <div class="task-item">
            <div class="task-left">
                <div class="check-circle"></div>
                <div class="task-title">Up Vid Berkahlangit.id</div>
            </div>
            <div class="task-right">
                <div class="counter-box">
                    <button class="btn-action">-</button>
                    <span>0/2</span>
                    <button class="btn-action btn-plus">+</button>
                </div>
                <button class="btn-action">✏️</button>
                <button class="btn-action">🗑️</button>
            </div>
        </div>

        <div class="task-item">
            <div class="task-left">
                <div class="check-circle"></div>
                <div class="task-title">Upload Shopee Video</div>
            </div>
            <div class="task-right">
                <div class="counter-box">
                    <button class="btn-action">-</button>
                    <span>1/2</span>
                    <button class="btn-action btn-plus">+</button>
                </div>
                <button class="btn-action">✏️</button>
                <button class="btn-action">🗑️</button>
            </div>
        </div>

        <div class="task-item">
            <div class="task-left">
                <div class="check-circle"></div>
                <div class="task-title">Share link shopee</div>
            </div>
            <div class="task-right">
                <div class="counter-box">
                    <button class="btn-action">-</button>
                    <span>0/50</span>
                    <button class="btn-action btn-plus">+</button>
                </div>
                <button class="btn-action">✏️</button>
                <button class="btn-action">🗑️</button>
            </div>
        </div>

        <div class="task-item">
            <div class="task-left">
                <div class="check-circle completed">✓</div>
                <div class="task-title">Generate AI Video</div>
            </div>
            <div class="task-right">
                <div class="counter-box">
                    <button class="btn-action">-</button>
                    <span>2/2</span>
                    <button class="btn-action btn-plus">+</button>
                </div>
                <button class="btn-action">✏️</button>
                <button class="btn-action">🗑️</button>
            </div>
        </div>
    </div>

    <!-- Tombol Tambah Tugas -->
    <div class="add-btn">
        + Tambah Tugas Baru
    </div>

</body>
</html>
"""

# Render Komponen HTML
components.html(html_code, height=650, scrolling=True)
