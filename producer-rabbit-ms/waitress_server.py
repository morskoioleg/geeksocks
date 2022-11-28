from waitress import serve
import main
import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

serve(main.app, host='0.0.0.0', port=5000)
