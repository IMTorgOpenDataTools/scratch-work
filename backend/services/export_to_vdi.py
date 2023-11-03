#!/usr/bin/env python3
"""
Export to VDI Workspace Storage.
"""

from ._constants import logger
from ..structures.url import UniformResourceLocator
from ..structures.document import DocumentFactory, Document
from ..structures.crawler import BaseExporter, BaseLogger

from genson import SchemaBuilder

import shutil
from pathlib import Path
import json
import pickle



logger = BaseLogger()

class ExportToVdiStorage(BaseExporter):
    def export(self, url_list):
        schema = get_vdi_store_schema()
        for Url, hrefs in url_list.items():
            #prepare
            name = Url.get_domain()
            output_name = f'{name}'
            output_path = Path() / 'static' / 'results'
            output_full = Path(output_path) / output_name

            #process urls into Documents
            docs = url_to_document(hrefs)

            #export to vdi store
            vdi_store = save_to_vdi_store(schema, docs)

        return vdi_store



def url_to_document(hrefs):
    doc_factory = DocumentFactory(logger)
    docs = []
    for href in hrefs:
        doc = doc_factory.register(href)
        docs.append(doc)
    return docs


def save_to_vdi_store(schema, docs, output_name):
    """Save to vdi store json then zip.

    TODO:save directly to schema
    """
    
    mapVDISchemaToDoc = {
        'filepath': 'filepath',
        'filename_original': 'filename_original',
        'body_chars':'',
        'body_pages':'',
        'length_lines_array':'',
        'body':'body',
        'clean_body':'clean_body',
        'readability_score':'readability_score',
        'tag_categories':'',
        'keywords':'keywords',
        'summary':'summary',
        'html_body':'',
        'date_created':'date',
        'date_mod':'',
        'canvas_array':'',
        'sort_key':'',
        'hit_count':'',
        'snippets':'',
        'selected_snippet_page':'',
        '_showDetails':'',
        '_activeDetailsTab':'',
        'accumPageLines':'',
    }
    
    documentIndex = {
        'documents': [],
        'indices': {      
            'lunrIndex': {},
            'strIndex': ''
        }
    }

    managedNotes = {
        'topics':[],
        'notes':[]
    }

    vdi_store = {
        'documentsIndex':documentIndex,
        'managedNotes':managedNotes
    }

    documents = []
    for doc in docs:
        record = {}
        for key in mapVDISchemaToDoc.keys():
            doc_key = mapVDISchemaToDoc[key]
            if hasattr(doc, doc_key):
                record[key] = str( getattr(doc, doc_key) )
        documents.append(record)

    vdi_store['documentsIndex']['documents'] = documents
    with open(output_name.with_suffix('.json') ,'w') as f:
        json.dump(vdi_store, f)

    output_filename = 'vdi_store.zip'
    shutil.make_archive(output_name, 'zip', output_name.with_suffix('.json'))

    return True










def get_vdi_store_schema(schema_file=None):
    """Import previously-extracted vdi storage schema from file."""
    if not schema_file:
        schema_file = Path() / 'tests' / 'data' / 'vdi_schema.json'
        record_file = Path() / 'tests' / 'data' / 'documentRecord.json'
    with open(schema_file, 'r') as f:
        result_schema = json.load(f)
    #with open(record_file, 'r') as f:
    #    result_record = f.read()
    schema = {'vdi_store:': vdi_store,     #json.loads(result_schema),
              'record': record
              }
    return schema


def get_schema_from_object(source_file=None, output_file=None):
    """Get schema of final output object from current object.

    In this context, it is used to get the schema from unzipped `VDI_ApplicationStateData_v0.2.0`.

    arg: source_file - object's file path
    arg: output_file - return / save schema string to file based on output_file (None, True, or path)

    Output needed: { 'type':type, 'len':len, 'head':head() }

    >>> sStore.keys()
        dict_keys(['documentsIndex', 'managedNotes'])
    >>> sStore['documentsIndex'].keys()
        dict_keys(['documents', 'indices'])
    >>> sStore['documentsIndex']['documents'].__len__()
        2
    >>> sStore['documentsIndex']['documents'][0].keys()
        dict_keys(['id', 'reference_number', 'filepath', 'filename_original', 'filename_modified', 
                'file_extension', 'filetype', 'page_nos', 'length_lines', 'file_size_mb', 'date', 
                'title', 'toc', 'body_chars', 'body_pages', 'length_lines_array', 'summary', 
                'html_body', 'date_created', 'canvas_array', 'sort_key', 'hit_count', 'snippets', 
                'selected_snippet_page', '_showDetails', '_activeDetailsTab', 'accumPageLines', 
                'original_date', 'body', 'clean_body', 'pp_toc', 'accumPageChars'
                ])
    >>> print(builder.to_json(indent=2))
    """
    if not source_file:
        source_file = Path() / 'tests' / 'data' / 'VDI_ApplicationStateData_v0.2.0'
    with open(source_file, 'r') as f:
        strStore = f.read()
    sStore = json.loads(strStore)
    
    builder = SchemaBuilder()
    builder.add_object(sStore)

    if not output_file:
        return builder
    elif output_file == True:    #use default
        outfile = Path() / 'tests' / 'data' / 'vdi_schema.pickle'
    else:
        outfile = output_file

    jsonSchema = builder.to_schema()
    with open(outfile, 'w') as f:
        json.dump(jsonSchema, f)
    return True


vdi_store = {'documentsIndex':{
                'documents':[],
                'indices':{
                    'lunrIndex': {...}, 
                    'strIndex': {...}
                }
            },
           'managedNotes':{
               'topics':[],
               'notes':[]
            }
        }
    
record = {
'DocumentRecord': {
      #file indexing
      'id':None,
      'reference_number':None,
      'filepath' : None,
      'filename_original':None,
      'filename_modified':None,

      #raw
      'file_extension':None,
      'filetype':None, 
      'page_nos':None,
      'length_lines':None,
      'file_size_mb':None, 
      'date':None,

      #inferred / searchable
      'title':None,
      'author':None, 
      'subject':None,
      'toc':[],
      'pp_toc':None,

      'body_chars': {},
      'body_pages': {},
      'length_lines_array': [],
      'length_lines':0,
      'body':None,
      'clean_body':None,
      'readability_score':None,
      'tag_categories':None,
      'keywords':None,
      'summary':None,

      #added by frontend
      'html_body': None,
      'date_created': None,
      'date_mod': None,
      'canvas_array': [],

      'sort_key': None,
      'hit_count': None,
      'snippets': None,
      'selected_snippet_page': None,
      '_showDetails': False,
      '_activeDetailsTab': 0,
      'accumPageLines': None
    }
}

DocumentIndexData: {
  'documents': [],
  'indices': {      
    'lunrIndex': {},
    'strIndex': None
  }
}