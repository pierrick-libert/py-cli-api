'''Script launch when you install the project through `make install`'''
from models.sport import SportModel
from models.event import EventModel, EventType, EventStatus
from models.market import MarketModel
from models.selection import SelectionModel, SelectionOutcome

from utils.db import DB

# We're doing a simple creation of tables with no migrations
# Check `markdown.md` to understand how it could be improved
DB.get_instance().create_enum(EventType, 'eventtype')
DB.get_instance().create_enum(EventStatus, 'eventstatus')
DB.get_instance().create_enum(SelectionOutcome, 'selectionoutcome')
DB.get_instance().create_table_from_model(SportModel())
DB.get_instance().create_table_from_model(EventModel())
DB.get_instance().create_table_from_model(MarketModel())
DB.get_instance().create_table_from_model(SelectionModel())
