Editing raster graphics with Gimp
=================================
As described in the :ref:`vector graphics tutorial <vector_graphics>`, there are two types of graphics: vector graphics (generally diagrams in .ai, .eps, .pdf, or .svg format) and raster graphics (generally photos in .gif, .jpg, or .png format). This tutorial will teach you how to edit raster graphics with `Gimp <https://www.gimp.org/>`_, an open-source raster graphic editing program, by creating a head shot for a website.

Concepts
--------
The exercise below will introduce you to the following key concepts of raster graphic editing:

* Zooming
* Adding layers
* Selecting regions
* Expanding selections
* Clearing selections
* Filling selections
* Changing the color mode
* Cropping images
* Rescaling images


Required software
-----------------
This tutorial requires Gimp.

On Ubuntu, Gimp can be installed by running this command::

    sudo apt-get install gimp


Exercise
------------
In this exercise, we will learn how to edit raster graphics by creating a head shot of President Obama for a website. This will include selecting the face, removing the background, cropping the image, resizing the image, and exporting the image for fast.

#. Download a photo of :download:`President Obama <example_photo.jpg>`
#. Open Gimp
#. Open the photo
#. Add an alpha channel to enable a transparent background ("Layer" >> "Transparency" >> "Add a alpha channel")
#. Use the Intelligent scissors select tool ("Tools" >> "Selection Tools" >> "Intelligent scissors") to select only the face. Zoom in to select the face precisely. Note, Gimp provides several additional selection tools including tools to select rectangles and ovals and to select regions by color.
#. Type enter to accept the selection
#. Feather the selection so that the transition between the face and background is not so abrupt when we cut out the background ("Select" >> "Feather...")
#. Select the background by inverting the selection ("Select" >> "Invert")
#. Delete the background ("Edit" >> "Clear")
#. Change the color mode to gray scale ("Image" >> "Mode" >> Select "Grayscale")
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


Screen capture
^^^^^^^^^^^^^^
.. raw:: html

    <object data="../../../_static/tutorials/scientific_communication/raster_graphics/screen_capture.swf" width="697" height="403" >
    </object>

`Open the screen capture in a separate page <../../../_static/tutorials/scientific_communication/raster_graphics/index.html>`_


Additional tutorials
--------------------
`Learn GIMP <https://www.youtube.com/watch?v=bqF4X1bs6NA&list=PLMK2xMz5H5ZuPzp5FfEIDjeYavpyRgpcb>`_ has several helpful short tutorial videos.
