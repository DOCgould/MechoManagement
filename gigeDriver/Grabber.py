import PySpin

class CameraDriver:
    """ A class for interacting with a gige Camera

    Attributes
    ----------
    cam : PySpin.Camera
        Actual Camera object

    Methods
    -------
    GetNextImage()
        Grabs reference to next available image from camera
    DeInit()
        Clean up all camera related objects in memory
    """
    def __init__(self,serial):
        """
        Parameters
        ----------
        serial : str
            Serial number of camera
        """
        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        assert len(self.cam_list) != 0, "No Cameras Found"

        self.cam = self.cam_list.GetBySerial(serial) 
        self.cam_list.Clear()

        self.cam.Init()
        nodemap = self.cam.GetNodeMap()
        s_node_map = self.cam.GetTLStreamNodeMap()

        # Set Camera Acquisition Mode to Continuous
        node_acq_mode = PySpin.CEnumerationPtr(
            nodemap.GetNode('AcquisitionMode'))
        node_acq_mode_continuous = node_acq_mode.GetEntryByName('Continuous')

        acq_mode_continuous = node_acq_mode_continuous.GetValue()
        node_acq_mode.SetIntValue(acq_mode_continuous)

        # Set Buffer to Newest First
        handling_mode = PySpin.CEnumerationPtr(
            s_node_map.GetNode('StreamBufferHandlingMode'))
        handling_mode_entry = PySpin.CEnumEntryPtr(
            handling_mode.GetCurrentEntry())

        handling_mode_entry = handling_mode.GetEntryByName('NewestFirst')
        handling_mode.SetIntValue(handling_mode_entry.GetValue())

        # Set Image Pixel Format to RGB8
        node_pixel_format = PySpin.CEnumerationPtr(
            nodemap.GetNode('PixelFormat'))
        node_pixel_format_rgb8 = PySpin.CEnumEntryPtr(
            node_pixel_format.GetEntryByName('RGB8'))

        pixel_format_rgb8 = node_pixel_format_rgb8.GetValue()
        node_pixel_format.SetIntValue(pixel_format_rgb8)

        self.cam.BeginAcquisition()
    
    
    def GetNextImage(self):
        """ Grabs reference to next available image from camera

        Returns
        -------
        img : PySpin.ImagePtr
            Reference to image
        """
        try:
            img = self.cam.GetNextImage()
            #TODO: I forgot to check if this line was necessary
            # after changing the camera's pixelFormat in __init__()
            img = img.Convert(PySpin.PixelFormat_RGB8, PySpin.HQ_LINEAR)

            if img.IsIncomplete():
                print("Image Incomplete with status: {}".format(
                    img.GetImageStatus()))
                return None
            else: # good image!
                return img
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return None 

    def DeInit(self):
        """Clean up all camera related objects in memory"""
        self.cam.EndAcquisition()
        self.cam.DeInit()
        del self.cam
        self.system.ReleaseInstance()

if __name__ == "__main__":
    c = CameraDriver("16456291")
    for i in range(10):
        name = "%d.jpg" % i
        c.GetNextImage().Save(name)
    c.DeInit() #if you don't DeInit Spinnaker will yell at you