from Bluetooth import Bluetooth

class CommunicatorFactory:
    @staticmethod
    def createCommunicator(type):
        if type == 'bluetooth':
            return Bluetooth()
        elif type == 'serial':
            pass
        else:
            raise Exception('Unkonwn comminicator type', type)