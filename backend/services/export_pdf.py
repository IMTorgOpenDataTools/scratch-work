#!/usr/bin/env python3
"""
Export to PDF functionality.
"""

"""
The approach below works, it was tested via terminal, see 'googley6 merged_pages.pdf:
>>> urls = ['https://www.google.com/imghp?hl=en&tab=wi', 'https://maps.google.com/maps?hl=en&tab=wl', 'https://play.google.com/?hl=en&tab=w8', 'https://drive.google.com/?tab=wo', 'https://www.google.com/intl/en/about/products?tab=wh', 'https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ', 'https://mail.google.com/mail/?tab=wm', 'https://news.google.com/?tab=wn']
>>> output_name = './google.pdf' 
>>> pdfkit.from_url(urls, output_name) 

However, there are some difficulties with: i) dynamic web pages, ii) processing speed.  It would 
be preferable to provide to VDI in a cleaner manner, such as:
1) get page visible text, and hrefs, using bs4
2) provide bs4 html string to `https://github.com/vgalin/html2image`, which has added benefit of pure python
3) results are sent to VDI for indexing after processing
"""

from .url import UniformResourceLocator

from PyPDF2 import PdfMerger
import pdfkit

import signal
import time




def url_to_pdf(UrlHrefs, N=10):
    """Given a list of urls 
    i) attempts to convert url to pdf
    ii) returns the pdf structure as string

    use: url_to_pdf(urls, N=10)
    N = 4  #wait N seconds before terminating
    """
    # Register an handler for the timeout
    def handler(signum, frame):
        print("Forever is over!")
        #raise Exception("end of time")
    
    def run_pdfkit(Url, pdfs):
        print(f'running href: {Url}')
        result = pdfkit.from_url(Url.__repr__())
        pdfs[Url.url] = result
        time.sleep(1)
        
    pdfs = {}
    UrlHrefList = []
    for url in UrlHrefs:
        Url = url if type(url) == UniformResourceLocator else UniformResourceLocator(url)
        if Url.get_file_artifact_() != 'NA':
            UrlHrefList.append(Url)

    for idx, Url in enumerate(UrlHrefList):
        if Url.file_format == 'html':
            signal.signal(signal.SIGALRM, handler)    #register the signal function handler
            signal.alarm(N)    #define a timeout for your function
            try:
                run_pdfkit(Url, pdfs)
                print(f'completed href: {Url} with length {len(pdfs[Url.__repr__()])}')
                signal.alarm(0)    #cancel
            except Exception as e:
                print(f'There was an error: {e}')
        elif Url.file_format == 'pdf' and Url.file_document:
            pdfs[Url.url] = Url.file_str
    return pdfs


def save_individual_pdfs(pdfs, output_name):
    """Save each individual pdf to file."""
    #usage: save_pdfs(pdfs, output_path)
    if len(pdfs) > 0:
        print(len(pdfs))
        pdf_files = []
        for url, pdf in pdfs.items():
            if len(pdf) > 100:
                url_mod = url.replace('/','\\')
                filename = str(output_name) + '-' + str(url_mod) + '.pdf'
                bytes_name = bytes(str(url_mod), 'utf-8')
                bytes_path = bytes(filename, 'utf-8')
                if( len(bytes_name) < 255 and len(bytes_path) < 4096 ):
                    with open(filename, 'wb') as f:
                        f.write(pdf)
                    pdf_files.append(filename)
    return True


def save_combine_pdfs(pdfs, output_name):
    """Save each individual pdf to file, then merge all into a combined file."""
    #usage: save_pdfs(pdfs, output_path)
    if len(pdfs) > 0:
        print(len(pdfs))
        pdf_files = []
        for idx, pdf in enumerate(pdfs):
            if len(pdf) > 100:
                filename = str(output_name) + str(idx) + '.pdf'
                with open(filename, 'wb') as f:
                    f.write(pdf)
                pdf_files.append(filename)
        merger = PdfMerger()    #Create an instance of PdfFileMerger() class
        #Create a list with the file paths
        #pdf_files = [output_name+str(idx) for idx,pdf in enumerate(pdfs)]
        for pdf_file in pdf_files:
            merger.append(pdf_file)
        #Write out the merged PDF file
        merger.write(f"{output_name}_merged_pages.pdf")
        merger.close()
    return True


















"""
import multiprocessing
import time

def url_to_pdf(hrefs, output_name, N=4):
    Given a list of urls 
    i) saves a combined pdf file
    ii) returns the external url to the static asset (pdf file)

    use: url_to_pdf(urls, output_path)
    N = 4  #wait N seconds before terminating
    
    def run_pdfkit(href, pdfs):
        print(f'running href: {href}')
        result = pdfkit.from_url(href)    # toc=toc, cover=cover, cover_first=True)
        pdfs.append(result)
    
    toc = {
        'xsl-style-sheet': 'toc.xsl'
    }
    cover = 'cover.html'
    
    pdfs = []
    for idx, href in enumerate(hrefs):
        try:
            p = multiprocessing.Process(target=run_pdfkit, name="PdfKit", args=(href, pdfs))
            p.start()
            print(f'started process for href: {href}')
            p.join(N)
            if p.is_alive():
                print('kill job...')
                p.terminate()
                p.join()
            print(f'completed href: {href} with length {len(pdfs[idx])}')
        except:
            print(f'There was an error')
    if len(pdfs) > 0:
        with open(output_name, 'w+b') as f:
            for pdf in pdfs:
                f.write(pdf)
    return True



import os
def generate_pdf(html, static_path,  _path):
    WKHTMLTOPDF_PATH = '/usr/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    _status = pdfkit.from_url(
        html,
        os.path.join(static_path, _path),
        configuration=config,
        options={
            'page-size': 'A4',
            'margin-top': '0',
            'margin-right': '0',
            'margin-left': '0',
            'margin-bottom': '0',
            'zoom': '1.2',
            'encoding': "UTF-8",
        })
    return _path if _status else ''
"""