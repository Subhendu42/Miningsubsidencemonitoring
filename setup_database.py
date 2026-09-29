"""
Coal Mine Subsidence Monitoring & Safety System
Database Initialization & CSV Ingestion Script
Builds the complete relational correspondence database for the COAL_MINE_SHI2026 project.
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "coal_mine_subsidence.db")
SQL_EXPORT_PATH = os.path.join(os.path.dirname(__file__), "correspondence_database.sql")

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Sensors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensors (
        sensor_id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        sensor_type VARCHAR(50) NOT NULL,
        sector VARCHAR(100) NOT NULL,
        location_desc VARCHAR(200),
        depth_m REAL DEFAULT 0.0,
        latitude REAL,
        longitude REAL,
        frequency VARCHAR(50),
        mesh_network VARCHAR(50),
        status VARCHAR(20) DEFAULT 'Active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Personnel Table (Admin & Safety Personnel)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personnel (
        badge_id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        role VARCHAR(100) NOT NULL,
        department VARCHAR(100),
        sector_assigned VARCHAR(100),
        email VARCHAR(100),
        clearance_level VARCHAR(50),
        tactical_comm_channel VARCHAR(100),
        status VARCHAR(20) DEFAULT 'Active'
    );
    """)

    # 3. Telemetry & Geotechnical Subsidence Readings (Joined Raw + Anomaly + Risk)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        sensor_id VARCHAR(20) NOT NULL,
        tilt REAL NOT NULL,
        displacement REAL NOT NULL,
        vibration REAL NOT NULL,
        crack_width REAL NOT NULL,
        tilt_change REAL,
        vibration_change REAL,
        crack_width_change REAL,
        future_displacement REAL,
        anomaly_prediction INTEGER,
        anomaly_status VARCHAR(20),
        risk_percentage REAL,
        risk_level VARCHAR(20),
        FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
    );
    """)

    # 4. Regulatory & Safety Correspondence Database (Statutory notices, DGMS communications, incident warnings)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS safety_correspondence (
        correspondence_id VARCHAR(30) PRIMARY KEY,
        timestamp DATETIME NOT NULL,
        category VARCHAR(50) NOT NULL,
        urgency_level VARCHAR(20) NOT NULL,
        sender_badge_id VARCHAR(20),
        recipient VARCHAR(150) NOT NULL,
        subject VARCHAR(200) NOT NULL,
        body_content TEXT NOT NULL,
        statutory_regulation VARCHAR(100),
        acknowledgement_status VARCHAR(30) DEFAULT 'Pending',
        action_taken TEXT,
        FOREIGN KEY (sender_badge_id) REFERENCES personnel(badge_id)
    );
    """)

    # 5. Emergency Dispatches & Incident Actions (Console Action Logs)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_dispatches (
        dispatch_id VARCHAR(30) PRIMARY KEY,
        timestamp DATETIME NOT NULL,
        defcon_level VARCHAR(20) NOT NULL,
        trigger_node VARCHAR(20),
        trigger_metric VARCHAR(100),
        observed_value REAL,
        threshold_value REAL,
        dispatched_team VARCHAR(100),
        action_type VARCHAR(50),
        comm_channel VARCHAR(100),
        incident_commander VARCHAR(100),
        evac_status VARCHAR(50),
        FOREIGN KEY (trigger_node) REFERENCES sensors(sensor_id)
    );
    """)

    # 6. Audit Trail & Access Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        badge_id VARCHAR(20),
        action VARCHAR(100) NOT NULL,
        module VARCHAR(50) NOT NULL,
        details TEXT,
        ip_address VARCHAR(45) DEFAULT '192.168.4.101',
        FOREIGN KEY (badge_id) REFERENCES personnel(badge_id)
    );
    """)

    # Create Indexes for fast querying
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_sensor_time ON sensor_telemetry (sensor_id, timestamp);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_risk ON sensor_telemetry (risk_level);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_corr_time ON safety_correspondence (timestamp);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_corr_cat ON safety_correspondence (category);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_dispatch_time ON emergency_dispatches (timestamp);")

    conn.commit()
    return conn

def seed_reference_data(conn):
    cursor = conn.cursor()

    # Seed Sensors (Fleet matching home.html and sensor_dataset N001-N020)
    sensors = [
        ('N001', 'MPBX-01 [Multipoint Extensometer]', 'Extensometer', 'Sector 04 Longwall North', 'Borehole P-01 • Face Rib Line', -120.0, -23.7366, 148.2022, '868 MHz LoRa • 5m Tick', 'Mesh 01', 'Active'),
        ('N002', 'MPBX-02 [Multipoint Extensometer]', 'Extensometer', 'Sector 04 Longwall North', 'Borehole P-02 • Central Gate', -115.0, -23.7368, 148.2030, '868 MHz LoRa • 5m Tick', 'Mesh 01', 'Active'),
        ('N003', 'MPBX-03 [Multipoint Extensometer]', 'Extensometer', 'Sector 04 Longwall North', 'Borehole P-03 • Tailgate Heading', -130.0, -23.7371, 148.2038, '868 MHz LoRa • 5m Tick', 'Mesh 01', 'Active'),
        ('N004', 'MPBX-04 [Multipoint Extensometer]', 'Extensometer', 'Sector 04 Longwall North', 'Borehole P-04B • Critical Rib Sec 4-B', -125.0, -23.7375, 148.2045, '868 MHz LoRa • 1s Tick', 'Mesh 01', 'Critical Alert'),
        ('N005', 'TLT-01 [Biaxial Tiltmeter Array]', 'Tiltmeter', 'Shaft Sector 04 Central', 'Main Hoist Substation Slab', 0.0, -23.7360, 148.2015, '868 MHz LoRa • 5m Tick', 'Mesh 03', 'Active'),
        ('N006', 'TLT-02 [Biaxial Tiltmeter Array]', 'Tiltmeter', 'Sector 04 Portal Slope', 'Portal Slope Anchor Incline', 0.0, -23.7358, 148.2025, '868 MHz LoRa • 5m Tick', 'Mesh 03', 'High Risk'),
        ('N007', 'VIB-01 [Geophone Triaxial Array]', 'Geophone', 'Sub-level 420m Gallery', 'Shaft Crosscut Pillar 12', -420.0, -23.7380, 148.2050, 'LoRaWAN 868 MHz', 'Mesh 02', 'Active'),
        ('N008', 'VIB-02 [Geophone Triaxial Array]', 'Geophone', 'Sub-level 420m Gallery', 'Shaft Crosscut Pillar 14', -420.0, -23.7384, 148.2058, 'LoRaWAN 868 MHz', 'Mesh 02', 'Active'),
        ('N009', 'CRK-01 [Optical Crack Extensometer]', 'Crack Sensor', 'Extraction Return Airway', 'Overburden Concrete Lining Sec C', -210.0, -23.7369, 148.2062, 'Sub-GHz Mesh', 'Mesh 02', 'Active'),
        ('N010', 'CRK-02 [Optical Crack Extensometer]', 'Crack Sensor', 'Extraction Return Airway', 'Overburden Concrete Lining Sec D', -215.0, -23.7374, 148.2068, 'Sub-GHz Mesh', 'Mesh 02', 'Active'),
        ('N011', 'GNSS-09 [Kinematic Surface Rover]', 'GNSS RTK', 'Surface Crown Pillar Crest', 'Crown Pillar Crest Post 09', 4.5, -23.7350, 148.2070, 'UHF RTK • 1s Tick', 'Mesh 04', 'Active'),
        ('N012', 'GNSS-10 [Kinematic Surface Rover]', 'GNSS RTK', 'Surface North Embankment', 'Embankment Benchmark 10', 4.5, -23.7345, 148.2080, 'UHF RTK • 1s Tick', 'Mesh 04', 'Active'),
        ('N013', 'PZ-07 [VW Hydraulic Piezometer]', 'Piezometer', 'Confined Aquifer Zone', 'Borehole P-01 Aquifer Depressurizing', -88.5, -23.7390, 148.2010, 'Vibrating Wire', 'Mesh 02', 'Active'),
        ('N014', 'PZ-08 [VW Hydraulic Piezometer]', 'Piezometer', 'Confined Aquifer Zone', 'Borehole P-02 Strata Dewatering', -92.0, -23.7395, 148.2018, 'Vibrating Wire', 'Mesh 02', 'Active'),
        ('N015', 'STR-01 [Fiber Strain Gauge]', 'Fiber Strain', 'Underground Haulage Road', 'Support Arch Steelwork Beam 45', -380.0, -23.7382, 148.2040, 'Fiber Optic FBG', 'Mesh 01', 'Active'),
        ('N016', 'STR-02 [Fiber Strain Gauge]', 'Fiber Strain', 'Underground Haulage Road', 'Support Arch Steelwork Beam 52', -380.0, -23.7386, 148.2046, 'Fiber Optic FBG', 'Mesh 01', 'Active'),
        ('N017', 'RAD-01 [InSAR Ground Radar Point]', 'InSAR Radar', 'Surface Open Slope', 'Slope Face Bench B-3', 12.0, -23.7340, 148.2035, 'Ku-Band Radar', 'Mesh 04', 'Active'),
        ('N018', 'RAD-02 [InSAR Ground Radar Point]', 'InSAR Radar', 'Surface Open Slope', 'Slope Face Bench B-4', 12.0, -23.7335, 148.2045, 'Ku-Band Radar', 'Mesh 04', 'Active'),
        ('N019', 'US-01 [Ultrasonic Convergence]', 'Ultrasonic', 'Longwall Tailgate Heading', 'Roof-to-Floor Convergence Station', -420.0, -23.7388, 148.2072, 'LoRaWAN 868 MHz', 'Mesh 01', 'Active'),
        ('N020', 'US-02 [Ultrasonic Convergence]', 'Ultrasonic', 'Longwall Maingate Heading', 'Roof-to-Floor Convergence Station', -420.0, -23.7392, 148.2080, 'LoRaWAN 868 MHz', 'Mesh 01', 'Active')
    ]

    cursor.executemany("""
    INSERT OR REPLACE INTO sensors (sensor_id, name, sensor_type, sector, location_desc, depth_m, latitude, longitude, frequency, mesh_network, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, sensors)

    # Seed Personnel (Authorized engineers and safety officers from admin.html and emergency.html)
    personnel = [
        ('TS-8841', 'Dr. Marcus Vance', 'Chief Geotechnical Engineer', 'Strata Mechanics & Sub-Surface Geodesy', 'Sector 04 Longwall North (Shaft 04)', 'm.vance@terrasync-geo.com', 'Level 4 (Full Command)', 'UHF Tac Channel 04', 'Active'),
        ('TS-9014', 'Elena Rostova', 'Senior Seismologist & Analyst', 'Micro-Seismic Monitoring & Waveform Inversion', 'Sector 04 Fault Zone East', 'e.rostova@terrasync-geo.com', 'Level 3 (Model Calibration)', 'UHF Repeater 04-B', 'Active'),
        ('TS-4310', 'Tariq Al-Mansoor', 'Mine Operations Superintendent', 'Sub-Terra Operations & Personnel Safety', 'Shaft 04 / Central Gallery', 't.mansoor@terrasync-geo.com', 'Level 4 (Emergency Override)', '1-800-MINE-SAFE (Ext 401)', 'Active'),
        ('TS-6629', 'Sarah Jenkins', 'Telemetry & LoRa Systems Tech', 'Sub-GHz Telemetry Infrastructure', 'Relay Nodes North 01-16', 's.jenkins@terrasync-geo.com', 'Level 2 (Hardware & OTA)', 'Mesh Operations Net 2', 'Active'),
        ('MS-092', 'Marcus Sterling, PE', 'Geotechnical Safety Director', 'Mine Geotechnical & Safety Team', 'Portal B North Station', 'm.sterling@coalmine-safety.gov.in', 'Level 4 (Directorate Auth)', 'Direct PTT Tactical Radio', 'Active'),
        ('ERT-701', 'Capt. D. Vance', 'Emergency Response Commander', 'ERT Squadron Alpha-7 & Flight Paramedics', 'Shaft 04 Surface Hoist Building', 'ert-alpha7@coalmine-safety.org', 'Level 4 (Extraction Incident Cmd)', 'VHF Tac-1 (154.280 MHz)', 'Active')
    ]

    cursor.executemany("""
    INSERT OR REPLACE INTO personnel (badge_id, name, role, department, sector_assigned, email, clearance_level, tactical_comm_channel, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, personnel)

    # Seed Safety & Regulatory Correspondence Records (DGMS, Incident Orders, Landowner & Environmental Notices)
    correspondence = [
        (
            'CORR-2026-08-001',
            '2026-08-29 08:30:00',
            'DGMS Regulatory Notice',
            'Priority',
            'MS-092',
            'Directorate General of Mines Safety (DGMS) Eastern Zone',
            'Statutory Baseline Filing: Continuous Real-Time Subsidence Monitoring Deployment',
            'Form-IV Submission under Coal Mines Regulations (CMR) 2017 Regulation 111. 20 multi-parameter sensors online in Sector 04 Longwall extraction panel. LoRaWAN telemetry operating at 99.8% mesh reliability.',
            'CMR 2017 Reg 111 & 112',
            'Acknowledged',
            'Official acknowledgment receipt #DGMS/EZ/SUB/2026/894 received and archived.'
        ),
        (
            'CORR-2026-08-002',
            '2026-08-29 14:15:00',
            'Inter-shift Safety Memo',
            'Routine',
            'TS-8841',
            'Underground Shift Supervisors & Strata Control Cell',
            'Convergence Baseline Threshold Confirmation for Shaft 04 Ribs',
            'All sensor baselines verified. Rate of displacement normal (<0.5 mm/day). Threshold set to 10.0 mm critical displacement. Isolation Forest anomaly scoring enabled.',
            'Internal Safety SOP-GEO-04',
            'Acknowledged',
            'Signed off by Shift Engineers Shift A, B, and C.'
        ),
        (
            'CORR-2026-08-30 02:45:00',
            '2026-08-30 02:45:00',
            'Subsidence Incident Warning',
            'Critical Urgent',
            'TS-8841',
            'Mine Operations Superintendent Tariq Al-Mansoor & DGMS Inspectorate',
            'CRITICAL SUBSIDENCE ALERT: Accelerated Convergence Rate Exceeds Envelope (Node N004 / MPBX-04)',
            'Urgent notification: MPBX-04 borehole extensometer registered abnormal rate of strain (+6.2 mm/day) and displacement exceeding 100mm threshold. Inverse velocity singularity solver indicates impending strata tensile cracking in rib sector 4-B.',
            'CMR 2017 Reg 115 (Danger from Fall of Ground)',
            'Action Taken',
            'Emergency Protocol Level 3 activated. Automatic acoustic siren countdown triggered.'
        ),
        (
            'CORR-2026-08-30 03:00:00',
            '2026-08-30 03:00:00',
            'Evacuation Directive',
            'Critical Urgent',
            'MS-092',
            'ERT Squadron Alpha-7, Sector 04 Field Safety Marshals, Hoist Operators',
            'EVACUATION ORDER: Sector 04 Sub-level 420m Withdrawal to Refuge Chamber 04',
            'Immediate evacuation ordered for 14 RFID-tagged miners in Sector 04 Longwall Face. Cage Capsule 02 mobilized. Medical trauma flight placed on standby at Surface North Pad.',
            'Disaster Management Plan Section 6.2',
            'Action Taken',
            'All 14 underground personnel successfully mustered in Refuge Chamber 04 at 03:22 UTC. Zero casualties reported.'
        ),
        (
            'CORR-2026-08-30 09:15:00',
            '2026-08-30 09:15:00',
            'Landowner & Surface Audit Notice',
            'Routine',
            'TS-4310',
            'District Revenue Officer & Mine Subsidence Compensation Board',
            'Surface Subsidence Profile Report - Crown Pillar Section & Agricultural Perimeter',
            'Sub-surface displacement of 138.4mm localized underground; surface GNSS-09 Kinematic base confirms surface deflection constrained to 4.2mm. No surface agrarian or railway infrastructure damage observed.',
            'Mine Subsidence Compensation Act Sec 14',
            'Pending',
            'Surface survey team deployed with Terrestrial LiDAR scanner for verification.'
        )
    ]

    cursor.executemany("""
    INSERT OR REPLACE INTO safety_correspondence (
        correspondence_id, timestamp, category, urgency_level, sender_badge_id, recipient,
        subject, body_content, statutory_regulation, acknowledgement_status, action_taken
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, correspondence)

    # Seed Emergency Dispatches
    dispatches = [
        (
            'DISP-2026-001',
            '2026-08-30 02:46:12',
            'DEFCON LEVEL 3',
            'N004',
            'Extensometer Rib Displacement',
            138.4,
            100.0,
            'Mine Geotechnical & Safety Team',
            'Direct PTT Call & Radio Broadcast',
            'UHF Channel 04 (Sub-surface Tac)',
            'Marcus Sterling, PE',
            'Evac in Progress'
        ),
        (
            'DISP-2026-002',
            '2026-08-30 02:47:30',
            'DEFCON LEVEL 3',
            'N004',
            'Acoustic Siren Activation',
            138.4,
            100.0,
            'Underground Horns & Surface Strobe',
            'Autonomous Siren Strobe Broadcast',
            'Sub-surface Mesh Tone 140dB',
            'Autonomous Control Kernel',
            'Siren Sounded'
        ),
        (
            'DISP-2026-003',
            '2026-08-30 02:50:00',
            'DEFCON LEVEL 3',
            'N004',
            'ERT Extraction Unit Mobilization',
            138.4,
            100.0,
            'ERT Squadron Alpha-7 & Flight Paramedics',
            'Mobilize Capsule Rig C-2',
            'VHF Tac-1 (154.280 MHz)',
            'Capt. D. Vance',
            'Chamber 04 Secured'
        )
    ]

    cursor.executemany("""
    INSERT OR REPLACE INTO emergency_dispatches (
        dispatch_id, timestamp, defcon_level, trigger_node, trigger_metric, observed_value,
        threshold_value, dispatched_team, action_type, comm_channel, incident_commander, evac_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, dispatches)

    # Seed Audit Logs
    audit_logs = [
        ('TS-8841', 'Model Inference Run (GEO-RBF-LSTM & Isolation Forest)', 'Live Dashboard', 'Trained on 5,760 samples, contamination=0.40. Anomaly flag rate 40%.', '192.168.4.12'),
        ('TS-4310', 'Emergency Evacuation Broadcast Triggered', 'Emergency Console', 'Broadcasted Level 3 audio/visual strobe across Sector 04.', '192.168.4.15'),
        ('TS-9014', 'Risk Boundary Recalibration', 'Admin & Config', 'Critical displacement set to 10.0mm; normalization weights updated.', '192.168.4.22'),
        ('MS-092', 'Statutory DGMS Notice Filing Dispatched', 'Correspondence Engine', 'Dispatched Form-IV notification to DGMS Inspectorate.', '192.168.4.10')
    ]

    cursor.executemany("""
    INSERT INTO audit_logs (badge_id, action, module, details, ip_address)
    VALUES (?, ?, ?, ?, ?);
    """, audit_logs)

    conn.commit()

def ingest_csv_telemetry(conn):
    cursor = conn.cursor()
    workspace_dir = os.path.dirname(__file__)

    raw_path = os.path.join(workspace_dir, "mine_subsidence_sensor_dataset.csv")
    risk_path = os.path.join(workspace_dir, "risk_result.csv")

    if not os.path.exists(raw_path) or not os.path.exists(risk_path):
        print(f"Error: Missing CSV files at {workspace_dir}")
        return

    print("Loading CSV files into pandas DataFrames...")
    df_raw = pd.read_csv(raw_path)
    df_risk = pd.read_csv(risk_path)

    # Merge/correspond row-by-row
    # df_raw contains: timestamp, sensor_id, tilt, displacement, vibration, crack_width
    # df_risk contains: Sl.No, tilt, displacement, vibration, crack_width, prediction, status,
    #                   Tilt_change, vibration_change, crack_width_change, Future displacement,
    #                   risk_percentage, risk_level

    print(f"Ingesting {len(df_raw)} corresponding telemetry records...")

    merged_data = []
    for i in range(len(df_raw)):
        raw_row = df_raw.iloc[i]
        risk_row = df_risk.iloc[i]

        merged_data.append((
            int(risk_row["Sl.No"]) if "Sl.No" in risk_row and not pd.isna(risk_row["Sl.No"]) else (i + 1),
            str(raw_row["timestamp"]),
            str(raw_row["sensor_id"]),
            float(raw_row["tilt"]),
            float(raw_row["displacement"]),
            float(raw_row["vibration"]),
            float(raw_row["crack_width"]),
            float(risk_row["Tilt_change"]) if not pd.isna(risk_row["Tilt_change"]) else None,
            float(risk_row["vibration_change"]) if not pd.isna(risk_row["vibration_change"]) else None,
            float(risk_row["crack_width_change"]) if not pd.isna(risk_row["crack_width_change"]) else None,
            float(risk_row["Future displacement"]) if not pd.isna(risk_row["Future displacement"]) else None,
            int(risk_row["prediction"]) if not pd.isna(risk_row["prediction"]) else 1,
            str(risk_row["status"]) if not pd.isna(risk_row["status"]) else "Normal",
            float(risk_row["risk_percentage"]) if not pd.isna(risk_row["risk_percentage"]) else 0.0,
            str(risk_row["risk_level"]) if not pd.isna(risk_row["risk_level"]) else "low"
        ))

    cursor.executemany("""
    INSERT OR REPLACE INTO sensor_telemetry (
        id, timestamp, sensor_id, tilt, displacement, vibration, crack_width,
        tilt_change, vibration_change, crack_width_change, future_displacement,
        anomaly_prediction, anomaly_status, risk_percentage, risk_level
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, merged_data)

    conn.commit()
    print(f"Successfully ingested {len(merged_data)} rows into sensor_telemetry table.")

def export_to_sql_dump(conn):
    print("Exporting database schema and data to correspondence_database.sql...")
    with open(SQL_EXPORT_PATH, "w", encoding="utf-8") as f:
        f.write("-- ==================================================================\n")
        f.write("-- Coal Mine Subsidence Monitoring & Safety System\n")
        f.write("-- Comprehensive Relational Correspondence Database Export (SQL DDL + DML)\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-- Supports: SQLite, PostgreSQL (compatible), MySQL, PostGIS\n")
        f.write("-- ==================================================================\n\n")

        for line in conn.iterdump():
            f.write(f"{line}\n")
    print(f"Export completed: {SQL_EXPORT_PATH}")

if __name__ == "__main__":
    print("Initializing Database...")
    conn = create_database()
    print("Seeding sensor fleet, personnel, correspondence, and emergency dispatches...")
    seed_reference_data(conn)
    print("Ingesting telemetry datasets...")
    ingest_csv_telemetry(conn)
    print("Exporting SQL dump...")
    export_to_sql_dump(conn)
    conn.close()
    print("Database build complete: coal_mine_subsidence.db")
