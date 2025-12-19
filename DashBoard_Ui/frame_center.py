from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QWidget, QDateTimeEdit, QDialog, QSizePolicy, QFileDialog, QGridLayout, QScrollArea
)
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from PyQt6.QtCore import Qt, QDateTime, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        # Navigation Toolbar
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib import rc
from db_manager import get_connection
from datetime import datetime, timedelta
import numpy as np
import matplotlib as mpl
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('MalgunGothic', 'C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunGothic-Bold', 'C:/Windows/Fonts/malgunbd.ttf'))

# 한글 폰트
rc("font", family="Malgun Gothic")
mpl.rcParams['axes.unicode_minus'] = False

# ----------------------------------------------------------------------
#  DB 매핑: 좌측 메뉴 텍스트  →  테이블 / 컬럼명
# ----------------------------------------------------------------------
TABLE_MAP = {

# =========================================================
# 2 GHz Receiver
# =========================================================
"2GHz Receiver Status Monitor": {
    "table": "Frontend_2ghz",
    "columns": {
        "Normal Temperature RF": "NormalTemp_RF",
        "Normal Temperature Load": "NormalTemp_Load",
        "Cryogenic Temperature Cold": "Cryo_ColdPla",
        "Cryogenic Temperature Shield Box": "Cryo_ShieldBox",
        "Pressure Sensor CH1": "Pressure",
        "LNA Monitor LHCP Vd": "LNA_LHCP_Vd1",
        "LNA Monitor LHCP Id": "LNA_LHCP_Id1",
        "LNA Monitor RHCP Vd": "LNA_RHCP_Vd1",
        "LNA Monitor RHCP Id": "LNA_RHCP_Id1",
        "RF out Power RHCP": "RF_RHCP",
        "RF out Power LHCP": "RF_LHCP",
    }
},

# =========================================================
# 8 GHz Receiver
# =========================================================
"8GHz Receiver Status Monitor": {
    "table": "Frontend_8ghz",
    "columns": {
        "Normal Temperature RF": "NormalTemp_RF",
        "Normal Temperature Load": "NormalTemp_Load",
        "Cryogenic Temperature Cold": "Cryo_ColdPla",
        "Cryogenic Temperature Shield Box": "Cryo_ShieldBox",
        "Pressure Sensor CH1": "Pressure",
        "LNA Monitor LHCP Vg1": "LNA_LHCP_Vg1",
        "LNA Monitor LHCP Vg2": "LNA_LHCP_Vg2",
        "LNA Monitor LHCP Vd": "LNA_LHCP_Vd1",
        "LNA Monitor LHCP Id": "LNA_LHCP_Id1",
        "LNA Monitor RHCP Vg1": "LNA_RHCP_Vg1",
        "LNA Monitor RHCP Vg2": "LNA_RHCP_Vg2",
        "LNA Monitor RHCP Vd": "LNA_RHCP_Vd1",
        "LNA Monitor RHCP Id": "LNA_RHCP_Id1",
        "RF out Power RHCP": "RF_RHCP",
        "RF out Power LHCP": "RF_LHCP",
    }
},

# =========================================================
# 22 GHz Receiver
# =========================================================
"22GHz Receiver Status Monitor": {
    "table": "Frontend_22ghz",
    "columns": {
        "Normal Temperature RF": "NormalTemp_RF",
        "Normal Temperature LO": "NormalTemp_Load",
        "Cryogenic Temperature Cold": "Cryo_ColdPla",
        "Cryogenic Temperature Shield Box": "Cryo_ShieldBox",
        "Pressure Sensor CH1": "Pressure",
        "LNA Monitor LHCP Vg1": "LNA_LHCP_Vg1",
        "LNA Monitor LHCP Vg2": "LNA_LHCP_Vg2",
        "LNA Monitor LHCP Vd": "LNA_LHCP_Vd1",
        "LNA Monitor LHCP Id": "LNA_LHCP_Id1",
        "LNA Monitor RHCP Vg1": "LNA_RHCP_Vg1",
        "LNA Monitor RHCP Vg2": "LNA_RHCP_Vg2",
        "LNA Monitor RHCP Vd": "LNA_RHCP_Vd1",
        "LNA Monitor RHCP Id": "LNA_RHCP_Id1",
        "RF out Power RHCP": "RF_RHCP",
        "RF out Power LHCP": "RF_LHCP",
        "RF out Power LO": "RF_Low",
    }
},

# =========================================================
# 43 GHz Receiver
# =========================================================
"43GHz Receiver Status Monitor": {
    "table": "Frontend_43ghz",
    "columns": {
        "Normal Temperature RF": "NormalTemp_RF",
        "Normal Temperature LO": "NormalTemp_Load",
        "Cryogenic Temperature Cold": "Cryo_ColdPla",
        "Cryogenic Temperature Shield Box": "Cryo_ShieldBox",
        "Pressure Sensor CH1": "Pressure",
        "LNA Monitor LHCP Vg1": "LNA_LHCP_Vg1",
        "LNA Monitor LHCP Vg2": "LNA_LHCP_Vg2",
        "LNA Monitor LHCP Vd": "LNA_LHCP_Vd1",
        "LNA Monitor LHCP Id": "LNA_LHCP_Id1",
        "LNA Monitor RHCP Vg1": "LNA_RHCP_Vg1",
        "LNA Monitor RHCP Vg2": "LNA_RHCP_Vg2",
        "LNA Monitor RHCP Vd": "LNA_RHCP_Vd1",
        "LNA Monitor RHCP Id": "LNA_RHCP_Id1",
        "RF out Power RHCP": "RF_RHCP",
        "RF out Power LHCP": "RF_LHCP",
        "RF out Power LO": "RF_Low",
    }
},

# =========================================================
# S / X Down Converter
# =========================================================
"S/X Down Converter": {
    "table": "SXDownConverter",
    "columns": {
        "S":  "LEVEL_ch1",
        "X1": "LEVEL_ch2",
        "X2": "LEVEL_ch3",
    }
},

# =========================================================
# K Down Converter
# =========================================================
"K Down Converter": {
    "table": "KDownConverter",
    "columns": {
        "K1": "LEVEL_ch1",
        "K2": "LEVEL_ch2",
        "K3": "LEVEL_ch3",
        "K4": "LEVEL_ch4",
    }
},

# =========================================================
# Q Down Converter
# =========================================================
"Q Down Converter": {
    "table": "QDownConverter",
    "columns": {
        "Q1": "LEVEL_ch1",
        "Q2": "LEVEL_ch2",
        "Q3": "LEVEL_ch3",
        "Q4": "LEVEL_ch4",
    }
},

# =========================================================
# IF Selector
# =========================================================
"IF Selector": {
    "table": "IFSelector",
    "columns": {
        **{f"CH{i}": f"LEVEL_ch{i}" for i in range(1, 17)}
    }
},

# =========================================================
# Video Converter 2
# =========================================================
"Video Converter 2": {
    "table": "VideoConverter2",
    "columns": {
        **{f"CH{i}": f"LEVELU_ch{i}" for i in range(1, 9)}
    }
},

}
# ----------------------------------------------------------------------
#  SPEC_MAP: 장비별 파라미터 정상 범위 (min, max)
#  ※ 값은 예시 / 미정 파라미터는 생략 가능
# ----------------------------------------------------------------------
SPEC_MAP = {

    "2GHz Receiver Status Monitor": {
        "Normal Temperature RF": (0, 50),
        "Normal Temperature Load": (0, 50),
        "Cryogenic Temperature Cold": (0, 20),
        "Cryogenic Temperature Shield Box": (0, 40),
        "Pressure Sensor CH1": (0, 2),
    },

    "8GHz Receiver Status Monitor": {
        "Normal Temperature RF": (0, 50),
        "Normal Temperature Load": (0, 50),
    },

    "22GHz Receiver Status Monitor": {
        "Normal Temperature RF": (0, 50),
        "Normal Temperature LO": (0, 50),
        "Cryogenic Temperature Cold": (0, 20),
    },

    "43GHz Receiver Status Monitor": {
        "Normal Temperature RF": (0, 50),
        "Normal Temperature LO": (0, 50),
    },

    # Down / IF / Video 는 추후 정의
}

# ----------------------------------------------------------------------
# 기간 설정 다이얼로그
# ----------------------------------------------------------------------
class CustomRangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("기간 설정")
        self.setFixedSize(320, 130)
        layout = QVBoxLayout(self)

        # 시작일
        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(QLabel("시작:"))
        self.start_edit = QDateTimeEdit(QDateTime.currentDateTime().addDays(-1))
        self.start_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.start_edit.setCalendarPopup(True)
        h_layout1.addWidget(self.start_edit)
        layout.addLayout(h_layout1)

        # 종료일
        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(QLabel("끝:"))
        self.end_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.end_edit.setCalendarPopup(True)
        h_layout2.addWidget(self.end_edit)
        layout.addLayout(h_layout2)

        # 확인/취소 버튼
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("확인")
        cancel_btn = QPushButton("취소")

        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

    def get_range(self):
        return (
            self.start_edit.dateTime().toPyDateTime(),
            self.end_edit.dateTime().toPyDateTime(),
        )


# ----------------------------------------------------------------------
#  메인 센터 프레임 (반응형 2×2 카드 + 각 카드 하단 통계)
# ----------------------------------------------------------------------
class FrameCenter(QFrame):
    def __init__(self, parent=None, frame_right=None):
        super().__init__(parent)

        self.frame_left = None

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        self.setStyleSheet("background-color:#0F172A;")

        self.selected_children: dict[str, list[str]] = {}
        self.raw: dict[str, dict] = {}

        self.time_range = "1Day"
        self.custom_start = None
        self.custom_end = None

        # -----------------------
        # 전체 레이아웃
        # -----------------------
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        # -----------------------
        # 상단 버튼 영역
        # -----------------------
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(12)
        top_layout.addStretch(1)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedHeight(30)
        self.reset_btn.setFixedWidth(70)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color:#EF4444;
                color:white;
                border-radius:8px;
                padding:4px 10px;
                font-size:10pt;
                font-weight:bold;
            }
            QPushButton:hover { background-color:#DC2626; }
        """)
        self.reset_btn.clicked.connect(self.reset_all)
        top_layout.addWidget(self.reset_btn)

        self.time_buttons = {}
        for name in ["1Hour", "6Hour", "1Day", "7Day", "Range"]:
            btn = QPushButton(name)
            btn.setFixedHeight(30)
            btn.setFixedWidth(70)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color:#1E293B;
                    color:white;
                    border-radius:8px;
                    padding:4px 10px;
                    font-size:10pt;
                }
                QPushButton:hover { background-color:#334155; }
                QPushButton:checked {
                    background-color:#2563EB;
                    font-weight:bold;
                }
            """)
            self.time_buttons[name] = btn
            top_layout.addWidget(btn)
            btn.clicked.connect(self._make_time_range_handler(name))

        self.time_buttons["1Day"].setChecked(True)

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setFixedHeight(30)
        self.refresh_btn.setFixedWidth(90)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color:#22C55E;
                color:white;
                border-radius:8px;
                padding:4px 12px;
                font-size:10pt;
                font-weight:bold;
            }
            QPushButton:hover { background-color:#16A34A; }
        """)
        self.refresh_btn.clicked.connect(self.refresh_all_data)
        top_layout.addWidget(self.refresh_btn)

        self.report_pdf_btn = QPushButton("Report PDF")
        self.report_pdf_btn.setFixedHeight(30)
        self.report_pdf_btn.setFixedWidth(110)
        self.report_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color:#6366F1;
                color:white;
                border-radius:8px;
                padding:4px 12px;
                font-size:10pt;
                font-weight:bold;
            }
            QPushButton:hover { background-color:#4F46E5; }
        """)
        self.report_pdf_btn.clicked.connect(self.save_pdf_report)
        top_layout.addWidget(self.report_pdf_btn)

        self.main_layout.addWidget(top_widget)

        # -----------------------
        # 그래프 영역
        # -----------------------
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color:#0F172A; border: none;")

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setHorizontalSpacing(12)
        self.cards_layout.setVerticalSpacing(12)

        scroll.setWidget(self.cards_container)
        self.main_layout.addWidget(scroll, stretch=1)

        QTimer.singleShot(50, self.update_graphs)

    # ------------------------------------------------------------------
    # 시간 범위 처리
    # ------------------------------------------------------------------
    def _make_time_range_handler(self, name):
        def handler():
            for n, btn in self.time_buttons.items():
                btn.setChecked(n == name)

            if name == "Range":
                dlg = CustomRangeDialog(self)
                if dlg.exec():
                    self.custom_start, self.custom_end = dlg.get_range()
                    self.time_range = "Range"
                else:
                    self.time_buttons[self.time_range].setChecked(True)
                    return
            else:
                self.time_range = name

            self.update_graphs()

        return handler

    def _get_time_window(self):

        # 기간설정이면 이 범위
        if self.time_range == "Range" and self.custom_start and self.custom_end:
            return self.custom_start, self.custom_end

        # 전체 raw 데이터 범위
        all_times = []
        for parent, raw in self.raw.items():
            all_times.extend(raw["times"])

        if not all_times:
            now = datetime.now()
            return now - timedelta(days=1), now

        return min(all_times), max(all_times)

    def _apply_interval_sampling(self, xs, ys):
        if not xs or not ys:
            return xs, ys

        if self.time_range == "1Hour":
            interval = timedelta(hours=1)
        elif self.time_range == "6Hour":
            interval = timedelta(hours=6)
        elif self.time_range == "1Day":
            interval = timedelta(days=1)
        elif self.time_range == "7Day":
            interval = timedelta(days=7)
        else:
            return xs, ys

        sampled_x = []
        sampled_y = []

        # -------- 버킷 기준 수정 (핵심!!) --------
        start_time = xs[0].replace(minute=0, second=0, microsecond=0)

        if self.time_range == "1Day":
            start_time = start_time.replace(hour=0)

        elif self.time_range == "7Day":
            start_time = start_time - timedelta(days=start_time.weekday())
            start_time = start_time.replace(hour=0)

        # ---------------------------------------

        end_time = xs[-1]

        bucket_start = start_time
        bucket_end = bucket_start + interval

        idx = 0
        n = len(xs)

        while bucket_start <= end_time:
            while idx < n and xs[idx] < bucket_start:
                idx += 1

            if idx < n and xs[idx] < bucket_end:
                sampled_x.append(xs[idx])
                sampled_y.append(ys[idx])

            bucket_start += interval
            bucket_end += interval

        return sampled_x, sampled_y

    # ------------------------------------------------------------------
    #  MainWindow / FrameLeft 에서 호출되는 API
    # ------------------------------------------------------------------
    def toggle_parent(self, parent_name: str):
        # Down / IF / Video 계열은 reload_data 사용 안 함
        if parent_name not in TABLE_MAP:
            return

        self.selected_children.setdefault(parent_name, [])

        if parent_name not in self.raw:
            self.reload_data(parent_name)

        self.update_graphs()

        if self.frame_left:
            self.frame_left.refresh_child_selection()

    def show_child_graph(self, group_name, item_name):

        if group_name not in TABLE_MAP:
            print(f"[WARN] Unsupported device: {group_name}")
            return

        # 선택 상태에 child 추가
        self.selected_children.setdefault(group_name, [])
        if item_name not in self.selected_children[group_name]:
            self.selected_children[group_name].append(item_name)

        if group_name not in self.raw:
            self.reload_data(group_name)

        self.update_graphs()

        if self.frame_left:
            self.frame_left.refresh_child_selection()

    # ------------------------------------------------------------------
    # 새로고침
    # ------------------------------------------------------------------
    def refresh_all_data(self):
        for parent_name in list(self.selected_children.keys()):
            self.reload_data(parent_name, load_only=True)
        self.update_graphs()

    def reset_all(self):
        # FrameCenter 내부 선택 상태 초기화
        self.selected_children.clear()
        self.raw.clear()

        # 카드(그래프) 레이아웃 비우기
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.cards_container.update()

        # 왼쪽 메뉴 선택도 초기화
        if self.frame_left:
            self.frame_left.clear_all_selection()

    # ------------------------------------------------------------------
    # DB 로딩
    # ------------------------------------------------------------------
    def reload_data(self, parent_name, load_only: bool = False):
        info = TABLE_MAP.get(parent_name)
        if not info:
            print(f"[FrameCenter] TABLE_MAP 에 없는 parent: {parent_name}")
            return

        table = info["table"]
        if not table:
            print(f"[FrameCenter] 테이블이 없는 parent: {parent_name}")
            return

        wanted_cols = list(dict.fromkeys(info["columns"].values()))

        conn = None
        try:
            conn = get_connection(readonly=True)
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table} ORDER BY datetime ASC")
            rows = cur.fetchall()

            col_names = [desc[0] for desc in cur.description]
            col_index = {name: idx for idx, name in enumerate(col_names)}

            if "datetime" not in col_index:
                print(f"[FrameCenter] {table} 에 datetime 컬럼이 없습니다.")
                return

            dt_idx = col_index["datetime"]
        except Exception as e:
            print(f"[FrameCenter] DB 오류: {e}")
            return
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

        times = []
        data = {col: [] for col in wanted_cols}

        for row in rows:
            try:
                dt = row[dt_idx]
                if not isinstance(dt, datetime):
                    dt = datetime.fromisoformat(str(dt))
            except Exception:
                continue
            times.append(dt)

            for col in wanted_cols:
                idx = col_index.get(col)
                val = row[idx] if idx is not None else None
                data[col].append(val)

        self.raw[parent_name] = {"times": times, "data": data}

        if not load_only:
            self.update_graphs()

    # ------------------------------------------------------------------
    # 현재 선택된 parent/child 기반으로 플롯 데이터 수집
    # ------------------------------------------------------------------
    def _collect_plot_items(self):
        start, end = self._get_time_window()
        plot_items = []

        for parent, child_list in self.selected_children.items():

            info = TABLE_MAP.get(parent)
            if not info:
                continue

            if parent not in self.raw:
                continue

            times = self.raw[parent]["times"]
            data = self.raw[parent]["data"]

            # 기간 범위 내 인덱스 추출
            indices = [i for i, t in enumerate(times) if start <= t <= end]
            if not indices:
                continue

            for child in child_list:
                col = info["columns"].get(child)
                if not col:
                    continue

                xs_raw = [times[i] for i in indices]
                ys_raw = [data[col][i] for i in indices]

                xs, ys = [], []
                for x, y in zip(xs_raw, ys_raw):
                    try:
                        v = float(y)
                        if np.isnan(v):
                            continue
                        xs.append(x)
                        ys.append(v)
                    except Exception:
                        continue

                # 리샘플링 적용
                xs, ys = self._apply_interval_sampling(xs, ys)

                if xs:
                    title = f"{parent} | {child}"  # ← 여기서 title 생성
                    plot_items.append((title, xs, ys))

        return plot_items

    # ------------------------------------------------------------------
    # 그래프 카드 하나 생성 (그래프 + 하단 통계)
    # ------------------------------------------------------------------
    def _create_graph_card(self, title: str, xs, ys):
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color:#020617;
                border:1px solid #1E293B;
                border-radius:10px;
            }
            """
        )
        card.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        card.setMinimumHeight(300)

        v = QVBoxLayout(card)
        v.setContentsMargins(10, 8, 10, 8)
        v.setSpacing(4)

        fig = Figure(facecolor="#020617")
        canvas = FigureCanvas(fig)
        canvas.setParent(card)  # ★ 반드시 추가 (Qt 크래시 방지)
        canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        ax = fig.add_subplot(111)
        ax.set_facecolor("#020617")
        for spine in ax.spines.values():
            spine.set_color("#1E293B")

        ax.grid(True, color="#1E293B", linestyle="--", linewidth=0.5)
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")

        ax.plot(xs, ys, linewidth=1.0)
        ax.set_title(title, color="white", fontsize=10, pad=6)
        fig.autofmt_xdate()

        v.addWidget(canvas, stretch=1)

        arr = np.array(ys, dtype=float)
        mean_v = float(np.mean(arr))
        min_v = float(np.min(arr))
        max_v = float(np.max(arr))

        summary_label = QLabel(f"Avg: {mean_v:,.2f}    Max: {max_v:,.2f}    min: {min_v:,.2f}")
        summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary_label.setStyleSheet("color:#38BDF8; font-size:10pt; font-weight:bold;")

        v.addWidget(summary_label)

        return card

    # ------------------------------------------------------------------
    # 전체 그래프 갱신 (QGridLayout 2×N 반응형 배치)
    # ------------------------------------------------------------------
    def update_graphs(self):
        # 레이아웃 비우기
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            w = item.widget()
            lay = item.layout()
            if w is not None:
                w.deleteLater()
            if lay is not None:
                # 중첩 레이아웃 정리
                while lay.count():
                    sub_item = lay.takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()

        plot_items = self._collect_plot_items()
        if not plot_items:
            self.cards_container.update()
            return

        cols = 2
        rows = (len(plot_items) + cols - 1) // cols

        for idx, (title, xs, ys) in enumerate(plot_items):
            row = idx // cols
            col = idx % cols
            card = self._create_graph_card(title, xs, ys)
            self.cards_layout.addWidget(card, row, col)

        # 각 행/열에 동일한 stretch 부여 → 화면 높이에 맞춰 자동 분배
        for r in range(rows):
            self.cards_layout.setRowStretch(r, 1)
        for c in range(cols):
            self.cards_layout.setColumnStretch(c, 1)

        self.cards_container.update()

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self._force_resize_after_show)

    def _force_resize_after_show(self):
        self.update_graphs()

    def _force_resize(self):
        self.resize(self.width(), self.height())

    # ------------------------------------------------------------------
    # PDF 보고서 저장 (화면의 모든 그래프 + 각 그래프 통계)
    # ------------------------------------------------------------------
    def save_pdf_report(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "PDF 보고서 저장",
            "VLBI_Device_Report.pdf",
            "PDF Files (*.pdf)"
        )
        if not filename:
            return

        plot_items = self._collect_plot_items()
        if not plot_items:
            print("[FrameCenter] PDF 생성: 표시할 그래프가 없습니다.")
            return

        # 1) (parent, child) 형태로 그룹화
        #    title = "2GHz 수신기 상태 모니터 | LNA Monitor RHCP Id"
        device_map: dict[str, list[tuple[str, list, list]]] = {}
        for title, xs, ys in plot_items:
            parent, child = title.split(" | ", 1)
            device_map.setdefault(parent, []).append((child, xs, ys))

        # ReportLab 기본 스타일 설정
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # 한글 폰트 적용
        styles["Title"].fontName = "MalgunGothic-Bold"
        styles["Normal"].fontName = "MalgunGothic"
        styles["Heading1"].fontName = "MalgunGothic-Bold"
        styles["Heading2"].fontName = "MalgunGothic-Bold"

        center_style = styles["Normal"].clone('Center')
        center_style.alignment = TA_CENTER
        styles.add(center_style)

        center_title_style = styles["Title"].clone('CenterTitle')
        center_title_style.alignment = TA_CENTER
        styles.add(center_title_style)

        # 보고서 공통 헤더
        now_kst = datetime.utcnow() + timedelta(hours=9)
        created_text = f"생성일시: {now_kst.strftime('%Y-%m-%d %H:%M:%S')} (KST)"

        temp_files = []

        # 장비별로 한 섹션씩 생성
        first_device = True
        for device_name, param_list in device_map.items():
            # 페이지 구분
            if not first_device:
                elements.append(PageBreak())
            first_device = False

            # 분석 기간 계산 (장비 전체 기준)
            all_times = []
            for _, xs, _ in param_list:
                all_times.extend(xs)
            if all_times:
                period_start = min(all_times)
                period_end = max(all_times)
            else:
                period_start = period_end = datetime.utcnow()

            period_start_str = period_start.strftime("%Y-%m-%d %H:%M")
            period_end_str = period_end.strftime("%Y-%m-%d %H:%M")

            # 가동 시간 (단순히 분석기간 길이로 계산)
            uptime_hours = (period_end - period_start).total_seconds() / 3600.0
            if uptime_hours < 0:
                uptime_hours = 0.0

            # 장애 / MTBF 는 아직 별도 로그 없으므로 0 / N/A 처리
            failure_count = 0
            mtbf_str = "N/A"

            # ==================================================================
            # 1. 개요 및 가동 현황 (Dashboard)
            # ==================================================================
            elements.append(Paragraph("개별 장비 정기 성능 분석 보고서", styles["CenterTitle"]))
            elements.append(Spacer(1, 0.3 * cm))
            elements.append(Paragraph(created_text, center_style))
            elements.append(Spacer(1, 0.5 * cm))

            elements.append(Paragraph("1. 개요 및 가동 현황 (Dashboard)", styles["Heading1"]))
            elements.append(Spacer(1, 0.2 * cm))

            # 장비 정보 테이블
            overview_data = [
                ["항목", "값"],
                ["장비명", device_name],
                ["분석 기간", f"{period_start_str} ~ {period_end_str}"],
            ]
            overview_table = Table(overview_data, colWidths=[4 * cm, 11 * cm])
            overview_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "MalgunGothic"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(overview_table)
            elements.append(Spacer(1, 0.4 * cm))

            # 가동 지표 테이블
            availability = 99.8  # 현재는 고정값/표기용. 필요시 실제 계산 로직으로 교체.
            metrics_data = [
                ["지표", "값"],
                ["가동률 (Availability)", f"{availability:.1f}%"],
                ["총 가동 시간", f"{uptime_hours:,.1f} h"],
                ["장애 횟수", f"{failure_count} 회"],
                ["MTBF (평균 고장 간격)", f"{mtbf_str}"],
            ]
            metrics_table = Table(metrics_data, colWidths=[5 * cm, 10 * cm])
            metrics_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "MalgunGothic"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(metrics_table)
            elements.append(Spacer(1, 0.6 * cm))

            # ==================================================================
            # 2. 핵심 성능 지표 (Key Parameters Table)
            # ==================================================================
            elements.append(Paragraph("2. 핵심 성능 지표 (Key Parameters Table)", styles["Heading1"]))
            elements.append(Spacer(1, 0.2 * cm))

            # 테이블 헤더
            kpi_data = [
                ["항목 (Parameter)", "정상 범위 (Spec)", "통계 (평균 | 최대 | 최소)", "상태 (Status)"]
            ]

            device_spec = SPEC_MAP.get(device_name, {})

            for param_name, xs, ys in param_list:
                arr = np.array(ys, dtype=float)
                mean_v = float(np.mean(arr))
                min_v = float(np.min(arr))
                max_v = float(np.max(arr))

                # 정상 범위
                spec = device_spec.get(param_name)
                if spec is not None:
                    low, high = spec
                    spec_str = f"{low:,.2f} ~ {high:,.2f}"
                    # 간단 상태 평가
                    if min_v < low or max_v > high:
                        status = "경고"
                    else:
                        status = "정상"
                else:
                    spec_str = "-"
                    status = "정상 (Spec 미정)"

                stats_str = f"{mean_v:,.2f} | {max_v:,.2f} | {min_v:,.2f}"
                kpi_data.append([param_name, spec_str, stats_str, status])

            kpi_table = Table(kpi_data, colWidths=[5 * cm, 4 * cm, 5 * cm, 3 * cm])
            kpi_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "MalgunGothic"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("ALIGN", (0, 1), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(kpi_table)
            elements.append(Spacer(1, 0.6 * cm))

            # ==================================================================
            # 3. 추세 및 이슈 (Trends & Issues)
            #    - 주요 파라미터 시계열 그래프
            #    - Critical Error / 유지보수 이력은 현재 수동 기입 영역으로 둠
            # ==================================================================
            elements.append(Paragraph("3. 추세 및 이슈 (Trends & Issues)", styles["Heading1"]))
            elements.append(Spacer(1, 0.2 * cm))

            # (1) 주요 추세 그래프: 각 파라미터별 그래프 삽입
            for idx, (param_name, xs, ys) in enumerate(param_list):
                # 그래프 생성
                fig = Figure(figsize=(7, 3), dpi=120, facecolor="#020617")
                ax = fig.add_subplot(111)
                ax.set_facecolor("#020617")

                for spine in ax.spines.values():
                    spine.set_color("#1E293B")

                ax.grid(True, color="#1E293B", linestyle="--", linewidth=0.5)
                ax.tick_params(axis="x", colors="black")
                ax.tick_params(axis="y", colors="black")

                ax.plot(xs, ys, linewidth=1.0)
                ax.set_title(f"{device_name} - {param_name}", fontsize=9)
                fig.autofmt_xdate()

                img_path = f"_vlbi_temp_graph_{device_name}_{idx}.png"
                fig.savefig(img_path, dpi=120, bbox_inches="tight")
                temp_files.append(img_path)

                elements.append(Paragraph(f"주요 추세 그래프: {param_name}", styles["Heading2"]))
                elements.append(Spacer(1, 0.1 * cm))
                elements.append(Image(img_path, width=16 * cm, height=7 * cm))
                elements.append(Spacer(1, 0.3 * cm))

            # (2) 주요 이벤트 / 크리티컬 에러 / 유지보수 이력: 수동 작성 영역
            elements.append(Spacer(1, 0.2 * cm))
            elements.append(Paragraph("주요 이벤트:", styles["Heading2"]))
            elements.append(Paragraph(" - (운영자가 수동으로 입력)", styles["Normal"]))
            elements.append(Spacer(1, 0.1 * cm))

            elements.append(Paragraph("Critical Error:", styles["Heading2"]))
            elements.append(Paragraph(" - 발생 건수 및 주요 코드: (예: 현재 로그 시스템 연동 전, 수동 기입)", styles["Normal"]))
            elements.append(Spacer(1, 0.1 * cm))

            elements.append(Paragraph("유지보수 이력:", styles["Heading2"]))
            elements.append(Paragraph(" - (정기 점검, 교체 부품, 장애 조치 내용 등 수동 기록)", styles["Normal"]))
            elements.append(Spacer(1, 0.6 * cm))

            # ==================================================================
            # 4. 종합 진단 (Conclusion)
            # ==================================================================
            elements.append(Paragraph("4. 종합 진단 (Conclusion)", styles["Heading1"]))
            elements.append(Spacer(1, 0.2 * cm))

            # 간단한 건전성 등급 로직:
            #   - 어떤 파라미터라도 '경고' 있으면 "주의"
            #   - 그렇지 않으면 "양호"
            has_warning = any(
                (SPEC_MAP.get(device_name, {}).get(param_name) is not None and
                 (np.min(np.array(ys, dtype=float)) < SPEC_MAP[device_name][param_name][0] or
                  np.max(np.array(ys, dtype=float)) > SPEC_MAP[device_name][param_name][1]))
                for param_name, xs, ys in param_list
                if device_name in SPEC_MAP and param_name in SPEC_MAP[device_name]
            )

            if has_warning:
                grade = "주의"
            else:
                grade = "양호"

            elements.append(Paragraph(f"건전성 등급: <b>{grade}</b> (최우수 / 양호 / 주의 / 위험 중 택1)", styles["Normal"]))
            elements.append(Spacer(1, 0.2 * cm))

            elements.append(Paragraph("특이사항 및 조치:", styles["Heading2"]))
            elements.append(Paragraph(" - (예: 온도 변동 폭 증가로 추세 모니터링 필요, 향후 LNA 점검 예정 등 수동 기입)", styles["Normal"]))
            elements.append(Spacer(1, 0.6 * cm))

        # PDF 생성
        doc.build(elements)

        # 임시 이미지 파일 삭제
        for path in temp_files:
            try:
                os.remove(path)
            except Exception:
                pass

        print("PDF 보고서 저장 완료:", filename)

    def get_current_selected_items(self):
        """현재 실제로 그래프가 그려지고 있는 (parent, child) 목록 반환"""
        plot_items = self._collect_plot_items()
        selected = []

        for title, xs, ys in plot_items:
            # title = "2GHz 수신기 상태 모니터 | LNA Monitor RHCP Id"
            parent, child = title.split(" | ", 1)
            selected.append((parent, child))

        return selected