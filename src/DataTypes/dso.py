class TriggerModes(object):
    """
    Description:
        This class enumerates the trigger modes

        @author:       Troy Anderson
        @category:     Utilities
        @since:        12/08/07, Created
    """
    SINGLE = 0      # Single trigger mode (triggers once)
    CONTINUOUS = 1  # Continuous trigger mode


class TriggerInformation(object):
    """
    Description:
        This class encapsulates the trigger information

        @author:       Troy Anderson
        @category:     Utilities
        @since:        12/08/07, Created
    """
    def __init__(self, level=0, numPre=0, numPost=0, mode=0, source=0, slope=0):
        """
        Description:
            This method initializes this instance
        Arguments:
            level (int) The trigger level
            numPre (int) The number of pretrigger samples
            numPost (int) The number of posttrigger samples
            mode (int) The trigger mode
            source (int) The trigger source
            slope (int) The trigger slope
        Return:
            none
        """
        self.__level = level
        self.__numPre = numPre
        self.__numPost = numPost
        self.__mode = mode
        self.__source = source
        self.__slope = slope

    @property
    def level(self):
        """
        Description:
            This method gets the trigger level
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__level

    @level.deleter
    def level(self):
        raise TypeError("Cannot delete this property 'level'")

    @property
    def numPreTriggerSamples(self):
        """
        Description:
            This method gets the number of pretrigger samples
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__numPre

    @numPreTriggerSamples.deleter
    def numPreTriggerSamples(self):
        raise TypeError("Cannot delete this property 'numPreTriggerSamples'")

    @property
    def numPostTriggerSamples(self):
        """
        Description:
            This method gets the number of posttrigger samples
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__numPost

    @numPostTriggerSamples.deleter
    def numPostTriggerSamples(self):
        raise TypeError("Cannot delete this property 'numPostTriggerSamples'")

    @property
    def mode(self):
        """
        Description:
            This method gets the trigger mode
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__mode

    @mode.deleter
    def mode(self):
        raise TypeError("Cannot delete this property 'mode'")

    @property
    def source(self):
        """
        Description:
            This method gets the trigger source
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__source

    @source.deleter
    def source(self):
        raise TypeError("Cannot delete this property 'source'")

    @property
    def slope(self):
        """
        Description:
            This method gets the trigger slope
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__slope

    @slope.deleter
    def slope(self):
        raise TypeError("Cannot delete this property 'slope'")


class SamplePoint(object):
    """
    Description:
        This class encapsulates an oscilloscope sample point

        @author:       Troy Anderson
        @category:     Utilities
        @since:        12/08/07, Created
    """
    def __init__(self, digital, analog):
        """
        Description:
            This method initializes this instance
        Arguments:
            digital (int[]) The digital signal values
            analog (float[]) The analog signal values
        Return:
            none
        """
        self.__digital = digital
        self.__analog = analog

    @property
    def digitalSignals(self):
        """
        Description:
            This method gets the logic states for each
            digital signal
        Arguments:
            none
        Return:
            (int[]) The values
        """
        return self.__digital

    @digitalSignals.deleter
    def digitalSignals(self):
        raise TypeError("Cannot delete this property 'digitalSignals'")

    @property
    def analogSignals(self):
        """
        Description:
            This method gets the value for each
            analog signal
        Arguments:
            none
        Return:
            (int[]) The values
        """
        return self.__analog

    @analogSignals.deleter
    def analogSignals(self):
        raise TypeError("Cannot delete this property 'analogSignals'")

class DigitalOscilloscopeData(object):
    """
    Description:
        This class encapsulates an oscilloscope data buffer

        @author:       Troy Anderson
        @category:     Utilities
        @since:        12/08/07, Created
    """
    def __init__(self, start=None, captureInterval=0, sampleRate=0, averageSweeps=0,
                 flags=0, analogSignalMask=0, triggerInfo=None, samples=None):
        """
        Description:
            This method initializes this instance
        Arguments:
            start (datetime) The acquisition start time
            captureInterval (float) The capture interval
            sampleRate (float) The sample rate
            averageSweeps (float) The average number of sweeps
            flags (float) The acquisition flags
            analogSignalMask (float) The analog signal mask
            triggerInfo (TriggerInformation) The trigger information
            samples (SamplePoint[]) The sample points
        Return:
            none
        """
        self.__start = start
        self.__captureInterval = captureInterval
        self.__sampleRate = sampleRate
        self.__averageSweeps = averageSweeps
        self.__flags = flags
        self.__analogSignalMask = analogSignalMask
        self.__triggerInfo = triggerInfo
        self.__samples = samples

    @property
    def startTime(self):
        """
        Description:
            This method gets the acquisition start time
        Arguments:
            none
        Return:
            (datetime) The value
        """
        return self.__start

    @startTime.deleter
    def startTime(self):
        raise TypeError("Cannot delete this property 'startTime'")

    @property
    def captureInterval(self):
        """
        Description:
            This method gets the capture interval
        Arguments:
            none
        Return:
            (float) The value
        """
        return self.__captureInterval

    @captureInterval.deleter
    def captureInterval(self):
        raise TypeError("Cannot delete this property 'captureInterval'")

    @property
    def sampleRate(self):
        """
        Description:
            This method gets the sample rate
        Arguments:
            none
        Return:
            (float) The value
        """
        return self.__sampleRate

    @sampleRate.deleter
    def sampleRate(self):
        raise TypeError("Cannot delete this property 'sampleRate'")

    @property
    def averageSweeps(self):
        """
        Description:
            This method gets the average number of sweeps
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__averageSweeps

    @averageSweeps.deleter
    def averageSweeps(self):
        raise TypeError("Cannot delete this property 'averageSweeps'")

    @property
    def flags(self):
        """
        Description:
            This method gets the acquisition flags
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__flags

    @flags.deleter
    def flags(self):
        raise TypeError("Cannot delete this property 'flags'")

    @property
    def analogSignalMask(self):
        """
        Description:
            This method gets the analog signal mask
        Arguments:
            none
        Return:
            (int) The value
        """
        return self.__analogSignalMask

    @analogSignalMask.deleter
    def analogSignalMask(self):
        raise TypeError("Cannot delete this property 'analogSignalMask'")

    @property
    def trigger(self):
        """
        Description:
            This method gets the trigger information
        Arguments:
            none
        Return:
            (TriggerInformation) The value
        """
        return self.__triggerInfo

    @trigger.deleter
    def trigger(self):
        raise TypeError("Cannot delete this property 'trigger'")

    @property
    def samples(self):
        """
        Description:
            This method gets the samples
        Arguments:
            none
        Return:
            (SamplePoint[]) The values
        """
        return self.__samples

    @samples.deleter
    def samples(self):
        raise TypeError("Cannot delete this property 'samples'")