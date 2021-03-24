
from libs.config import get_config

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)

def run():
    config = get_config()

if __name__ == '__main__':
    run()
