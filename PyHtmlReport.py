import matplotlib.pyplot as plt, mpld3
from scipy.misc import imsave
import os
import hashlib


class htmlReport():
    def __init__(self,defaultImageDirectory='.'):
        self.bodyList=[]
        if not os.path.isdir(defaultImageDirectory):
            os.makedirs(defaultImageDirectory)
	
        self.defaultImageDirectory=defaultImageDirectory
    
    def write(self,string,newline=True):
        self.bodyList.append(string)
        if newline:
            self.newlines()
            
    def writeLines(self,lines):
        for line in lines : 
            self.write(line)
        
    def newlines(self,n=1):
        self.bodyList.append('<br>\n '*n)
     
        
    def addPlot(self,*args,**kargs):
        fig = plt.figure()
        if "title" in kargs : 
            plt.title(kargs["title"])
            del(kargs["title"])
        plt.plot(*args,**kargs)
        self.addFig(fig)
        plt.close(fig)

    def addFig(self,fig):
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
        
        self.bodyList.append('<img src="%s" alt="%s"  align="middle"'%(src,alt))
        if not width is None:
            self.bodyList.append(' width="%d"'%width)
        if not height is None: 
            self.bodyList.append(' height="%d"'%height)
        self.bodyList.append('>')
    
    
    
    def save(self,file=None):
        if file is None:
            file=os.path.join(self.defaultImageDirectory,'report.html')
        output= open(file, 'w') 
        output.write('<!DOCTYPE html><html><body>')
        for bodyElt in self.bodyList : 
            output.write(bodyElt)
        output.write('</body></html>' )
        output.close()
        
 




