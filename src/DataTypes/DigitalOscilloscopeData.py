from SerializableObject import SerializableObject
from TypeCode import TypeCode
import ApplicationSerializer
from dso import SamplePoint, TriggerInformation


class DigitalOscilloscopeData(SerializableObject):
    """
    Description:
        An instance of this class is used to encapsulate the
        attributes of a DSO data
    """
    def __init__(self):
        """
        Description:
            Initializes this instance
        Arguments:
            none
        Return:
            none
        """
        SerializableObject.__init__(self, TypeCode.DsoData)
        self.__data=None

    @property
    def data(self):
        """
        Description:
            Returns the DSO data
        Arguments:
            none
        Return:
            (int)    The value
        """
        return self.__data

    def getDataSize(self):
        """
        Description:
            Gets the size in bytes of data to serialize
        Arguments:
            none
        Return:
            (int) the value
        """
        return 0
    def serializeData(self, stream):
        """
        Description:
            Serializes all data contained in this instance into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream containing the results
        """
        return stream
    def deserializeData(self, stream):
        """
        Description:
            Deserializes all data contained in this instance into
            a stream
        Arguments:
            stream (in, char [])    The stream to append to
        Returns:
            char[]    The stream minus the deserialized data
        """
        [start, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.DateTime)
        [size, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Uint)
        [captureInterval, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Uint)
        [sampleRate, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Uint)
        [avgSweeps, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Uint)
        [flags, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Uint)
        [analogSignals, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Uint)

        [level, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ushort)
        [numPre, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ushort)
        [numPost, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ushort)
        [mode, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ubyte)
        [source, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ubyte)
        [slope, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ubyte)

        [spare, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ubyte)
        [spare, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ubyte)
        [spare, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ubyte)

        [num, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ushort)
        [bper, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ushort)
        numAnalog = int(bper/2-1)
        if numAnalog < 0:
            numAnalog=0

        samples = []
        for i in range(num):
            digital = []
            analog = []

            for j in range(2):
                [data, stream] = ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Ubyte)
                for k in range(8):
                    masked = 1 if int(data & (1 << k)) != 0 else 0
                    digital.append(masked)
            for k in range(numAnalog):
                analog.append(ApplicationSerializer.ApplicationSerializer.deserialize(stream, TypeCode.Short))

            samples.append(SamplePoint(digital, analog))
        self.__data = DigitalOscilloscopeData(start=start,
                                              captureInterval=captureInterval,
                                              sampleRate=sampleRate,
                                              averageSweeps=avgSweeps,
                                              flags=flags,
                                              analogSignalMask=analogSignals,
                                              triggerInfo=TriggerInformation(
                                                level=level,
                                                numPre=numPre,
                                                numPost=numPost,
                                                mode=mode,
                                                source=source,
                                                slope=slope),
                                              samples=samples)
        return stream
