#VTK Tutorial
import time
import vtkmodules.all as vtk

import vtkmodules.vtkInteractionStyle

import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderer
)

def main(arg):
    #Select colors for object and background

    colors = vtkNamedColors()

    #Customize Cone
    cone = vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(100)

    '''Terminate pipeline to map data into graphics by connecting
    output of cone source to the input of a mapper'''
    coneMapper = vtkPolyDataMapper()
    coneMapper.SetInputConnection(cone.GetOutputPort())

    #Create actor to represent cone, renders the mapper's graphics

    coneActor = vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

    #Create renderer and assign actors to it (renders window)

    ren1 = vtkRenderer()
    ren1.AddActor(coneActor)
    ren1.SetBackground(colors.GetColor3d('MidnightBlue'))

    #Finally, create render window and use defined renderer
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)
    renWin.SetWindowName('Tutorial_Step1')

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    for i in range(0, 360):
        # Render the image
        renWin.Render()
        # Rotate the active camera by one degree.
        ren1.GetActiveCamera().Azimuth(1)
        time.sleep(0.01)

    iren.Start()
if __name__ == '__main__':
    import sys

    main(sys.argv)