# BERLIOZ
# Classical Music Recommendation Engine (Berlioz)

## Background

Classical music is fantastic, but for beginners like me, it can be daunting to figure out where to start. On platforms like Spotify, a single piece of music, such as Beethoven’s 5th, can have over 10 different recordings by different performers. This variety not only makes it hard to choose but also means that the quality can vary widely. Unlike modern popular music, where a song typically has one official recording, classical pieces come in so many variations.

My goal with this project is to create a space for new classical music enthusiasts to easily find the most popular recordings of classical pieces on Spotify. The app, "Berlioz," will be regularly updated to include new recordings of better quality or from renowned music halls like the NY Philharmonic. Each piece will be given a star rating based on quality, although measuring quality might be tricky since it's subjective. The app will also allow users to play a snippet of a piece and then direct them to Spotify if they want to listen to the full recording. The snippet played will be the most recognized movement from that symphony. For example, in Gustav Holst’s Planets, the most recognizable movement is “Jupiter.”

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

This project README outlines the Classical Music Recommendation Engine project, detailing its goals, design outline, and tools used. For more detailed information, refer to the project documentation and code repository.
