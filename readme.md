# Initial Idea
1. Use vecteezy to search for free videos based on query. 
https://www.vecteezy.com/search?qterm=sports-and-cars&content_type=video
- scrape free videos using html/css elements and atributes

2. Cache video embeddings with the original url to the raw file.
- video > source (save url)
- video embeddings (TODO: pick a model for this)

3. Score the videos that most align with the company ideals.
- Via embeddings
- Feed a few documents for RAG

4. UI: Upload company profile or chat. If chat: ask questions until satisfatory. Generate a company profile and save it on a db.
(This could be a side by side agents preview of the final document)

5. Caching: public assets become public. Whilst private assets are protected.
