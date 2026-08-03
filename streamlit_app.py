import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile
import os
from fpdf import FPDF

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
# 1. CLASE PDF Y UTILIDADES (Mantenidas idénticas)
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

# (Las funciones generar_pdf_oee y generar_pdf_prod permanecen intactas...)
# He omitido las funciones de generación de PDF aquí por brevedad, usa EXACTAMENTE
# las mismas funciones generar_pdf_oee y generar_pdf_prod del código anterior.

# ==========================================
# 4. APP STREAMLIT (UI OPTIMIZADA CON LAYOUT)
# ==========================================
st.title("🖨️ Generador de Reportes (Layout Editor)")
st.markdown("Revisa y edita los datos organizados por el **Área** exacta donde se imprimirán en los reportes.")

with st.sidebar:
    st.header("🔧 Parámetros Generales")
    planta_sel = st.selectbox("Seleccionar Planta", ["FUMISCOR", "FAMMA"])
    modo_datos = st.radio("Origen de Datos", ["📊 Automático (SQL)", "📝 Manual (Vacío)"])
    st.divider()
    m_sel = st.selectbox("Mes", range(1, 13), index=pd.Timestamp.now().month-1)
    a_sel = st.selectbox("Año", [2024, 2025, 2026], index=2)
    st.divider()
    hs_rt = st.number_input("Horas Extras RT (Estampado):", 0.0, 1000.0, 0.0)

with st.spinner(f"Sincronizando con {planta_sel}..."):
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


# --- INTERFAZ POR ÁREA (LAYOUT MAP) ---
tab_e, tab_s, tab_g, tab_d = st.tabs(["⚙️ Área ESTAMPADO", "🔥 Área SOLDADURA", "🌍 Área GLOBAL", "🖨️ Exportar PDFs"])

def build_editor_kpi(df_subset, key_suffix):
    return st.data_editor(df_subset, use_container_width=True, hide_index=True, key=f"kpi_{key_suffix}", column_config={
        "Nivel": st.column_config.TextColumn("Nivel", disabled=True), "Grupo": st.column_config.TextColumn("Sección / Línea", disabled=True),
        "Performance": st.column_config.NumberColumn("Performance (%)", format="%.2f %%", step=0.01),
        "Disp": st.column_config.NumberColumn("Disponibilidad (%)", format="%.2f %%", step=0.01),
        "Cal": st.column_config.NumberColumn("Calidad (%)", format="%.2f %%", step=0.01),
        "Oee": st.column_config.NumberColumn("OEE (%)", format="%.2f %%", step=0.01)
    })

def build_editor_prod(df_subset, key_suffix):
    return st.data_editor(df_subset, use_container_width=True, hide_index=True, key=f"prod_{key_suffix}", column_config={
        "Nivel": st.column_config.TextColumn("Nivel", disabled=True), "Grupo": st.column_config.TextColumn("Sección / Línea", disabled=True),
        "Totales": st.column_config.NumberColumn("Piezas Totales", step=1), "Scrap": st.column_config.NumberColumn("Scrap (Cant)", step=1), "Retrabajo": st.column_config.NumberColumn("Re-Trabajo (Cant)", step=1)
    })

def build_editor_piezas(df_subset, allowed_groups, key_suffix):
    return st.data_editor(df_subset, use_container_width=True, hide_index=True, num_rows="dynamic", key=f"pza_{key_suffix}", column_config={
        "Grupo": st.column_config.SelectboxColumn("Sección / Línea", options=allowed_groups),
        "Pieza": st.column_config.TextColumn("Código/Nombre de Pieza"),
        "Scrap": st.column_config.NumberColumn("Scrap (Cant)", step=1), "RT": st.column_config.NumberColumn("Re-Trabajo (Cant)", step=1)
    })

# --- ESTAMPADO ---
with tab_e:
    st.markdown("### 📄 Páginas del PDF de Estampado")
    st.info("Los datos que edites aquí se reflejarán tanto en el PDF OEE como en el PDF Productivo de la planta de Estampado.")
    
    st.markdown("#### 1. Gestión OEE (General y Líneas)")
    df_oee_e = df_base_oee[(df_base_oee['Grupo'] == 'ESTAMPADO') | (df_base_oee['Grupo'].isin(conf['grupos_estampado']))]
    ed_oee_e = build_editor_kpi(df_oee_e, "est")

    st.markdown("#### 2. Informe Productivo (Cantidades Totales)")
    df_prod_e = df_base_prod[(df_base_prod['Grupo'] == 'ESTAMPADO') | (df_base_prod['Grupo'].isin(conf['grupos_estampado']))]
    ed_prod_e = build_editor_prod(df_prod_e, "est")

    st.markdown("#### 3. Top 5 Defectos por Pieza")
    df_piezas_e = df_base_piezas[df_base_piezas['Grupo'].isin(conf['grupos_estampado'])]
    ed_piezas_e = build_editor_piezas(df_piezas_e, conf['grupos_estampado'], "est")

# --- SOLDADURA ---
with tab_s:
    st.markdown("### 📄 Páginas del PDF de Soldadura")
    
    st.markdown("#### 1. Gestión OEE (General y Líneas)")
    df_oee_s = df_base_oee[(df_base_oee['Grupo'] == 'SOLDADURA') | (df_base_oee['Grupo'].isin(conf['grupos_soldadura']))]
    ed_oee_s = build_editor_kpi(df_oee_s, "sol")

    st.markdown("#### 2. Informe Productivo (Cantidades Totales)")
    df_prod_s = df_base_prod[(df_base_prod['Grupo'] == 'SOLDADURA') | (df_base_prod['Grupo'].isin(conf['grupos_soldadura']))]
    ed_prod_s = build_editor_prod(df_prod_s, "sol")

    st.markdown("#### 3. Top 5 Defectos por Pieza")
    df_piezas_s = df_base_piezas[df_base_piezas['Grupo'].isin(conf['grupos_soldadura'])]
    ed_piezas_s = build_editor_piezas(df_piezas_s, conf['grupos_soldadura'], "sol")

# --- GLOBAL ---
with tab_g:
    st.markdown("### 📄 Página del PDF Resumen Global")
    
    st.markdown("#### 1. Gestión OEE Global")
    df_oee_g = df_base_oee[df_base_oee['Grupo'] == 'GLOBAL']
    ed_oee_g = build_editor_kpi(df_oee_g, "glob")

    st.markdown("#### 2. Cantidades Globales")
    df_prod_g = df_base_prod[df_base_prod['Grupo'] == 'GLOBAL']
    ed_prod_g = build_editor_prod(df_prod_g, "glob")


# --- COMBINAR DATOS EDITADOS PARA PDF ---
df_oficial_editado = pd.concat([ed_oee_g, ed_oee_e, ed_oee_s]).drop_duplicates(subset=['Nivel', 'Grupo'], keep='last')
df_prod_editado = pd.concat([ed_prod_g, ed_prod_e, ed_prod_s]).drop_duplicates(subset=['Nivel', 'Grupo'], keep='last')
df_piezas_editado = pd.concat([ed_piezas_e, ed_piezas_s])

# --- EXPORTAR ---
with tab_d:
    st.subheader(f"🖨️ Generar y Descargar ({planta_sel} - {m_sel}/{a_sel})")
    col_d1, col_d2, col_d3 = st.columns(3)
    label_rep = f"{m_sel}/{a_sel}"
    
    with col_d1:
        st.markdown("### ⚙️ Área Estampado")
        if st.button("Generar OEE Estampado", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['oee_e'] = generar_pdf_oee(planta_sel, "Estampado", label_rep, df_m, df_r, df_t, df_oficial_editado, df_t_04, df_t_05, df_t_06, m_sel)
        if 'oee_e' in st.session_state: st.download_button("📥 Bajar OEE Estampado", st.session_state['oee_e'], f"{planta_sel}_Gestion_Vista_ESTAMPADO.pdf", use_container_width=True)

        if st.button("Generar Prod. Estampado", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['pr_e'] = generar_pdf_prod(planta_sel, "Estampado", label_rep, df_t, df_p, m_sel, hs_rt, df_prod_editado, df_piezas_editado)
        if 'pr_e' in st.session_state: st.download_button("📥 Bajar Prod. Estampado", st.session_state['pr_e'], f"{planta_sel}_Productivo_Vista_ESTAMPADO.pdf", use_container_width=True)

    with col_d2:
        st.markdown("### 🔥 Área Soldadura")
        if st.button("Generar OEE Soldadura", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['oee_s'] = generar_pdf_oee(planta_sel, "Soldadura", label_rep, df_m, df_r, df_t, df_oficial_editado, df_t_04, df_t_05, df_t_06, m_sel)
        if 'oee_s' in st.session_state: st.download_button("📥 Bajar OEE Soldadura", st.session_state['oee_s'], f"{planta_sel}_Gestion_Vista_SOLDADURA.pdf", use_container_width=True)

        if st.button("Generar Prod. Soldadura", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['pr_s'] = generar_pdf_prod(planta_sel, "Soldadura", label_rep, df_t, df_p, m_sel, hs_rt, df_prod_editado, df_piezas_editado)
        if 'pr_s' in st.session_state: st.download_button("📥 Bajar Prod. Soldadura", st.session_state['pr_s'], f"{planta_sel}_Productivo_Vista_SOLDADURA.pdf", use_container_width=True)

    with col_d3:
        st.markdown("### 🌍 Resumen Global")
        if st.button("Generar Reporte Global", use_container_width=True):
            with st.spinner("Generando..."): st.session_state['glob'] = generar_pdf_oee(planta_sel, "GLOBAL", label_rep, df_m, df_r, df_t, df_oficial_editado, df_t_04, df_t_05, df_t_06, m_sel)
        if 'glob' in st.session_state: st.download_button("📥 Bajar Global", st.session_state['glob'], f"{planta_sel}_Vista_GENERAL.pdf", use_container_width=True)
