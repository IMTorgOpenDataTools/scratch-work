#!/usr/bin/env python3
"""
Test exporting to pdf.
"""

from backend.structures.url import UniformResourceLocator
from backend.services.export_to_vdi import (
    get_schema_from_object,
    get_vdi_store_schema,
    url_to_document,
    save_to_vdi_store
)

from pathlib import Path


def test_get_schema_from_object():
    result = get_schema_from_object(output_file=True)
    assert result == True

def test_create_vdi_store():
    #prepare
    version = '0.2.0'
    name = 'VDI_ServerStateData_v' + version
    output_name = Path() / 'tests' / 'result' / name
    schema = get_vdi_store_schema()
    #with open('./tests/data/jpmorgan_hrefs.txt', 'r') as file:
    #    hrefs = [line.rstrip() for line in file]
    hrefs = ['https://www.chase.com/personal/banking/education/basics/overdraft-fees',
             'https://www.jpmorgan.com/content/dam/jpm/merchant-services/documents/jpmorgan-interchange-guide.pdf',
             ]

    #get url artifacts
    unique_hrefs = list(set(hrefs))
    Urls = []
    for href in unique_hrefs:
        Url = UniformResourceLocator(href)
        check_artifact_exists = Url.get_file_artifact_()
        if check_artifact_exists:
            Urls.append(Url)
    
    #process
    docs = url_to_document(Urls)
    result = save_to_vdi_store(schema, docs, output_name)
    #result = save_combine_pdfs(pdfs, output_name)
    
    assert result == True