# Dependencies
The project depends on `docker-compose` to orchestrate the containers.

# Instructions
- Download `ca.pem`, `service.cert`, `service.key` from the Aiven Kafka console.
- Copy those files into the `collector/` and `sink/` dirs.
- Create a `collector/.env` file with the necessary config for the collector according to the template below:
    ```
    TAKEHOME_KAFKA_HOST=
    TAKEHOME_KAFKA_PORT=
    TAKEHOME_KAFKA_CA=</rel/path/to/ca.pem>
    TAKEHOME_KAFKA_CERT=</rel/path/to/service.cert>
    TAKEHOME_KAFKA_KEY=</rel/path/to/service.key>
    TAKEHOME_KAFKA_TOPIC=

    ```
- Create a `sink/.env` file with the necessary config for the sink according to the template below:
    ```
    TAKEHOME_PG_HOST=
    TAKEHOME_PG_PORT=
    TAKEHOME_PG_DATABASE=
    TAKEHOME_PG_USER=
    TAKEHOME_PG_PASSWORD=

    TAKEHOME_KAFKA_URI=<service uri as host:port>
    TAKEHOME_KAFKA_CA=</rel/path/to/ca.pem>
    TAKEHOME_KAFKA_CERT=</rel/path/to/service.cert>
    TAKEHOME_KAFKA_KEY=</rel/path/to/service.key>
    TAKEHOME_KAFKA_TOPIC=

    TAKEHOME_CONSUMER_INTERVAL=3.0

    ```

- `make build` to build the Docker images.
- `make up` to start the collector and sink

# Known Issues
- Couldn't get `statsd` to work -- so no monitoring for now.
- Not enough time to write proper tests, except for one end-to-end test as a catch-all.
- The timestamp stored in Postgres per metric _should_ reflect the time of sampling, but figuring out the proper mapping between Python and Postgres data types felt like it wasn't worth wasting time on for the purposes of the exercise. As is, the timestamp reflects the time of insert instead.
- General cleanup is needed (obsolete dependencies in requirements.txt, better logging with timestamps)
- Health checks do not provide HTTP endpoint.



