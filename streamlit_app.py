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
st.set_page_config(page_title="Generador de Reportes | Grupo Fumiscor", layout="wide", page_icon="📊")

CONFIG_PLANTAS = {
    "FUMISCOR": {
        "maquinas": {
            "P-023": "GME-04 - PRENSA PROGRESIVA", "P-024": "GME-04 - PRENSA PROGRESIVA", 
            "P-025": "GME-04 - PRENSA PROGRESIVA", "P-026": "GME-04 - PRENSA PROGRESIVA",
            "P-027": "PRENSAS PROGRESIVAS GRANDES", "P-028": "PRENSAS PROGRESIVAS GRANDES", 
            "P-029": "PRENSAS PROGRESIVAS GRANDES", "P-030": "PRENSAS PROGRESIVAS GRANDES",
            "BAL-002": "GME-01 - BALANCIN", "BAL-003": "GME-01 - BALANCIN", "BAL-005": "GME-01 - BALANCIN", 
            "BAL-006": "GME-01 - BALANCIN", "BAL-007": "GME-01 - BALANCIN", "BAL-008": "GME-01 - BALANCIN", 
            "BAL-009": "GME-01 - BALANCIN", "BAL-010": "GME-01 - BALANCIN", "BAL-011": "GME-01 - BALANCIN", 
            "BAL-012": "GME-01 - BALANCIN", "BAL-013": "GME-01 - BALANCIN", "BAL-014": "GME-01 - BALANCIN", 
            "BAL-015": "GME-01 - BALANCIN",
            "P-011": "GME-02 - PRENSA HIDRAULICA", "P-012": "GME-02 - PRENSA HIDRAULICA", 
            "P-013": "GME-02 - PRENSA HIDRAULICA", "P-014": "GME-02 - PRENSA HIDRAULICA", 
            "P-016": "GME-02 - PRENSA HIDRAULICA", "P-017": "GME-02 - PRENSA HIDRAULICA", 
            "P-018": "GME-02 - PRENSA HIDRAULICA", 
            "P-015": "GME-03 - PRENSA MECANICA", "P-019": "GME-03 - PRENSA MECANICA", 
            "P-020": "GME-03 - PRENSA MECANICA", "P-021": "GME-03 - PRENSA MECANICA", 
            "P-022": "GME-03 - PRENSA MECANICA", "GOF01": "GME-03 - PRENSA MECANICA",
            "SOP-003": "GMS-02 - PRP", "SOP-005": "GMS-02 - PRP", "SOP-008": "GMS-02 - PRP", 
            "SOP-009": "GMS-02 - PRP", "SOP-010": "GMS-02 - PRP", "SOP-017": "GMS-02 - PRP", 
            "SOP-018": "GMS-02 - PRP", "SOP-019": "GMS-02 - PRP", "SOP-020": "GMS-02 - PRP", 
            "SOP-022": "GMS-02 - PRP", "SOP-023": "GMS-02 - PRP", "SOP-024": "GMS-02 - PRP", 
            "SOP-025": "GMS-02 - PRP", "SOP-026": "GMS-02 - PRP", "SOP-027": "GMS-02 - PRP",
            "SOP-028": "GMS-02 - PRP", "SOP-029": "GMS-02 - PRP", "SOP-030": "GMS-02 - PRP",
            "DOB-001": "GME-05 - DOBLADORA", "DOB-01": "GME-05 - DOBLADORA", "DOB-002": "GME-05 - DOBLADORA", 
            "DOB-003": "GME-05 - DOBLADORA", "DOB-004": "GME-05 - DOBLADORA", "DOB-005": "GME-05 - DOBLADORA", 
            "DOB-006": "GME-05 - DOBLADORA", "DOB-007": "GME-05 - DOBLADORA", "DOB-008": "GME-05 - DOBLADORA", 
            "DOB-009": "GME-05 - DOBLADORA", "DOB-010": "GME-05 - DOBLADORA",
            "Celda 01 Fumis": "CELDAS NUEVAS", "Celda 02 Fumis": "CELDAS NUEVAS", "Celda 03 Fumis": "CELDAS NUEVAS", 
            "Celda 04 Fumis": "CELDAS NUEVAS", "Celda 05 Fumis": "CELDAS NUEVAS", "Celda 06 Fumis": "CELDAS NUEVAS",
            "Celda 07 Fumis": "CELDAS NUEVAS", "Celda 08 Fumis": "CELDAS NUEVAS", "Celda 09 Fumis": "CELDAS NUEVAS",
            "Celda 10 Fumis": "CELDAS NUEVAS", "Celda 11 Fumis": "CELDAS NUEVAS", "Celda 12 Fumis": "CELDAS NUEVAS",
            "Celda 13 Fumis": "CELDAS NUEVAS", "Celda 14 Fumis": "CELDAS NUEVAS", "Celda 15 Fumis": "CELDAS NUEVAS",
            "Cel1 - Rob13 - RUEDA AUX.": "GMS-01 - ROBOT", "Cel2 - Rob1 - ALMOHADON": "GMS-01 - ROBOT",
            "Cel3 - Rob14 - HANGERS": "GMS-01 - ROBOT", "Cel4 - Rob6 - DOB TORCHA": "GMS-01 - ROBOT",
            "Cel5 - Rob4 - Respaldo 60/40": "GMS-01 - ROBOT", "HANGERS NISSAN": "GMS-01 - ROBOT"
        },
        "grupos_estampado": ['CORTADORA LASER', 'GME-01 - BALANCIN', 'GME-02 - PRENSA HIDRAULICA', 'GME-03 - PRENSA MECANICA', 'GME-04 - PRENSA PROGRESIVA', 'PRENSAS PROGRESIVAS GRANDES'],
        "grupos_soldadura": ['GME-05 - DOBLADORA', 'GMS-01 - ROBOT', 'GMS-02 - PRP', 'GMS-03 - COLGANTE', 'GMS-03 - SOLDADORA MANUAL', 'CELDAS NUEVAS']
    },
    "FAMMA": {
        "maquinas": {
            "LINEA 1.2": "LINEA 1.2", "LINEA 1.4": "LINEA 1.4", "LINEA 1.5": "LINEA 1.5",
            "LINEA 2": "LINEA 2", "LINEA 3": "LINEA 3", "LINEA 4": "LINEA 4",
            "Cell 1 Famma": "CELDAS", "Cell 2 Famma": "CELDAS", "Cell 3 Famma": "CELDAS",
            "Cell 4 Famma": "CELDAS", "Cell 5 Famma": "CELDAS", "Cell 6 Famma": "CELDAS",
            "Cell 7 Famma": "CELDAS", "Cell 8 Famma": "CELDAS", "Cell 9 Famma": "CELDAS",
            "Cell 10 Famma": "CELDAS", "Cell 11 Famma": "CELDAS", "Cell 12 Famma": "CELDAS",
            "Cell 13 Famma": "CELDAS", "Cell 14 Famma": "CELDAS", "Cell 15A Famma": "CELDAS",
            "Cell 15B Famma": "CELDAS", "Cell 16 Famma": "CELDAS", "Cell 17 Famma": "CELDAS",
            "PRP 1": "PRP", "PRP 2": "PRP", "PRP 3": "PRP", "PRP 4": "PRP", "PRP 5": "PRP", "PRP 6": "PRP",
            "MIG 1": "MIG", "MIG 2": "MIG"
        },
        "grupos_estampado": ['LINEA 1.2', 'LINEA 1.4', 'LINEA 1.5', 'LINEA 2', 'LINEA 3', 'LINEA 4'],
        "grupos_soldadura": ['CELDAS', 'PRP', 'MIG']
    }
}

# ==========================================
# 1. CLASE PDF Y UTILIDADES
# ==========================================
class ReportePDF(FPDF):
    def __init__(self, area, fecha_str, theme_color):
        super().__init__()
        self.area = area; self.fecha_str = fecha_str; self.theme_color = theme_color

    def add_gradient_background(self):
        r1, g1, b1 = 240, 242, 246; r2, g2, b2 = 215, 220, 225
        h = self.h; w = self.w
        for i in range(int(h * 2)):
            ratio = i / (h * 2)
            self.set_fill_color(int(r1 + (r2 - r1) * ratio), int(g1 + (g2 - g1) * ratio), int(b1 + (b2 - b1) * ratio))
            self.rect(0, i / 2, w, 0.5, 'F')

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

def generate_empty_schemas():
    df_m = pd.DataFrame(columns=['Máquina', 'Buenas', 'Retrabajo', 'Observadas', 'T_Operativo', 'T_Parada', 'T_Planificado', 'Perf_Num', 'Disp_Num', 'Cal_Num', 'OEE_Num'])
    df_raw = pd.DataFrame(columns=['Máquina', 'Tiempo (Min)', 'Nivel Evento 1', 'Nivel Evento 2', 'Nivel Evento 3', 'Nivel Evento 4', 'Estado_Global', 'Categoria_Macro', 'Detalle_Final'])
    df_trend = pd.DataFrame(columns=['Month', 'Máquina', 'Buenas', 'Retrabajo', 'Observadas', 'Totales', 'T_Operativo', 'T_Parada', 'T_Planificado', 'Perf_Num', 'Disp_Num', 'Cal_Num', 'OEE_Num'])
    df_piezas = pd.DataFrame(columns=['Máquina', 'Pieza', 'Scrap', 'RT'])
    df_oficial = pd.DataFrame(columns=['Nivel', 'Grupo', 'Performance', 'Disp', 'Cal', 'Oee'])
    df_t_04 = pd.DataFrame(columns=['Month', 'Planta_Linea', 'OEE_Num', 'Perf_Num', 'Disp_Num', 'Cal_Num'])
    df_t_05 = pd.DataFrame(columns=['Month', 'Planta', 'OEE_Num', 'Perf_Num', 'Disp_Num', 'Cal_Num'])
    df_t_06 = pd.DataFrame(columns=['Month', 'OEE_Num', 'Perf_Num', 'Disp_Num', 'Cal_Num'])
    return df_m, df_raw, df_trend, df_piezas, df_oficial, df_t_04, df_t_05, df_t_06

# ==========================================
# 2. OBTENCIÓN DE DATOS (SQL)
# ==========================================
@st.cache_data(ttl=300, show_spinner=False)
def fetch_data_from_db(planta, fecha_ini, fecha_fin, mes, anio):
    try:
        # CONEXIÓN DINÁMICA BASADA EN LA PLANTA
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
            
            df_metrics = conn.query(q_metrics).fillna(0)
            df_raw = conn.query(q_event)
            df_piezas = conn.query(q_piezas).fillna(0)
            t_oee = conn.query(q_trend_oee).fillna(0)
            t_pcs = conn.query(q_trend_pcs).fillna(0)
            df_trend = pd.merge(t_pcs, t_oee, on=['Month', 'Máquina'], how='outer').fillna(0) if not t_pcs.empty else t_oee
            df_oficial = pd.concat([conn.query(q_m06).fillna(0), conn.query(q_m05).fillna(0), conn.query(q_m04).fillna(0)], ignore_index=True)
            
            if not df_raw.empty:
                df_raw['Tiempo (Min)'] = pd.to_numeric(df_raw['Tiempo (Min)'], errors='coerce').fillna(0)
                mask = (df_raw['Nivel Evento 1'].astype(str).str.upper().str.contains('PROYECTO') | df_raw['Nivel Evento 2'].astype(str).str.upper().str.contains('PROYECTO'))
                df_raw = df_raw[~mask].copy()
                df_raw['Estado_Global'] = df_raw.apply(lambda r: 'Producción' if 'PRODUC' in str(r.get('Nivel Evento 1','')).upper() else ('Parada Programada' if 'PARADA' in str(r.get('Nivel Evento 1','')).upper() else 'Falla/Gestión'), axis=1)
                df_raw['Categoria_Macro'] = df_raw.apply(lambda r: 'Gestión' if 'GESTION' in str(r.get('Nivel Evento 1','')).upper() else (str(r.get('Nivel Evento 2','')).title() if 'FALLA' in str(r.get('Nivel Evento 1','')).upper() else 'Otra Falla'), axis=1)
                df_raw['Detalle_Final'] = df_raw.apply(lambda r: str(r.get('Nivel Evento 4', r.get('Nivel Evento 3', r.get('Nivel Evento 2', 'Sin Detalle')))), axis=1)

            return df_metrics, df_raw, df_trend, df_piezas, df_oficial, pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

        else: # FAMMA
            q_oee_m = f"SELECT c.Name as Máquina, p.Performance as Perf_Num, p.Availability as Disp_Num, p.Quality as Cal_Num, p.Oee as OEE_Num, COALESCE(p.ProductiveTime, 0) as T_Operativo, (COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0)) as T_Planificado FROM PROD_M_03 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month = {mes}"
            q_pcs_m = f"SELECT c.Name as Máquina, SUM(COALESCE(p.Good, 0)) as Buenas, SUM(COALESCE(p.Rework, 0)) as Retrabajo, SUM(COALESCE(p.Scrap, 0)) as Observadas FROM PROD_M_01 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month = {mes} GROUP BY c.Name"
            df_metrics = pd.merge(conn.query(q_oee_m).fillna(0), conn.query(q_pcs_m).fillna(0), on='Máquina', how='outer').fillna(0)

            df_piezas = conn.query(f"SELECT c.Name as Máquina, COALESCE(pr.Code, 'S/C') as Pieza, SUM(COALESCE(p.Scrap, 0)) as Scrap, SUM(COALESCE(p.Rework, 0)) as RT FROM PROD_M_01 p JOIN CELL c ON p.CellId = c.CellId LEFT JOIN PRODUCT pr ON p.ProductId = pr.ProductId WHERE p.Year = {anio} AND p.Month = {mes} GROUP BY c.Name, pr.Code").fillna(0)
            
            t_oee = conn.query(f"SELECT p.Month, c.Name as Máquina, p.Performance as Perf_Num, p.Availability as Disp_Num, p.Quality as Cal_Num, p.Oee as OEE_Num, COALESCE(p.ProductiveTime, 0) as T_Operativo, (COALESCE(p.ProductiveTime, 0) + COALESCE(p.DownTime, 0)) as T_Planificado FROM PROD_M_03 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month <= {mes}").fillna(0)
            t_pcs = conn.query(f"SELECT p.Month, c.Name as Máquina, SUM(COALESCE(p.Good, 0)) as Buenas, SUM(COALESCE(p.Rework, 0)) as Retrabajo, SUM(COALESCE(p.Scrap, 0)) as Observadas, SUM(COALESCE(p.Good, 0) + COALESCE(p.Rework, 0) + COALESCE(p.Scrap, 0)) as Totales FROM PROD_M_01 p JOIN CELL c ON p.CellId = c.CellId WHERE p.Year = {anio} AND p.Month <= {mes} GROUP BY p.Month, c.Name").fillna(0)
            df_trend = pd.merge(t_pcs, t_oee, on=['Month', 'Máquina'], how='outer').fillna(0)

            q_event = f"SELECT c.Name as Máquina, e.Interval as [Tiempo (Min)], t1.Name as [Nivel Evento 1], t2.Name as [Nivel Evento 2], t3.Name as [Nivel Evento 3], t4.Name as [Nivel Evento 4], t5.Name as [Nivel Evento 5], t6.Name as [Nivel Evento 6] FROM EVENT_01 e JOIN CELL c ON e.CellId = c.CellId LEFT JOIN EVENTTYPE t1 ON e.EventTypeLevel1 = t1.EventTypeId LEFT JOIN EVENTTYPE t2 ON e.EventTypeLevel2 = t2.EventTypeId LEFT JOIN EVENTTYPE t3 ON e.EventTypeLevel3 = t3.EventTypeId LEFT JOIN EVENTTYPE t4 ON e.EventTypeLevel4 = t4.EventTypeId LEFT JOIN EVENTTYPE t5 ON e.EventTypeLevel5 = t5.EventTypeId LEFT JOIN EVENTTYPE t6 ON e.EventTypeLevel6 = t6.EventTypeId WHERE e.Date BETWEEN '{ini_str}' AND '{fin_str}'"
            df_raw = conn.query(q_event)
            
            if not df_raw.empty:
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
                df_raw[['Estado_Global', 'Categoria_Macro', 'Detalle_Final']] = df_raw.apply(lambda r: pd.Series(parse_ev(r)), axis=1)

            q_m06 = f"SELECT 'GLOBAL' as Nivel, 'GLOBAL' as Grupo, Performance, Availability as Disp, Quality as Cal, Oee FROM PROD_M_06 WHERE Year = {anio} AND Month = {mes}"
            q_m05 = f"SELECT 'FABRICA' as Nivel, UPPER(Factory) as Grupo, Performance, Availability as Disp, Quality as Cal, Oee FROM PROD_M_05 WHERE Year = {anio} AND Month = {mes}"
            q_m04 = f"SELECT 'LINEA' as Nivel, UPPER(Line) as Grupo, Performance, Availability as Disp, Quality as Cal, Oee FROM PROD_M_04 WHERE Year = {anio} AND Month = {mes}"
            df_oficial = pd.concat([conn.query(q_m06).fillna(0), conn.query(q_m05).fillna(0), conn.query(q_m04).fillna(0)], ignore_index=True)
            
            df_t_04 = conn.query(f"SELECT Month, Line as Planta_Linea, Oee as OEE_Num, Performance as Perf_Num, Availability as Disp_Num, Quality as Cal_Num FROM PROD_M_04 WHERE Year = {anio} AND Month <= {mes}").fillna(0)
            df_t_05 = conn.query(f"SELECT Month, Factory as Planta, Oee as OEE_Num, Performance as Perf_Num, Availability as Disp_Num, Quality as Cal_Num FROM PROD_M_05 WHERE Year = {anio} AND Month <= {mes}").fillna(0)
            df_t_06 = conn.query(f"SELECT Month, Oee as OEE_Num, Performance as Perf_Num, Availability as Disp_Num, Quality as Cal_Num FROM PROD_M_06 WHERE Year = {anio} AND Month <= {mes}").fillna(0)

            return df_metrics, df_raw, df_trend, df_piezas, df_oficial, df_t_04, df_t_05, df_t_06
            
    except Exception as e:
        st.error(f"Error conectando a SQL ({planta}): {str(e)}")
        return generate_empty_schemas()

# ==========================================
# 3. MOTORES DE PDF UNIFICADOS
# ==========================================
def render_and_insert_chart(fig, pdf, x, y, w, h_fig=300):
    """ Función auxiliar para generar imagen y asegurar su limpieza en memoria """
    fig.update_layout(width=600, height=h_fig, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        fig.write_image(tmp.name, engine="kaleido", scale=2.5)
        tmp_path = tmp.name
    
    try:
        pdf.image(tmp_path, x, y, w)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def generar_pdf_oee(planta, area, label_reporte, df_m, df_r, df_t, df_oficial, df_t_04, df_t_05, df_t_06, mes_sel):
    conf = CONFIG_PLANTAS[planta]
    if area.upper() == "ESTAMPADO": theme_color = (15, 76, 129); grupos = conf["grupos_estampado"]
    elif area.upper() == "SOLDADURA": theme_color = (211, 84, 0); grupos = conf["grupos_soldadura"]
    else: theme_color = (40, 40, 40); grupos = conf["grupos_estampado"] + conf["grupos_soldadura"]

    mapa = {str(k).strip().upper(): str(v).strip().upper() for k, v in conf["maquinas"].items()}
    
    df_m = df_m.copy(); df_t = df_t.copy(); df_r = df_r.copy()
    for d in [df_m, df_t, df_r]:
        if not d.empty and 'Máquina' in d.columns: d['Grupo'] = d['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    
    df_m = df_m[df_m['Grupo'].isin(grupos)]; df_t = df_t[df_t['Grupo'].isin(grupos)]; df_r = df_r[df_r['Grupo'].isin(grupos)]
    
    pdf = ReportePDF(f"GESTIÓN A LA VISTA - {area}", label_reporte, theme_color)
    paginas = ['GENERAL'] if area.upper() == "GLOBAL" else ['GENERAL'] + [g for g in grupos if g in df_m['Grupo'].unique()]

    for target in paginas:
        pdf.add_page(orientation='L'); pdf.set_auto_page_break(False); pdf.add_gradient_background()
        
        df_m_t = df_m if target == 'GENERAL' else df_m[df_m['Grupo'] == target]
        df_t_t = df_t if target == 'GENERAL' else df_t[df_t['Grupo'] == target]
        df_r_t = df_r if target == 'GENERAL' else df_r[df_r['Grupo'] == target]

        pdf.set_y(10); pdf.set_fill_color(*theme_color); pdf.set_text_color(255); pdf.set_font("Arial", 'B', 10)
        pdf.cell(40, 6, "PERIODO", 1, 0, 'C', True); pdf.cell(197, 6, f"PLANTA {area.upper()} - {target}", 1, 0, 'C', True); pdf.cell(40, 6, "INFORME", 1, 1, 'C', True)
        pdf.set_fill_color(255, 255, 255); pdf.set_text_color(0); pdf.set_font("Arial", '', 10)
        pdf.cell(40, 6, label_reporte, 1, 0, 'C', True); pdf.cell(197, 6, f"EMPRESA: {planta}", 1, 0, 'C', True); pdf.cell(40, 6, "DISPONIBILIDAD", 1, 1, 'C', True)

        v_oee, v_perf, v_disp, v_cal = 0, 0, 0, 0
        if not df_oficial.empty:
            if target == 'GENERAL':
                if area.upper() == 'GLOBAL': row = df_oficial[df_oficial['Nivel'] == 'GLOBAL']
                else: row = df_oficial[(df_oficial['Nivel'] == 'FABRICA') & (df_oficial['Grupo'].str.contains(area.upper(), na=False))]
            else:
                row = df_oficial[(df_oficial['Nivel'] == 'LINEA') & (df_oficial['Grupo'] == target)]
            if not row.empty:
                v_oee = row['Oee'].values[0]; v_perf = row['Performance'].values[0]; v_disp = row['Disp'].values[0]; v_cal = row['Cal'].values[0]

        if v_oee > 1.5 or v_perf > 1.5 or v_disp > 1.5:
            v_oee /= 100.0; v_perf /= 100.0; v_disp /= 100.0; v_cal /= 100.0

        kpis = {"OEE": (v_oee, 0.75), "PERFORMANCE": (v_perf, 0.90), "DISPONIBILIDAD": (v_disp, 0.88), "CALIDAD": (v_cal, 0.95)}
        for i, (lbl, (v, obj)) in enumerate(kpis.items()):
            bg = (46, 204, 113) if v >= obj else (231, 76, 60)
            pdf.draw_kpi_panel(x := 10 + (i * 68.5), 25, 65, 20, bg_color=bg)
            pdf.set_xy(x, 27); pdf.set_font("Arial", 'B', 10); pdf.set_text_color(255); pdf.cell(65, 6, lbl, 0, 1, 'L')
            pdf.set_xy(x, 33); pdf.set_font("Arial", 'B', 20); pdf.cell(65, 10, f"{v*100:.1f}%", 0, 0, 'C')
        pdf.set_text_color(0)

        def add_trend(df_in, col, title, x_pos, y_pos, tgt, is_large):
            if df_in.empty: return
            res = []
            
            use_historics = planta == "FAMMA" and target != 'GENERAL'
            if planta == "FAMMA" and target == 'GENERAL' and area.upper() == 'GLOBAL': 
                df_exact = df_t_06.copy(); use_historics = True
            elif planta == "FAMMA" and target == 'GENERAL': 
                df_exact = df_t_05[df_t_05['Planta'] == area.upper()].copy(); use_historics = True
            elif planta == "FAMMA":
                df_exact = df_t_04[df_t_04['Planta_Linea'] == target].copy()
                
            if use_historics and not df_exact.empty:
                for m, grp in df_exact.groupby('Month'):
                    val = grp['OEE_Num'].iloc[0] if col == 'OEE' else (grp['Perf_Num'].iloc[0] if col == 'PERFORMANCE' else (grp['Disp_Num'].iloc[0] if col == 'DISPONIBILIDAD' else grp['Cal_Num'].iloc[0]))
                    res.append({'M': int(m), 'V': val/100 if val > 1.5 else val})
            else:
                for m, grp in df_in.groupby('Month'):
                    tp, to = grp['T_Planificado'].sum(), grp['T_Operativo'].sum()
                    if col == 'OEE': val = (grp['OEE_Num']*grp['T_Planificado']).sum()/tp if tp>0 else 0
                    elif col == 'PERFORMANCE': val = (grp['Perf_Num']*grp['T_Operativo']).sum()/to if to>0 else 0
                    elif col == 'DISPONIBILIDAD': val = (grp['Disp_Num']*grp['T_Planificado']).sum()/tp if tp>0 else 0
                    else: val = (grp['Cal_Num']*grp['T_Operativo']).sum()/to if to>0 else 0
                    res.append({'M': int(m), 'V': val/100 if val > 1.5 else val})

            df_g = pd.DataFrame(res)
            tp_ytd, to_ytd = df_in['T_Planificado'].sum(), df_in['T_Operativo'].sum()
            ytd = 0
            if col == 'OEE': ytd = (df_in['OEE_Num']*df_in['T_Planificado']).sum()/tp_ytd if tp_ytd>0 else 0
            elif col == 'PERFORMANCE': ytd = (df_in['Perf_Num']*df_in['T_Operativo']).sum()/to_ytd if to_ytd>0 else 0
            elif col == 'DISPONIBILIDAD': ytd = (df_in['Disp_Num']*df_in['T_Planificado']).sum()/tp_ytd if tp_ytd>0 else 0
            else: ytd = (df_in['Cal_Num']*df_in['T_Operativo']).sum()/to_ytd if to_ytd>0 else 0
            if ytd > 1.5: ytd /= 100
            
            df_g = pd.concat([df_g, pd.DataFrame([{'M': 99, 'V': ytd}])], ignore_index=True) if not df_g.empty else pd.DataFrame([{'M': 99, 'V': ytd}])
            df_g['Mes'] = df_g['M'].map({1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic',99:'Acum.'})
            df_g['C'] = df_g['V'].apply(lambda v: '#2ECC71' if v >= tgt else '#E74C3C')
            
            fig = go.Figure(go.Bar(x=df_g['Mes'], y=df_g['V'], marker_color=df_g['C'], text=df_g['V'], texttemplate='<b>%{text:.1%}</b>', textposition='outside'))
            fig.add_hline(y=tgt, line_dash="dash", line_color="#2ECC71", annotation_text=f"<b>Obj: {tgt*100:.0f}%</b>")
            if len(df_g) > 1: fig.add_vline(x=len(df_g)-1.5, line_dash="dot")
            fig.update_layout(title=dict(text=f"<b>{title}</b>", font=dict(size=13)), margin=dict(t=35, b=20, l=10, r=10), yaxis=dict(visible=False, range=[0, max(1.1, df_g['V'].max()*1.3) if not df_g.empty else 1]))
            
            render_and_insert_chart(fig, pdf, x_pos+2, y_pos+2, 134 if is_large else 132, 300 if is_large else 220)

        if area.upper() == "GLOBAL":
            pdf.draw_panel(10, 48, 136, 75); pdf.draw_panel(149, 48, 138, 75); add_trend(df_t_t, 'OEE', 'OEE (%)', 10, 48, 0.75, True); add_trend(df_t_t, 'PERFORMANCE', 'PERFORMANCE (%)', 150, 48, 0.90, True)
            pdf.draw_panel(10, 126, 136, 75); pdf.draw_panel(149, 126, 138, 75); add_trend(df_t_t, 'DISPONIBILIDAD', 'DISPONIBILIDAD (%)', 10, 126, 0.88, True); add_trend(df_t_t, 'CALIDAD', 'CALIDAD (%)', 150, 126, 0.95, True)
        else:
            pdf.draw_panel(10, 48, 136, 52); pdf.draw_panel(149, 48, 138, 52); add_trend(df_t_t, 'OEE', 'OEE (%)', 10, 48, 0.75, False); add_trend(df_t_t, 'PERFORMANCE', 'PERFORMANCE (%)', 150, 48, 0.90, False)
            pdf.draw_panel(10, 102, 136, 52); pdf.draw_panel(149, 102, 138, 52); add_trend(df_t_t, 'DISPONIBILIDAD', 'DISPONIBILIDAD (%)', 10, 102, 0.88, False); add_trend(df_t_t, 'CALIDAD', 'CALIDAD (%)', 150, 102, 0.95, False)
            
            pdf.draw_panel(10, 156, 136, 45); pdf.draw_panel(149, 156, 138, 45)
            df_f = df_r_t[df_r_t['Estado_Global'] == 'Falla/Gestión']
            if not df_f.empty and df_f['Tiempo (Min)'].sum() > 0:
                top5 = df_f.groupby('Detalle_Final')['Tiempo (Min)'].sum().nlargest(5).reset_index()
                pdf.set_xy(10, 158); pdf.set_font("Arial", 'B', 8); pdf.set_fill_color(*theme_color); pdf.set_text_color(255)
                pdf.cell(100, 5, "FALLO", 1, 0, 'L', True); pdf.cell(18, 5, "MIN", 1, 0, 'C', True); pdf.cell(18, 5, "%", 1, 1, 'C', True)
                pdf.set_font("Arial", '', 7.5); pdf.set_text_color(0); tt = df_f['Tiempo (Min)'].sum()
                for _, r in top5.iterrows():
                    pdf.set_x(10); pdf.cell(100, 6, clean_text(r['Detalle_Final'])[:65], 1); pdf.cell(18, 6, f"{r['Tiempo (Min)']:.0f}", 1, 0, 'C'); pdf.cell(18, 6, f"{(r['Tiempo (Min)']/tt)*100:.1f}%", 1, 1, 'C')
                
                df_macro = df_f.groupby('Categoria_Macro')['Tiempo (Min)'].sum().reset_index()
                df_macro['%'] = df_macro['Tiempo (Min)'] / tt
                df_macro['Label'] = df_macro.apply(lambda r: f"{r['Categoria_Macro']} ({r['Tiempo (Min)']/60:.1f}h | {r['%']:.1%})", axis=1)
                fig_s = px.bar(df_macro, x='%', y=['Pérdidas']*len(df_macro), color='Label', orientation='h', color_discrete_sequence=px.colors.qualitative.Safe)
                fig_s.update_layout(barmode='stack', legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5, font=dict(size=9), title=""), margin=dict(t=25, b=20, l=10, r=10), xaxis=dict(visible=False, range=[0, 1]), yaxis=dict(visible=False))
                
                render_and_insert_chart(fig_s, pdf, 151, 158, 134, 180)

    return pdf.output(dest='S').encode('latin-1')

def generar_pdf_prod(planta, area, label_reporte, df_t, df_p, mes_sel, hs_rt, df_prod_editado, df_piezas_editado):
    conf = CONFIG_PLANTAS[planta]
    theme_color = (15, 76, 129) if area.upper() == "ESTAMPADO" else (211, 84, 0)
    target_scrap = 0.50 if area.upper() == "ESTAMPADO" else 0.30
    target_rt = 2.00
    
    pdf = ReportePDF(f"INFORME PRODUCTIVO - {area}", label_reporte, theme_color)
    mapa = {str(k).strip().upper(): str(v).strip().upper() for k, v in conf["maquinas"].items()}
    
    df_t = df_t.copy()
    df_p = df_piezas_editado.copy() if df_piezas_editado is not None and not df_piezas_editado.empty else df_p.copy()
    
    for d in [df_t, df_p]: 
        if not d.empty and 'Máquina' in d.columns: d['Grupo'] = d['Máquina'].str.strip().str.upper().map(mapa).fillna('OTRO')
    if not df_p.empty and 'Pieza' in df_p.columns: df_p['Pieza'] = df_p['Pieza'].astype(str).fillna('S/C')

    grupos = conf["grupos_estampado"] if area.upper() == "ESTAMPADO" else conf["grupos_soldadura"]
    df_t = df_t[df_t['Grupo'].isin(grupos)]
    if not df_p.empty and 'Grupo' in df_p.columns: df_p = df_p[df_p['Grupo'].isin(grupos)]
    
    grupos_activos = set(df_t[df_t['Month'] == mes_sel]['Grupo'].unique()) if not df_t.empty else set()
    if df_prod_editado is not None and not df_prod_editado.empty:
        grupos_activos.update(df_prod_editado[(df_prod_editado['Nivel'] == 'LINEA') & (df_prod_editado['Totales'] > 0)]['Grupo'].unique())
        
    paginas = ['GENERAL'] + [g for g in grupos if g in grupos_activos]

    for target in paginas:
        pdf.add_page(orientation='L'); pdf.set_auto_page_break(False); pdf.add_gradient_background()
        df_t_t = df_t if target == 'GENERAL' else df_t[df_t['Grupo'] == target]
        df_p_t = df_p if target == 'GENERAL' else df_p[df_p['Grupo'] == target]

        pdf.set_y(10); pdf.set_fill_color(*theme_color); pdf.set_text_color(255); pdf.set_font("Arial", 'B', 10)
        pdf.cell(40, 6, f"MES: {mes_sel}", 1, 0, 'C', True); pdf.cell(197, 6, f"PLANTA {area.upper()} - {target}", 1, 0, 'C', True); pdf.cell(40, 6, "PRODUCTIVO", 1, 1, 'C', True)
        
        df_ev = df_t_t.groupby('Month')[['Buenas', 'Observadas', 'Retrabajo', 'Totales']].sum().reset_index()

        lookup_grupo = area.upper() if target == 'GENERAL' else target
        if df_prod_editado is not None and not df_prod_editado.empty:
            fila = df_prod_editado[df_prod_editado['Grupo'] == lookup_grupo]
            if not fila.empty:
                t_ed, s_ed, r_ed = fila['Totales'].values[0], fila['Scrap'].values[0], fila['Retrabajo'].values[0]
                if mes_sel in df_ev['Month'].values:
                    df_ev.loc[df_ev['Month'] == mes_sel, ['Totales', 'Observadas', 'Retrabajo']] = [t_ed, s_ed, r_ed]
                else:
                    df_ev = pd.concat([df_ev, pd.DataFrame([{'Month': mes_sel, 'Buenas': t_ed-s_ed-r_ed, 'Observadas': s_ed, 'Retrabajo': r_ed, 'Totales': t_ed}])], ignore_index=True)

        df_ev['% Scrap'] = (df_ev['Observadas'] / df_ev['Totales'].replace(0, 1)) * 100
        df_ev['% RT'] = (df_ev['Retrabajo'] / df_ev['Totales'].replace(0, 1)) * 100
        df_ev['Mes'] = df_ev['Month'].map({1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'})

        def add_p_chart(y_col, title, y_pos, tgt, is_pct):
            if df_ev.empty: return
            color = '#E74C3C' if is_pct and df_ev[y_col].iloc[-1] > tgt else ('#0F4C81' if area.upper() == "ESTAMPADO" else '#D35400')
            fig = go.Figure(go.Bar(x=df_ev['Mes'], y=df_ev[y_col], marker_color=color, text=df_ev[y_col], texttemplate='<b>%{text:.2f}%</b>' if is_pct else '<b>%{text:.3s}</b>', textposition='outside'))
            if tgt: fig.add_hline(y=tgt, line_dash="dash", line_color="#E74C3C", annotation_text=f"Obj: {tgt}%")
            fig.update_layout(title=dict(text=f"<b>{title}</b>", font=dict(size=14), x=0.5, xanchor='center'), margin=dict(t=35, b=20, l=10, r=10), yaxis=dict(visible=False, range=[0, max(tgt*1.5 if tgt else 0, df_ev[y_col].max()*1.3) if not df_ev.empty else 1]), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            
            render_and_insert_chart(fig, pdf, 11, y_pos, 133, 240)

        pdf.draw_panel(10, 20, 135, 58); add_p_chart('Totales', 'PIEZAS TOTALES', 22, None, False)
        pdf.draw_panel(10, 82, 135, 58); add_p_chart('% Scrap', '% SCRAP', 84, target_scrap, True)
        pdf.draw_panel(10, 144, 135, 58); add_p_chart('% RT', '% RE-TRABAJO', 146, target_rt, True)

        pdf.draw_panel(150, 20, 135, 87); pdf.draw_panel(150, 111, 135, 87)
        if not df_p_t.empty:
            ts = df_p_t.groupby('Pieza')['Scrap'].sum().nlargest(5).reset_index().sort_values('Scrap', ascending=True)
            tr = df_p_t.groupby('Pieza')['RT'].sum().nlargest(5).reset_index().sort_values('RT', ascending=True)
            bar_color = ['#0F4C81'] if area.upper() == "ESTAMPADO" else ['#D35400']
            for df_plot, col, title, y_pos in [(ts, 'Scrap', 'TOP 5 SCRAP', 20), (tr, 'RT', 'TOP 5 RT', 111)]:
                if not df_plot.empty and df_plot[col].sum() > 0:
                    f = px.bar(df_plot, x=col, y='Pieza', orientation='h', title=f"<b>{title}</b>", color_discrete_sequence=bar_color)
                    f.update_layout(title=dict(font=dict(size=14), x=0.5, xanchor='center'), margin=dict(t=40, b=20, l=120, r=45), xaxis=dict(visible=False), yaxis=dict(title="", type='category', tickfont=dict(size=10)), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    f.update_traces(texttemplate='<b>%{x}</b>', textposition='outside', cliponaxis=False)
                    
                    render_and_insert_chart(f, pdf, 151, y_pos + 1, 133, 360)

        if target == 'GENERAL' and area.upper() == 'ESTAMPADO':
            pdf.draw_panel(150, 199, 135, 10, 2, (240, 240, 240)); pdf.set_xy(150, 199); pdf.set_font("Arial", 'B', 10); pdf.set_text_color(50, 50, 50); pdf.cell(67.5, 10, "HS RE-TRABAJO TOTAL:", 0, 0, 'C'); pdf.set_text_color(*theme_color); pdf.set_font("Arial", 'B', 11); pdf.cell(67.5, 10, f"{hs_rt:.1f} hs", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 4. APP STREAMLIT (UI)
# ==========================================
st.title("🖨️ Generador Unificado de Reportes")
st.markdown("Selecciona los parámetros y visualiza las tablas interactivas. Luego de confirmar los datos, descarga los PDFs listos para presentar.")

with st.sidebar:
    st.header("🔧 Parámetros")
    planta_sel = st.selectbox("Seleccionar Planta", ["FUMISCOR", "FAMMA"])
    modo_datos = st.radio("Origen de Datos", ["📊 Automático (Wiidem SQL)", "📝 Manual (Plantillas Vacías)"])
    st.divider()
    m_sel = st.selectbox("Mes", range(1, 13), index=pd.Timestamp.now().month-1)
    a_sel = st.selectbox("Año", [2024, 2025, 2026], index=2)
    st.divider()
    hs_rt = st.number_input("Horas Extras RT (Estampado):", 0.0, 1000.0, 0.0)

with st.spinner(f"Sincronizando {planta_sel}..."):
    ini = pd.to_datetime(f"{a_sel}-{m_sel}-01")
    fin = ini + pd.offsets.MonthEnd(0)
    
    if "Automático" in modo_datos:
        df_m, df_r, df_t, df_p, df_oficial, df_t_04, df_t_05, df_t_06 = fetch_data_from_db(planta_sel, ini, fin, m_sel, a_sel)
    else:
        df_m, df_r, df_t, df_p, df_oficial, df_t_04, df_t_05, df_t_06 = generate_empty_schemas()

conf = CONFIG_PLANTAS[planta_sel]
mapa = {str(k).strip().upper(): str(v).strip().upper() for k, v in conf["maquinas"].items()}

# --- BASE EDITORES ---
df_base_oee = pd.DataFrame()
if not df_m.empty:
    df_temp = df_m.copy()
    df_temp['Grupo'] = df_temp['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    def cr(name, niv, data):
        if data.empty: return {'Nivel':niv, 'Grupo':name, 'Performance':0.0, 'Disp':0.0, 'Cal':0.0, 'Oee':0.0}
        tp, to = data['T_Planificado'].sum(), data['T_Operativo'].sum()
        vo = (data['OEE_Num']*data['T_Planificado']).sum()/tp if tp>0 else 0
        vd = (data['Disp_Num']*data['T_Planificado']).sum()/tp if tp>0 else 0
        vp = (data['Perf_Num']*data['T_Operativo']).sum()/to if to>0 else 0
        vc = (data['Cal_Num']*data['T_Operativo']).sum()/to if to>0 else 0
        return {'Nivel':niv, 'Grupo':name, 'Performance':(vp*100 if vp<=1.5 else vp), 'Disp':(vd*100 if vd<=1.5 else vd), 'Cal':(vc*100 if vc<=1.5 else vc), 'Oee':(vo*100 if vo<=1.5 else vo)}
    
    res = [cr('GLOBAL','GLOBAL', df_temp), cr('ESTAMPADO','FABRICA', df_temp[df_temp['Grupo'].isin(conf["grupos_estampado"])]), cr('SOLDADURA','FABRICA', df_temp[df_temp['Grupo'].isin(conf["grupos_soldadura"])])]
    for g in conf["grupos_estampado"] + conf["grupos_soldadura"]: res.append(cr(g, 'LINEA', df_temp[df_temp['Grupo']==g]))
    df_base_oee = pd.DataFrame(res)

if not df_base_oee.empty and not df_oficial.empty:
    df_base_oee.set_index(['Nivel', 'Grupo'], inplace=True)
    df_of_idx = df_oficial.set_index(['Nivel', 'Grupo'])
    for c in ['Performance', 'Disp', 'Cal', 'Oee']:
        if c in df_of_idx.columns: df_base_oee.update(df_of_idx[df_of_idx[c] > 0][c])
    df_base_oee.reset_index(inplace=True)
elif df_base_oee.empty:
    est = [{'Nivel':'GLOBAL','Grupo':'GLOBAL'}, {'Nivel':'FABRICA','Grupo':'ESTAMPADO'}, {'Nivel':'FABRICA','Grupo':'SOLDADURA'}] + [{'Nivel':'LINEA','Grupo':g} for g in conf["grupos_estampado"]+conf["grupos_soldadura"]]
    df_base_oee = pd.DataFrame(est); df_base_oee[['Performance','Disp','Cal','Oee']] = 0.0

df_base_prod = pd.DataFrame()
if not df_t.empty:
    df_temp2 = df_t[df_t['Month'] == m_sel].copy()
    df_temp2['Grupo'] = df_temp2['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    def cp(name, niv, data):
        return {'Nivel':niv, 'Grupo':name, 'Totales':int(data['Totales'].sum() if not data.empty else 0), 'Scrap':int(data['Observadas'].sum() if not data.empty else 0), 'Retrabajo':int(data['Retrabajo'].sum() if not data.empty else 0)}
    res2 = [cp('GLOBAL','GLOBAL', df_temp2), cp('ESTAMPADO','FABRICA', df_temp2[df_temp2['Grupo'].isin(conf["grupos_estampado"])]), cp('SOLDADURA','FABRICA', df_temp2[df_temp2['Grupo'].isin(conf["grupos_soldadura"])])]
    for g in conf["grupos_estampado"] + conf["grupos_soldadura"]: res2.append(cp(g, 'LINEA', df_temp2[df_temp2['Grupo']==g]))
    df_base_prod = pd.DataFrame(res2)
else:
    est2 = [{'Nivel':'GLOBAL','Grupo':'GLOBAL'}, {'Nivel':'FABRICA','Grupo':'ESTAMPADO'}, {'Nivel':'FABRICA','Grupo':'SOLDADURA'}] + [{'Nivel':'LINEA','Grupo':g} for g in conf["grupos_estampado"]+conf["grupos_soldadura"]]
    df_base_prod = pd.DataFrame(est2); df_base_prod[['Totales','Scrap','Retrabajo']] = 0

df_base_piezas = pd.DataFrame(columns=['Grupo','Pieza','Scrap','RT'])
if not df_p.empty:
    df_temp3 = df_p.copy()
    df_temp3['Grupo'] = df_temp3['Máquina'].astype(str).str.strip().str.upper().map(mapa).fillna('OTRO')
    df_temp3['Pieza'] = df_temp3['Pieza'].astype(str).fillna('S/C')
    df_base_piezas = df_temp3.groupby(['Grupo','Pieza'])[['Scrap','RT']].sum().reset_index()

# --- INTERFAZ TABS ---
tab1, tab2, tab3 = st.tabs(["⚙️ OEE y Disponibilidad", "🏭 Producción y Calidades", "🖨️ Generar y Descargar"])

with tab1:
    st.subheader(f"Edición de KPIs ({planta_sel})")
    df_oficial_editado = st.data_editor(df_base_oee, use_container_width=True, hide_index=True, column_config={
        "Nivel": st.column_config.TextColumn("Nivel", disabled=True), "Grupo": st.column_config.TextColumn("Grupo", disabled=True),
        "Performance": st.column_config.NumberColumn("Performance", format="%.2f", step=0.01),
        "Disp": st.column_config.NumberColumn("Disponibilidad", format="%.2f", step=0.01),
        "Cal": st.column_config.NumberColumn("Calidad", format="%.2f", step=0.01),
        "Oee": st.column_config.NumberColumn("OEE", format="%.2f", step=0.01)
    })

with tab2:
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.subheader("Cantidades Generales")
        df_prod_editado = st.data_editor(df_base_prod, use_container_width=True, hide_index=True, column_config={
            "Nivel": st.column_config.TextColumn("Nivel", disabled=True), "Grupo": st.column_config.TextColumn("Grupo", disabled=True),
            "Totales": st.column_config.NumberColumn("Totales", step=1), "Scrap": st.column_config.NumberColumn("Scrap", step=1), "Retrabajo": st.column_config.NumberColumn("RT", step=1)
        })
    with col_p2:
        st.subheader("Top 5 Defectos por Pieza")
        df_piezas_editado = st.data_editor(df_base_piezas, use_container_width=True, hide_index=True, num_rows="dynamic", column_config={
            "Grupo": st.column_config.SelectboxColumn("Grupo", options=conf["grupos_estampado"]+conf["grupos_soldadura"]),
            "Pieza": st.column_config.TextColumn("Pieza"),
            "Scrap": st.column_config.NumberColumn("Scrap", step=1), "RT": st.column_config.NumberColumn("RT", step=1)
        })

with tab3:
    st.subheader(f"Generar PDFs - {planta_sel} ({m_sel}/{a_sel})")
    col_down1, col_down2, col_down3 = st.columns(3)

    label_rep = f"{m_sel}/{a_sel}"
    
    with col_down1:
        st.markdown("### ⚙️ Gestión OEE")
        if st.button("Preparar OEE Estampado", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['oee_e'] = generar_pdf_oee(planta_sel, "Estampado", label_rep, df_m, df_r, df_t, df_oficial_editado, df_t_04, df_t_05, df_t_06, m_sel)
        if 'oee_e' in st.session_state: st.download_button("📥 Descargar OEE Estampado", st.session_state['oee_e'], f"{planta_sel}_Gestion_Vista_ESTAMPADO.pdf", use_container_width=True)

        if st.button("Preparar OEE Soldadura", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['oee_s'] = generar_pdf_oee(planta_sel, "Soldadura", label_rep, df_m, df_r, df_t, df_oficial_editado, df_t_04, df_t_05, df_t_06, m_sel)
        if 'oee_s' in st.session_state: st.download_button("📥 Descargar OEE Soldadura", st.session_state['oee_s'], f"{planta_sel}_Gestion_Vista_SOLDADURA.pdf", use_container_width=True)

    with col_down2:
        st.markdown("### 🏭 Informe Productivo")
        if st.button("Preparar Prod. Estampado", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['pr_e'] = generar_pdf_prod(planta_sel, "Estampado", label_rep, df_t, df_p, m_sel, hs_rt, df_prod_editado, df_piezas_editado)
        if 'pr_e' in st.session_state: st.download_button("📥 Descargar Prod. Estampado", st.session_state['pr_e'], f"{planta_sel}_Productivo_Vista_ESTAMPADO.pdf", use_container_width=True)

        if st.button("Preparar Prod. Soldadura", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['pr_s'] = generar_pdf_prod(planta_sel, "Soldadura", label_rep, df_t, df_p, m_sel, hs_rt, df_prod_editado, df_piezas_editado)
        if 'pr_s' in st.session_state: st.download_button("📥 Descargar Prod. Soldadura", st.session_state['pr_s'], f"{planta_sel}_Productivo_Vista_SOLDADURA.pdf", use_container_width=True)

    with col_down3:
        st.markdown("### 🌎 Reporte Maestro")
        if st.button("Preparar Reporte Global", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['glob'] = generar_pdf_oee(planta_sel, "GLOBAL", label_rep, df_m, df_r, df_t, df_oficial_editado, df_t_04, df_t_05, df_t_06, m_sel)
        if 'glob' in st.session_state: st.download_button("📥 Descargar Global", st.session_state['glob'], f"{planta_sel}_Vista_GENERAL.pdf", use_container_width=True)
