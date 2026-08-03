import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile
import os
import calendar
from fpdf import FPDF
from datetime import timedelta

# ==========================================
# 0. CONFIGURACIÓN Y CONSTANTES
# ==========================================
st.set_page_config(page_title="Reportes | Grupo Fumiscor", layout="wide", page_icon="📊")

CONFIG_PLANTAS = {
    "FUMISCOR": {
        "maquinas": {
            "P-023": "GME-04 - PRENSA PROGRESIVA", "P-024": "GME-04 - PRENSA PROGRESIVA", "P-025": "GME-04 - PRENSA PROGRESIVA", "P-026": "GME-04 - PRENSA PROGRESIVA",
            "P-027": "PRENSAS PROGRESIVAS GRANDES", "P-028": "PRENSAS PROGRESIVAS GRANDES", "P-029": "PRENSAS PROGRESIVAS GRANDES", "P-030": "PRENSAS PROGRESIVAS GRANDES",
            "BAL-002": "GME-01 - BALANCIN", "BAL-003": "GME-01 - BALANCIN", "BAL-005": "GME-01 - BALANCIN", "BAL-006": "GME-01 - BALANCIN", "BAL-007": "GME-01 - BALANCIN", "BAL-008": "GME-01 - BALANCIN", "BAL-009": "GME-01 - BALANCIN", "BAL-010": "GME-01 - BALANCIN", "BAL-011": "GME-01 - BALANCIN", "BAL-012": "GME-01 - BALANCIN", "BAL-013": "GME-01 - BALANCIN", "BAL-014": "GME-01 - BALANCIN", "BAL-015": "GME-01 - BALANCIN",
            "P-011": "GME-02 - PRENSA HIDRAULICA", "P-012": "GME-02 - PRENSA HIDRAULICA", "P-013": "GME-02 - PRENSA HIDRAULICA", "P-014": "GME-02 - PRENSA HIDRAULICA", "P-016": "GME-02 - PRENSA HIDRAULICA", "P-017": "GME-02 - PRENSA HIDRAULICA", "P-018": "GME-02 - PRENSA HIDRAULICA", 
            "P-015": "GME-03 - PRENSA MECANICA", "P-019": "GME-03 - PRENSA MECANICA", "P-020": "GME-03 - PRENSA MECANICA", "P-021": "GME-03 - PRENSA MECANICA", "P-022": "GME-03 - PRENSA MECANICA", "GOF01": "GME-03 - PRENSA MECANICA",
            "SOP-003": "GMS-02 - PRP", "SOP-005": "GMS-02 - PRP", "SOP-008": "GMS-02 - PRP", "SOP-009": "GMS-02 - PRP", "SOP-010": "GMS-02 - PRP", "SOP-017": "GMS-02 - PRP", "SOP-018": "GMS-02 - PRP", "SOP-019": "GMS-02 - PRP", "SOP-020": "GMS-02 - PRP", "SOP-022": "GMS-02 - PRP", "SOP-023": "GMS-02 - PRP", "SOP-024": "GMS-02 - PRP", "SOP-025": "GMS-02 - PRP", "SOP-026": "GMS-02 - PRP", "SOP-027": "GMS-02 - PRP", "SOP-028": "GMS-02 - PRP", "SOP-029": "GMS-02 - PRP", "SOP-030": "GMS-02 - PRP",
            "DOB-001": "GME-05 - DOBLADORA", "DOB-01": "GME-05 - DOBLADORA", "DOB-002": "GME-05 - DOBLADORA", "DOB-003": "GME-05 - DOBLADORA", "DOB-004": "GME-05 - DOBLADORA", "DOB-005": "GME-05 - DOBLADORA", "DOB-006": "GME-05 - DOBLADORA", "DOB-007": "GME-05 - DOBLADORA", "DOB-008": "GME-05 - DOBLADORA", "DOB-009": "GME-05 - DOBLADORA", "DOB-010": "GME-05 - DOBLADORA",
            "Celda 01 Fumis": "CELDAS NUEVAS", "Celda 02 Fumis": "CELDAS NUEVAS", "Celda 03 Fumis": "CELDAS NUEVAS", "Celda 04 Fumis": "CELDAS NUEVAS", "Celda 05 Fumis": "CELDAS NUEVAS", "Celda 06 Fumis": "CELDAS NUEVAS", "Celda 07 Fumis": "CELDAS NUEVAS", "Celda 08 Fumis": "CELDAS NUEVAS", "Celda 09 Fumis": "CELDAS NUEVAS", "Celda 10 Fumis": "CELDAS NUEVAS", "Celda 11 Fumis": "CELDAS NUEVAS", "Celda 12 Fumis": "CELDAS NUEVAS", "Celda 13 Fumis": "CELDAS NUEVAS", "Celda 14 Fumis": "CELDAS NUEVAS", "Celda 15 Fumis": "CELDAS NUEVAS",
            "Cel1 - Rob13 - RUEDA AUX.": "GMS-01 - ROBOT", "Cel2 - Rob1 - ALMOHADON": "GMS-01 - ROBOT", "Cel3 - Rob14 - HANGERS": "GMS-01 - ROBOT", "Cel4 - Rob6 - DOB TORCHA": "GMS-01 - ROBOT", "Cel5 - Rob4 - Respaldo 60/40": "GMS-01 - ROBOT", "HANGERS NISSAN": "GMS-01 - ROBOT"
        },
        "grupos_estampado": ['CORTADORA LASER', 'GME-01 - BALANCIN', 'GME-02 - PRENSA HIDRAULICA', 'GME-03 - PRENSA MECANICA', 'GME-04 - PRENSA PROGRESIVA', 'PRENSAS PROGRESIVAS GRANDES'],
        "grupos_soldadura": ['GME-05 - DOBLADORA', 'GMS-01 - ROBOT', 'GMS-02 - PRP', 'GMS-03 - COLGANTE', 'GMS-03 - SOLDADORA MANUAL', 'CELDAS NUEVAS']
    },
    "FAMMA": {
        "maquinas": {
            "LINEA 1.2": "LINEA 1.2", "LINEA 1.4": "LINEA 1.4", "LINEA 1.5": "LINEA 1.5", "LINEA 2": "LINEA 2", "LINEA 3": "LINEA 3", "LINEA 4": "LINEA 4",
            "Cell 1 Famma": "CELDAS", "Cell 2 Famma": "CELDAS", "Cell 3 Famma": "CELDAS", "Cell 4 Famma": "CELDAS", "Cell 5 Famma": "CELDAS", "Cell 6 Famma": "CELDAS", "Cell 7 Famma": "CELDAS", "Cell 8 Famma": "CELDAS", "Cell 9 Famma": "CELDAS", "Cell 10 Famma": "CELDAS", "Cell 11 Famma": "CELDAS", "Cell 12 Famma": "CELDAS", "Cell 13 Famma": "CELDAS", "Cell 14 Famma": "CELDAS", "Cell 15A Famma": "CELDAS", "Cell 15B Famma": "CELDAS", "Cell 16 Famma": "CELDAS", "Cell 17 Famma": "CELDAS",
            "PRP 1": "PRP", "PRP 2": "PRP", "PRP 3": "PRP", "PRP 4": "PRP", "PRP 5": "PRP", "PRP 6": "PRP", "MIG 1": "MIG", "MIG 2": "MIG"
        },
        "grupos_estampado": ['LINEA 1.2', 'LINEA 1.4', 'LINEA 1.5', 'LINEA 2', 'LINEA 3', 'LINEA 4'],
        "grupos_soldadura": ['CELDAS', 'PRP', 'MIG']
    }
}

MESES_MAP = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}

# ==========================================
# 1. CLASE PDF Y UTILIDADES
# ==========================================
class ReportePDF(FPDF):
    def __init__(self, area, fecha_str, theme_color):
        super().__init__()
        self.area = area; self.fecha_str = fecha_str; self.theme_color = theme_color

    def add_gradient_background(self):
        r1, g1, b1 = 240, 242, 246; r2, g2, b2 = 215, 220, 225
        for i in range(int(self.h * 2)):
            ratio = i / (self.h * 2)
            self.set_fill_color(int(r1 + (r2 - r1) * ratio), int(g1 + (g2 - g1) * ratio), int(b1 + (b2 - b1) * ratio))
            self.rect(0, i / 2, self.w, 0.5, 'F')

    def rounded_rect(self, x, y, w, h, r, style=''):
        k = self.k; hp = self.h
        op = 'f' if style == 'F' else 'B' if style in ['FD', 'DF'] else 'S'
        MyArc = 4/3 * ((2 ** 0.5) - 1)
        self._out(f'{(x + r) * k:.2f} {(hp - y) * k:.2f} m')
        xc = x + w - r; yc = y + r
        self._out(f'{xc * k:.2f} {(hp - y) * k:.2f} l')
        self._out(f'{(xc + r * MyArc) * k:.2f} {(hp - y) * k:.2f} {(x + w) * k:.2f} {(hp - yc + r * MyArc) * k:.2f} {(x + w) * k:.2f} {(hp - yc) * k:.2f} c')
        yc = y + h - r
        self._out(f'{(x + w) * k:.2f} {(hp - yc) * k:.2f} l')
        self._out(f'{(x + w) * k:.2f} {(hp - yc - r * MyArc) * k:.2f} {(xc + r * MyArc) * k:.2f} {(hp - y - h) * k:.2f} {xc * k:.2f} {(hp - y - h) * k:.2f} c')
        xc = x + r
        self._out(f'{xc * k:.2f} {(hp - y - h) * k:.2f} l')
        self._out(f'{(xc - r * MyArc) * k:.2f} {(hp - y - h) * k:.2f} {x * k:.2f} {(hp - yc - r * MyArc) * k:.2f} {x * k:.2f} {(hp - yc) * k:.2f} c')
        yc = y + r
        self._out(f'{x * k:.2f} {(hp - yc) * k:.2f} l')
        self._out(f'{x * k:.2f} {(hp - yc + r * MyArc) * k:.2f} {(xc - r * MyArc) * k:.2f} {(hp - y) * k:.2f} {xc * k:.2f} {(hp - y) * k:.2f} c')
        self._out(op)

    def draw_panel(self, x, y, w, h, r=3, bg_color=(255,255,255)):
        self.set_fill_color(210, 210, 210); self.rounded_rect(x + 1.5, y + 1.5, w, h, r, style='F')
        self.set_fill_color(*bg_color); self.set_draw_color(180, 180, 180); self.rounded_rect(x, y, w, h, r, style='DF')

    def draw_kpi_panel(self, x, y, w, h, r=3, bg_color=None):
        bg = bg_color if bg_color else self.theme_color
        self.set_fill_color(200, 200, 200); self.rounded_rect(x + 1.5, y + 1.5, w, h, r, style='F')
        self.set_fill_color(*bg); self.rounded_rect(x, y, w, h, r, style='F')

def clean_text(text):
    if pd.isna(text): return "-"
    return str(text).replace('•', '-').replace('➤', '>').encode('latin-1', 'replace').decode('latin-1')

def render_and_insert_chart(fig, pdf, x, y, w, h_fig=300):
    fig.update_layout(width=600, height=h_fig, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        fig.write_image(tmp.name, engine="kaleido", scale=2.5)
        tmp_path = tmp.name
    try:
        pdf.image(tmp_path, x, y, w)
    finally:
        if os.path.exists(tmp_path): os.remove(tmp_path)

def generate_empty_schemas():
    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# ==========================================
# 2. OBTENCIÓN DE DATOS (SQL)
# ==========================================
@st.cache_data(ttl=300, show_spinner=False)
def fetch_data_from_db(planta, fecha_ini, fecha_fin, mes, anio):
    try:
        conn_name = "fumiscor" if planta == "FUMISCOR" else "famma"
        conn = st.connection(conn_name, type="sql")
        ini_str = fecha_ini.strftime('%Y-%m-%d 00:00:00')
        fin_str = fecha_fin.strftime('%Y-%m-%d 23:59:59')
        
        if planta == "FUMISCOR":
            q_metrics = f"SELECT c.Name as Máquina, SUM(COALESCE(p.Good, 0)) as Buenas, SUM(COALESCE(p.Rework, 0)) as Retrabajo, SUM(COALESCE(p.Scrap, 0)) as Observadas, SUM(COALESCE(p.ProductiveTime, 0)) as T_Operativo, SUM(COALESCE(p.DownTime, 0)) as T_Parada, SUM(COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0)) as T_Planificado, SUM(COALESCE(p.Performance, 0) * COALESCE(p.ProductiveTime, 0)) as Perf_Num, SUM(COALESCE(p.Availability, 0) * (COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0))) as Disp_Num, SUM(COALESCE(p.Quality, 0) * (COALESCE(p.Good, 0) + COALESCE(p.Rework, 0) + COALESCE(p.Scrap, 0))) as Cal_Num, SUM(COALESCE(p.Oee, 0) * (COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0))) as OEE_Num FROM PROD_M_03 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month = {mes} GROUP BY c.Name"
            q_event = f"SELECT c.Name as Máquina, e.Interval as [Tiempo (Min)], t1.Name as [Nivel Evento 1], t2.Name as [Nivel Evento 2], t3.Name as [Nivel Evento 3], t4.Name as [Nivel Evento 4] FROM EVENT_01 e LEFT JOIN CELL c ON e.CellId = c.CellId LEFT JOIN EVENTTYPE t1 ON e.EventTypeLevel1 = t1.EventTypeId LEFT JOIN EVENTTYPE t2 ON e.EventTypeLevel2 = t2.EventTypeId LEFT JOIN EVENTTYPE t3 ON e.EventTypeLevel3 = t3.EventTypeId LEFT JOIN EVENTTYPE t4 ON e.EventTypeLevel4 = t4.EventTypeId WHERE e.Date BETWEEN '{ini_str}' AND '{fin_str}'"
            q_piezas = f"SELECT c.Name as Máquina, COALESCE(pr.Code, 'S/C') as Pieza, SUM(COALESCE(p.Scrap, 0)) as Scrap, SUM(COALESCE(p.Rework, 0)) as RT FROM PROD_M_01 p JOIN CELL c ON p.CellId = c.CellId LEFT JOIN PRODUCT pr ON p.ProductId = pr.ProductId WHERE p.Year = {anio} AND p.Month = {mes} GROUP BY c.Name, pr.Code"
            q_trend_oee = f"SELECT p.Month, c.Name as Máquina, SUM(COALESCE(p.ProductiveTime, 0)) as T_Operativo, SUM(COALESCE(p.DownTime, 0)) as T_Parada, SUM(COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0)) as T_Planificado, SUM(COALESCE(p.Performance, 0) * COALESCE(p.ProductiveTime, 0)) as Perf_Num, SUM(COALESCE(p.Availability, 0) * (COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0))) as Disp_Num, SUM(COALESCE(p.Quality, 0) * (COALESCE(p.Good, 0) + COALESCE(p.Rework, 0) + COALESCE(p.Scrap, 0))) as Cal_Num, SUM(COALESCE(p.Oee, 0) * (COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0))) as OEE_Num FROM PROD_M_03 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month <= {mes} GROUP BY p.Month, c.Name"
            q_trend_pcs = f"SELECT p.Month, c.Name as Máquina, SUM(COALESCE(p.Good, 0)) as Buenas, SUM(COALESCE(p.Rework, 0)) as Retrabajo, SUM(COALESCE(p.Scrap, 0)) as Observadas, SUM(COALESCE(p.Good, 0) + COALESCE(p.Rework, 0) + COALESCE(p.Scrap, 0)) as Totales FROM PROD_M_03 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month <= {mes} GROUP BY p.Month, c.Name"
            q_m06 = f"SELECT 'GLOBAL' as Nivel, 'GLOBAL' as Grupo, Performance, Availability as Disp, Quality as Cal, Oee FROM PROD_M_06 WHERE Year = {anio} AND Month = {mes}"
            q_m05 = f"SELECT 'FABRICA' as Nivel, UPPER(f.Name) as Grupo, p.Performance, p.Availability as Disp, p.Quality as Cal, p.Oee FROM PROD_M_05 p JOIN FACTORY f ON p.FactoryId = f.FactoryId WHERE p.Year = {anio} AND p.Month = {mes}"
            q_m04 = f"SELECT 'LINEA' as Nivel, UPPER(l.Name) as Grupo, p.Performance, p.Availability as Disp, p.Quality as Cal, p.Oee FROM PROD_M_04 p JOIN LINE l ON p.LineId = l.LineId WHERE p.Year = {anio} AND p.Month = {mes}"
            
            df_m = conn.query(q_metrics).fillna(0)
            df_r = conn.query(q_event)
            df_p = conn.query(q_piezas).fillna(0)
            t_oee = conn.query(q_trend_oee).fillna(0)
            t_pcs = conn.query(q_trend_pcs).fillna(0)
            df_t = pd.merge(t_pcs, t_oee, on=['Month', 'Máquina'], how='outer').fillna(0) if not t_pcs.empty else t_oee
            df_o = pd.concat([conn.query(q_m06).fillna(0), conn.query(q_m05).fillna(0), conn.query(q_m04).fillna(0)], ignore_index=True)
            
            if not df_r.empty:
                df_r['Tiempo (Min)'] = pd.to_numeric(df_r['Tiempo (Min)'], errors='coerce').fillna(0)
                
                # LIMPIEZA AGRESIVA DE NANs
                for c in ['Nivel Evento 1', 'Nivel Evento 2', 'Nivel Evento 3', 'Nivel Evento 4']:
                    df_r[c] = df_r[c].astype(str).replace(['nan', 'None', 'NaN'], '').str.strip()

                mask = (df_r['Nivel Evento 1'].str.upper().str.contains('PROYECTO') | df_r['Nivel Evento 2'].str.upper().str.contains('PROYECTO'))
                df_r = df_r[~mask].copy()
                df_r['Estado_Global'] = df_r.apply(lambda r: 'Producción' if 'PRODUC' in str(r.get('Nivel Evento 1','')).upper() else ('Parada Programada' if 'PARADA' in str(r.get('Nivel Evento 1','')).upper() else 'Falla/Gestión'), axis=1)
                
                def get_cat(r):
                    n1 = str(r.get('Nivel Evento 1', '')).upper()
                    n2 = str(r.get('Nivel Evento 2', '')).title()
                    if 'GESTION' in n1 or 'GESTIÓN' in n1: return 'Gestión'
                    if 'FALLA' in n1: return n2 if n2 else 'Otra Falla'
                    return n1.title() if n1 else 'Sin Categoría'
                df_r['Categoria_Macro'] = df_r.apply(get_cat, axis=1)
                
                def get_det(r):
                    for lvl in ['Nivel Evento 4', 'Nivel Evento 3', 'Nivel Evento 2', 'Nivel Evento 1']:
                        if r.get(lvl): return r[lvl]
                    return 'Sin Detalle'
                df_r['Detalle_Final'] = df_r.apply(get_det, axis=1)

            return df_m, df_r, df_t, df_p, df_o, pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        else: # FAMMA
            q_oee_m = f"SELECT c.Name as Máquina, p.Performance as Perf_Num, p.Availability as Disp_Num, p.Quality as Cal_Num, p.Oee as OEE_Num, COALESCE(p.ProductiveTime, 0) as T_Operativo, (COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0)) as T_Planificado FROM PROD_M_03 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month = {mes}"
            q_pcs_m = f"SELECT c.Name as Máquina, SUM(COALESCE(p.Good, 0)) as Buenas, SUM(COALESCE(p.Rework, 0)) as Retrabajo, SUM(COALESCE(p.Scrap, 0)) as Observadas FROM PROD_M_01 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month = {mes} GROUP BY c.Name"
            df_m = pd.merge(conn.query(q_oee_m).fillna(0), conn.query(q_pcs_m).fillna(0), on='Máquina', how='outer').fillna(0)

            df_p = conn.query(f"SELECT c.Name as Máquina, COALESCE(pr.Code, 'S/C') as Pieza, SUM(COALESCE(p.Scrap, 0)) as Scrap, SUM(COALESCE(p.Rework, 0)) as RT FROM PROD_M_01 p JOIN CELL c ON p.CellId = c.CellId LEFT JOIN PRODUCT pr ON p.ProductId = pr.ProductId WHERE p.Year = {anio} AND p.Month = {mes} GROUP BY c.Name, pr.Code").fillna(0)
            
            t_oee = conn.query(f"SELECT p.Month, c.Name as Máquina, p.Performance as Perf_Num, p.Availability as Disp_Num, p.Quality as Cal_Num, p.Oee as OEE_Num, COALESCE(p.ProductiveTime, 0) as T_Operativo, (COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0)) as T_Planificado FROM PROD_M_03 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month <= {mes}").fillna(0)
            t_pcs = conn.query(f"SELECT p.Month, c.Name as Máquina, SUM(COALESCE(p.Good, 0)) as Buenas, SUM(COALESCE(p.Rework, 0)) as Retrabajo, SUM(COALESCE(p.Scrap, 0)) as Observadas, SUM(COALESCE(p.Good, 0) + COALESCE(p.Rework, 0) + COALESCE(p.Scrap, 0)) as Totales FROM PROD_M_01 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month <= {mes} GROUP BY p.Month, c.Name").fillna(0)
            df_t = pd.merge(t_pcs, t_oee, on=['Month', 'Máquina'], how='outer').fillna(0)
            
            q_ev = f"SELECT c.Name as Máquina, e.Interval as [Tiempo (Min)], t1.Name as [Nivel Evento 1], t2.Name as [Nivel Evento 2], t3.Name as [Nivel Evento 3], t4.Name as [Nivel Evento 4], t5.Name as [Nivel Evento 5], t6.Name as [Nivel Evento 6] FROM EVENT_01 e JOIN CELL c ON e.CellId = c.CellId LEFT JOIN EVENTTYPE t1 ON e.EventTypeLevel1 = t1.EventTypeId LEFT JOIN EVENTTYPE t2 ON e.EventTypeLevel2 = t2.EventTypeId LEFT JOIN EVENTTYPE t3 ON e.EventTypeLevel3 = t3.EventTypeId LEFT JOIN EVENTTYPE t4 ON e.EventTypeLevel4 = t4.EventTypeId LEFT JOIN EVENTTYPE t5 ON e.EventTypeLevel5 = t5.EventTypeId LEFT JOIN EVENTTYPE t6 ON e.EventTypeLevel6 = t6.EventTypeId WHERE e.Date BETWEEN '{ini_str}' AND '{fin_str}'"
            df_r = conn.query(q_ev)
            
            if not df_r.empty:
                for i in range(1, 7):
                    c = f'Nivel Evento {i}'
                    if c in df_r.columns: df_r[c] = df_r[c].astype(str).replace(['nan', 'None', 'NaN'], '').str.strip()

                def parse_ev(row):
                    n = [str(row.get(f'Nivel Evento {i}', '')).strip().upper() for i in range(1, 7)]
                    v = [x for x in n if x and x not in ['NONE', 'NAN', 'NULL']]
                    if not v: return 'Falla/Gestión', 'Otra', 'Sin detalle'
                    txt = " > ".join(v)
                    est = 'Falla/Gestión'
                    if any(x in txt for x in ['BAÑO', 'REFRIGERIO', 'DESCANSO']): est = 'Descanso'
                    elif any(x in txt for x in ['PARADA PROGRAMADA', 'SMED']): est = 'Parada Programada'
                    elif 'PRODUCCION' in v[0]: est = 'Producción'
                    mac = 'Otra Falla/Gestión'
                    areas = {'MANTENIMIENTO': 'Mantenimiento', 'MATRICERIA': 'Matricería', 'GESTION': 'Gestión', 'CALIDAD': 'Calidad'}
                    for ev in reversed(v):
                        for k, a in areas.items():
                            if k in ev: mac = a; break
                        if mac != 'Otra Falla/Gestión': break
                    return est, mac, f"[{mac.upper()}] {v[-1]}" if mac != 'Otra Falla/Gestión' else v[-1]
                df_r[['Estado_Global', 'Categoria_Macro', 'Detalle_Final']] = df_r.apply(lambda r: pd.Series(parse_ev(r)), axis=1)

            q_m06 = f"SELECT 'GLOBAL' as Nivel, 'GLOBAL' as Grupo, Performance, Availability as Disp, Quality as Cal, Oee FROM PROD_M_06 WHERE Year = {anio} AND Month = {mes}"
            q_m05 = f"SELECT 'FABRICA' as Nivel, UPPER(Factory) as Grupo, Performance, Availability as Disp, Quality as Cal, Oee FROM PROD_M_05 WHERE Year = {anio} AND Month = {mes}"
            q_m04 = f"SELECT 'LINEA' as Nivel, UPPER(Line) as Grupo, Performance, Availability as Disp, Quality as Cal, Oee FROM PROD_M_04 WHERE Year = {anio} AND Month = {mes}"
            df_o = pd.concat([conn.query(q_m06).fillna(0), conn.query(q_m05).fillna(0), conn.query(q_m04).fillna(0)], ignore_index=True)
            
            df_t_04 = conn.query(f"SELECT Month, Line as Planta_Linea, Oee as OEE_Num, Performance as Perf_Num, Availability as Disp_Num, Quality as Cal_Num FROM PROD_M_04 WHERE Year = {anio} AND Month <= {mes}").fillna(0)
            df_t_05 = conn.query(f"SELECT Month, Factory as Planta, Oee as OEE_Num, Performance as Perf_Num, Availability as Disp_Num, Quality as Cal_Num FROM PROD_M_05 WHERE Year = {anio} AND Month <= {mes}").fillna(0)
            df_t_06 = conn.query(f"SELECT Month, Oee as OEE_Num, Performance as Perf_Num, Availability as Disp_Num, Quality as Cal_Num FROM PROD_M_06 WHERE Year = {anio} AND Month <= {mes}").fillna(0)

            return df_m, df_r, df_t, df_p, df_o, df_t_04, df_t_05, df_t_06
    except Exception as e:
        st.error(f"Error conectando a SQL ({planta}): {str(e)}")
        return generate_empty_schemas()

# ==========================================
# 3. CONVERSORES Y MOTORES DE PDF
# ==========================================
def run_pdf_oee(planta, area, label_rep, df_kpi, df_trend, df_fallos, conf):
    theme_color = (15, 76, 129) if area.upper() == "ESTAMPADO" else ((211, 84, 0) if area.upper() == "SOLDADURA" else (40, 40, 40))
    grupos = conf["grupos_estampado"] if area.upper() == "ESTAMPADO" else (conf["grupos_soldadura"] if area.upper() == "SOLDADURA" else conf["grupos_estampado"] + conf["grupos_soldadura"])
    
    pdf = ReportePDF(f"GESTIÓN A LA VISTA - {area}", label_rep, theme_color)
    paginas = ['GLOBAL'] if area.upper() == "GLOBAL" else [area.upper()] + [g for g in grupos if g in df_kpi['Grupo'].unique()]

    for target in paginas:
        pdf.add_page(orientation='L'); pdf.set_auto_page_break(False); pdf.add_gradient_background()
        
        pdf.set_y(10); pdf.set_fill_color(*theme_color); pdf.set_text_color(255); pdf.set_font("Arial", 'B', 10)
        pdf.cell(40, 6, "PERIODO", 1, 0, 'C', True)
        pdf.cell(197, 6, f"PLANTA {area.upper()} - {target if target not in ['GLOBAL', area.upper()] else 'GENERAL'}", 1, 0, 'C', True)
        pdf.cell(40, 6, "INFORME", 1, 1, 'C', True)
        pdf.set_fill_color(255, 255, 255); pdf.set_text_color(0); pdf.set_font("Arial", '', 10)
        pdf.cell(40, 6, label_rep, 1, 0, 'C', True); pdf.cell(197, 6, f"EMPRESA: {planta}", 1, 0, 'C', True); pdf.cell(40, 6, "DISPONIBILIDAD", 1, 1, 'C', True)

        row = df_kpi[df_kpi['Grupo'] == target]
        v_oee = row['Oee'].values[0] / 100 if not row.empty else 0
        v_perf = row['Performance'].values[0] / 100 if not row.empty else 0
        v_disp = row['Disp'].values[0] / 100 if not row.empty else 0
        v_cal = row['Cal'].values[0] / 100 if not row.empty else 0

        kpis = {"OEE": (v_oee, 0.75), "PERFORMANCE": (v_perf, 0.90), "DISPONIBILIDAD": (v_disp, 0.88), "CALIDAD": (v_cal, 0.95)}
        for i, (lbl, (v, obj)) in enumerate(kpis.items()):
            bg = (46, 204, 113) if v >= obj else (231, 76, 60)
            pdf.draw_kpi_panel(x := 10 + (i * 68.5), 25, 65, 20, bg_color=bg)
            pdf.set_xy(x, 27); pdf.set_font("Arial", 'B', 10); pdf.set_text_color(255); pdf.cell(65, 6, lbl, 0, 1, 'L')
            pdf.set_xy(x, 33); pdf.set_font("Arial", 'B', 20); pdf.cell(65, 10, f"{v*100:.1f}%", 0, 0, 'C')
        pdf.set_text_color(0)

        df_g_trend = df_trend[df_trend['Grupo'] == target].sort_values('Mes')
        
        def add_trend_chart(col, title, x_pos, y_pos, tgt, is_large):
            if df_g_trend.empty: return
            df_plot = df_g_trend[['Mes_Str', col]].copy()
            df_plot.columns = ['Mes', 'V']
            df_plot['V'] = df_plot['V'] / 100
            
            ytd = df_plot['V'].mean() if len(df_plot) > 0 else 0
            df_plot = pd.concat([df_plot, pd.DataFrame([{'Mes': 'Acum.', 'V': ytd}])], ignore_index=True)
            df_plot['C'] = df_plot['V'].apply(lambda v: '#2ECC71' if v >= tgt else '#E74C3C')
            
            fig = go.Figure(go.Bar(x=df_plot['Mes'], y=df_plot['V'], marker_color=df_plot['C'], text=df_plot['V'], texttemplate='<b>%{text:.1%}</b>', textposition='outside'))
            fig.add_hline(y=tgt, line_dash="dash", line_color="#2ECC71", annotation_text=f"<b>Obj: {tgt*100:.0f}%</b>")
            if len(df_plot) > 1: fig.add_vline(x=len(df_plot)-1.5, line_dash="dot", line_color="black")
            fig.update_layout(title=dict(text=f"<b>{title}</b>", font=dict(size=13)), margin=dict(t=35, b=20, l=10, r=10), yaxis=dict(visible=False, range=[0, max(1.1, df_plot['V'].max()*1.3) if not df_plot.empty else 1]))
            render_and_insert_chart(fig, pdf, x_pos+2, y_pos+2, 134 if is_large else 132, 300 if is_large else 220)

        if area.upper() == "GLOBAL":
            pdf.draw_panel(10, 48, 136, 75); pdf.draw_panel(149, 48, 138, 75)
            add_trend_chart('OEE', 'OEE (%)', 10, 48, 0.75, True); add_trend_chart('Performance', 'PERFORMANCE (%)', 150, 48, 0.90, True)
            pdf.draw_panel(10, 126, 136, 75); pdf.draw_panel(149, 126, 138, 75)
            add_trend_chart('Disponibilidad', 'DISPONIBILIDAD (%)', 10, 126, 0.88, True); add_trend_chart('Calidad', 'CALIDAD (%)', 150, 126, 0.95, True)
        else:
            pdf.draw_panel(10, 48, 136, 52); pdf.draw_panel(149, 48, 138, 52)
            add_trend_chart('OEE', 'OEE (%)', 10, 48, 0.75, False); add_trend_chart('Performance', 'PERFORMANCE (%)', 150, 48, 0.90, False)
            pdf.draw_panel(10, 102, 136, 52); pdf.draw_panel(149, 102, 138, 52)
            add_trend_chart('Disponibilidad', 'DISPONIBILIDAD (%)', 10, 102, 0.88, False); add_trend_chart('Calidad', 'CALIDAD (%)', 150, 102, 0.95, False)
            
            pdf.draw_panel(10, 156, 136, 45); pdf.draw_panel(149, 156, 138, 45)
            df_g_fal = df_fallos[df_fallos['Grupo'] == target].sort_values('Minutos', ascending=False)
            if not df_g_fal.empty and df_g_fal['Minutos'].sum() > 0:
                tt = df_g_fal['Minutos'].sum()
                pdf.set_xy(10, 158); pdf.set_font("Arial", 'B', 8); pdf.set_fill_color(*theme_color); pdf.set_text_color(255)
                pdf.cell(100, 5, "FALLO", 1, 0, 'L', True); pdf.cell(18, 5, "MIN", 1, 0, 'C', True); pdf.cell(18, 5, "%", 1, 1, 'C', True)
                pdf.set_font("Arial", '', 7.5); pdf.set_text_color(0)
                
                for _, r in df_g_fal.head(5).iterrows():
                    pdf.set_x(10); pdf.cell(100, 6, clean_text(r['Fallo'])[:65], 1)
                    pdf.cell(18, 6, f"{r['Minutos']:.0f}", 1, 0, 'C')
                    pdf.cell(18, 6, f"{(r['Minutos']/tt)*100:.1f}%", 1, 1, 'C')
                
                df_mac = df_g_fal.groupby('Categoria')['Minutos'].sum().reset_index()
                df_mac['%'] = df_mac['Minutos'] / tt
                df_mac['Lbl'] = df_mac.apply(lambda r: f"{r['Categoria']} ({r['Minutos']/60:.1f}h | {r['%']:.1%})", axis=1)
                fig_s = px.bar(df_mac, x='%', y=['Pérdidas']*len(df_mac), color='Lbl', orientation='h', color_discrete_sequence=px.colors.qualitative.Safe)
                fig_s.update_layout(barmode='stack', legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5, font=dict(size=9), title=""), margin=dict(t=25, b=20, l=10, r=10), xaxis=dict(visible=False, range=[0, 1]), yaxis=dict(visible=False))
                render_and_insert_chart(fig_s, pdf, 151, 158, 134, 180)

    return pdf.output(dest='S').encode('latin-1')

def run_pdf_prod(planta, area, label_rep, df_prod, df_tprod, df_pza, hs_rt, conf):
    theme_color = (15, 76, 129) if area.upper() == "ESTAMPADO" else (211, 84, 0)
    tgt_scrap = 0.50 if area.upper() == "ESTAMPADO" else 0.30
    tgt_rt = 2.00
    
    pdf = ReportePDF(f"INFORME PRODUCTIVO - {area}", label_rep, theme_color)
    grupos = conf["grupos_estampado"] if area.upper() == "ESTAMPADO" else conf["grupos_soldadura"]
    paginas = [area.upper()] + [g for g in grupos if g in df_prod['Grupo'].unique()]

    for target in paginas:
        pdf.add_page(orientation='L'); pdf.set_auto_page_break(False); pdf.add_gradient_background()
        
        pdf.set_y(10); pdf.set_fill_color(*theme_color); pdf.set_text_color(255); pdf.set_font("Arial", 'B', 10)
        pdf.cell(40, 6, f"PERIODO: {label_rep}", 1, 0, 'C', True)
        pdf.cell(197, 6, f"PLANTA {area.upper()} - {target if target != area.upper() else 'GENERAL'}", 1, 0, 'C', True)
        pdf.cell(40, 6, "PRODUCTIVO", 1, 1, 'C', True)

        df_g_tprod = df_tprod[df_tprod['Grupo'] == target].sort_values('Mes').copy()
        # Recalcular porcentajes dinámicamente si el usuario editó las cantidades
        df_g_tprod['Scrap_pct'] = (df_g_tprod['Scrap'] / df_g_tprod['Totales'].replace(0,1)) * 100
        df_g_tprod['RT_pct'] = (df_g_tprod['RT'] / df_g_tprod['Totales'].replace(0,1)) * 100
        
        def add_p_chart(col, title, y_pos, tgt, is_pct):
            if df_g_tprod.empty: return
            df_plot = df_g_tprod[['Mes_Str', col]].copy()
            df_plot.columns = ['Mes', 'V']
            
            c = '#E74C3C' if is_pct and not df_plot.empty and df_plot['V'].iloc[-1] > tgt else ('#0F4C81' if area.upper() == "ESTAMPADO" else '#D35400')
            fig = go.Figure(go.Bar(x=df_plot['Mes'], y=df_plot['V'], marker_color=c, text=df_plot['V'], texttemplate='<b>%{text:.2f}%</b>' if is_pct else '<b>%{text:.3s}</b>', textposition='outside'))
            if tgt: fig.add_hline(y=tgt, line_dash="dash", line_color="#E74C3C", annotation_text=f"Obj: {tgt}%")
            fig.update_layout(title=dict(text=f"<b>{title}</b>", font=dict(size=14), x=0.5, xanchor='center'), margin=dict(t=35, b=20, l=10, r=10), yaxis=dict(visible=False, range=[0, max(tgt*1.5 if tgt else 0, df_plot['V'].max()*1.3) if not df_plot.empty else 1]), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            render_and_insert_chart(fig, pdf, 11, y_pos, 133, 240)

        pdf.draw_panel(10, 20, 135, 58); add_p_chart('Totales', 'PIEZAS TOTALES', 22, None, False)
        pdf.draw_panel(10, 82, 135, 58); add_p_chart('Scrap_pct', '% SCRAP', 84, tgt_scrap, True)
        pdf.draw_panel(10, 144, 135, 58); add_p_chart('RT_pct', '% RE-TRABAJO', 146, tgt_rt, True)

        pdf.draw_panel(150, 20, 135, 87); pdf.draw_panel(150, 111, 135, 87)
        
        df_g_pza = df_pza[df_pza['Grupo'] == target]
        if not df_g_pza.empty:
            ts = df_g_pza.nlargest(5, 'Scrap').sort_values('Scrap', ascending=True)
            tr = df_g_pza.nlargest(5, 'RT').sort_values('RT', ascending=True)
            b_col = ['#0F4C81'] if area.upper() == "ESTAMPADO" else ['#D35400']
            
            for df_plot, col, title, y_pos in [(ts, 'Scrap', 'TOP 5 SCRAP', 20), (tr, 'RT', 'TOP 5 RT', 111)]:
                if not df_plot.empty and df_plot[col].sum() > 0:
                    f = px.bar(df_plot, x=col, y='Pieza', orientation='h', title=f"<b>{title}</b>", color_discrete_sequence=b_col)
                    f.update_layout(title=dict(font=dict(size=14), x=0.5, xanchor='center'), margin=dict(t=40, b=20, l=120, r=45), xaxis=dict(visible=False), yaxis=dict(title="", type='category', tickfont=dict(size=10)), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    f.update_traces(texttemplate='<b>%{x}</b>', textposition='outside', cliponaxis=False)
                    render_and_insert_chart(f, pdf, 151, y_pos + 1, 133, 360)

        if target == area.upper() and area.upper() == 'ESTAMPADO':
            pdf.draw_panel(150, 199, 135, 10, 2, (240, 240, 240)); pdf.set_xy(150, 199); pdf.set_font("Arial", 'B', 10); pdf.set_text_color(50, 50, 50); pdf.cell(67.5, 10, "HS RE-TRABAJO TOTAL:", 0, 0, 'C'); pdf.set_text_color(*theme_color); pdf.set_font("Arial", 'B', 11); pdf.cell(67.5, 10, f"{hs_rt:.1f} hs", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 4. APP STREAMLIT (UI OPTIMIZADA CON LAYOUT)
# ==========================================
st.title("🖨️ Generador de Reportes (Data & Layout Editor)")
st.markdown("Los datos vienen directamente de **SQL**. Revisa y edita las tablas por área antes de generar los PDFs.")

with st.sidebar:
    st.header("🔧 Parámetros Generales")
    planta_sel = st.selectbox("Seleccionar Planta", ["FUMISCOR", "FAMMA"])
    st.divider()
    m_sel = st.selectbox("Mes", range(1, 13), index=pd.Timestamp.now().month-1)
    a_sel = st.selectbox("Año", [2024, 2025, 2026], index=2)
    st.divider()
    hs_rt = st.number_input("Hs Extra RT (Estampado):", 0.0, 1000.0, 0.0)

with st.spinner(f"Sincronizando {planta_sel} desde SQL..."):
    ini = pd.to_datetime(f"{a_sel}-{m_sel}-01")
    fin = ini + pd.offsets.MonthEnd(0)
    df_m, df_r, df_t, df_p, df_o, df_t04, df_t05, df_t06 = fetch_data_from_db(planta_sel, ini, fin, m_sel, a_sel)

conf = CONFIG_PLANTAS[planta_sel]
mapa = {str(k).strip().upper(): str(v).strip().upper() for k, v in conf["maquinas"].items()}

# --- CÁLCULO DE BASES PREVIAS (AGREGACIONES SQL PARA LA INTERFAZ) ---
# 1. Base KPIs (OEE Mes Actual)
df_b_oee = pd.DataFrame()
if not df_m.empty:
    dt = df_m.copy()
    dt['Grupo'] = dt['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    def cr(name, niv, data):
        if data.empty: return {'Nivel':niv, 'Grupo':name, 'Performance':0.0, 'Disp':0.0, 'Cal':0.0, 'Oee':0.0}
        if planta_sel == 'FUMISCOR':
            tp, to = data['T_Planificado'].sum(), data['T_Operativo'].sum()
            tpz = data['Buenas'].sum() + data['Retrabajo'].sum() + data['Observadas'].sum() if 'Buenas' in data.columns else 1
            vo = data['OEE_Num'].sum() / tp if tp > 0 else 0
            vd = data['Disp_Num'].sum() / tp if tp > 0 else 0
            vp = data['Perf_Num'].sum() / to if to > 0 else 0
            vc = data['Cal_Num'].sum() / tpz if tpz > 0 else 0
        else: # FAMMA
            tp, to = data['T_Planificado'].sum(), data['T_Operativo'].sum()
            vo = (data['OEE_Num'] * data['T_Planificado']).sum() / tp if tp > 0 else 0
            vd = (data['Disp_Num'] * data['T_Planificado']).sum() / tp if tp > 0 else 0
            vp = (data['Perf_Num'] * data['T_Operativo']).sum() / to if to > 0 else 0
            vc = (data['Cal_Num'] * data['T_Operativo']).sum() / to if to > 0 else 0
            
        return {'Nivel':niv, 'Grupo':name, 'Performance':(vp*100 if vp<=1.5 else vp), 'Disp':(vd*100 if vd<=1.5 else vd), 'Cal':(vc*100 if vc<=1.5 else vc), 'Oee':(vo*100 if vo<=1.5 else vo)}
    
    r_kpi = [cr('GLOBAL','GLOBAL', dt), cr('ESTAMPADO','FABRICA', dt[dt['Grupo'].isin(conf["grupos_estampado"])]), cr('SOLDADURA','FABRICA', dt[dt['Grupo'].isin(conf["grupos_soldadura"])])]
    for g in conf["grupos_estampado"] + conf["grupos_soldadura"]: r_kpi.append(cr(g, 'LINEA', dt[dt['Grupo']==g]))
    df_b_oee = pd.DataFrame(r_kpi)
    
    if not df_o.empty:
        df_b_oee.set_index(['Nivel', 'Grupo'], inplace=True)
        df_of_idx = df_o.set_index(['Nivel', 'Grupo'])
        for c in ['Performance', 'Disp', 'Cal', 'Oee']:
            if c in df_of_idx.columns: df_b_oee.update(df_of_idx[df_of_idx[c] > 0][c])
        df_b_oee.reset_index(inplace=True)
else:
    est = [{'Nivel':'GLOBAL','Grupo':'GLOBAL'}, {'Nivel':'FABRICA','Grupo':'ESTAMPADO'}, {'Nivel':'FABRICA','Grupo':'SOLDADURA'}] + [{'Nivel':'LINEA','Grupo':g} for g in conf["grupos_estampado"]+conf["grupos_soldadura"]]
    df_b_oee = pd.DataFrame(est); df_b_oee[['Performance','Disp','Cal','Oee']] = 0.0

# 2. Base Producción (Totales Mes Actual)
df_b_prod = pd.DataFrame()
if not df_t.empty:
    dt2 = df_t[df_t['Month'] == m_sel].copy()
    dt2['Grupo'] = dt2['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    def cp(name, niv, data): return {'Nivel':niv, 'Grupo':name, 'Totales':int(data['Totales'].sum() if not data.empty else 0), 'Scrap':int(data['Observadas'].sum() if not data.empty else 0), 'Retrabajo':int(data['Retrabajo'].sum() if not data.empty else 0)}
    r2 = [cp('GLOBAL','GLOBAL', dt2), cp('ESTAMPADO','FABRICA', dt2[dt2['Grupo'].isin(conf["grupos_estampado"])]), cp('SOLDADURA','FABRICA', dt2[dt2['Grupo'].isin(conf["grupos_soldadura"])])]
    for g in conf["grupos_estampado"] + conf["grupos_soldadura"]: r2.append(cp(g, 'LINEA', dt2[dt2['Grupo']==g]))
    df_b_prod = pd.DataFrame(r2)
else:
    est2 = [{'Nivel':'GLOBAL','Grupo':'GLOBAL'}, {'Nivel':'FABRICA','Grupo':'ESTAMPADO'}, {'Nivel':'FABRICA','Grupo':'SOLDADURA'}] + [{'Nivel':'LINEA','Grupo':g} for g in conf["grupos_estampado"]+conf["grupos_soldadura"]]
    df_b_prod = pd.DataFrame(est2); df_b_prod[['Totales','Scrap','Retrabajo']] = 0

# 3. Base Fallos Top 5
df_b_fallos = pd.DataFrame(columns=['Grupo', 'Fallo', 'Minutos', 'Categoria'])
if not df_r.empty:
    dtr = df_r[df_r['Estado_Global'] == 'Falla/Gestión'].copy()
    dtr['Grupo'] = dtr['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    f_list = []
    for g in ['GLOBAL', 'ESTAMPADO', 'SOLDADURA'] + conf['grupos_estampado'] + conf['grupos_soldadura']:
        d = dtr if g == 'GLOBAL' else (dtr[dtr['Grupo'].isin(conf['grupos_estampado'])] if g == 'ESTAMPADO' else (dtr[dtr['Grupo'].isin(conf['grupos_soldadura'])] if g == 'SOLDADURA' else dtr[dtr['Grupo'] == g]))
        if not d.empty:
            for _, r in d.groupby(['Detalle_Final', 'Categoria_Macro'])['Tiempo (Min)'].sum().nlargest(5).reset_index().iterrows():
                f_list.append({'Grupo': g, 'Fallo': r['Detalle_Final'], 'Categoria': r['Categoria_Macro'], 'Minutos': r['Tiempo (Min)']})
    df_b_fallos = pd.DataFrame(f_list)

# 4. Base Tendencias OEE (Mes a Mes)
res_toee = []
if planta_sel == 'FUMISCOR' and not df_t.empty:
    dtm = df_t.copy(); dtm['Grupo'] = dtm['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    def cto(g_name, d):
        for m, grp in d.groupby('Month'):
            tp, to = grp['T_Planificado'].sum(), grp['T_Operativo'].sum()
            tpz = grp['Buenas'].sum() + grp['Retrabajo'].sum() + grp['Observadas'].sum() if 'Buenas' in grp.columns else 1
            vo = grp['OEE_Num'].sum() / tp if tp > 0 else 0
            vp = grp['Perf_Num'].sum() / to if to > 0 else 0
            vd = grp['Disp_Num'].sum() / tp if tp > 0 else 0
            vc = grp['Cal_Num'].sum() / tpz if tpz > 0 else 0
            res_toee.append({'Grupo': g_name, 'Mes': int(m), 'Mes_Str': MESES_MAP[int(m)], 'OEE': vo*100 if vo<=1.5 else vo, 'Performance': vp*100 if vp<=1.5 else vp, 'Disponibilidad': vd*100 if vd<=1.5 else vd, 'Calidad': vc*100 if vc<=1.5 else vc})
    cto('GLOBAL', dtm); cto('ESTAMPADO', dtm[dtm['Grupo'].isin(conf['grupos_estampado'])]); cto('SOLDADURA', dtm[dtm['Grupo'].isin(conf['grupos_soldadura'])])
    for g in conf['grupos_estampado'] + conf['grupos_soldadura']: cto(g, dtm[dtm['Grupo'] == g])
elif planta_sel == 'FAMMA':
    for m, grp in df_t06.groupby('Month'): res_toee.append({'Grupo': 'GLOBAL', 'Mes': int(m), 'Mes_Str': MESES_MAP[int(m)], 'OEE': grp['OEE_Num'].iloc[0], 'Performance': grp['Perf_Num'].iloc[0], 'Disponibilidad': grp['Disp_Num'].iloc[0], 'Calidad': grp['Cal_Num'].iloc[0]})
    for m, grp in df_t05[df_t05['Planta'] == 'ESTAMPADO'].groupby('Month'): res_toee.append({'Grupo': 'ESTAMPADO', 'Mes': int(m), 'Mes_Str': MESES_MAP[int(m)], 'OEE': grp['OEE_Num'].iloc[0], 'Performance': grp['Perf_Num'].iloc[0], 'Disponibilidad': grp['Disp_Num'].iloc[0], 'Calidad': grp['Cal_Num'].iloc[0]})
    for m, grp in df_t05[df_t05['Planta'] == 'SOLDADURA'].groupby('Month'): res_toee.append({'Grupo': 'SOLDADURA', 'Mes': int(m), 'Mes_Str': MESES_MAP[int(m)], 'OEE': grp['OEE_Num'].iloc[0], 'Performance': grp['Perf_Num'].iloc[0], 'Disponibilidad': grp['Disp_Num'].iloc[0], 'Calidad': grp['Cal_Num'].iloc[0]})
    for g in conf['grupos_estampado'] + conf['grupos_soldadura']:
        for m, grp in df_t04[df_t04['Planta_Linea'] == g].groupby('Month'): res_toee.append({'Grupo': g, 'Mes': int(m), 'Mes_Str': MESES_MAP[int(m)], 'OEE': grp['OEE_Num'].iloc[0], 'Performance': grp['Perf_Num'].iloc[0], 'Disponibilidad': grp['Disp_Num'].iloc[0], 'Calidad': grp['Cal_Num'].iloc[0]})

df_b_toee = pd.DataFrame(res_toee)
if not df_b_toee.empty:
    for c in ['OEE', 'Performance', 'Disponibilidad', 'Calidad']: df_b_toee[c] = df_b_toee[c].apply(lambda x: x*100 if x <= 1.5 else x)

# 5. Base Tendencias Prod (Mes a Mes)
res_tprod = []
if not df_t.empty:
    dtpm = df_t.copy(); dtpm['Grupo'] = dtpm['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    def ctp(g_name, d):
        for m, grp in d.groupby('Month'): res_tprod.append({'Grupo': g_name, 'Mes': int(m), 'Mes_Str': MESES_MAP[int(m)], 'Totales': int(grp['Totales'].sum()), 'Scrap': int(grp['Observadas'].sum()), 'RT': int(grp['Retrabajo'].sum())})
    ctp('GLOBAL', dtpm); ctp('ESTAMPADO', dtpm[dtpm['Grupo'].isin(conf['grupos_estampado'])]); ctp('SOLDADURA', dtpm[dtpm['Grupo'].isin(conf['grupos_soldadura'])])
    for g in conf['grupos_estampado'] + conf['grupos_soldadura']: ctp(g, dtpm[dtpm['Grupo'] == g])
df_b_tprod = pd.DataFrame(res_tprod)

# 6. Base Top 5 Piezas
df_b_pza = pd.DataFrame(columns=['Grupo','Pieza','Scrap','RT'])
if not df_p.empty:
    d3 = df_p.copy(); d3['Grupo'] = d3['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO'); d3['Pieza'] = d3['Pieza'].astype(str).fillna('S/C')
    df_b_pza = d3.groupby(['Grupo','Pieza'])[['Scrap','RT']].sum().reset_index()


# --- FUNCIONES RENDER DE EDITORES ---
def edit_kpi(df, key):
    return st.data_editor(df, use_container_width=True, hide_index=True, key=f"kpi_{key}", column_config={
        "Nivel": st.column_config.TextColumn(disabled=True), "Grupo": st.column_config.TextColumn("Línea/Grupo", disabled=True),
        "Performance": st.column_config.NumberColumn("Performance (%)", format="%.2f%%", step=0.01), "Disp": st.column_config.NumberColumn("Disponibilidad (%)", format="%.2f%%", step=0.01),
        "Cal": st.column_config.NumberColumn("Calidad (%)", format="%.2f%%", step=0.01), "Oee": st.column_config.NumberColumn("OEE (%)", format="%.2f%%", step=0.01)
    })

def edit_toee(df, key):
    if df.empty: return pd.DataFrame(columns=['Grupo', 'Mes', 'Mes_Str', 'OEE', 'Performance', 'Disponibilidad', 'Calidad'])
    return st.data_editor(df, use_container_width=True, hide_index=True, key=f"toee_{key}", column_config={
        "Grupo": st.column_config.TextColumn(disabled=True), "Mes": st.column_config.NumberColumn(disabled=True), "Mes_Str": st.column_config.TextColumn("Mes", disabled=True),
        "OEE": st.column_config.NumberColumn("OEE (%)", format="%.2f%%", step=0.01), "Performance": st.column_config.NumberColumn("Performance (%)", format="%.2f%%", step=0.01),
        "Disponibilidad": st.column_config.NumberColumn("Disp. (%)", format="%.2f%%", step=0.01), "Calidad": st.column_config.NumberColumn("Calidad (%)", format="%.2f%%", step=0.01)
    })

def edit_fallos(df, key):
    if df.empty: return pd.DataFrame(columns=['Grupo', 'Fallo', 'Minutos', 'Categoria'])
    return st.data_editor(df, use_container_width=True, hide_index=True, key=f"fallos_{key}", num_rows="dynamic", column_config={
        "Grupo": st.column_config.TextColumn(disabled=True), "Fallo": st.column_config.TextColumn("Defecto / Parada"),
        "Categoria": st.column_config.TextColumn("Categoría Macro"), "Minutos": st.column_config.NumberColumn("Minutos", step=1)
    })

def edit_prod(df, key):
    return st.data_editor(df, use_container_width=True, hide_index=True, key=f"prod_{key}", column_config={
        "Nivel": st.column_config.TextColumn(disabled=True), "Grupo": st.column_config.TextColumn("Línea/Grupo", disabled=True),
        "Totales": st.column_config.NumberColumn("Piezas Totales", step=1), "Scrap": st.column_config.NumberColumn("Scrap (Cant)", step=1), "Retrabajo": st.column_config.NumberColumn("RT (Cant)", step=1)
    })

def edit_tprod(df, key):
    if df.empty: return pd.DataFrame(columns=['Grupo', 'Mes', 'Mes_Str', 'Totales', 'Scrap', 'RT'])
    st.info("💡 Edita las cantidades base. El sistema calculará automáticamente los % de Scrap y RT para los gráficos.")
    return st.data_editor(df, use_container_width=True, hide_index=True, key=f"tprod_{key}", column_config={
        "Grupo": st.column_config.TextColumn(disabled=True), "Mes": st.column_config.NumberColumn(disabled=True), "Mes_Str": st.column_config.TextColumn("Mes", disabled=True),
        "Totales": st.column_config.NumberColumn("Totales", step=1), "Scrap": st.column_config.NumberColumn("Scrap (Cant)", step=1), "RT": st.column_config.NumberColumn("RT (Cant)", step=1)
    })

def edit_pza(df, grps, key):
    return st.data_editor(df, use_container_width=True, hide_index=True, num_rows="dynamic", key=f"pzas_{key}", column_config={
        "Grupo": st.column_config.SelectboxColumn("Línea/Grupo", options=grps), "Pieza": st.column_config.TextColumn("Código Pieza"),
        "Scrap": st.column_config.NumberColumn("Scrap (Cant)", step=1), "RT": st.column_config.NumberColumn("Re-Trabajo (Cant)", step=1)
    })

# --- INTERFAZ TABS 6 ---
t_oe, t_os, t_pe, t_ps, t_g, t_d = st.tabs(["⚙️ OEE Estamp.", "🔥 OEE Sold.", "🏭 Prod. Estamp.", "🏭 Prod. Sold.", "🌍 Global", "🖨️ Exportar PDFs"])

with t_oe:
    st.markdown("### Área: ESTAMPADO - GESTIÓN A LA VISTA (OEE)")
    st.write("1. **KPIs del Mes**")
    ek_e = edit_kpi(df_b_oee[(df_b_oee['Grupo']=='ESTAMPADO') | df_b_oee['Grupo'].isin(conf['grupos_estampado'])], "e")
    st.write("2. **Tendencia Mes a Mes (Gráficos de Barras)**")
    eto_e = edit_toee(df_b_toee[(df_b_toee['Grupo']=='ESTAMPADO') | df_b_toee['Grupo'].isin(conf['grupos_estampado'])], "e")
    st.write("3. **Principales Fallos (Top 5 y Gráfico de Torta)**")
    ef_e = edit_fallos(df_b_fallos[(df_b_fallos['Grupo']=='ESTAMPADO') | df_b_fallos['Grupo'].isin(conf['grupos_estampado'])], "e")

with t_os:
    st.markdown("### Área: SOLDADURA - GESTIÓN A LA VISTA (OEE)")
    st.write("1. **KPIs del Mes**")
    ek_s = edit_kpi(df_b_oee[(df_b_oee['Grupo']=='SOLDADURA') | df_b_oee['Grupo'].isin(conf['grupos_soldadura'])], "s")
    st.write("2. **Tendencia Mes a Mes (Gráficos de Barras)**")
    eto_s = edit_toee(df_b_toee[(df_b_toee['Grupo']=='SOLDADURA') | df_b_toee['Grupo'].isin(conf['grupos_soldadura'])], "s")
    st.write("3. **Principales Fallos (Top 5 y Gráfico de Torta)**")
    ef_s = edit_fallos(df_b_fallos[(df_b_fallos['Grupo']=='SOLDADURA') | df_b_fallos['Grupo'].isin(conf['grupos_soldadura'])], "s")

with t_pe:
    st.markdown("### Área: ESTAMPADO - INFORME PRODUCTIVO")
    st.write("1. **Cantidades del Mes**")
    ep_e = edit_prod(df_b_prod[(df_b_prod['Grupo']=='ESTAMPADO') | df_b_prod['Grupo'].isin(conf['grupos_estampado'])], "e")
    st.write("2. **Tendencia Mes a Mes (Cantidades para Gráficos)**")
    etp_e = edit_tprod(df_b_tprod[(df_b_tprod['Grupo']=='ESTAMPADO') | df_b_tprod['Grupo'].isin(conf['grupos_estampado'])], "e")
    st.write("3. **Top 5 Piezas Defectuosas**")
    epz_e = edit_pza(df_b_pza[df_b_pza['Grupo'].isin(conf['grupos_estampado'])], conf['grupos_estampado'], "e")

with t_ps:
    st.markdown("### Área: SOLDADURA - INFORME PRODUCTIVO")
    st.write("1. **Cantidades del Mes**")
    ep_s = edit_prod(df_b_prod[(df_b_prod['Grupo']=='SOLDADURA') | df_b_prod['Grupo'].isin(conf['grupos_soldadura'])], "s")
    st.write("2. **Tendencia Mes a Mes (Cantidades para Gráficos)**")
    etp_s = edit_tprod(df_b_tprod[(df_b_tprod['Grupo']=='SOLDADURA') | df_b_tprod['Grupo'].isin(conf['grupos_soldadura'])], "s")
    st.write("3. **Top 5 Piezas Defectuosas**")
    epz_s = edit_pza(df_b_pza[df_b_pza['Grupo'].isin(conf['grupos_soldadura'])], conf['grupos_soldadura'], "s")

with t_g:
    st.markdown("### Área: GLOBAL")
    st.write("1. **KPIs del Mes (OEE)**")
    ek_g = edit_kpi(df_b_oee[df_b_oee['Grupo']=='GLOBAL'], "g")
    st.write("2. **Tendencia Mes a Mes (OEE)**")
    eto_g = edit_toee(df_b_toee[df_b_toee['Grupo']=='GLOBAL'], "g")
    st.write("3. **Cantidades del Mes (Producción)**")
    ep_g = edit_prod(df_b_prod[df_b_prod['Grupo']=='GLOBAL'], "g")
    st.write("4. **Tendencia Mes a Mes (Producción)**")
    etp_g = edit_tprod(df_b_tprod[df_b_tprod['Grupo']=='GLOBAL'], "g")

# --- CONSOLIDACIÓN FINAL PARA EL GENERADOR ---
df_k_f = pd.concat([ek_e, ek_s, ek_g])
df_to_f = pd.concat([eto_e, eto_s, eto_g])
df_fal_f = pd.concat([ef_e, ef_s])
df_p_f = pd.concat([ep_e, ep_s, ep_g])
df_tp_f = pd.concat([etp_e, etp_s, etp_g])
df_pz_f = pd.concat([epz_e, epz_s])

# Sustituir mes actual en la tendencia productiva editada automáticamente
for _, r in df_p_f.iterrows():
    idx = (df_tp_f['Grupo'] == r['Grupo']) & (df_tp_f['Mes'] == m_sel)
    if any(idx): df_tp_f.loc[idx, ['Totales', 'Scrap', 'RT']] = [r['Totales'], r['Scrap'], r['Retrabajo']]
    else: df_tp_f = pd.concat([df_tp_f, pd.DataFrame([{'Grupo':r['Grupo'], 'Mes':m_sel, 'Mes_Str':MESES_MAP[m_sel], 'Totales':r['Totales'], 'Scrap':r['Scrap'], 'RT':r['Retrabajo']}])], ignore_index=True)

# --- GENERACIÓN ---
with t_d:
    st.subheader(f"🖨️ Generar y Descargar ({planta_sel} - {m_sel}/{a_sel})")
    c1, c2, c3 = st.columns(3)
    l_rep = f"{m_sel}/{a_sel}"
    
    with c1:
        st.markdown("#### ⚙️ Estampado")
        if st.button("Generar OEE Estampado", use_container_width=True):
            with st.spinner("Procesando..."): st.session_state['pe1'] = run_pdf_oee(planta_sel, "Estampado", l_rep, df_k_f, df_to_f, df_fal_f, conf)
        if 'pe1' in st.session_state: st.download_button("📥 Descargar OEE", st.session_state['pe1'], f"{planta_sel}_OEE_ESTAMPADO.pdf", use_container_width=True)

        if st.button("Generar Prod. Estampado", use_container_width=True):
            with st.spinner("Procesando..."): st.session_state['pe2'] = run_pdf_prod(planta_sel, "Estampado", l_rep, df_p_f, df_tp_f, df_pz_f, hs_rt, conf)
        if 'pe2' in st.session_state: st.download_button("📥 Descargar Prod.", st.session_state['pe2'], f"{planta_sel}_PROD_ESTAMPADO.pdf", use_container_width=True)

    with c2:
        st.markdown("#### 🔥 Soldadura")
        if st.button("Generar OEE Soldadura", use_container_width=True):
            with st.spinner("Procesando..."): st.session_state['ps1'] = run_pdf_oee(planta_sel, "Soldadura", l_rep, df_k_f, df_to_f, df_fal_f, conf)
        if 'ps1' in st.session_state: st.download_button("📥 Descargar OEE", st.session_state['ps1'], f"{planta_sel}_OEE_SOLDADURA.pdf", use_container_width=True)

        if st.button("Generar Prod. Soldadura", use_container_width=True):
            with st.spinner("Procesando..."): st.session_state['ps2'] = run_pdf_prod(planta_sel, "Soldadura", l_rep, df_p_f, df_tp_f, df_pz_f, hs_rt, conf)
        if 'ps2' in st.session_state: st.download_button("📥 Descargar Prod.", st.session_state['ps2'], f"{planta_sel}_PROD_SOLDADURA.pdf", use_container_width=True)

    with c3:
        st.markdown("#### 🌍 Resumen Global")
        if st.button("Generar PDF Global", use_container_width=True):
            with st.spinner("Procesando..."): st.session_state['pg'] = run_pdf_oee(planta_sel, "GLOBAL", l_rep, df_k_f, df_to_f, pd.DataFrame(columns=['Grupo','Fallo','Minutos','Categoria']), conf)
        if 'pg' in st.session_state: st.download_button("📥 Descargar Global", st.session_state['pg'], f"{planta_sel}_GENERAL.pdf", use_container_width=True)
