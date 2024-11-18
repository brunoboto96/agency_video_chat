# Video Search Engine for Agencies

## Description
The Video Search Engine for Agencies is a tool designed to help advertising agencies find and analyze free videos that align with their media profiles. By leveraging the Pexels API, the tool scrapes and stores video context and URLs, allowing agencies to select and analyze videos based on their specific needs.  
The system also includes a focus group analysis feature, enabling agencies to gain insights and feedback on selected videos.

- [Frontend](https://agency-video-chat-frontend-583182365017.europe-west2.run.app) 🧑‍💻
- [Backend](https://agency-video-chat-backend-wwsbodm2ma-nw.a.run.app/docs) 💼
 
## Tech Stack
- **Frontend:** Node.js, React, Tailwind, MaterialUI
- **Backend:** Python, FastAPI
- **Database:** ChromaDB
- **AI:** CrewAI, OpenAI
- **APIs:** Replicate (video analysis model), Selenium
- **Containerization:** Docker
- **Deployment:** Google Cloud Run
- **Version Control:** Git, GitHub


## Updates

[Update history ->](https://github.com/brunoboto96/agency_video_chat/blob/main/updates.md)

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

## Installation

Follow these steps to set up the project locally:

### Prerequisites

- [Node.js](https://nodejs.org/)
- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Git](https://git-scm.com/)

### Steps

1. **Clone the Repository**

   ```
   git clone https://github.com/brunoboto96/agency_video_chat.git
   cd agency_video_chat
   ```

2.	Setup Backend

    ```
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.	Setup Frontend
    ```
    cd ../frontend
    npm install
    ```

4.  Add your own env variables, instead of the get_secret() function in llm_functions.py

5.	Run Docker Containers
Ensure Docker is running, then:
    ```
    docker-compose up --build
    ```


## TODO
- Chromadb -> Update to storage bucket for file persistency