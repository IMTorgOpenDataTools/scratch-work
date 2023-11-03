#!/usr/bin/env python3
"""
URL to PDF Workflow
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from ..structures.crawler import Crawler
from .export_to_pdf import url_to_pdf, save_combine_pdfs
from ._constants import logger

from pathlib import Path



def domains_workflow(post_data):
    """Receive the post request, (background) process the domains,
    and return the paths.
    """
    #collect urls
    url_list = post_data.get('domainUrl')
    ValidatedUrls = Crawler.check_urls_are_valid(url_list)
    results = []
    for Url in ValidatedUrls:
        UrlCrawl = Crawler(Url, logger)
        result_urls = UrlCrawl.generate_href_chain()
        results.extend( UrlCrawl.export(result_urls) )

    return results