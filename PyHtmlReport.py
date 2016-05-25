import matplotlib.pyplot as plt, mpld3
from scipy.misc import imread,imsave
import os
import hashlib


class htmlReport():
    def __init__(self,defaultImageDirectory='.'):
        self.body=''
	if not os.path.isdir(defaultImageDirectory):
	    os.makedirs(defaultImageDirectory)
	
        self.defaultImageDirectory=defaultImageDirectory
    
    def write(self,string,newline=True):
        self.body+=string
        if newline:
            self.newlines()
        
    def newlines(self,n=1):
        self.body+='<br>\n '*n
        
    def addPlot(self,fig):
        self.write(mpld3.fig_to_html(fig))
        
    def setDefaultImageDirectory(self,directory):
        self.defaultImageDirectory=directory
        
    def saveAndIncludeGraphic(self,im,name=None,width=None,height=None):
        if name is None:
            name=hashlib.sha1(im).hexdigest()   
            filename=name+'.png'
            if not os.path.isfile(filename):
                imsave(filename,im)
        else:
            filename=name+'.png'
            imsave(filename,im)
        filename=os.path.join(self.defaultImageDirectory,filename)
        
        self.includeGraphic(filename,width,height)
    
        
    def includeGraphic(self,src,width=None,height=None,alt=''):
        
        self.body+='<img src="%s" alt="%s"  align="middle"'%(src,alt)
        if not width is None:
            self.body+=' width="%d"'%width
        if not height is None: 
            self.body+=' height="%d"'%height
        self.body+='>'
    
    
    
    def save(self,file=None):
	if file is None:
	    file=os.path.join(self.defaultImageDirectory,'report.html')
        string='<!DOCTYPE html><html><body>'+self.body+'</body></html>' 
        output= open(file, 'w') 
        output.write(string)
        output.close()
        
 




