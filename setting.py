from logging import getLoger, basicConfig, FileHandler, StreamHandler, DEBUG, ERROR

logger = getLoger()
FORMAT = '%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s : %(message)s'
file_handler = FileHandler("data.log")
file_handler.setLevel(DEBUG)
console = StreamHandler()
console.setLevel(ERROR)
basicConfig(level=DEBUG, format=FORMAT, handlers=[file_handler, console])