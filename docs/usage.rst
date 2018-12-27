Usage
=====

Data structure
--------------

pyandi uses a model that reflects IATI architecture.

.. graphviz::

   digraph structure {
       bgcolor="#fcfcfc";

       registry [label="Registry"];
       publishers [label="Publishers", shape="box3d"];
       publisher [label="Publisher"];
       datasets [label="Datasets", shape="box3d"];
       dataset [label="Dataset"];
       activities [label="Activities", shape="box3d"];
       organisations [label="Organisations", shape="box3d"];

       registry -> publishers -> publisher -> datasets -> dataset;

       registry -> datasets [style="dashed"];
       registry -> activities [style="dashed"];
       registry -> organisations [style="dashed"];

       publisher -> activities [style="dashed"];
       publisher -> organisations [style="dashed"];

       dataset -> activities;
       dataset -> organisations;

   }

The solid arrows show the main links between data types. The dotted arrows
show additional links that pyandi provides.

The :ref:`registry <registry>` contains a list of :ref:`publishers <publisher>`.
Each :ref:`publisher <publisher>` has zero or more :ref:`datasets <dataset>`.
Each :ref:`dataset <dataset>` contains zero or more :ref:`activities <activity>`,
or zero or more :ref:`organisations <organisation>`.

Data operations
---------------

To construct a new :ref:`Registry <registry>` object, use:

.. code:: python

    import pyandi

    registry = pyandi.data()

If no data can be found, a ``NoDataError`` is raised. If data is found to be
“stale” (i.e. more than 7 days old) a warning is shown.
