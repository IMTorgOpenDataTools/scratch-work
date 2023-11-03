#!/usr/bin/env python3
"""
Test the Scraper class.
"""
"""
from backend.services.url_to_pdf import (
    get_hrefs_within_depth, 
    check_urls_are_valid,
    get_initial_url_list,


    url_to_pdf,
    save_combine_pdfs, 
    domains_workflow
)"""
from backend.services.utils import check_urls_are_valid

import requests

from pathlib import Path


def test_check_urls_are_valid():
    hrefs = ['https://www.google.com/imghp?hl=en&tab=wi', 
        'https://maps.google.com/maps?hl=en&tab=wl', 
        'https://play.google.com/?hl=en&tab=w8', 
        'https://drive.google.com/?tab=wo', 
        'https://www.google.com/intl/en/about/products?tab=wh', 
        'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ', 
        'https://mail.google.com/mail/?tab=wm', 
        'https://news.google.com/?tab=wn'
        ]
    result = check_urls_are_valid(hrefs)
    assert len(result) == 8

"""
def test_get_initial_url_list():
    #list_of_search_terms = ['credit', 'card', 'terms', 'conditions']
    list_of_search_terms = ['creditcard`, `fees', 'terms conditions', 'overdraft', 'non in sufficient funds']
    url = 'https://www.jpmorgan.com'
    initial_list = get_initial_url_list(url, 
                                        list_of_search_terms
                                        )
    assert len(initial_list) > 1

def test_get_hrefs_within_depth():
    url = 'https://www.google.com'
    hrefs = get_hrefs_within_depth(url)
    assert len(hrefs) > 0







def test_create_pdfs():
    output_name = Path() / 'pdfs' / 'test'
    hrefs = ['https://www.google.com/imghp?hl=en&tab=wi',
             'https://www.gstatic.com/policies/terms/pdf/20220105/it7r24p9/google_terms_of_service_en_us.pdf', 
            'https://maps.google.com/maps?hl=en&tab=wl', 
            'https://play.google.com/?hl=en&tab=w8', 
            'https://drive.google.com/?tab=wo', 
            'https://www.google.com/intl/en/about/products?tab=wh', 
            'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ', 
            'https://mail.google.com/mail/?tab=wm', 
            'https://news.google.com/?tab=wn'
            ]

    #comment-out
    with open('./data/jpmorgan_hrefs.txt', 'r') as file:
        hrefs = [line.rstrip() for line in file]

    pdfs = url_to_pdf(hrefs, N=4)
    result = save_combine_pdfs(pdfs, output_name)
    
    assert result == True


def test_run_process_steps():
    output_name = Path() / 'pdfs' / 'test'
    url = 'https://www.jpmorgan.com'
    hrefs = get_hrefs_within_depth(url)
    pdfs = url_to_pdf(hrefs, N=4)
    result = save_combine_pdfs(pdfs, output_name)
    
    assert result == True

def test_domains_workflow():
    post_data = {
        'domainUrl':['https://www.jpmorgan.com']
        }
    tmp = domains_workflow(post_data)

    assert tmp == True

"""