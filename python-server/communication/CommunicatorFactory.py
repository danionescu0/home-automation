from Bluetooth import Bluetooth

class CommunicatorFactory:
    @staticmethod
    def create_communicator(type):
        if type == 'bluetooth':
            return Bluetooth()
        elif type == 'serial':
            pass
        else:
            raise Exception('Unkonwn comminicator type', type)