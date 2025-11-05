from lxml import etree
from models import XliffDocument, XliffFile, TransUnit, SegmentContent, XliffTag
from typing import List, Tuple, Dict

class XliffParser:
    """Parser for XLIFF 1.1 and 1.2 files with support for various tag types"""
    
    # Support both XLIFF 1.1 and 1.2 namespaces
    XLIFF_NS_12 = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}
    XLIFF_NS_11 = {'xliff': 'urn:oasis:names:tc:xliff:document:1.1'}
    
    # Supported inline tag types
    INLINE_TAGS = {'g', 'x', 'bpt', 'ept', 'ph', 'it', 'mrk', 'sub', 'bx', 'ex'}
    
    @staticmethod
    def detect_namespace(tree) -> tuple:
        """
        Detect which XLIFF namespace version is being used
        Returns (namespace_dict, use_namespace_prefix)
        """
        root_ns = tree.nsmap.get(None, '')
        
        # Check if file has no default namespace (common with some CAT tools)
        if not root_ns or root_ns == '':
            # No namespace - elements are in null namespace
            return ({}, False)
        
        if '1.2' in root_ns:
            return (XliffParser.XLIFF_NS_12, True)
        elif '1.1' in root_ns:
            return (XliffParser.XLIFF_NS_11, True)
        else:
            # Default to 1.2 with namespace
            return (XliffParser.XLIFF_NS_12, True)
    
    @staticmethod
    def parse_segment(element) -> SegmentContent:
        """Parse source or target element, extracting text and inline tags"""
        if element is None:
            return None
        
        tags = []
        text_parts = []
        position = 0
        
        def extract_text_and_tags(elem, current_pos):
            """Recursively extract text and tags from element"""
            nonlocal position
            
            # Add text before any child elements
            if elem.text:
                text_parts.append(elem.text)
                current_pos += len(elem.text)
            
            # Process child elements (inline tags)
            for child in elem:
                tag_type = etree.QName(child).localname
                
                # Only process known inline tags
                if tag_type in XliffParser.INLINE_TAGS:
                    # Create tag marker for position tracking
                    tag_marker = f"⟨{tag_type}⟩"
                    
                    # Extract tag information
                    tag = XliffTag(
                        tag_type=tag_type,
                        id=child.get('id'),
                        position=current_pos,
                        ctype=child.get('ctype'),  # Content type attribute
                        content=child.text if child.text else None,  # Inner content
                        attributes={k: v for k, v in child.attrib.items() 
                                  if k not in ['id', 'ctype']}
                    )
                    
                    tags.append(tag)
                    text_parts.append(tag_marker)
                    current_pos += len(tag_marker)
                    
                    # For paired tags like <bpt>/<ept>, store pairing info
                    if tag_type in ['bpt', 'ept'] and tag.id:
                        tag.paired_with = tag.id
                
                # Add tail text (text after the tag)
                if child.tail:
                    text_parts.append(child.tail)
                    current_pos += len(child.tail)
            
            return current_pos
        
        # Extract all text and tags
        position = extract_text_and_tags(element, 0)
        full_text = ''.join(text_parts)
        
        return SegmentContent(text=full_text, tags=tags)
    
    @staticmethod
    def parse_trans_unit(tu_element, namespace=None, use_prefix=True) -> TransUnit:
        """Parse a single trans-unit element"""
        if namespace is None:
            namespace = XliffParser.XLIFF_NS_12
        
        # Find source and target
        if use_prefix:
            source_elem = tu_element.find('xliff:source', namespace)
            target_elem = tu_element.find('xliff:target', namespace)
            note_elements = tu_element.findall('xliff:note', namespace)
        else:
            source_elem = tu_element.find('source')
            target_elem = tu_element.find('target')
            note_elements = tu_element.findall('note')
        
        # Parse notes
        notes = [note.text for note in note_elements if note.text]
        
        return TransUnit(
            id=tu_element.get('id'),
            source=XliffParser.parse_segment(source_elem),
            target=XliffParser.parse_segment(target_elem) if target_elem is not None else None,
            state=target_elem.get('state') if target_elem is not None else None,
            notes=notes,
            attributes={k: v for k, v in tu_element.attrib.items() if k != 'id'}
        )
    
    @staticmethod
    def extract_trans_units_recursive(element, namespace, use_prefix) -> List[TransUnit]:
        """Recursively extract trans-units from an element and its groups"""
        trans_units = []
        
        # Get trans-units directly in this element
        if use_prefix:
            tu_elements = element.findall('xliff:trans-unit', namespace)
        else:
            tu_elements = element.findall('trans-unit')
        
        for tu_elem in tu_elements:
            trans_units.append(XliffParser.parse_trans_unit(tu_elem, namespace, use_prefix))
        
        # Recursively get trans-units from group elements
        if use_prefix:
            group_elements = element.findall('xliff:group', namespace)
        else:
            group_elements = element.findall('group')
        
        for group_elem in group_elements:
            trans_units.extend(XliffParser.extract_trans_units_recursive(group_elem, namespace, use_prefix))
        
        return trans_units
    
    @staticmethod
    def parse_file(content: bytes) -> XliffDocument:
        """Parse XLIFF file content (supports XLIFF 1.1 and 1.2, with or without namespace)"""
        tree = etree.fromstring(content)
        
        # Detect namespace version and whether to use prefix
        namespace, use_prefix = XliffParser.detect_namespace(tree)
        
        # Get version
        version = tree.get('version', '1.2')
        
        files = []
        
        # Find file elements
        if use_prefix:
            file_elements = tree.findall('xliff:file', namespace)
        else:
            file_elements = tree.findall('file')
        
        for file_elem in file_elements:
            # Find body element
            if use_prefix:
                body_elem = file_elem.find('xliff:body', namespace)
            else:
                body_elem = file_elem.find('body')
            
            trans_units = []
            if body_elem is not None:
                # Extract all trans-units (including those in nested groups)
                trans_units = XliffParser.extract_trans_units_recursive(body_elem, namespace, use_prefix)
            
            xliff_file = XliffFile(
                original=file_elem.get('original'),
                source_language=file_elem.get('source-language'),
                target_language=file_elem.get('target-language'),
                datatype=file_elem.get('datatype'),
                trans_units=trans_units
            )
            files.append(xliff_file)
        
        return XliffDocument(version=version, files=files)
    
    @staticmethod
    def reconstruct_segment(text: str, tags: List[XliffTag], parent_elem):
        """Reconstruct a segment element with inline tags"""
        # Detect namespace from parent element
        parent_ns = etree.QName(parent_elem).namespace
        
        # Clear the element
        parent_elem.text = None
        parent_elem.tail = None
        for child in list(parent_elem):
            parent_elem.remove(child)
        
        # Build a mapping of tag positions
        tag_positions = {tag.position: tag for tag in tags}
        sorted_positions = sorted(tag_positions.keys())
        
        last_pos = 0
        last_element = parent_elem
        
        for tag_pos in sorted_positions:
            tag = tag_positions[tag_pos]
            tag_marker = f"⟨{tag.tag_type}⟩"
            
            # Add text before the tag
            text_before = text[last_pos:tag_pos]
            if last_element == parent_elem:
                parent_elem.text = (parent_elem.text or '') + text_before
            else:
                last_element.tail = (last_element.tail or '') + text_before
            
            # Create the tag element with correct namespace (or no namespace)
            if parent_ns:
                tag_elem = etree.SubElement(parent_elem, f'{{{parent_ns}}}{tag.tag_type}')
            else:
                tag_elem = etree.SubElement(parent_elem, tag.tag_type)
            
            # Set attributes
            if tag.id:
                tag_elem.set('id', tag.id)
            if tag.ctype:
                tag_elem.set('ctype', tag.ctype)
            for attr, val in tag.attributes.items():
                tag_elem.set(attr, val)
            
            # Set content
            if tag.content:
                tag_elem.text = tag.content
            
            last_element = tag_elem
            last_pos = tag_pos + len(tag_marker)
        
        # Add remaining text
        remaining_text = text[last_pos:]
        if last_element == parent_elem:
            parent_elem.text = (parent_elem.text or '') + remaining_text
        else:
            last_element.tail = (last_element.tail or '') + remaining_text
    
    @staticmethod
    def update_trans_unit(tree: etree.Element, file_index: int, trans_unit_id: str, 
                         target_text: str, target_tags: List[XliffTag]) -> bytes:
        """Update a trans-unit's target in the XML tree"""
        # Detect namespace
        namespace, use_prefix = XliffParser.detect_namespace(tree)
        
        # Find file element
        if use_prefix:
            file_elements = tree.findall('xliff:file', namespace)
        else:
            file_elements = tree.findall('file')
        
        file_elem = file_elements[file_index]
        
        # Find body element
        if use_prefix:
            body_elem = file_elem.find('xliff:body', namespace)
        else:
            body_elem = file_elem.find('body')
        
        # Find the trans-unit (may be in groups)
        def find_trans_unit_in_element(element, tu_id):
            # Check direct children
            if use_prefix:
                tu_elements = element.findall('xliff:trans-unit', namespace)
            else:
                tu_elements = element.findall('trans-unit')
            
            for tu_elem in tu_elements:
                if tu_elem.get('id') == tu_id:
                    return tu_elem
            
            # Check in groups
            if use_prefix:
                group_elements = element.findall('xliff:group', namespace)
            else:
                group_elements = element.findall('group')
            
            for group_elem in group_elements:
                result = find_trans_unit_in_element(group_elem, tu_id)
                if result is not None:
                    return result
            
            return None
        
        tu_elem = find_trans_unit_in_element(body_elem, trans_unit_id)
        
        if tu_elem is not None:
            # Find or create target element
            if use_prefix:
                target_elem = tu_elem.find('xliff:target', namespace)
            else:
                target_elem = tu_elem.find('target')
            
            if target_elem is None:
                # Determine the correct namespace URI (or none)
                if use_prefix:
                    ns_uri = namespace['xliff']
                    target_elem = etree.SubElement(tu_elem, f'{{{ns_uri}}}target')
                else:
                    target_elem = etree.SubElement(tu_elem, 'target')
            
            # Reconstruct the target with tags
            XliffParser.reconstruct_segment(target_text, target_tags, target_elem)
        
        return etree.tostring(tree, encoding='utf-8', xml_declaration=True, pretty_print=True)