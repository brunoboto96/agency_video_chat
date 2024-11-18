from google.cloud import secretmanager


project_id = "583182365017"


def get_secret(name):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{name}/versions/latest"

    try:
        response = client.access_secret_version(name=secret_name)
        secret = response.payload.data.decode("UTF-8")

        return secret
    except Exception as e:
        print("Error: ", e)
        raise e


from crewai import LLM

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

llm = LLM(
    model="gpt-4o-mini",
    api_key=get_secret("openai_api_key"),
)


@CrewBase
class VideoFocusGroupCrew:
    """VideoFocusGroup crew"""

    # tech_enthusiast
    # young_social_media_influencer
    # business_professional
    # family_focus_viewer
    # environmentalist
    # senior_expert
    # art_critic
    # health_wellness_enthusiast
    # educator
    # reporting_analyst
    @agent
    def tech_enthusiast(self) -> Agent:
        return Agent(
            config=self.agents_config["tech_enthusiast"],
            verbose=True,
            llm=llm,
        )

    @task
    def tech_review_task(self) -> Task:
        return Task(
            config=self.tasks_config["tech_enthusiast_task"],
            async_execution=True,
        )

    @agent
    def young_social_media_influencer(self) -> Agent:
        return Agent(
            config=self.agents_config["young_social_media_influencer"],
            verbose=True,
            llm=llm,
        )

    @task
    def young_social_media_influencer_task(self) -> Task:
        return Task(
            config=self.tasks_config["young_social_media_influencer_task"],
            async_execution=True,
        )

    @agent
    def business_professional(self) -> Agent:
        return Agent(
            config=self.agents_config["business_professional"],
            verbose=True,
            llm=llm,
        )

    @task
    def business_professional_task(self) -> Task:
        return Task(
            config=self.tasks_config["business_professional_task"],
            async_execution=True,
        )

    @agent
    def family_focus_viewer(self) -> Agent:
        return Agent(
            config=self.agents_config["family_focus_viewer"],
            verbose=True,
            llm=llm,
        )

    @task
    def family_focus_viewer_task(self) -> Task:
        return Task(
            config=self.tasks_config["family_focus_viewer_task"],
            async_execution=True,
        )

    @agent
    def environmentalist(self) -> Agent:
        return Agent(
            config=self.agents_config["environmentalist"],
            verbose=True,
            llm=llm,
        )

    @task
    def environmentalist_task(self) -> Task:
        return Task(
            config=self.tasks_config["environmentalist_task"],
            async_execution=True,
        )

    @agent
    def senior_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_expert"],
            verbose=True,
            llm=llm,
        )

    @task
    def senior_expert_task(self) -> Task:
        return Task(
            config=self.tasks_config["senior_expert_task"],
            async_execution=True,
        )
        
    @agent
    def art_critic(self) -> Agent:
        return Agent(
            config=self.agents_config["art_critic"],
            verbose=True,
            llm=llm,
        )
        
    @task
    def art_critic_task(self) -> Task:
        return Task(
            config=self.tasks_config["art_critic_task"],
            async_execution=True,
        )
        
    @agent
    def health_wellness_enthusiast(self) -> Agent:
        return Agent(
            config=self.agents_config["health_wellness_enthusiast"],
            verbose=True,
            llm=llm,
        )

    @task
    def health_wellness_enthusiast_task(self) -> Task:
        return Task(
            config=self.tasks_config["health_wellness_enthusiast_task"],
            async_execution=True,
        )
        
    @agent
    def educator(self) -> Agent:
        return Agent(
            config=self.agents_config["educator"],
            verbose=True,
            llm=llm,
        )
        
    @task
    def educator_task(self) -> Task:
        return Task(
            config=self.tasks_config["educator_task"],
            async_execution=True,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],
            verbose=True,
            llm=llm,
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the VideoFocusGroup crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


async def focus_group(
    agency_info: str,
    video_context: list,
    audio_context: list,
    text_context: list,
    topic_context: str = 'n videos',
):
    """
    Docs: https://docs.crewai.com/introduction

    Description: A focus group is a qualitative research method that involves a group of people who are asked about their perceptions, opinions, beliefs, and attitudes towards a product, service, concept, advertisement, idea, or packaging. The focus group is led by a moderator who guides the discussion and ensures that all participants have an opportunity to express their views.
    """

    print("Inputs:", agency_info, video_context, audio_context, text_context, topic_context)

    inputs = {
        "topic": topic_context,
        "agency_info": agency_info,
        "video_context": video_context,
        "audio_context": audio_context,
        "text_context": "",
    }
    response = VideoFocusGroupCrew().crew().kickoff(inputs=inputs)
    print("Final Response:", response)
    return response.raw


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
from audio_analysis import analyse_audio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

async def collect_videos(query: str, n: int, offset: int = 0):
    """
    Description: Find and collect videos that are relevant to the given agency information.
    """
    videos_to_collect = n
    n = n + offset
    query = query.replace(" ", "%20")
    query_builder = f"https://www.pexels.com/search/videos/{query}/"

    chrome_options = Options()
    # Updated headless mode configuration
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    
    # Additional required options for stable headless operation
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    
    # Additional options to improve stability
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")

    # Add user agent to avoid detection
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Set up ChromeDriver Service with logging
    service = Service(ChromeDriverManager().install())
    driver = None

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"Navigating to URL: {query_builder}")
        
        # Set page load timeout
        driver.set_page_load_timeout(30)
        driver.get(query_builder)

        # Wait for initial page load
        time.sleep(5)  # Allow time for dynamic content to load

        # Scroll down to load more videos
        scroll_pause_time = 2
        screen_height = driver.execute_script("return window.screen.height;")
        i = 1
        
        while i < 3:  # Adjust number of scrolls as needed
            driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
            time.sleep(scroll_pause_time)
            i += 1

        # Wait for video elements with explicit wait
        wait = WebDriverWait(driver, 20)
        video_elements = wait.until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "video"))
        )
        
        print(f"Found {len(video_elements)} video elements")
        
        video_links = []
        for source in video_elements[offset:n]:
            if len(video_links) >= videos_to_collect:
                break
            try:
                video_link = source.get_attribute("src")
                if video_link:
                    video_links.append(video_link)
                    print(f"Found video link: {video_link}")
            except Exception as e:
                print(f"Error extracting video link: {str(e)}")
                continue

        if not video_links:
            print("No video links found")
            return "No results found"

        # Process video links asynchronously
        video_analysis = await asyncio.gather(
            *[video_analyse(video_link) for video_link in video_links]
        )
        print(f"Completed video analysis for {len(video_analysis)} videos")

        return str(video_analysis)

    except Exception as e:
        print(f"Error during video collection: {str(e)}")
        return f"Error occurred: {str(e)}"

    finally:
        if driver:
            driver.quit()
            print("Browser session closed")



from video_analysis import analyse_video
from db import chroma_client


async def video_analyse(video_link):
    """
    Placeholder for video analysis logic
    """

    print(f"Analyzing video link: {video_link}")

    # check if video is already in the database
    collection = chroma_client.get_collection(name="video_embeddings")
    results = collection.get(ids=[video_link])

    if results['ids'] != []:
        print("Video already in database", results)
        return results["metadatas"][0]
    

    video_context = await analyse_video(
        video_link,
        "Describe this video in detail and the style of editing and shooting.",
    )
    
    audio_context = analyse_audio(video_link)
    
    response = {
        "link": video_link,
        "video_context": video_context,
        "audio_context": audio_context,
        "text_context": "",
    }
    # print('Video and audio analysis completed:', response)
    collection.add(documents=[video_context], metadatas=[response], ids=[video_link])
    return response



async def analyse_videos(video_links: list, query: str) -> str:
    """
    Analyse a list of video links asynchronously
    """

    print(f"Analyzing video links: {video_links}")

    results = await asyncio.gather(
        *[analyse_video(video_link, query) for video_link in video_links]
    )
    collection = chroma_client.get_collection(name="video_embeddings")
    documents = collection.get(ids=video_links)

    new_documents = []
    for idx, result in enumerate(results):
        # Grow the video_context with the result
        new_documents.append(documents["documents"][idx] + result)
    
    # TODO: Add audio analysis
    
    # Update the documents in the collection with the new extended context
    collection.update(
        ids=video_links,
        documents=[*new_documents],
    )

    return str(new_documents)


tools = [
    {
        "type": "function",
        "function": {
            "name": "focus_group",
            "description": "A focus group that analyses and provides insights on the given context. It can identify the best video, audio, or text content for a certain agency based on the context provided.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agency_info": {
                        "type": "string",
                        "description": "Information about the agency.",
                    },
                    "video_context": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "description": "Description of the video context.",
                                },
                                "type": {
                                    "type": "string",
                                    "description": "Type of the video context.",
                                },
                            },
                            "required": ["description", "type"],
                            "additionalProperties": False,
                        },
                        "description": "List of video context.",
                    },
                    "audio_context": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "description": "Description of the audio context.",
                                },
                                "type": {
                                    "type": "string",
                                    "description": "Type of the audio context.",
                                },
                            },
                            "required": ["description", "type"],
                            "additionalProperties": False,
                        },
                        "description": "List of audio context.",
                    },
                    "text_context": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "description": "Description of the text context.",
                                },
                                "type": {
                                    "type": "string",
                                    "description": "Type of the text context.",
                                },
                            },
                            "required": ["description", "type"],
                            "additionalProperties": False,
                        },
                        "description": "List of text context.",
                    },
                    "topic_context": {
                        "type": "string",
                        "description": "Description of what the context is about. ie. 3 videos",
                    },
                },
                "required": [
                    "agency_info",
                    "video_context",
                    "audio_context",
                    "text_context",
                    "topic_context",
                ],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "collect_videos",
            "description": "Find and collect videos that are relevant to the given agency information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "keywords to search for relevant videos.",
                    },
                    "n": {
                        "type": "number",
                        "description": "Number of videos to collect.",
                    },
                    "offset": {
                        "type": "number",
                        "description": "Offset for the number of videos to collect (default: 0).",
                    },
                },
                "required": [
                    "query",
                    "n",
                ],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyse_videos",
            "description": "Analyse a list of video links asynchronously (VQA).",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_links": {
                        "type": "array",
                        "items": {
                            "type": "string",
                        },
                        "description": "List of video links to analyse.",
                    },
                    "query": {
                        "type": "string",
                        "description": "Query for VQA.",
                    },
                },
                "required": [
                    "video_links",
                    "query",
                ],
                "additionalProperties": False,
            },
        },
    }
]


function_map = {
    "focus_group": focus_group,
    "collect_videos": collect_videos,
    "analyse_videos": analyse_videos,
}
