#!/usr/bin/env python3
"""
URL to PDF Workflow
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"


from .url import UniformResourceLocator
from .utils import check_urls_are_valid
from .export_pdf import url_to_pdf, save_combine_pdfs
from ._constants import logger

import googlesearch

from pathlib import Path
import itertools






def domains_workflow(post_data):
    """Receive the post request, (background) process the domains,
    and return the paths.
    """
    #collect urls
    url_list = post_data.get('domainUrl')
    ValidatedUrls = check_urls_are_valid(url_list)
    results = []
    for Url in ValidatedUrls:
        UrlCrawl = Crawler(Url, logger)
        result_urls = UrlCrawl.generate_href_chain()
        results.extend( UrlCrawl.export_pdfs(result_urls) )

    return results
        

    






class Crawler:

    def __init__(self, url, logger):
        self.url = UniformResourceLocator(url)
        self.logger = logger

    def __repr__(self):
        return self.url

    def generate_href_chain(self):
        """Given a domain name, collects the appropriate
        href links."""
        LIST_OF_SEARCH_TERMS = ['creditcard`, `fees', 'terms conditions', 'overdraft', 'non insufficient funds']
        result_urls = {}
        
        initial_list = self.get_initial_url_list(self.url, LIST_OF_SEARCH_TERMS)
        hrefs = self.get_hrefs_within_depth(base_url = self.url, 
                                           depth = 0, 
                                           initial_url_list = initial_list
                                           )
        result_urls[self.url] = hrefs
        self.logger.info(f"result_urls: {result_urls}")
        return result_urls

    def get_initial_url_list(self, url, list_of_search_terms=[]):
        """Get initial list of urls from google given search terms."""
        NumberOfSearchResults = 5
        BaseUrl = UniformResourceLocator('https://www.jpmorgan.com')
        domain = url.get_domain()

        term_permutations = list(itertools.permutations(list_of_search_terms, r=2))
        search_terms_list = []
        for tup in term_permutations:
            tmp = list(tup)
            tmp.append(domain)
            search_terms_list.append(tmp)
        stringified_lists = [' '.join(terms) for terms in search_terms_list]

        result_url_list = []
        for terms in stringified_lists:
            try:
                search_results = googlesearch.search(query = terms, 
                                                     stop =  NumberOfSearchResults,
                                                     pause = 1 
                                                     )
                unique_urls = [url for url in search_results if url not in result_url_list]
                SearchUrls = [UniformResourceLocator(result) for result in unique_urls]
                ValidUrls = check_urls_are_valid(url_list = SearchUrls, 
                                                 base_url = BaseUrl
                                                 )
                result_url_list.extend(ValidUrls)
            except:
                self.logger.error('ERROR: there was a problem making the request to google.com.')
        return result_url_list


    def get_hrefs_within_depth(self, base_url, depth=1, initial_url_list=[]):
        """Get all hrefs from a page, within a depth, and certain criteria.

        This is similar to `wget --recursive http://site.com`, but it removes 
        links that are out of scope.
        """
        BaseUrl_JPM = UniformResourceLocator('https://www.jpmorgan.com')
        searched_hrefs = set()
        BaseUrl = base_url if type(base_url) == UniformResourceLocator else UniformResourceLocator(base_url)
        #if len(initial_url_list) == 0:
        #    hrefs = BaseUrl.get_hrefs_within_hostname_(searched_hrefs = searched_hrefs)
        #    #searched_hrefs = add_list_to_set(searched_hrefs, hrefs)
        #else:
        #    hrefs = initial_url_list
        hrefs = initial_url_list
        while depth > -1:
            level_hrefs = []
            for url in hrefs:
                Url = url if type(url) == UniformResourceLocator else UniformResourceLocator(url)
                check_owner = Url.has_same_url_owner_(BaseUrl)
                if not (Url in searched_hrefs) and not check_owner:
                    new_hrefs = Url.get_hrefs_within_hostname_(searched_hrefs = searched_hrefs)
                    valid_hrefs = check_urls_are_valid(url_list = new_hrefs, 
                                                       base_url = BaseUrl_JPM
                                                       )
                    searched_hrefs.add(Url)
                    level_hrefs.extend(valid_hrefs)
            hrefs = list(set(level_hrefs))
            depth = depth - 1

        return searched_hrefs
    

    def export_pdfs(self, result_urls):
        #convert to pdf
        processing_results = {}
        for Url, hrefs in result_urls.items():
            name = Url.get_domain()
            output_name = f'{name}'
            output_path = Path() / 'static' / 'pdf'
            output_full = Path(output_path) / output_name

            pdfs = url_to_pdf(hrefs)
            results = save_combine_pdfs(pdfs, output_name)
            #return dict of data
            #processing_results[str(Url)] = (result, str(output_full))

        return results