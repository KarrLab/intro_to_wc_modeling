.. _vector_graphics:

Drawing vector graphics with Adobe Illustrator and Inkscape
===========================================================
There are two types of graphics: vector graphics and raster graphics. Vector graphics are composed of basic graphical elements such as lines, curves, arcs, and ellipses. As a result, vector graphics are infinitely scalable (i.e. they never become pixelated when they are enlarged). Consequently, vector graphics are used to make diagrams such as in scientific publications. Some of the most common vector graphic editing programs are `Illustrator <https://www.adobe.com/products/illustrator.html>`_ and `Inkscape <https://inkscape.org>`_. Illustrator is a commercial program developed by Adobe and Inkscape is a free, open-source program. Illustrator is the industry standard and more powerful than Inkscape. However, Inkscape is a little easier to learn. Some of the most common file formats used to store vector graphics are .ai, .eps, .pdf, and .svg.

Raster graphics are matrices of colored pixels. Raster graphics are commonly used for photographs as well as to display graphics originally created as vector graphics in websites and other documents. Some of the most common raster graphic editing programs are `Photoshop <https://www.adobe.com/products/photoshop.html>`_ and `Gimp <https://www.gimp.org/>`_. Photoshop is a commercial program developed by Adobe and Gimp is a free, open-source program. Photoshop is the standard among graphics professionals, but Gimp is easier to learn and sufficient for our needs as scientists. Some of the most common file formats used to store raster graphics are .gif, .jpg, and .png format. 

In this tutorial, we will teach you how to draw vector graphics with Illustrator.


Required software
-----------------
Run the following commands to install the software required for this tutorial::

    sudo apt-get install inkscape


Instructions
------------
In this tutorial we will learn how to use Inkscape to draw a digram of a cell

#. Open Illustrator
#. Set the size of the canvas

    #. Open "File" >> "Document Properties..."
    #. Set "Units" to "in"
    #. Set "Width" to "7.5"
    #. Set "Height" to "5"
    #. Close the window
    #. Type "5" to fit the canvas to your screen

#. Draw the cell membrane

    #. Select the ellipse tool
    #. Drag an ellipse over the canvas
    #. Right click on the ellipse and select "Fill and Stroke..." to edit the line and fill colors and line style of the membrane. 

        #. Increase the stroke width of the membrane
        #. Change the stroke style of the membrane to dashed
        #. Apply a radial gradient fill to the body of the membrane
        #. Adjust the center and shape of the radial gradient

    #. Add a drop shadow to the cell by selecting "Filters" >> "Shadows and Glows" >> "Drop Shadow..."

#. Draw an arrow into the cell

    #. Select the Bezier curves tool
    #. Select one or more points on the canvas. Optionally, hold down the control key to draw a straight line.
    #. Double click to finish the curve
    #. Optionally, use the "Align and Distribute" tool to straighten the line
    #. Use the edit path tools to fine tune the curve
    #. Right click on the line and select "Fill and Stroke..." >> "Stroke style" to apply arrow markers to the line

#. Create an arrow which points out of the cell by copying the first arrow

    #. Left click on the first arrow and hold down
    #. While still holding down the left mouse button, click the space bar
    #. Begin dragging your mouse
    #. Press down the control key to constraint the dragging so that the second arrow is vertically aligned with the first

#. Vertically align the cell and lines

    #. Open the "Align and distribute objects" window
    #. Select both the cell and line
    #. Click the "Center on horizontal axis" button to align the objects

#. Add a label to the cell

    #. Select the text tool
    #. Click on the canvas where you want the text to appear
    #. Type "Cell"
    #. Right click on the label and select "Text and Font..." to adjust the font type, font size, text color, and text alignment
    #. Use the dropper tool to copy the cell stroke color to the text 
    #. Bring the text in front of the cell by selecting "Object" >> "Raise to Top"

#. Group the cell and label

    #. Select the cell and label
    #. Select "Object" >> "Group"
    #. Now you can move the objects together
    #. Double click on the combine object to access the individual cell and label objects

#. Highlight a specific part of the cell

    #. Draw a rectangle over the portion of the cell that you would like to highlight
    #. Select both this new rectangle and the cell
    #. Right click on the objects and select "Set Mask"


Other useful features
---------------------

Selecting other objects with the same fill and/or stroke
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Select an object
* Right click on the object and select "Select Same" >> "Fill and Stroke"


Joining lines
^^^^^^^^^^^^^

* Use the "Edit paths by node" to select a node in a curve
* Hold to the shift key and select another node in another curve
* Click the "Join selected nodes" button to join the curves


Additional tutorials
--------------------

Illustrator
^^^^^^^^^^^
`Kevin Bonham <https://www.youtube.com/watch?v=z2bcqyRxFrI&list=PLhKpKEPEAauYIsyjnIN2YXztNo7BrZVxQ>`_ has several helpful tutorials videos designed for scientists. `Skill Developer <https://www.youtube.com/watch?v=mqJ8FyJwShw&list=PLSraMTfTYtEIrn__P9EzxFY5bYHEPC6gS>`_ also has a large number of brief tutorial videos.

Inkscape 
^^^^^^^^
`Derek Banas <https://www.youtube.com/watch?v=zUIOEXssTSE&list=PLGLfVvz_LVvTSi9bKrvGR2_DBg0Tv8Dxo>`_ has several helpful short tutorial videos. The `Inkscape Tutorials Blog <https://inkscapetutorials.org/>`_ has numerous examples of how to draw a variety of graphics.