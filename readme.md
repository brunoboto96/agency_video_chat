# Idea
1. Input agency information (ie. advertising agencies)
- *Upload a short video to set the profile about the agency media.

2. Use vecteezy to search for free videos based on agency information. 
https://www.vecteezy.com/search?qterm=sports-and-cars&content_type=video
- scrape free videos using html/css elements and atributes

2. Store video embeddings and the original url.
- video > source (save url)
- video embeddings (videoLlava)

3. Return a few examples of videos with score out of 10 that aligns with agency.

4. Select which ones to keep and shuffle the rest. Once x is achieved (max 5)... 

5. Chat with the video as context or Button -> Focus Group Analysis

# Updates

[Update history ->](https://github.com/brunoboto96/agency_video_chat/blob/main/updates.md)

## TODO
- Add more functionality*
- Fix up and review the system prompts, roles, backstories.. Refine the focus groups
- Basic UI for chat ✅
- UI: Build an agency profile ✅
- UI: Upload videos*
- Create embeddings from assets ✅
- Add chromadb ✅
- Add a function and then provide a tool on an agent to collect royalty free videos from Pexel and store their embeddings, original url and description ✅
- Build Chat ✅

...

- Host in cloud functions
- Use functions-framework for serverless
- Host chromadb in CE or Cloud functions and Storage bucket for file persistency




