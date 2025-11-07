from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from models import XliffDocument, TransUnitUpdate
from xliff_parser import XliffParser
from xlz_handler import XLZHandler
from lxml import etree
import io

app = FastAPI(title="XLIFF Editor API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Store the current XML tree and skeleton files in memory
current_file_store = {}

@app.get("/")
async def root():
    return {"message": "XLIFF Editor API", "version": "1.0", "supports": ["xliff", "xlf", "xlz", "sdlxliff"]}

@app.post("/upload", response_model=XliffDocument)
async def upload_xliff(file: UploadFile = File(...)):
    """Upload and parse an XLIFF or XLZ file"""
    filename = file.filename.lower()
    
    # Check file extension (FIXED: added dot before sdlxliff)
    if not (filename.endswith(('.xliff', '.xlf', '.xlz', '.sdlxliff'))):
        raise HTTPException(
            status_code=400, 
            detail="File must be XLIFF (.xliff, .xlf, .sdlxliff) or XLZ (.xlz)"
        )
    
    try:
        content = await file.read()
        
        # Handle XLZ files
        if XLZHandler.is_xlz_file(filename):
            try:
                xliff_content, skeleton_files = XLZHandler.extract_xliff_from_xlz(content)
                
                # Store skeleton files for later download
                current_file_store['skeleton_files'] = skeleton_files
                current_file_store['is_xlz'] = True
                
                # Use extracted XLIFF content
                content = xliff_content
                
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error extracting XLZ: {str(e)}")
        else:
            current_file_store['is_xlz'] = False
            current_file_store['skeleton_files'] = {}
        
        # Store the original XML tree for later updates
        tree = etree.fromstring(content)
        current_file_store['tree'] = tree
        current_file_store['filename'] = file.filename  # Store original filename with correct case
        
        # Parse and return structured data
        document = XliffParser.parse_file(content)
        return document
        
    except etree.XMLSyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Invalid XLIFF XML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")

@app.get("/xlz/info")
async def get_xlz_info():
    """Get information about the currently loaded XLZ file"""
    if 'tree' not in current_file_store:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    return {
        "is_xlz": current_file_store.get('is_xlz', False),
        "filename": current_file_store.get('filename'),
        "skeleton_files": list(current_file_store.get('skeleton_files', {}).keys())
    }

@app.put("/trans-unit")
async def update_trans_unit(update: TransUnitUpdate):
    """Update a trans-unit's target translation"""
    if 'tree' not in current_file_store:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    try:
        updated_xml = XliffParser.update_trans_unit(
            current_file_store['tree'],
            update.file_index,
            update.trans_unit_id,
            update.target_text,
            update.target_tags
        )
        
        # Update stored tree
        current_file_store['tree'] = etree.fromstring(updated_xml)
        
        return {"message": "Trans-unit updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating trans-unit: {str(e)}")

@app.get("/download")
async def download_xliff():
    """Download the modified XLIFF file with original filename and extension"""
    if 'tree' not in current_file_store:
        raise HTTPException(status_code=400, detail="No file to download")
    
    try:
        xml_content = etree.tostring(
            current_file_store['tree'],
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=True
        )
        
        # Get original filename (preserves case and extension)
        filename = current_file_store.get('filename', 'modified.xliff')
        
        # If original was XLZ, recreate XLZ with skeleton files
        if current_file_store.get('is_xlz', False):
            skeleton_files = current_file_store.get('skeleton_files', {})
            xlz_content = XLZHandler.create_xlz_archive(xml_content, skeleton_files)
            
            # Ensure .xlz extension
            if not filename.lower().endswith('.xlz'):
                filename = filename.rsplit('.', 1)[0] + '.xlz'
            
            return Response(
                content=xlz_content,
                media_type='application/zip',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )
        
        # Return as XLIFF with appropriate media type based on extension
        filename_lower = filename.lower()
        if filename_lower.endswith('.sdlxliff'):
            media_type = 'application/x-sdlxliff+xml'
        else:
            media_type = 'application/x-xliff+xml'
        
        return Response(
            content=xml_content,
            media_type=media_type,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating download: {str(e)}")

@app.delete("/clear")
async def clear_current_file():
    """Clear the currently loaded file"""
    current_file_store.clear()
    return {"message": "File cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)