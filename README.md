# Python CLI API

Requires Python 3.9+ and PostgreSQL 14+

## Install

To install all dependencies:

```bash
make install
```

To delete all dependencies:

```bash
make clean
```

## Test

You can test the code by launching this command:

```bash
make test
```

*You need to have all environment variables set in order to launch the command above*

## Launch Sample

*You need to have all environment variables set in order to launch those commands*

### Sport

*Create*
```bash
. env/bin/activate && python main.py create -t sport -d '{"name": "Football", "display_name": "Football", "order": 0, "is_active": true}'
````

*Update*
```bash
. env/bin/activate && python main.py update --type sport --data '{"is_active": false}' --id 'sport_uuid'
````

*Delete*
```bash
. env/bin/activate && python main.py delete --type sport --id 'sport_uuid'
````

*Search*
```bash
. env/bin/activate && python main.py search --type sport --data '[{"field": "name", "operator": "in", "value": ["Football", "Test"]}, {"field": "is_active", "operator": "=", "value": false}]'
```

### Event

*Create*
```bash
. env/bin/activate && python main.py create -t event -d '{"sport_id": "sport_uuid", "name": "Football v England", "display_name": "Football v England", "type": "inplay", "status": "inplay", "is_active": true}'
````

*Update*
```bash
. env/bin/activate && python main.py update --type event --data '{"is_active": false}' --id 'event_uuid'
````

*Delete*
```bash
. env/bin/activate && python main.py delete --type event --id 'event_uuid'
````

*Search*
```bash
. env/bin/activate && python main.py search --type event --data '[{"field": "type", "operator": "notin", "value": ["PREPLAY"]}]'
```

### Market

*Create*
```bash
. env/bin/activate && python main.py create -t market -d '{"event_id": "event_uuid", "name": "Full Time Result", "display_name": "Full Time Result", "order": 0, "schema": 1, "columns": 5, "is_active": true}'
````

*Update*
```bash
. env/bin/activate && python main.py update --type market --data '{"is_active": false}' --id 'market_uuid'
````

*Delete*
```bash
. env/bin/activate && python main.py delete --type market --id 'market_uuid'
````

*Search*
```bash
. env/bin/activate && python main.py search --type market --data '[{"field": "columns", "operator": ">=", "value": 5}]'
```

### Selection

*Create*
```bash
. env/bin/activate && python main.py create -t selection -d '{"market_id": "market_uuid", "name": "Full Time Result", "display_name": "Full Time Result", "price": 10.01, "outcome": "UNSETTLED", "is_active": true}'
````

*Update*
```bash
. env/bin/activate && python main.py update --type selection --data '{"is_active": false}' --id 'selection_uuid'
````

*Delete*
```bash
. env/bin/activate && python main.py delete --type selection --id 'selection_uuid'
````

*Search*
```bash
. env/bin/activate && python main.py search --type selection --data '[{"field": "name", "operator": "regex", "value": "Full Time Result"}]'
```

## Search

The search has been built to be as dynamic as possible. You can use any field present in DB and as operators:

 * Equal: `=`
 * Lesser than: `<`
 * Lesser or equal than: `<=`
 * Greater than: `>`
 * Greater or equal than: `>=`
 * Like case sensitive: `like`
 * Like case ìnsensitive: `ilike`
 * Like case sensitive: `notlike`
 * Like case ìnsensitive: `notilike`
 * In: `in`
 * Not In: `notin`
 * Regex case sensitive: `regex`
 * Regex case ìnsensitive: `iregex`
 * Excluding Regex case sensitive: `notregex`
 * Excluding Regex case ìnsensitive: `notiregex`

For `in` and `notin`, you may send an array or a single value which will be converted into array.

## Code linting

```bash
make lint
```

In order to enforce a certain code quality, [pylint](https://pypi.org/project/pylint/) with the option `--fail-under` is used, and is configured to fail if the score is below 9.0 (see Makefile).

Before each Pull Request, we expect developers to run this command and fix most of errors or warnings displayed.

After creating a new module, it has to be added into the Makefile command.

## Environment variables

| Name                          | Type    | Default                                      | Description                                                                                      |
| ----------------------------- | ------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| POSTGRESQL_ADDON_DB           | String  | base                                         | Name of the psql database                                                                   |
| POSTGRESQL_ADDON_USER         | String  | base                                         | Name of the psql user                                                                       |
| POSTGRESQL_ADDON_PASSWORD     | String  | base                                         | Password of the psql user                                                                       |
| POSTGRESQL_ADDON_HOST         | String  | localhost                                    | Domain/Ip of the psql database                                                                   |
| POSTGRESQL_ADDON_PORT         | Integer | 5432                                         | Port of the psql database                                                                   |
| POSTGRESQL_ADDON_URI			| String  | None | URI to connect to the DB |
| ENV 							| String  | dev | Env of the program |
