# Video Search Engine for Agencies

## Description
The Video Search Engine for Agencies is a tool designed to help advertising agencies find and analyze free videos that align with their media profiles. By leveraging the Pexels API, the tool scrapes and stores video context and URLs, allowing agencies to select and analyze videos based on their specific needs.  
The system also includes a focus group analysis feature, enabling agencies to gain insights and feedback on selected videos.

- [Frontend](https://agency-video-chat-frontend-583182365017.europe-west2.run.app) 🧑‍💻
- [Backend](https://agency-video-chat-backend-wwsbodm2ma-nw.a.run.app/docs) 💼
 

## Idea
1. Input agency information (ie. advertising agencies)
- *Upload a short video to set the profile about the agency media.

2. Use pexels to search for free videos based on agency information. 
https://www.pexels.com/search/videos/wine/
- scrape free videos using html/css elements and attributes

3. Store video embeddings and the original url.
- video > source (save url)
- video embeddings (videoLlava)

4. Return a few examples of videos with score out of 10 that aligns with agency.

5. Select which ones to keep and shuffle the rest. Once x is achieved (max 5)... 

6. Chat with the video as context or Button -> Focus Group Analysis

### Features
- Caching mechanism prevents from processing video twice.

## Updates

[Update history ->](https://github.com/brunoboto96/agency_video_chat/blob/main/updates.md)

## TODO
- Add more functionality ✅
- Fix up and review the system prompts, roles, backstories.. Refine the focus groups ✅
- Basic UI for chat ✅
- UI: Build an agency profile ✅
- UI: Upload videos ✅
- Create embeddings from assets ✅
- Add chromadb ✅
- Add a function and then provide a tool on an agent to collect royalty free videos from Pexel and store their embeddings, original url and description ✅
- Build Chat ✅

...

- Host in cloud Run ✅ 
- Host chromadb in CE or Cloud functions and Storage bucket for file persistency