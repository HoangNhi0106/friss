# Build & Run

```docker-compose build```

```docker-compose up```

# Endpoints

## POST /store
- store person to database
- request body:
```
{
    "firstname": <str>,
    "lastname": <str>,
    "birthday": <date>,
    "identification": <str>
}
```
- response body: if success
```
{
    "status": 200,
    "message": "Person created successfully",
    "data": {
        "firstname": <str>,
        "lastname": <str>,
        "birthday": <date>,
        "identification": <str>,
        "id": 1
    }
}
```

## POST /check
- check if person is in database by getting persons highest match probability
- request body:
```
{
    "firstname": <str>,
    "lastname": <str>,
    "birthday": <date>,
    "identification": <str>
}
```
- response body: if success
```
{
    "status": 200,
    "message": "Get persons successfully",
    "data": {
        "matches": [
            {
                "firstname": <str>,
                "lastname": <str>,
                "birthday": <date>,
                "identification": <str>,
                "probability": <int>
            }
        ]
    }
}
```