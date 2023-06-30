## Building the API and database
To start the psql database and the Flask server together  
`docker compose up -d`

## Triggering the ETL
Run `curl http://127.0.0.1:8000/etl` on the command line  
This should return `{"message":"ETL process started"}` if successfully started

## Verifying the results of the ETL in the database
To print the complete contents of the features table, which is populated by the ETL  
`docker exec -it db psql -U postgres -c 'select * from features'`

## Assumptions made based on ambiguities
- "Average experiments amount per user" means the average number of compounds used by the user per experiment
- For the "User's most commonly experimented compound" feature, if there are multiple compounds used the same number of times, the name of each compound is saved together as a comma separated string