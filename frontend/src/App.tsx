import React, { useState, useEffect } from 'react';
import { Upload, Download, FileText, ChevronRight, ChevronDown, Lock } from 'lucide-react';

interface XliffTag {
  tag_type: string;
  id?: string;
  content?: string;
  attributes: Record<string, string>;
  position: number;
  ctype?: string;
  paired_with?: string;
}

interface SegmentContent {
  text: string;
  tags: XliffTag[];
}

interface TransUnit {
  id: string;
  source: SegmentContent;
  target?: SegmentContent;
  state?: string;
  notes: string[];
  attributes: Record<string, any>;
}

interface XliffFile {
  original: string;
  source_language: string;
  target_language?: string;
  datatype?: string;
  trans_units: TransUnit[];
}

interface XliffDocument {
  version: string;
  files: XliffFile[];
}

const API_BASE = 'http://localhost:8000';

export default function XliffEditor() {
  const [document, setDocument] = useState<XliffDocument | null>(null);
  const [selectedTransUnit, setSelectedTransUnit] = useState<{fileIndex: number, tuIndex: number} | null>(null);
  const [expandedFiles, setExpandedFiles] = useState<Set<number>>(new Set());
  const [uploading, setUploading] = useState(false);
  const [hideEmptySources, setHideEmptySources] = useState(true);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
        return;
      }

      const data: XliffDocument = await response.json();
      setDocument(data);
      setExpandedFiles(new Set([0]));
      
      if (file.name.toLowerCase().endsWith('.xlz')) {
        try {
          const xlzInfo = await fetch(`${API_BASE}/xlz/info`);
          if (xlzInfo.ok) {
            const info = await xlzInfo.json();
            console.log('XLZ Info:', info);
          }
        } catch (e) {
          console.log('Could not fetch XLZ info');
        }
      }
    } catch (error) {
      alert('Failed to upload file: ' + error);
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await fetch(`${API_BASE}/download`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'modified.xliff';
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert('Failed to download file: ' + error);
    }
  };

  const toggleFile = (index: number) => {
    const newExpanded = new Set(expandedFiles);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedFiles(newExpanded);
  };

  const getFilteredTransUnits = (transUnits: TransUnit[]) => {
    if (!hideEmptySources) return transUnits;
    return transUnits.filter(tu => tu.source?.text && tu.source.text.trim().length > 0);
  };

  useEffect(() => {
    const getAllFilteredTransUnits = () => {
      if (!document) return [];
      
      const allUnits: Array<{fileIndex: number, tuIndex: number, originalIndex: number}> = [];
      
      document.files.forEach((file, fileIndex) => {
        file.trans_units.forEach((tu, originalIndex) => {
          if (!hideEmptySources || (tu.source?.text && tu.source.text.trim().length > 0)) {
            allUnits.push({ fileIndex, tuIndex: allUnits.length, originalIndex });
          }
        });
      });
      
      return allUnits;
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (!document || !selectedTransUnit) return;
      
      const allUnits = getAllFilteredTransUnits();
      if (allUnits.length === 0) return;
      
      const currentIndex = allUnits.findIndex(
        u => u.fileIndex === selectedTransUnit.fileIndex && 
             u.originalIndex === selectedTransUnit.tuIndex
      );
      
      if (currentIndex === -1) return;
      
      let newIndex = currentIndex;
      
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        newIndex = Math.min(currentIndex + 1, allUnits.length - 1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        newIndex = Math.max(currentIndex - 1, 0);
      } else {
        return;
      }
      
      const newUnit = allUnits[newIndex];
      setSelectedTransUnit({ 
        fileIndex: newUnit.fileIndex, 
        tuIndex: newUnit.originalIndex 
      });
      
      setTimeout(() => {
        const element = globalThis.document.getElementById(`tu-${newUnit.fileIndex}-${newUnit.originalIndex}`);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      }, 50);
    };
    
    globalThis.window.addEventListener('keydown', handleKeyDown);
    return () => globalThis.window.removeEventListener('keydown', handleKeyDown);
  }, [document, selectedTransUnit, hideEmptySources]);

  const selectedTU = selectedTransUnit 
    ? document?.files[selectedTransUnit.fileIndex]?.trans_units[selectedTransUnit.tuIndex]
    : null;

  const renderTag = (tag: XliffTag) => {
    const getTagDisplay = () => {
      if (tag.tag_type === 'bpt') {
        return `<bpt>${tag.content || ''}`;
      } else if (tag.tag_type === 'ept') {
        return `</${tag.content || 'ept'}>`;
      } else if (tag.tag_type === 'ph') {
        return tag.content || `{${tag.id}}`;
      } else if (tag.content) {
        return `<${tag.tag_type}>${tag.content}</${tag.tag_type}>`;
      } else {
        return `<${tag.tag_type}/>`;
      }
    };

    const getTagColor = () => {
      if (tag.tag_type === 'bpt' || tag.tag_type === 'ept') {
        return 'bg-purple-100 text-purple-800 border-purple-300';
      } else if (tag.tag_type === 'ph') {
        return 'bg-green-100 text-green-800 border-green-300';
      } else {
        return 'bg-blue-100 text-blue-800 border-blue-300';
      }
    };

    const tagTitle = [
      `Type: ${tag.tag_type}`,
      tag.id ? `ID: ${tag.id}` : '',
      tag.ctype ? `Content Type: ${tag.ctype}` : '',
      tag.content ? `Content: ${tag.content}` : ''
    ].filter(Boolean).join('\n');

    return (
      <span
        key={`${tag.tag_type}-${tag.position}`}
        className={`inline-flex items-center px-2 py-0.5 mx-0.5 rounded text-xs font-mono border ${getTagColor()}`}
        title={tagTitle}
      >
        <Lock size={10} className="mr-1" />
        {getTagDisplay()}
        {tag.ctype && (
          <span className="ml-1 opacity-60 text-[10px]">
            [{tag.ctype}]
          </span>
        )}
      </span>
    );
  };

  const renderSegmentWithTags = (segment: SegmentContent | undefined) => {
    if (!segment) return <span className="text-gray-400 italic">No translation</span>;
    
    const parts = [];
    let lastPos = 0;
    
    const sortedTags = [...segment.tags].sort((a, b) => a.position - b.position);
    
    sortedTags.forEach((tag, idx) => {
      const textBefore = segment.text.slice(lastPos, tag.position);
      if (textBefore) {
        parts.push(<span key={`text-${idx}`}>{textBefore}</span>);
      }
      
      parts.push(renderTag(tag));
      
      const tagMarker = `⟨${tag.tag_type}⟩`;
      lastPos = tag.position + tagMarker.length;
    });
    
    const remainingText = segment.text.slice(lastPos);
    if (remainingText) {
      parts.push(<span key="text-end">{remainingText}</span>);
    }
    
    return <div className="flex flex-wrap items-center gap-1">{parts}</div>;
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">File Structure</h2>
          
          <label className="flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700 transition-colors mb-3">
            <Upload size={18} className="mr-2" />
            {uploading ? 'Uploading...' : 'Upload XLIFF/XLZ'}
            <input
              type="file"
              accept=".xliff,.xlf,.xlz"
              onChange={handleFileUpload}
              className="hidden"
              disabled={uploading}
            />
          </label>
          
          {document && (
            <label className="flex items-center text-sm text-gray-700 cursor-pointer hover:text-gray-900">
              <input
                type="checkbox"
                checked={hideEmptySources}
                onChange={(e) => setHideEmptySources(e.target.checked)}
                className="mr-2"
              />
              Hide empty sources
            </label>
          )}
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          {!document ? (
            <div className="text-center text-gray-500 mt-8">
              <FileText size={48} className="mx-auto mb-2 opacity-50" />
              <p>Upload an XLIFF file to begin</p>
            </div>
          ) : (
            <div className="space-y-2">
              {document.files.map((file, fileIdx) => (
                <div key={fileIdx} className="border border-gray-200 rounded-lg overflow-hidden">
                  <button
                    onClick={() => toggleFile(fileIdx)}
                    className="w-full px-3 py-2 bg-gray-50 hover:bg-gray-100 flex items-center justify-between text-sm font-medium text-gray-700"
                  >
                    <span className="flex items-center">
                      {expandedFiles.has(fileIdx) ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                      <span className="ml-2 truncate">{file.original}</span>
                    </span>
                    <span className="text-xs text-gray-500">
                      {hideEmptySources 
                        ? `${getFilteredTransUnits(file.trans_units).length}/${file.trans_units.length}`
                        : file.trans_units.length
                      }
                    </span>
                  </button>
                  
                  {expandedFiles.has(fileIdx) && (
                    <div className="bg-white">
                      {getFilteredTransUnits(file.trans_units).map((tu) => {
                        const tuIdx = file.trans_units.indexOf(tu);
                        return (
                          <button
                            key={tu.id}
                            id={`tu-${fileIdx}-${tuIdx}`}
                            onClick={() => setSelectedTransUnit({ fileIndex: fileIdx, tuIndex: tuIdx })}
                            className={`w-full px-4 py-2 text-left text-sm hover:bg-blue-50 border-t border-gray-100 ${
                              selectedTransUnit?.fileIndex === fileIdx && selectedTransUnit?.tuIndex === tuIdx
                                ? 'bg-blue-50 border-l-4 border-l-blue-500'
                                : ''
                            }`}
                          >
                            <div className="font-mono text-xs text-gray-500 mb-1">{tu.id}</div>
                            <div className="text-gray-700 truncate">{tu.source.text.replace(/⟨[^⟩]+⟩/g, '')}</div>
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {document && (
          <div className="p-4 border-t border-gray-200">
            <button
              onClick={handleDownload}
              className="w-full flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download size={18} className="mr-2" />
              Download XLIFF
            </button>
          </div>
        )}
      </div>

      <div className="flex-1 flex flex-col">
        {!selectedTU ? (
          <div className="flex-1 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <FileText size={64} className="mx-auto mb-4 opacity-30" />
              <p className="text-lg">Select a translation unit to edit</p>
            </div>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-8">
            <div className="max-w-4xl mx-auto space-y-6">
              <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold text-gray-800">Translation Unit: {selectedTU.id}</h3>
                  {selectedTU.state && (
                    <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                      {selectedTU.state}
                    </span>
                  )}
                </div>
                
                {selectedTU.notes.length > 0 && (
                  <div className="bg-blue-50 border border-blue-200 rounded p-3 text-sm text-blue-800">
                    <strong>Notes:</strong> {selectedTU.notes.join(', ')}
                  </div>
                )}
              </div>

              <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Source ({document?.files[selectedTransUnit.fileIndex].source_language})
                </label>
                <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 min-h-[80px]">
                  {renderSegmentWithTags(selectedTU.source)}
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Target ({document?.files[selectedTransUnit.fileIndex].target_language || 'Not specified'})
                </label>
                <div className="bg-white rounded-lg p-4 border-2 border-blue-300 min-h-[120px] focus-within:border-blue-500">
                  {renderSegmentWithTags(selectedTU.target)}
                </div>
                <p className="mt-2 text-xs text-gray-500 flex items-center">
                  <Lock size={12} className="mr-1" />
                  Tags are locked and cannot be edited
                </p>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-blue-800">
                <strong>Keyboard shortcuts:</strong> Use <kbd className="px-2 py-1 bg-white border border-blue-300 rounded">↑</kbd> and <kbd className="px-2 py-1 bg-white border border-blue-300 rounded">↓</kbd> arrow keys to navigate between translation units.
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}