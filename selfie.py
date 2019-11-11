import urllib
import rdflib
from rdflib import URIRef
from qgis.PyQt.QtCore import QAbstractListModel,QAbstractTableModel


SCHEMAS_ORG = rdflib.Namespace("http://schema.org/")
# request header simulate a browser. asks for a ttl in preference
request_headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Accept" : "application/x-turtle,text/turtle,application/rdf+xml,application/ld+json",
"Connection": "keep-alive" 
}


def getMir(sUri):
    request = urllib.request.Request(sUri, headers=request_headers)
    response = urllib.request.urlopen(request)
    content_type = response.info()['Content-type']
    g=rdflib.Graph()
    g.parse(data=response.read(),format=content_type)
    return Selfie(g,URIRef(sUri))

    
    
class Representation:
    def __init__(self,g,rep_resource):
        self.url = None
        self.label = None
        self.is_resource = False
        self.formats = []
        # TO DO , all the other properties
        for predicate,obj in g.predicate_objects(rep_resource):
            # we are looking for a schema.url
            if predicate == SCHEMAS_ORG['url']:
                self.url = obj.to_python()
            if predicate == RDFS['label']:
                self.label = obj.to_python
            if predicate == DCTERMS['format']:
                self.formats.append(obj.to_python())
        if self.url is None:
            # we did not find a url, we assume it's a resource
            self.url = rep_resource.to_python()
            self.is_resource = True
            
    def hasFormat(self,f):
        ''' check if this format is supported '''
        return f in self.formats
    
    def __repr__(self):
        return self.label
    
    
class Links:
    def __init__(self,predicate,obj):
        self.predicate = predicate
        self.obj = obj
        
    
class Selfie:
    def __init__(self,g,context_uri):
        self.g = g
        self.context_resource = context_uri
        self.representations = []
        for obj in g.objects(context_uri,SCHEMAS_ORG['subjectOf']):
            self.representation.append(Representation(obj))
        
        
    def representationModel(self):
        return RepresentationModel(self)
        pass
    
    def linkModel(self):
        ''' return a table model for links '''
        pass
        
class RepresentationModel(QAbstractListModel):
    def __init__(self, s, parent=None,*args):
        QAbstractListModel.__init__(self, parent, *args)
        self.selfie = s
        
        
    def rowCount(self):
        return len(self.selfie.representations)
    
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.selfie.representations[index.row()])
        else: 
            return QVariant()
        
        