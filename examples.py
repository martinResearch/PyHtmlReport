import matplotlib.pyplot as plt, mpld3
from PyHtmlReport import htmlReport	
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from mpl_toolkits.mplot3d import art3d

def example1():

    Im=np.random.rand(30,60)

    plt.ion()
    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure(figsize=[3,3])
    #ax = fig.gca(projection='3d')# does not seem to work with mpld3
    ax = fig.gca()
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    ax.plot(x, y, label='parametric curve')
    
    cloud=np.random.rand(60,2)*5
    
    ax.scatter(cloud[:,0],cloud[:,1])
    
    ax.set_title('simple plot example')
    ax.legend()
    #mpld3.show()
    #plt.show()
    
    cloud=np.random.rand(60,3)
    fig3D = plt.figure()
    ax = fig3D.add_subplot(111, projection='3d')    
    ax.scatter(cloud[:,0],cloud[:,1],cloud[:,2],marker ='d',s=2)
    plt.show()
    
    
    report=htmlReport()


    report.addFig(fig,method='plotly')
    report.addFig(fig3D,method='plotly')
    report.addImage(Im,width=300)
    report.newlines(5)
    report.addImage(Im,width=300)
    report.save('test3D.html')


if __name__ == "__main__":
    example1()


