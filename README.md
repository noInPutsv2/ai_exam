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

## vector database

## Graph dataBase
Som vores graph database bruger vi Neo4j. Vi bruger graph databasen til at kunne se realationer mellem fx karakterene fra bøgerne.
### transformere til graph
Vi bruger Diffbot til at transformere vores text data vi har hentet om til en graph. Vi har valgt at bruge det fordi det er hurtigere og nemmere end selv at skulle gennemgå de over 20000 dokumenter vi har hentet og lave noder og realationer. Dog ville det være bedst hvis vi selv gjorde det, da diffbot har nogle forud indstillinger som ikke er de bedste til vores text. Bla. kunne det være at vi havde brug for noder til besværgelser (fra bøgerne).
### graph shema
### graph algorithmer 

## SQL databse
### ER diagram

## MongoDB

## Streamlit app

## LLM