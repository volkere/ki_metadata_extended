# Erweiterte KI-Metadaten-Analyse

Ein fortschrittliches System zur automatischen Bildanalyse mit KI-gestützter Metadatenextraktion.

## 🚀 Features

- **FastAPI Backend** mit DeepFace und CLIP Integration
- **Streamlit UI** mit interaktiver Zeitachsen-Ansicht und Statistiken
- **Neo4j Graph Database** für Metadaten-Speicherung
- **minIO** für skalierbare Bildspeicherung
- **Umfassendes Logging** von Uploads und Analysen
- **Robuste Fehlerbehandlung** und Validierung

## 🛠️ Technologie-Stack

- **Backend**: FastAPI, Uvicorn
- **AI/ML**: DeepFace, CLIP (OpenAI), Transformers
- **Database**: Neo4j Graph Database
- **Storage**: minIO Object Storage
- **Frontend**: Streamlit, Plotly
- **Container**: Docker & Docker Compose

## 📋 Voraussetzungen

- Docker und Docker Compose
- Mindestens 4GB RAM (für ML-Modelle)
- Internetverbindung (für initiale Modell-Downloads)

## 🚀 Installation & Start

1. **Repository klonen:**
```bash
git clone <repository-url>
cd ki_metadata_extended
```

2. **Services starten:**
```bash
docker-compose up --build
```

3. **Services sind verfügbar unter:**
- **API Documentation**: http://localhost:8000/docs
- **Streamlit UI**: http://localhost:8501
- **Neo4j Browser**: http://localhost:7474 (neo4j / password)
- **minIO Console**: http://localhost:9001 (minioadmin / minioadmin)

## 📖 API Verwendung

### Bild-Upload
```bash
curl -X POST "http://localhost:8000/upload/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg"
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs abrufen
```bash
curl http://localhost:8000/logs/uploads
curl http://localhost:8000/logs/analysis
```

## 🔧 Konfiguration

### Umgebungsvariablen
Die Standard-Konfiguration ist in `docker-compose.yml` definiert:

- **Neo4j**: neo4j/password
- **minIO**: minioadmin/minioadmin
- **Ports**: 8000 (API), 8501 (Streamlit), 7474 (Neo4j), 9001 (minIO)

### Daten-Persistierung
- Neo4j Daten: `./neo4j-data/`
- minIO Daten: `./minio-data/`
- Logs: `./logs/`

## 📊 Funktionalitäten

### Bildanalyse
- **CLIP-basierte Bildklassifizierung** (Foto, Person, Performance)
- **DeepFace Gesichtsanalyse** (Alter, Geschlecht)
- **Automatische Metadatenextraktion**

### Visualisierung
- **Interaktive Timeline** der Analysen
- **Statistiken** zu Alters- und Geschlechterverteilung
- **Echtzeit-Updates** der Daten

### Datenmanagement
- **Graph-basierte Metadaten-Speicherung** in Neo4j
- **Skalierbare Bildspeicherung** in minIO
- **Umfassendes Logging** aller Operationen

## 🐛 Troubleshooting

### Häufige Probleme

1. **Port-Konflikte**: Stellen Sie sicher, dass die Ports 8000, 8501, 7474, 9001 frei sind
2. **Speicherplatz**: ML-Modelle benötigen ~2GB Speicherplatz
3. **RAM**: Mindestens 4GB RAM für stabile Performance

### Logs überprüfen
```bash
# Container-Logs
docker-compose logs app
docker-compose logs streamlit

# Anwendungs-Logs
docker-compose exec app cat /logs/analysis.log
docker-compose exec app cat /logs/uploads.log
```

## 🔄 Entwicklung

### Lokale Entwicklung
```bash
# Dependencies installieren
pip install -r requirements.txt

# Services einzeln starten
docker-compose up neo4j minio
python -m uvicorn app.main:app --reload
streamlit run streamlit_app/main.py
```

### Code-Struktur
```
ki_metadata_extended/
├── app/
│   ├── main.py              # FastAPI Application
│   ├── pipeline/
│   │   └── process_image.py # Bildverarbeitung
│   └── utils/
│       └── logger.py        # Logging Utilities
├── streamlit_app/
│   └── main.py              # Streamlit UI
├── docker-compose.yml       # Service-Konfiguration
├── Dockerfile              # Container-Build
└── requirements.txt        # Python Dependencies
```

## 📝 Lizenz

Dieses Projekt ist für Bildungs- und Forschungszwecke konzipiert.

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Committe deine Änderungen
4. Push zum Branch
5. Erstelle einen Pull Request

## 📞 Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue im Repository.
