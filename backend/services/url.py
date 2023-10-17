#!/usr/bin/env python3
"""
URL class
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from ._constants import logger

import tldextract
import whois

from requests_html import HTMLSession
import bs4
from bs4 import BeautifulSoup
import pypdf

import urllib
import io
import time


class UniformResourceLocator:
    """Describe class

    The URL could point to one of many options:
    * web page (ie. )
    * html or pdf file (ie. )
    * json or other data format (ie. )
    """

    _possible_schemes = ['http://', 'https://']
    _possible_suffixes = {'html': ['html','com','org','gov','md'],   #map url_type to suffix
                          'pdf': ['pdf'],
                          'data': ['json','jsonl','xml','csv','sql','txt'],
                          'msft': ['doc','ppt','xlsx']
                          }
    _possible_suffixes_list = []

    def __init__(self, url):
        self.url = None
        self.logger = None
        if type(url) == str:
            self.url = url.lower()
        elif type(url) == UniformResourceLocator:
            logger.error(f'url is already of type {UniformResourceLocator}')
            raise Exception
        else:
            raise TypeError

        #components   
        self.scheme = ''
        self.suffix = ''
        self.valid_url = ''
        self.url_type = None            #from suffix in  _possible_suffixes

        #metadata
        self.whois_account = None
        self.owner = None

        #artifacts
        self.file_type = None           #from url content-type
        self.file_format = None         #inferred from document
        self.file_str = ''              #document string
        self.file_document = None       #document
        self.file_visible_text = ''

        self.run_checks()

        
    #basic
    def __repr__(self):
        return self.url

    def __set_logger(self, logger=None):
        #TODO:use in-case logger not added
        if logger:
            return logger
        else:
            return {'info': print, 'error': print}
            
    def get_metadata_(self):
        """Return basic information about the URL."""
        return (
            f'URL: {self.url}\n'
            f'Domain: {self.get_domain()}\n'
            f'Owner: {self.owner}\n'
            f'Type: {self.url_type}\n'
            f'File Format: {self.file_format}\n'
            f'Length File: {len(self.file_str)}\n'
        )
    
    def _populate_possible_suffixes_list(self):
        self._possible_suffixes_list = []
        for val in self._possible_suffixes.values():
            self._possible_suffixes_list.extend(val)


    #checks
    def run_checks(self):
        """Run all checks."""
        self.check_scheme()
        self.check_suffix_and_url_type()
        self.check_valid_format()
        return True

    def check_scheme(self):
        """Check for valid scheme, populate `self.scheme`."""
        check_scheme = [scheme in self.url for scheme in self._possible_schemes]
        result = any(check_scheme)
        if result:
            self.scheme = self._possible_schemes[check_scheme.index(True)]
        return result

    def check_suffix_and_url_type(self):
        """Check for suffixes that are possible to parse, 
        populate `self.suffix` and `self.url_type`.
        """
        if not self._possible_suffixes_list:
            self._populate_possible_suffixes_list()
        result = ''
        psl = tldextract.extract(self.url).suffix
        split = self.url.split('.')
        endpt = split[len(split)-1]
        suffix = psl if (psl in endpt) else endpt

        check_suffix = [suffix_val in suffix for suffix_val in self._possible_suffixes_list]
        result = any(check_suffix)
        if result:
            self.suffix = suffix
            self.url_type = [k for k,v in self._possible_suffixes.items() if suffix in v][0]
        return result

    def check_valid_format(self):
        """Check if complete url is valid."""
        try:
            result = urllib.parse.urlparse(self.url)
            if result:
                return True
        except:
            return False

    
    #getters
    def get_fqdn(self):
        """Get Fully Qualified Domain Name (FQDN).
        Usually used for landing page.
        fqdn = <hostname> and <domain>
        """
        pass

    def get_hostname(self):
        """Get hostname.
        Network or system used to deliver a user to a certain address.
        hostname = <www>.<internal_network>.<suffix>
        """
        return urllib.parse.urlparse(self.url).hostname
    
    def get_domain(self):
        """Get domain name.
        Site or project the user is accessing.  This is typically used
        to ensure url is within same site.
        <subdomain>.<domain>.<suffix>
        """
        return tldextract.extract(self.url).domain

    def get_suffix(self):
        """Get actual suffix which might not align
        with PSL."""
        return self.suffix
    
    def get_scheme(self):
        """Get actual suffix which might not align
        with PSL."""
        return self.scheme
    
    def get_subdomain(self):
        return tldextract.extract(self.url).subdomain

    def get_domain_with_suffix(self):
        return f'{self.get_domain()}.{self.suffix}'

    def get_domain_with_scheme(self):
        return f'.{self.scheme}{self.get_subdomain()}{self.get_domain()}'
    
    def get_file_document(self):
        """Get the file in whatever file type is supported."""
        if not all([self.file_format, self.file_document]):
            logger.error(f"no data try calling `self.get_file_artifact_()")
        elif self.file_format == 'NA':
            logger.error(f"`self.get_file_artifact_() called, but no data")
        return (self.file_type ,self.file_document)


    #getters requiring requests
    def run_data_requests_(self):
        """Run all methods that require http requests."""
        try:
            self.get_owner_()
            self.get_file_artifact_()
        except:
            logger.error('there was a problem making requests.')
        return True
    
    def get_owner_(self):
        """Request the owner from ICANN WHOIS.

        Without 1sec delay ICANN will reject the request.  However, there
        are continued difficulties with not getting the owner.
        TODO:replace python-whois with custom lib that can: 
            - parse owner from text
            - improve error handling (too many errors)
        """
        ATTEMPTS = 2

        def request_iteration():
            try:
                self.whois_account = whois.whois(self.url)
                self.owner = self.whois_account.text.split('Organization:')[1].split('\n')[0].strip()
            except:
                logger.error(f'ICANN WHOIS gave no response for url: `{self.url}`')
            time.sleep(1)
            return self.owner

        while ATTEMPTS > 0:
            if not self.owner:
                request_iteration()
            ATTEMPTS =- 1
            
        return self.owner
    
    def has_same_url_owner_(self, comparison_url):
        """Compare this url owner with another url's owner."""
        if not type(comparison_url) == UniformResourceLocator:
            ComparisonUrl = UniformResourceLocator(comparison_url)
        else:
            ComparisonUrl = comparison_url

        #case-1: check domains
        if self.get_domain() == comparison_url.get_domain():
            result = True
            return result

        #case-2: check icann owners
        if not self.owner:
            self.get_owner_()
        if not ComparisonUrl.owner:
            ComparisonUrl.get_owner_()

        if self.owner and ComparisonUrl.owner:
            result = self.owner == ComparisonUrl.owner
        else:
            result = False
        if not result:
            logger.info(f'WARNING: Different Owners:\n'
                        f'current url: `{self.url}`'
                        f'    owner [{self.owner}]\n' 
                        f'comparison url: `{comparison_url.url}`' 
                        f'    owner [{comparison_url.owner}]'
                        )
        return result
    
    def get_file_artifact_(self):
        """Determine if url is page, file, data, etc., then populate the
        artifact and associated attributes.
        
        In the process this will use (`self.url_type` mapping from `self.suffix`) 
        to provision:
        * `self.file_type`
        * `self.file_format`
        * `self.file_str`
        * `self.file_document`

        note: Failing to parse the file will provision with an 'NA'.  This is used
        over `None` to document that parsing was attempted.
        """
        def get_artifact():
            """Get url artifact and verify self.url_type is correct."""
            resp = None
            try:
                session = HTMLSession()
                resp = session.get(self.url)
                if resp.status_code == 200:
                    content_type = resp.headers.get('content-type')
                    self.file_type = content_type
                    if 'text/html' in content_type:
                        if self.url_type != 'html':
                            logger.error('ERROR: `self.url_type` does not match content-type')  
                            raise Exception
                        resp.html.render()
                        txt = resp.html.text      #output as string
                        if len(txt) < 100:
                            logger.error('ERROR: HTML content length is insignificant')  
                            raise Exception
                        self.file_str = txt
                    elif 'application/pdf' in content_type:
                        if self.url_type != 'pdf':
                            logger.error('ERROR: `self.url_type` does not match content-type') 
                            raise Exception
                        bytes = resp.content
                        if len(bytes) < 100:
                            logger.error('ERROR: PDF content length is insignificant')  
                            raise Exception
                        self.file_str = bytes        #output as bytes for binary file (PDF file, audio, image, etc.)
                    else:
                        logger.error(f'ERROR: unaddressed content-type: {content_type}')
                        raise Exception
                else:
                    logger.error(f'ERROR: when requesting url, got status-code: {resp.status_code}')
                    raise Exception
            except Exception:
                logger.error(f'ERROR: in request for url: {self.url}')
            return resp

        def parse_artifact_from_suffix(resp):
            """Parese file and provision file attributes."""
            result = ''
            #html
            if resp and self.url_type == 'html':
                try: 
                    soup = BeautifulSoup(self.file_str, 'html.parser')
                    if soup:
                        result = 'html'
                        self.file_format = result
                        self.file_document = soup
                except:
                    logger.error(f'ERROR: file for url {self.url} is invalid HTML')
                    result = 'NA'
            #pdf
            elif resp and self.url_type == 'pdf':
                try:
                    file_stream = io.BytesIO(self.file_str)
                    pdf_file = pypdf.PdfReader(file_stream)
                    if pdf_file:
                        result = 'pdf'
                        self.file_format = result
                        self.file_document = pdf_file
                    else:
                        raise Exception
                except Exception:    #pypdf.errors.PdfReadError:
                    logger.error(f'ERROR: file for url {resp.url} is invalid PDF')
                    result = 'NA'
            #if no url (no file)
            else:
                result = 'NA'
                self.file_format = result
                self.file_document = result
            return result
        
        result = ''
        resp = get_artifact()
        result = parse_artifact_from_suffix(resp)
        time.sleep(1)
        return result
    
    def get_hrefs_under_criteria_(self):
        """Get all anchors from a `resp.text` html file under 
        specific criterion.
        """
        REMOVE = ['sign','login']

        anchors_with_stem = None
        if self.file_document and self.url_type == 'html':
            tmp =  self.get_hostname()     #urllib.parse.urlparse(resp.url).hostname    #Path(resp.url).stem.split('.')
            #stem = tmp[len(tmp)-1] if len(tmp) > 1 else tmp[0]
            soup = self.file_document

            #anchors
            anchors = soup.find_all('a')
            """
            anchors_with_hrefs = [anchor for anchor in anchors if anchor.has_attr('href')]
            anchors_with_www_hrefs = [anchor for anchor in anchors_with_hrefs if 'https://' in anchor['href']]
            anchors_without_removed = [anchor for anchor in anchors_with_www_hrefs 
                                       if not any(x in anchor['href'].lower() for x in REMOVE)
                                       ]
            anchors_with_stem = list(set([anchor['href'] for anchor in anchors_without_removed if stem in anchor['href']]))
            """
        return anchors    #_with_stem

    def get_hrefs_within_hostname_(self, searched_hrefs=set(), additional_scope=[]):
        """Get hrefs from html document that are within the scope of target hostnames.

        TODO: add additional_scope
        """
        hrefs = []
        #pre-checks
        if not (self.file_document or self.file_format):
            self.get_file_artifact_()

        #checks
        if (self.file_document and self.file_format == 'html'):
            tmp_hrefs = self.get_hrefs_under_criteria_()
            hrefs = [href for href in tmp_hrefs if href not in searched_hrefs]

        return hrefs

    def get_visible_text_(self):
        """Get visible text from html.

        ref: https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
        """
        def tag_visible(element):
            if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                return False
            if isinstance(element, bs4.element.Comment):
                return False
            return True

        if self.file_document and self.url_type == 'html':
            soup = self.file_document
            texts = soup.findAll(text=True)
            visible_texts = filter(tag_visible, texts)
            self.file_visible_text = visible_texts
            return u" ".join(t.strip() for t in visible_texts)
        else:
            return False