# XLIFF Editor

A modern, web-based XLIFF file editor with support for XLIFF 1.2 and XLZ (zipped XLIFF with skeleton) formats. Edit translation units while preserving XML tags and file structure.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)

## ✨ Features

- 📁 **Multiple Format Support**: XLIFF 1.2 and XLZ (zipped with skeleton files)
- 🔒 **Tag Protection**: Edit translation text while keeping XML tags locked
- 🌲 **Structure Viewer**: Visual tree representation of file hierarchy
- 🔍 **Search & Filter**: Quick search across all translation units
- 📊 **Statistics**: View word counts, completion status, and file metrics
- 🎯 **Inline Tag Display**: Visual representation of formatting tags
- 💾 **Export**: Download modified files in original format

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:5173` (or `http://localhost:3000`)

## 📁 Project Structure

```
xliff-editor/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── xliff_parser.py         # XLIFF parsing logic
│   ├── xlz_handler.py          # XLZ format handler
│   ├── requirements.txt        # Python dependencies
│   └── README.md              # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── main.jsx           # Application entry
│   │   └── index.css          # Tailwind CSS
│   ├── package.json
│   └── README.md              # Frontend documentation
└── README.md                  # This file
```

## 🎯 Usage

### 1. Upload XLIFF File

- Click "Choose File" button
- Select an XLIFF (.xlf, .xliff) or XLZ file
- File structure appears in left panel

### 2. Navigate Structure

- Click file names to expand/collapse
- Click translation units to view details
- Use search box to filter units

### 3. Edit Translation

- Select a translation unit
- Edit target text in the editor
- Tags are highlighted and protected
- Changes are tracked automatically

### 4. Export Modified File (in progress)

- Click "Export XLIFF" button
- File downloads in original format
- All tags and structure preserved

## 🔧 API Endpoints

### Upload File
```http
POST /api/upload
Content-Type: multipart/form-data

Response: {
  "files": [...],
  "stats": {...}
}
```

### Get Parsed Data
```http
GET /api/xliff/{file_id}

Response: {
  "files": [...],
  "stats": {...}
}
```

### Update Translation Unit
```http
PUT /api/xliff/{file_id}/files/{file_index}/trans-units/{tu_index}
Content-Type: application/json

{
  "target": "Updated translation text with ⟨tags⟩"
}
```

### Export File
```http
GET /api/export/{file_id}

Response: File download (XLIFF or XLZ)
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **lxml**: Powerful XML processing
- **uvicorn**: ASGI server
- **python-multipart**: File upload handling

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS
- **Lucide React**: Icon library

## 📋 Supported XLIFF Features

### XLIFF 1.2
- ✅ Single and multi-file documents
- ✅ Translation units with source/target
- ✅ Inline tags (bpt, ept, ph, g, x, it)
- ✅ Attributes preservation
- ✅ Group nesting
- ✅ File metadata

### XLZ Format
- ✅ Skeleton file preservation
- ✅ Content extraction and merging
- ✅ ZIP archive handling
- ✅ Multi-file support within archive

### Tag Types Supported
- `<bpt>` / `<ept>`: Begin/End paired tags
- `<ph>`: Placeholder tags
- `<g>`: Generic grouping tags
- `<x>`: Standalone tags
- `<it>`: Isolated tags

## 🔍 How It Works

### File Parsing Process

1. **Upload**: File received and stored in memory
2. **Detection**: Automatic format detection (XLIFF vs XLZ)
3. **Parsing**: XML parsing with namespace handling
4. **Tag Extraction**: Inline tags converted to markers (⟨tag⟩)
5. **Structure Building**: Hierarchical tree of files and units
6. **Storage**: In-memory storage with unique file ID

### Tag Protection

Tags are extracted and replaced with visual markers:
- Original: `<g id="1">Hello</g> World <x id="2"/>`
- Displayed: `⟨g-1⟩Hello⟨/g-1⟩ World ⟨x-2⟩`
- Tags remain protected during editing
- Original XML structure preserved on export

## 🚀 Deployment

### Backend (Production)

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Production)

```bash
# Build for production
npm run build

# Serve with any static server
# Output in dist/ directory
```

### Docker Support

Coming soon! Full Docker and docker-compose setup.

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📝 Development Roadmap

- [ ] XLIFF 2.0 support
- [ ] Database persistence (PostgreSQL)
- [ ] User authentication
- [ ] Real-time collaboration
- [ ] Translation memory integration
- [ ] Quality assurance checks
- [ ] Batch file processing
- [ ] Docker deployment
- [ ] Cloud storage integration

## 🐛 Known Issues

- Large files (>100MB) may cause performance issues
- Some complex XLIFF variants may not parse correctly
- In-memory storage means data loss on server restart

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**German** - Senior Software Engineer
- 20+ years in software development
- Expert in localization engineering
- Based in Dublin, Ireland

## 🙏 Acknowledgments

- Built with modern Python and React patterns
- Inspired by professional CAT tools
- Designed for localization professionals

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation in `/backend/README.md` and `/frontend/README.md`

---

**Made with ❤️ for the localization community**
