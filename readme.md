# Initial Idea
1. Use vecteezy to search for free videos based on query. 
https://www.vecteezy.com/search?qterm=sports-and-cars&content_type=video
- scrape free videos using html/css elements and atributes

2. Cache video embeddings with the original url to the raw file.
- video > source (save url)
- video embeddings (TODO: pick a model for this)

3. Score the videos that most align with the agency ideals.
- Via embeddings
- Feed a few documents for RAG

4. UI: Upload company profile or chat. If chat: ask questions until satisfatory. Generate a company profile and save it on a db.
(This could be a side by side agents preview of the final document)

5. Caching: public assets become public. Whilst private assets are protected.

# Updates

[Update history ->](https://github.com/brunoboto96/agency_video_chat/blob/main/updates.md)

## TODO
- Add more functionality
- Fix up and review the system prompts and similar.
- Basic UI for chat
- UI: Build an agency profile
- UI: Upload videos
- Create embeddings from assets
- Integrate a nosql db with vector search support: chromadb + sqlite || (mongodb or redis[2in1]) ??
- Add a function and then provide a tool on an agent to collect royalty free videos from vectoryeezy and store their embeddings, original url and description

...

- Host in cloud functions
- Use functions-framework for serverless



