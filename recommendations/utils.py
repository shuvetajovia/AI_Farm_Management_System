import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings

def render_to_pdf(template_src, context_dict={}):
    """
    Render a Django template to PDF using xhtml2pdf.
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    
    # Create a file-like buffer to receive PDF data.
    result = BytesIO()
    
    # Convert HTML to PDF
    # We need to handle static files correctly for xhtml2pdf
    def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can verify links and images.
        """
        # Global variables
        sUrl = settings.STATIC_ROOT if hasattr(settings, 'STATIC_URL') else '/static/'
        sUrl = settings.STATIC_URL
        sRoot = getattr(settings, 'STATIC_ROOT', None)      # Typically /path/to/static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /path/to/media/

        # Convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            if sRoot:
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                path = "" # Will fail isfile check and go to fallback
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # Make sure that file exists
        if not os.path.isfile(path):
             # Try to find in STATICFILES_DIRS if DEBUG is True and STATIC_ROOT is not populated
             if settings.DEBUG:
                 for static_dir in settings.STATICFILES_DIRS:
                     possible_path = os.path.join(static_dir, uri.replace(sUrl, ""))
                     if os.path.isfile(possible_path):
                         return possible_path
             raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
        return path

    # Generate PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
