#!/usr/bin/env python

from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser
from common.entities import MISPEvent
from canari.maltego.entities import EmailAddress
from canari.config import config
import xml.etree.ElementTree as xml
import urllib2

__author__ = 'deresz'
__copyright__ = 'Copyright 2013, Andrzej Dereszowski'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'deresz'
__email__ = 'deresz@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate'
]

# Uncomment the line below if the transform needs to run as super-user
#@superuser
"""
The @configure decorator tells mtginstall how to install the transform in Maltego. It takes the following parameters:
    - label:        the name of the transform as it appears in the Maltego UI transform selection menu
    - description:  a short description of the transform
    - uuids:        a list of unique transform IDs, one per input type. The order of this list must match that of the 
                    inputs parameter. Make sure you account for entity type inheritance in Maltego. For example, if you
                    choose a DNSName entity type as your input type you do not need to specify it again for MXRecord, 
                    NSRecord, etc.
    - inputs:       a list of tuples where the first item is the name of the transform set the transform should be part
                    of, and the second item is the input entity type.
    - debug:        Whether or not the debugging window should appear in Maltego's UI when running the transform.
TODO: set the appropriate configuration parameters for your transform.
"""
@configure(
    label='To Event [MISP]',
    description='Returns a MISPEvent entities containing the corresponding email attribute"',
    uuids=[ 'misp.v2.email2event' ],
    inputs=[ ( 'MISP', EmailAddress ) ],
    debug=True
)
def dotransform(request, response):
    """
    The dotransform function is our transform's entry point. The request object has the following properties:
        - value:    a string containing the value of the input entity.
        - fields:   a dictionary of entity field names and their respective values of the input entity.
        - params:   any additional command-line arguments to be passed to the transform.
    TODO: write your data mining logic below.
    """

    apikey = config['misp/apikey']
    url = config['misp/url']
    
    # Report transform progress
    
    # Send a debugging message to the Maltego UI console
    #debug('This was pointless!')

    # Create MyMispEntity entity with value set to 'Hello <request.value>!'

    complete_url = "%s/events/restSearch/%s/%s/email-src" % (url, apikey, request.value)
    #complete_url = "%s/events/restSearch/%s/%s" % (url, apikey, request.value)
    
    debug("Accessing %s" % complete_url)
    
    try:
    
        tree = xml.parse(urllib2.urlopen(complete_url))
    
    except IOError,e:
        if hasattr(e, 'code'):
            if e.code == 404:
                # normal condition
                return response
        raise
        
    rootElement = tree.getroot()
    progress(50)
    for a in rootElement.findall('Event'):
        # Add entity to response object
        e = MISPEvent(a.find('id').text)
        e.fieldN = a.find('info').text
        response += e
    # Setting field values on the entity
    #e.field1 = 2
    #e.fieldN = 'test'
    # Update progress
    progress(100)

    # Return response for visualization
    return response


"""
Called if transform interrupted. It's presence is optional; you can remove this function if you don't need to do any
resource clean up.

TODO: Write your cleanup logic below or delete the onterminate function and remove it from the __all__ variable 
"""
def onterminate():
    debug('Caught signal... exiting.')
    exit(0)