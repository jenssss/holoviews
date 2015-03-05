"""
Module defining input/output interfaces to HoloViews.

There are two components for input/output:

Exporters: Process (composite) HoloViews objects one at a time. For
           instance, an exporter may render a HoloViews object as a
           svg or perhaps pickle it.

Archives: A collection of HoloViews objects that are first collected
          then processed together. For instance, collecting HoloViews
          objects for a report then generating a PDF or collecting
          HoloViews objects to dump to HDF5.
"""

import pickle
import param


class Exporter(param.ParameterizedFunction):
    """
    An Exporter is a parameterized function that accepts a HoloViews
    object and converts it to a new some new format. This mechanism is
    designed to be very general so here are a few examples:

    Pickling:   Native Python, supported by HoloViews.
    Rendering:  Currently using matplotlib but could use any plotting backend.
    Storage:    Databases (e.g SQL), HDF5 etc.
    """

    def __call__(self, obj, fmt=None):
        """
        Given a HoloViews object return the raw exported data and
        corresponding metadata as the tuple (data, metadata). The
        metadata should include:

        'file-ext' : The file extension if applicable (else empty string)
        'mime-type': The mime-type of the data.
        'size'     : Size in bytes of the returned data.

        The fmt argument may be used with exporters that support multiple
        output formats. If not supplied, the exporter is to pick an
        appropriate format automatically.
        """
        raise NotImplementedError("Exporter not implemented.")

    def save(self, obj, basename, fmt=None):
        """
        Similar to the call method except saves exporter data to disk
        into a file with specified basename. For exporters that
        support multiple formats, the fmt argument may also be
        supplied (which typically corresponds to the file-extension).
        """
        raise NotImplementedError("Exporter save method not implemented.")


class Pickler(Exporter):
    """
    Simple example of an archiver that simply returns the pickled data.
    """

    protocol = param.Integer(default=2, doc="""
      The pickling protocol where 0 is ASCII, 1 supports old Python
      versions and 2 is efficient for new style classes.""")

    def __call__(self, obj):
        data = pickle.dumps(obj, protocol=self.protocol)
        return data, {'file-ext':'pkl',
                      'size':len(data),
                      'mime-type':'application/python-pickle'}

    def save(self, obj, basename):
        with open(basename+'.pkl', 'w') as f:
            pickle.dump(obj, f, protocol=self.protocol)



class Archive(param.Parameterized):
    """
    An Archive is a means to collect and store a collection of
    HoloViews objects in any number of different ways. Examples of
    possible archives:

    * Generating tar or zip files (compressed or uncompressed).
    * Collating a report or document (e.g. PDF, HTML, LaTex).
    * Storing a collection of HoloViews objects to a database or HDF5.
    """

    exporter= param.ClassSelector(class_=Exporter, doc="""
      The exporter function used to convert HoloViews objects into the
      appropriate format."""  )

    def add(self, obj, *args, **kwargs):
        """
        Add a HoloViews object to the archive.
        """
        raise NotImplementedError

    def export(self,*args, **kwargs):
        """
        Finalize and close the archive.
        """
        raise NotImplementedError
