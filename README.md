# challenge-aeromexico

## Ejecutar ETL y levantar API  con Docker

```sh
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

## Limpiar imagenes
```sh
docker-compose -f docker-compose.yml down --remove-orphans
```

## Probar Api

### Obtener todos los registros de la BD
```sh
curl --location 'http://localhost:8080/rows'
```

### Insertar un registro a la BD con la estructura del schema definido
```sh
curl --location 'http://localhost:8080/rows' \
--header 'Content-Type: application/json' \
--data-raw '{
"first_name":"Pedro",
"last_name":"Ruiz",
"company_name":"cocacola",
"address":"Reforma 77",
"city":"cdmx",
"state":"cdmx",
"zip":"12345",
"phone1":"123-888-999",
"phone2":"123-456-789",
"email":"pr@cocacola.com",
"department":"it"
}'
```

## Ejecutar unit tests con Docker
```sh
docker-compose -f docker-compose-tests.yml build
docker-compose -f docker-compose-tests.yml up
```
## Limpiar imagenes de tests
```sh
docker-compose -f docker-compose-tests.yml down --remove-orphans
```
