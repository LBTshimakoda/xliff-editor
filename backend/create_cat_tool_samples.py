"""
Create sample XLIFF files for different CAT tools
"""

import os

def create_sdlxliff_sample():
    """Create SDL Trados SDLXLIFF sample"""
    content = """<?xml version="1.0" encoding="utf-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2" xmlns:sdl="http://sdl.com/FileTypes/SdlXliff/1.0">
  <file original="sample.docx" source-language="en-US" target-language="de-DE" datatype="x-sdlfilterframework2">
    <header>
      <sdl:filetype-id>SDL Generic Filetype</sdl:filetype-id>
    </header>
    <body>
      <trans-unit id="1" sdl:seg-defs="1">
        <source>Welcome to <bpt id="1" ctype="bold">&lt;b&gt;</bpt>SDL Trados<ept id="1">&lt;/b&gt;</ept> Studio.</source>
        <target state="translated">Willkommen bei <bpt id="1" ctype="bold">&lt;b&gt;</bpt>SDL Trados<ept id="1">&lt;/b&gt;</ept> Studio.</target>
        <sdl:seg-defs>
          <sdl:seg id="1" conf="Translated" origin="tm"/>
        </sdl:seg-defs>
      </trans-unit>
      
      <trans-unit id="2" sdl:seg-defs="2">
        <source>Please save your work before <ph id="1" ctype="x-link">{closing}</ph> the application.</source>
        <target state="needs-translation"></target>
        <sdl:seg-defs>
          <sdl:seg id="2" conf="Draft"/>
        </sdl:seg-defs>
      </trans-unit>
      
      <trans-unit id="3" sdl:seg-defs="3" translate="no">
        <source>API_KEY_12345</source>
        <target>API_KEY_12345</target>
        <sdl:seg-defs>
          <sdl:seg id="3" conf="Unspecified" locked="true"/>
        </sdl:seg-defs>
      </trans-unit>
      
      <trans-unit id="4">
        <source>The <bpt id="2" ctype="italic">&lt;i&gt;</bpt>quick brown fox<ept id="2">&lt;/i&gt;</ept> jumps over the lazy dog.</source>
        <target state="translated">Der <bpt id="2" ctype="italic">&lt;i&gt;</bpt>schnelle braune Fuchs<ept id="2">&lt;/i&gt;</ept> springt über den faulen Hund.</target>
      </trans-unit>
    </body>
  </file>
</xliff>"""
    
    with open('sample_sdlxliff.sdlxliff', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created sample_sdlxliff.sdlxliff")

def create_phrase_sample():
    """Create Phrase (Memsource) XLIFF sample"""
    content = """<?xml version="1.0" encoding="UTF-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2" xmlns:m="http://www.memsource.com/mxlf/2.0">
  <file original="document.docx" source-language="en" target-language="fr" datatype="x-text/x-msdoc" m:documentId="abc123">
    <header>
      <m:project-id>proj_456</m:project-id>
      <m:job-id>job_789</m:job-id>
    </header>
    <body>
      <trans-unit id="1" m:confirmed="false" m:locked="false">
        <source>Welcome to <bpt id="1" ctype="bold">&lt;b&gt;</bpt>Phrase<ept id="1">&lt;/b&gt;</ept> platform.</source>
        <target state="translated" m:score="100">Bienvenue sur la plateforme <bpt id="1" ctype="bold">&lt;b&gt;</bpt>Phrase<ept id="1">&lt;/b&gt;</ept>.</target>
        <note>Translation from TM</note>
      </trans-unit>
      
      <trans-unit id="2" m:confirmed="true" m:locked="false">
        <source>Click <ph id="1" ctype="x-button">{button}</ph> to continue.</source>
        <target state="final">Cliquez sur <ph id="1" ctype="x-button">{button}</ph> pour continuer.</target>
      </trans-unit>
      
      <trans-unit id="3" m:confirmed="false" m:locked="false">
        <source>Your <bpt id="2" ctype="underline">&lt;u&gt;</bpt>account settings<ept id="2">&lt;/u&gt;</ept> have been updated.</source>
        <target state="needs-review-translation">Vos <bpt id="2" ctype="underline">&lt;u&gt;</bpt>paramètres de compte<ept id="2">&lt;/u&gt;</ept> ont été mis à jour.</target>
      </trans-unit>
      
      <trans-unit id="4">
        <source>Processing <ph id="3" ctype="x-variable">{count}</ph> items...</source>
        <target state="new"></target>
        <note>Untranslated</note>
      </trans-unit>
    </body>
  </file>
</xliff>"""
    
    with open('sample_phrase.xliff', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created sample_phrase.xliff")

def create_memoq_sample():
    """Create memoQ XLIFF sample"""
    content = """<?xml version="1.0" encoding="utf-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2" xmlns:mq="MQXliff">
  <file original="project.docx" source-language="en-GB" target-language="es-ES" datatype="x-mqdocument" mq:version="8.5">
    <header>
      <mq:meta>
        <mq:project-name>Marketing Campaign</mq:project-name>
        <mq:document-id>doc_001</mq:document-id>
      </mq:meta>
    </header>
    <body>
      <trans-unit id="1" mq:status="Confirmed">
        <source>Welcome to <bpt id="1" ctype="bold">&lt;b&gt;</bpt>memoQ<ept id="1">&lt;/b&gt;</ept> translation software.</source>
        <target state="signed-off">Bienvenido al software de traducción <bpt id="1" ctype="bold">&lt;b&gt;</bpt>memoQ<ept id="1">&lt;/b&gt;</ept>.</target>
        <mq:match-rate>102</mq:match-rate>
      </trans-unit>
      
      <trans-unit id="2" mq:status="Edited">
        <source>Please verify <ph id="1" ctype="x-field">{field_name}</ph> before submitting.</source>
        <target state="translated">Por favor, verifique <ph id="1" ctype="x-field">{field_name}</ph> antes de enviar.</target>
        <mq:match-rate>95</mq:match-rate>
      </trans-unit>
      
      <trans-unit id="3" mq:status="Locked">
        <source>COPYRIGHT_NOTICE_2024</source>
        <target>COPYRIGHT_NOTICE_2024</target>
        <note>Do not translate</note>
      </trans-unit>
      
      <trans-unit id="4" mq:status="Unconfirmed">
        <source>The <bpt id="2" ctype="italic">&lt;i&gt;</bpt>latest version<ept id="2">&lt;/i&gt;</ept> is now available.</source>
        <target state="needs-review-translation">La <bpt id="2" ctype="italic">&lt;i&gt;</bpt>última versión<ept id="2">&lt;/i&gt;</ept> ya está disponible.</target>
      </trans-unit>
      
      <trans-unit id="5">
        <source>Download now</source>
        <target state="new"></target>
      </trans-unit>
    </body>
  </file>
</xliff>"""
    
    with open('sample_memoq.xliff', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created sample_memoq.xliff")

def create_test_script():
    """Create test script for all CAT tool formats"""
    content = """#!/usr/bin/env python
\"\"\"
Test script for CAT tool XLIFF formats
\"\"\"

from xliff_parser import XliffParser
import sys

def test_cat_tool_file(filepath, tool_name):
    print("=" * 70)
    print(f"Testing {tool_name}: {filepath}")
    print("=" * 70)
    print()
    
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        document = XliffParser.parse_file(content)
        
        print(f"✓ Successfully parsed {tool_name} XLIFF")
        print(f"✓ Version: {document.version}")
        print(f"✓ Files: {len(document.files)}")
        print()
        
        for file_idx, xliff_file in enumerate(document.files):
            print(f"File {file_idx + 1}:")
            print(f"  Original: {xliff_file.original}")
            print(f"  Source: {xliff_file.source_language}")
            print(f"  Target: {xliff_file.target_language}")
            print(f"  Datatype: {xliff_file.datatype}")
            print(f"  Trans-units: {len(xliff_file.trans_units)}")
            print()
            
            # Show all trans-units
            for tu_idx, tu in enumerate(xliff_file.trans_units, 1):
                print(f"  Trans-unit {tu_idx} (ID: {tu.id}):")
                print(f"    Source: {tu.source.text[:80]}...")
                
                if tu.target:
                    print(f"    Target: {tu.target.text[:80]}...")
                    print(f"    State: {tu.state or 'N/A'}")
                else:
                    print(f"    Target: [Empty]")
                
                if tu.source.tags:
                    print(f"    Tags: {len(tu.source.tags)} ({', '.join(set(t.tag_type for t in tu.source.tags))})")
                
                if tu.notes:
                    print(f"    Notes: {', '.join(tu.notes)}")
                
                print()
        
        print(f"✓ {tool_name} test PASSED!")
        print()
        return True
        
    except Exception as e:
        print(f"✗ {tool_name} test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\\n" + "=" * 70)
    print("CAT Tool XLIFF Format Tests")
    print("=" * 70)
    print()
    
    results = {}
    
    # Test SDL Trados
    if os.path.exists('sample_sdlxliff.sdlxliff'):
        results['SDL Trados'] = test_cat_tool_file('sample_sdlxliff.sdlxliff', 'SDL Trados')
    
    # Test Phrase
    if os.path.exists('sample_phrase.xliff'):
        results['Phrase'] = test_cat_tool_file('sample_phrase.xliff', 'Phrase')
    
    # Test memoQ
    if os.path.exists('sample_memoq.xliff'):
        results['memoQ'] = test_cat_tool_file('sample_memoq.xliff', 'memoQ')
    
    # Summary
    print("=" * 70)
    print("Test Summary:")
    print("=" * 70)
    for tool, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{tool:20} {status}")
    print("=" * 70)
    
    # Exit code
    sys.exit(0 if all(results.values()) else 1)
"""
    
    with open('test_cat_tools.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created test_cat_tools.py")

if __name__ == "__main__":
    print("=" * 70)
    print("Creating CAT Tool Sample Files")
    print("=" * 70)
    print()
    
    create_sdlxliff_sample()
    create_phrase_sample()
    create_memoq_sample()
    create_test_script()
    
    print()
    print("=" * 70)
    print("✓ All sample files created!")
    print("=" * 70)
    print()
    print("To test:")
    print("  python test_cat_tools.py")
    print()
    print("Files created:")
    print("  - sample_sdlxliff.sdlxliff")
    print("  - sample_phrase.xliff")
    print("  - sample_memoq.xliff")
    print("  - test_cat_tools.py")