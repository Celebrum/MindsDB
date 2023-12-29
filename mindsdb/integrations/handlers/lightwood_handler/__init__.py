from mindsdb.integrations.libs.const import HANDLER_TYPE

from .__about__ import __description__ as description
from .__about__ import __version__ as version

try:
    from .lightwood_handler import LightwoodHandler as Handler

    import_error = None
except Exception as e:
    print(f'ERROR import lightwood handler: {e}')  # noqa
    Handler = None
    import_error = e

title = 'Lightwood'
name = 'lightwood'
type = HANDLER_TYPE.ML

__all__ = ['Handler', 'version', 'name', 'type', 'title', 'description', 'import_error']
