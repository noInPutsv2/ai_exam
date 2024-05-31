# Database + AI eksamensprojekt
## Gruppemedlemmer
* Benjamin Ritthidech Sommervoll (CPH-BS202)
* Line Phoebe Wienke (*)
* Louise Sitting Estrup (*)

## Projektbeskrivelse
Formålet med dette projekt er at skabe en chatbot, der er i stand til at besvare spørgsmål om Harry Potter universet. Chatbotten skal hente informationer fra en database omhandlende bøgerne, filmene og andre relaterede medier for at give svar.


## Application Domain
### Use cases

### Functional requirements
- Chatbotten skal kunne svare på spørgsmål relateret til Harry Potter
- Brugere skal kunne se tidligere interaktioner med chatbotten (Chat historik)
### Non functional requirements
- Hurtig respons
- Skal kunne være fejl tolerante (queues)
- Skal have høj tilgængelighed
- Skalerbarhed
- 4 Forskellige database typer
    - NoSQL Database
    - Relationel Database (SQL)
    - Graph Database
    - Vector Database


## Henting af Harry Potter data
Vi henter al vores data omkring Harry Potter og universet fra denne side: https://harrypotter.fandom.com/wiki/Main_Page. Her starter vi med at gå ind på siderne omkrig de syv (main) bøger og derfra tager info om dem, samt alle links på de sider, hvorefter vi går ind på de link tager information om de sider plus links vi ikke alledrede har i forvejen. Dette bliver gjort i Harry_Potter_chatbot_get_info notebooken hvor funtioner til at hente fra siderne ligger i myloadlib.py. Efter at have hentet i ukendt tid, fik vi en connection error men valgt at vi havde nok info med de 21996 dokumenter vi havde hentet. Alle dokumenterne bliver lagt i en jsonl film, som ligger under data mappen men ikke på github da den fylder over 100Mb, her kan de så blive brugt i andre notebooks.

## Databaser
Projektet indeholder 4 forskellige typer databaser:
* SQL (MSSQL)
* NoSQL (MongoDB)
* Graph (Neo4J)
* Vector (Chroma)

Databaserne er sat op med Docker, testede operations systemer er:
* Windows 11 + 4.30.0 (149282)

### Vector database (Chroma)

### Graph database (Neo4J) 
Som vores graph database bruger vi Neo4j. Vi bruger graph databasen til at kunne se realationer mellem fx karakterene fra bøgerne.

#### Transformere til graph
Vi bruger Diffbot til at transformere vores text data vi har hentet om til en graph. Vi har valgt at bruge det fordi det er hurtigere og nemmere end selv at skulle gennemgå de over 20000 dokumenter vi har hentet og lave noder og realationer. Dog ville det være bedst hvis vi selv gjorde det, da diffbot har nogle forud indstillinger som ikke er de bedste til vores text. Bla. kunne det være at vi havde brug for noder til besværgelser (fra bøgerne).

#### graph shema
#### graph algorithmer 

### SQL database (MSSQL)

### NoSQL (MongoDB)
Vores MongoDB opsætning består af:
* 2 config server
* 2 routers
* 2 Shards (Replica sets)

![MongoDB architecture](./git_photos/mongodb_architecture.jpg)

#### Opsætning af MongoDB database
Vi bruger MongoDB version 7.0.
1. Opret netværk for alle mongo services 
    - ```
        docker network create mongo-db-network
        ```
2. Opret 2 config servers
    - ```
        docker run -d --net mongo-db-network --name config-server-1 -p 27101:27017 mongo:7.0 mongod --port 27017 --configsvr --replSet config-server-replSet
        docker run -d --net mongo-db-network --name config-server-2 -p 27102:27017 mongo:7.0 mongod --port 27017 --configsvr --replSet config-server-replSet
        ```
3. Initialize config replica sets
    - ```
        docker exec -it config-server-1 mongosh
        rs.initiate({_id: "config-server-replSet", configsvr: true, members: [ { _id: 0, host: "config-server-1:27017" }, { _id: 1, host: "config-server-2:27017" }]})
        ```
4. Create shards
    - ```
        docker run -d --net mongo-db-network --name shard-1-node-a -p 27111:27017 mongo:7.0 mongod --port 27017 --shardsvr --replSet shard-1-replSet 
        docker run -d --net mongo-db-network --name shard-1-node-b -p 27121:27017 mongo:7.0 mongod --port 27017 --shardsvr --replSet shard-1-replSet 
        docker run -d --net mongo-db-network --name shard-1-node-c -p 27131:27017 mongo:7.0 mongod --port 27017 --shardsvr --replSet shard-1-replSet
        ```
    - ```
        docker run -d --net mongo-db-network --name shard-2-node-a -p 27112:27017 mongo:7.0 mongod --port 27017 --shardsvr --replSet shard-2-replSet 
        docker run -d --net mongo-db-network --name shard-2-node-b -p 27122:27017 mongo:7.0 mongod --port 27017 --shardsvr --replSet shard-2-replSet 
        docker run -d --net mongo-db-network --name shard-2-node-c -p 27132:27017 mongo:7.0 mongod --port 27017 --shardsvr --replSet shard-2-replSet
        ```
5. Initialize shard replica sets
    - ```
        docker exec -it shard-1-node-a mongosh
        rs.initiate({_id: "shard-1-replSet", members: [{ _id: 0, host: "shard-1-node-a:27017" }, { _id: 1, host: "shard-1-node-b:27017" }, { _id: 2, host: "shard-1-node-c:27017" }] })
        ```
    - ```
        docker exec -it shard-2-node-a mongosh
        rs.initiate({_id: "shard-2-replSet", members: [{ _id: 0, host: "shard-2-node-a:27017" }, { _id: 1, host: "shard-2-node-b:27017" }, { _id: 2, host: "shard-2-node-c:27017" }] })
        ```
6. Create routers
    - ```
        docker run -d --net mongo-db-network --name router-1 -p 27141:27017 mongo:7.0 mongos --port 27017 --configdb config-server-replSet/config-server-1:27017,config-server-2:27017,config-server-3:27017 --bind_ip_all
        docker run -d --net mongo-db-network --name router-2 -p 27142:27017 mongo:7.0 mongos --port 27017 --configdb config-server-replSet/config-server-1:27017,config-server-2:27017,config-server-3:27017 --bind_ip_all
        ```
7. Add shards to router
    - ```
        docker exec -it router-1 mongosh
        sh.addShard("shard-1-replSet/shard-1-node-a:27017", "shard-1-replSet/shard-1-node-b:27017", "shard-1-replSet/shard-1-node-c:27017")
        sh.addShard("shard-2-replSet/shard-2-node-a:27017", "shard-2-replSet/shard-2-node-b:27017", "shard-2-replSet/shard-2-node-c:27017")
        ```
    - ```
        docker exec -it router-2 mongosh
        sh.addShard("shard-1-replSet/shard-1-node-a:27017", "shard-1-replSet/shard-1-node-b:27017", "shard-1-replSet/shard-1-node-c:27017")
        sh.addShard("shard-2-replSet/shard-2-node-a:27017", "shard-2-replSet/shard-2-node-b:27017", "shard-2-replSet/shard-2-node-c:27017")
        ```

### ER diagram

## MongoDB

## Streamlit app

## LLM