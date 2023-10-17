#!/usr/bin/env python3
"""
Utility functionality
"""

from .url import UniformResourceLocator
from ._constants import logger


def check_urls_are_valid(url_list, base_url=''):
    """Basic checks of urls in a list
    * ensure proper url formatting
    * consistent domain owner (if base_domain provided)
    """
    validated_urls = []
    BaseUrl = base_url if type(base_url) == UniformResourceLocator else UniformResourceLocator(base_url)
    if base_url:
        BaseUrl.check_valid_format()
    url_list = list(set(url_list))
    for url in url_list:  
        Url = url if type(url) == UniformResourceLocator else UniformResourceLocator(url)
        check_scheme = Url.check_scheme()
        check_owner = Url.has_same_url_owner_(BaseUrl) if base_url else True
        if check_scheme and check_owner:
            validated_urls.append(Url)
        else:
            pass
    logger.info(f'validated urls: {validated_urls}')
    return validated_urls