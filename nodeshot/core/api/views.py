from django.core.urlresolvers import NoReverseMatch

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .urls import urlpatterns


@api_view(('GET',))
def root_endpoint(request, format=None):
    """
    Summary of RESTful API.
    """
    endpoints = []
    
    # loop over url modules
    for urlmodule in urlpatterns:
        
        try:
            urlmodule.urlconf_module
            is_urlconf_module = True
        except AttributeError:
            is_urlconf_module = False
        
        # if url is really a urlmodule
        if is_urlconf_module:
            
            # loop over urls of that module
            for url in urlmodule.urlconf_module.urlpatterns:
                
                # try adding url to list of urls to show
                try:
                    endpoints.append({
                        'name': url.name.replace('api_', ''),
                        'url': reverse(url.name, request=request, format=format)
                    })
                # urls of object details will fail silently (eg: /nodes/<slug>/)
                except NoReverseMatch:
                    pass
                
    
    return Response(endpoints)