# BERLIOZ
# A Classical Music Recommendation Engine (Berlioz)

## Background 
Classical is great and all but if you are beginner like me, it is hard to know where to even start. 
On Spotify, one piece of music, like Beethoven’s 5th could have as many as 10 or more different recordings by different recordings, and it means the quality can wildly vary and it also makes it hard to know which to listen to. 
Unlike modern popular music where a song like “Yoga” by Asake will have one official recording on Spotify, classical pieces will have so many variations. 

## Project Goals (summarized)
- [ ] Create a user-friendly recommendation engine tailored for classical music enthusiasts.
- [ ] Provide users with the most listened-to recordings of classical music pieces.
- [ ] Prioritize backend development for efficient data processing and storage.

## Design Outline
- [ ] Connect to the Spotify API to get the metadata about classical music.
- [ ] Retrieve background information (background story, style, composer, any other relevant information) from Wikipedia about each piece.
- [ ] Stream all raw data from the Spotify API into an AWS S3 storage bucket.
- [ ] Clean up and preprocess the data to only have relevant information — composer, year, recording group or philharmonic, style, conductor, and our own rating based on how cool the piece is.
- [ ] Create a Snowflake wh/db to store the processed data and to allow us to interact/analyze this data.
- [ ] Create a schedule with Airflow to allow us to update this data regularly if a new recording comes out.
- [ ] Create a recommendation algorithm to recognize the most popular recording of each piece.
- [ ] Create an application — Berlioz — that’ll be used where the user can interact with this music and even play a snippet.

## Tools
- [ ] SQL: for Snowflake data warehousing.
- [ ] Python: for most everything.
- [ ] AWS: for storing raw data.
- [ ] Airflow: to schedule.
- [ ] Snowflake: storing processed data.
- [ ] But also open to learning a new one along the way.
