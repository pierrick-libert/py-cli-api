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

# Then we create the trigger and function
with DB.get_instance().get_session() as session:
    # Create TRIGGER and FUNCTION for SportModel
    session.execute('''
        CREATE OR REPLACE FUNCTION check_update_sport() RETURNS TRIGGER AS $check_update_sport$
            BEGIN
                -- Update the events if sport is disabled
                IF NEW.is_active = false THEN
                    UPDATE event SET is_active=false WHERE sport_id=NEW.id;
                END IF;
                RETURN NULL;
            END;
        $check_update_sport$ LANGUAGE plpgsql;

        DROP TRIGGER IF EXISTS check_update_sport ON sport;
        CREATE TRIGGER check_update_sport
            AFTER UPDATE ON sport
            FOR EACH ROW
            WHEN (OLD.is_active IS DISTINCT FROM NEW.is_active)
            EXECUTE FUNCTION check_update_sport();
    ''')

    # Create TRIGGER and FUNCTION for EventModel
    session.execute('''
        CREATE OR REPLACE FUNCTION check_upsert_event() RETURNS TRIGGER AS $check_upsert_event$
            DECLARE
                is_active BOOL;
            BEGIN
                -- Update the sport status if all events are inactive or if at least one if active
                EXECUTE format('SELECT s.is_active FROM sport s WHERE s.id=$1') INTO is_active USING NEW.sport_id;
                IF (SELECT COUNT(e.id) from event e WHERE e.is_active=true AND e.sport_id=NEW.sport_id) = 0 THEN
                    UPDATE sport SET is_active=false WHERE id=NEW.sport_id;
                ELSIF is_active = false AND NEW.is_active = true THEN
                    UPDATE sport SET is_active=false WHERE id=NEW.sport_id;
                END IF;
                -- In case of update with is_active=false, we need to impact all markets
                IF OLD.is_active IS NOT NULL AND NEW.is_active = false THEN
                    UPDATE market SET is_active=false WHERE event_id=NEW.id;
                END IF;
                RETURN NULL;
            END;
        $check_upsert_event$ LANGUAGE plpgsql;

        DROP TRIGGER IF EXISTS check_insert_event ON event;
        CREATE TRIGGER check_insert_event
            AFTER INSERT ON event
            FOR EACH ROW
            EXECUTE FUNCTION check_upsert_event();
        DROP TRIGGER IF EXISTS check_update_event ON event;
        CREATE TRIGGER check_update_event
            AFTER UPDATE ON event
            FOR EACH ROW
            WHEN (OLD.is_active IS DISTINCT FROM NEW.is_active)
            EXECUTE FUNCTION check_upsert_event();
    ''')


    # Create TRIGGER and FUNCTION for MarketModel
    session.execute('''
        CREATE OR REPLACE FUNCTION check_upsert_market() RETURNS TRIGGER AS $check_upsert_market$
            DECLARE
                is_active BOOL;
            BEGIN
                -- Update the event status if all markets are inactive or if at least one if active
                EXECUTE format('SELECT e.is_active FROM event e WHERE e.id=$1') INTO is_active USING NEW.event_id;
                IF (SELECT COUNT(m.id) from market m WHERE m.is_active=true AND m.event_id=NEW.event_id) = 0 THEN
                    UPDATE event SET is_active=false WHERE id=NEW.event_id;
                ELSIF is_active = false AND NEW.is_active = true THEN
                    UPDATE event SET is_active=false WHERE id=NEW.event_id;
                END IF;
                -- In case of update with is_active=false, we need to impact all selection
                IF OLD.is_active IS NOT NULL AND NEW.is_active = false THEN
                    UPDATE selection SET is_active=false WHERE market_id=NEW.id;
                END IF;
                RETURN NULL;
            END;
        $check_upsert_market$ LANGUAGE plpgsql;

        DROP TRIGGER IF EXISTS check_insert_market ON market;
        CREATE TRIGGER check_insert_market
            AFTER INSERT ON market
            FOR EACH ROW
            EXECUTE FUNCTION check_upsert_market();
        DROP TRIGGER IF EXISTS check_update_market ON market;
        CREATE TRIGGER check_update_market
            AFTER UPDATE ON market
            FOR EACH ROW
            WHEN (OLD.is_active IS DISTINCT FROM NEW.is_active)
            EXECUTE FUNCTION check_upsert_market();
    ''')

    # Create TRIGGER and FUNCTION for SelectionModel
    session.execute('''
        CREATE OR REPLACE FUNCTION check_upsert_selection() RETURNS TRIGGER AS $check_upsert_selection$
            DECLARE
                is_active BOOL;
            BEGIN
                -- Update the market status if all selections are inactive or if at least one if active
                EXECUTE format('SELECT m.is_active FROM market m WHERE m.id=$1') INTO is_active USING NEW.market_id;
                IF (SELECT COUNT(s.id) from selection s WHERE s.is_active=true AND s.market_id=NEW.market_id) = 0 THEN
                    UPDATE market SET is_active=false WHERE id=NEW.market_id;
                ELSIF is_active = false AND NEW.is_active = true THEN
                    UPDATE market SET is_active=false WHERE id=NEW.market_id;
                END IF;
                RETURN NULL;
            END;
        $check_upsert_selection$ LANGUAGE plpgsql;

        DROP TRIGGER IF EXISTS check_insert_selection ON selection;
        CREATE TRIGGER check_insert_selection
            AFTER INSERT ON selection
            FOR EACH ROW
            EXECUTE FUNCTION check_upsert_selection();
        DROP TRIGGER IF EXISTS check_update_selection ON selection;
        CREATE TRIGGER check_update_selection
            AFTER UPDATE ON selection
            FOR EACH ROW
            WHEN (OLD.is_active IS DISTINCT FROM NEW.is_active)
            EXECUTE FUNCTION check_upsert_selection();
    ''')
