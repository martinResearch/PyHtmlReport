import matplotlib.pyplot as plt, mpld3
from scipy.misc import imsave
import os
import hashlib
import json
import numpy as np
# http://visjs.org/index.html#download_install
# https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js
#https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css
class htmlReport():
    def __init__(self,defaultImageDirectory='.',file=None):
        self.bodyList=[]
        self.scriptlist=[]
        self.stylelist=[]  
        self.defaultImageDirectory=defaultImageDirectory
        if file is None:
            file=os.path.join(self.defaultImageDirectory,'report.html')
        self.file=file
        self.usePLotly=False
        if not os.path.isdir(defaultImageDirectory):
            os.makedirs(defaultImageDirectory)        
    
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
    
    def addFig(self,fig,method=None,width=None,height=None):
        fig.canvas.draw_idle()
        is3D= hasattr(fig.gca(), 'get_zlim')
        if method is None:
            if is3D:
                method='plotly'
            else:
                method='mpld3'
        plt.show()
        
        ax=fig.gca()
        title=ax.get_title()
        if title=='':
            print ('you should add a title to the figure')
        if method=='mpld3':
            if  hasattr(fig.gca(), 'get_zlim'):
                print ('3D plot are not handled by mpld3 yet , use plotly instead')
                raise
            self.write(mpld3.fig_to_html(fig))
        if method=='visjs':
            # mpld3 does not seem to support 3D plots
            # could use http://visjs.org/graph3d_examples.html   
            pass
        if method=='plotly':
            
            figsize = fig.get_size_inches()*fig.dpi # size in pixels            
            if width is None:
                width=figsize[0]
            if height is None:
                width=figsize[1]                
            jsonLayout,jsonData=self.matplotlibToPlotlyJson(ax)
            str='<div class="plotly"' ;
            if (not width is None) or (not height is None):
                str+='style="';
                if not width is None:
                    str+='width:%dpx;'%width
                if not height is None:
                    str+='height:%dpx;'%height
                str+='"'
            str+="data='%s' layout='%s' ></div>"%(jsonData,jsonLayout)
            self.write(str)  
            self.usePLotly=True
            
        if method=='svg':
            pass
            
        
    def matplotlibToPlotlyJson(self,ax):
 
        linesPlotly=[];
        is3D=hasattr(ax, 'get_zlim')
        hasline=False
        for line in ax.get_lines():
            s={}
            hasline=True
            color=line.get_color()
            if is3D:
                if np.any(np.isnan(line._verts3d)):
                    raise ('nans not handled yet for plotly export')               
                s['x']=line._verts3d[0].tolist()
                s['y']=line._verts3d[1].tolist()
                s['z']=line._verts3d[2].tolist()
                s['type']= 'scatter3d'
                s['mode']= 'lines'
            else:
                if np.any(np.isnan(s['x'])) or np.any(np.isnan(s['y'])):
                    raise ('nans not handled yet for plotly export')                   
                s['x']=line.get_xdata().tolist()
                s['y']=line.get_ydata().tolist()                
                s['name']=line.get_label()
                s['legendgroup']=line.get_label()
                s['showlegend']=True
                s['line']={'color':color[0:3],'width':line.get_lw()}
            
            
            linesPlotly.append(s)
            
            
        for collection in ax.collections:
            s={}
            if  is3D:
                tmp=collection.get_offsets()
                
                #s['x']=tmp[:,0].tolist()
                #s['y']=tmp[:,1].tolist()  
                if np.any(np.isnan(tmp)):
                    raise ('nans not handled yet for plotly export')
                tmp=collection._offsets3d
                s['x']=list(tmp[0])
                s['y']=list(tmp[1])
                s['z']=list(tmp[2])
                s['type']= 'scatter3d'
                
              
            else:
                tmp=collection.get_offsets()
                
                s['x']=tmp[:,0].tolist()
                s['y']=tmp[:,1].tolist()   
                s['type']= 'scatter'
                if np.any(np.isnan(s['x'])) or np.any(np.isnan(s['y'])):
                    raise ('nans not handled yet for plotly export')                  
            
     
            s['mode']=  'markers'
           
     
            makersDict={'+':'cross','d':'diamond','x':'x-dot','s':'square'}
            markerSize=collection.get_sizes()/10
            s['marker']={'symbol':'circle','size':int(markerSize[0]),'sizemode':'diameter'}# not sure how to retrieve the mqrker shape in matplotlib
            s['name']=collection.get_label()
            s['legendgroup']=collection.get_label()
            s['showlegend']=True 
            linesPlotly.append(s)
            
        layout={}
        layout['title']=ax.get_title()
      

        if is3D:
            layout['scene']={}
            plt.pause(1)# the axis infor,mation seem to lag 
            layout['scene']['xaxis']={'tile':ax.get_xlabel(),'range':ax.get_xbound()}
            layout['scene']['yaxis']={'tile':ax.get_ylabel(),'range':ax.get_ybound()}            
            layout['scene']['zaxis']={'tile':ax.get_zlabel(),'range':ax.get_zbound()}
        else:
            layout['xaxis']={'tile':ax.get_xlabel(),'range':ax.get_xbound()}
            layout['yaxis']={'tile':ax.get_ylabel(),'range':ax.get_ybound()}            
        jsonLayout=json.dumps(layout)
        jsonData=json.dumps(linesPlotly)
        return jsonLayout,jsonData
    
        
    def setDefaultImageDirectory(self,directory):
        self.defaultImageDirectory=directory
        
    def addImage(self,im,name=None,width=None,height=None):
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
    
    def addJavascriptSource():
        pass
    

   
    
    def save(self,file=None):
        
        if file is None:
           
            file=self.file
        output= open(file, 'w') 
        output.write('<!DOCTYPE html><html><body>\n')
        output.write('<head>\n');
        if self.usePLotly:
            output.write(' <script src="https://code.jquery.com/jquery-1.12.4.js"></script>\n')
            output.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n');
        output.write('</head>\n');        

        output.write('<body>\n' )
        for bodyElt in self.bodyList : 
            output.write(bodyElt)
        output.write('</body></html>\n' )
        
        if self.usePLotly:
            output.write('  <script>$( ".plotly" ).each(function( index ) {Plotly.plot( this ,jQuery.parseJSON($( this ).attr( "data")),jQuery.parseJSON($( this ).attr( "layout")));});</script>')
            output.write('  <script>(function() { $(''.zoomablesvg'').each(function( index ){var $panzoom = $(this).panzoom(); $panzoom.on(''mousewheel.focal'', function( e ) {var delta = e.delta || e.originalEvent.wheelDelta; var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0; $panzoom.panzoom(''zoom'', zoomOut, { increment: 0.1, animate: false,  focal: e    });   }  )  }); })();</script>')
        
        output.write('   <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>   ') 
        output.close()
        
 




