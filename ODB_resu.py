from abaqus import *
from abaqusConstants import *
from caeModules import *
import regionToolset 
import visualization
import odbAccess
from driverUtils import executeOnCaeStartup
import os


report_path='C:/Users/kian/Desktop/Panel/Results/'
try:
    os.makedirs(report_path)
    print 'Directory created'
except:
    print 'Directory exists'
    
########################post processing#################
job_name='Job-1'

odbname=job_name+'.odb'

odb = session.openOdb(name=odbname)

# Launching the session
session.viewports['Viewport: 1'].setValues(displayedObject=session.openOdb(name=odbname))
session.viewports['Viewport: 1'].setValues(displayedObject=session.odbs[odbname])
session.viewports['Viewport: 1'].setValues(displayedObject=None)

xy0 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 PI: ROD-2 Node 1', steps=('Step-1',))
xy1 = xyPlot.XYDataFromHistory(odb=odb, 
    outputVariableName='Reaction force: RF3 PI: ROD-2-LIN-1-2 Node 1', steps=('Step-1', ))
xy2 = sum((xy0, xy1, ), )
xy_result1 = session.XYData(name='Reaction-Force', objectToCopy=xy2)

xy_result2 = session.XYDataFromHistory(name='U3 PI: ROD N: 1 NSET DISP-1', 
    odb=odb,outputVariableName='Spatial displacement: U3 PI: ROD Node 1 in NSET DISP', 
    steps=('Step-1', ))
       
xy1 = session.xyDataObjects['U3 PI: ROD N: 1 NSET DISP-1']
xy2 = session.xyDataObjects['Reaction-Force']
xy3 = combine(xy1, -xy2/1000)
xy3.setValues(
    sourceDescription='combine ( "U3 PI: ROD N: 1 NSET DISP-1",-"Reaction-Force"/1000 )')
tmpName = xy3.name
session.xyDataObjects.changeKey(tmpName, 'XYData-2')

###write to file
report_name= job_name
report_address=report_path+report_name+'.txt'

with open(report_address, 'w') as fp:
    fp.write('\n'.join('%10.10f        %10.10f' % x for x in session.xyDataObjects['XYData-2'].data))
fp.close()

###close existing odbs
odb.close()
del session.xyDataObjects['U3 PI: ROD N: 1 NSET DISP-1']
del session.xyDataObjects['Reaction-Force']
del session.xyDataObjects['XYData-2']