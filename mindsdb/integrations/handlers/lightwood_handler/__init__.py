from mindsdb.integrations.libs.const import HANDLER_TYPE

from .__about__ import __description__ as description
from .__about__ import __version__ as version

from mindsdb.utilities import log
logger = log.getLogger(__name__)

try:
    logger.error('LIGHTWOOD importing')
    from .lightwood_handler import LightwoodHandler as Handler
    logger.error('LIGHTWOOD imported')
    import_error = None
except Exception as e:
    logger.error(f'LIGHTWOOD error {e}')
    print(f'ERROR import lightwood handler: {e}')  # noqa
    Handler = None
    import_error = e

title = 'Lightwood'
name = 'lightwood'
type = HANDLER_TYPE.ML

__all__ = ['Handler', 'version', 'name', 'type', 'title', 'description', 'import_error']
