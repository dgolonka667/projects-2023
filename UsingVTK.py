#Using VTK

import vtkmodules.all as vtk

# Create a rendering window
renWin = vtk.vtkRenderWindow()

# Create a renderer
renderer = vtk.vtkRenderer()
renWin.AddRenderer(renderer)

# Create a render window interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renWin)

# Create a sphere source
sphere = vtk.vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(1)

# Create a mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Create an actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

renWin.SetSize(800, 600)  # Set the render window size to 800x600 pixels

# Add the actor to the renderer
renderer.AddActor(actor)

renderer.ResetCamera()

renderWindowInteractor.Start()
