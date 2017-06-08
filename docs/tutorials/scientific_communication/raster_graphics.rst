Editing raster graphics with Gimp
=================================
As described in the :ref:`vector graphics tutorial <vector_graphics>`, there are two types of graphics: vector graphics (generally diagrams in .ai, .eps, .pdf, or .svg format) and raster graphics (generally photos in .gif, .jpg, or .png format). In this tutorial, we will teach you how to edit raster graphics with `Gimp <https://www.gimp.org/>`_, an open-source raster graphic editing program.


Required software
-----------------
Run the following commands to install the software required for this tutorial::

    sudo apt-get install gimp


Instructions
------------
In this tutorial we will learn how to crop a face out of a photo to create a headshot for a website

#. Open Gimp
#. Open a photo
#. Add a transparency channel ("Layer" >> "Transparency" >> "Add a alpha channel")
#. Use the Intelligent scissors select tool ("Tools" >> "Selection Tools" >> "Intelligent scissors") to select only the face. Zoom in to select the face precisely. Note, Gimp provides several additional selection tools including tools to select rectangles and ovals and to select regions by color.
#. Type enter to accept the selection
#. Feather the selection so that the transition between the face and background is not so abrupt when we cut out the background ("Select" >> "Feather...")
#. Select the background by inverting the selection ("Select" >> "Invert")
#. Delete the background ("Edit" >> "Clear")
#. Change the color mode to grey scale ("Image" >> "Mode" >> Select "Grayscale")
#. Crop the head and make the image square ("Tools" >> "Transform Tools" >> "Crop"). 
    
    #. Disable "Current layer only"
    #. Drag a rectangle over the photo
    #. In the "Tool Options" pane, 

        #. Set "Size" >> 10, 10
        #. Enable "Fixed" >> "Aspect ratio"

    #. Adjust the size and shape of the selection box
    #. Type enter to crop the image

#. Scale the image ("Image" >> "Scale Image...")
#. Export the image ("File" >> "Export As ...")


Additional tutorials
--------------------
`Learn GIMP <https://www.youtube.com/watch?v=bqF4X1bs6NA&list=PLMK2xMz5H5ZuPzp5FfEIDjeYavpyRgpcb>`_ has several helpful short tutorial videos.
