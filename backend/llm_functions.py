import os, logging, asyncio, time
from dotenv import load_dotenv

load_dotenv()
from google.cloud import secretmanager
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from video_analysis import analyse_video
from db import chroma_client
from audio_analysis import analyse_audio

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Retrieve project ID from environment
project_id = os.getenv("GCP_PROJECT_ID")


def get_secret(name):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{name}/versions/latest"

    try:
        response = client.access_secret_version(name=secret_name)
        secret = response.payload.data.decode("UTF-8")
        return secret
    except Exception as e:
        logger.error("Error accessing secret '%s': %s", name, e)
        raise e


# Initialize LLM
llm = LLM(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY") or get_secret("openai_api_key"),
)


@CrewBase
class VideoFocusGroupCrew:
    """
    Description: VideoFocusGroup crew

    Agents: [tech_enthusiast, young_social_media_influencer, business_professional,
             family_focus_viewer, environmentalist, senior_expert, art_critic,
             health_wellness_enthusiast, educator, reporting_analyst]
    """

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
    topic_context: str = "n videos",
):
    """
    Docs: https://docs.crewai.com/introduction

    Description: A focus group is a qualitative research method that involves a group of people who are asked about their perceptions, opinions, beliefs, and attitudes towards a product, service, concept, advertisement, idea, or packaging. The focus group is led by a moderator who guides the discussion and ensures that all participants have an opportunity to express their views.
    """

    logger.info(
        "Inputs: agency_info=%s, video_context=%s, audio_context=%s, text_context=%s, topic_context=%s",
        agency_info,
        video_context,
        audio_context,
        text_context,
        topic_context,
    )

    inputs = {
        "topic": topic_context,
        "agency_info": agency_info,
        "video_context": video_context,
        "audio_context": audio_context,
        "text_context": "",
    }
    response = VideoFocusGroupCrew().crew().kickoff(inputs=inputs)
    logger.info("Final Response: %s", response)
    return response.raw



async def collect_videos(query: str, n: int, offset: int = 0) -> str:
    """
    Description: Find and collect videos that are relevant to the given agency information.
    """
    n += offset
    query_encoded = query.replace(" ", "%20")
    query_builder = f"https://www.pexels.com/search/videos/{query_encoded}/"

    # Check if video links are already cached
    logging.info("Checking cache for query: %s", query)
    query_cache_collection = chroma_client.get_collection(name="video_query_cache")
    cached_query = query_cache_collection.get(ids=[query])
    video_elements = ""
    if not cached_query["documents"]:
        logging.info("Query '%s' not found in cache", query)
        logging.info("Navigating to URL: %s", query_builder)
        try:
            chrome_options = Options()
            chrome_options.add_argument ('--no-sandbox') 
            chrome_options.add_argument ('--headless-new')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )

            driver = webdriver.Remote(command_executor='http://selenium:4444' if os.getenv("SELENIUM_HOST") != 'localhost' else 'http://localhost:4444', options=chrome_options)

            driver.set_page_load_timeout(30)
            driver.get(query_builder)

            soup_lxml = BeautifulSoup(driver.page_source, 'lxml')

            sources = soup_lxml.find_all('video')

            video_elements = ",".join(
                [source.get("src") for source in sources]
            )

            # Cache video links
            query_cache_collection.add(
                ids=[query],
                documents=["video_cached"],
                metadatas=[{"results": video_elements}],
            )
        except Exception as e:
            logger.error("Error during video collection: %s", e)
            return f"Error occurred: {str(e)}"
        finally:
            if "driver" in locals() and driver:
                driver.quit()
                logger.info("Browser session closed")
    else:
        logging.info("Query '%s' found in cache", query)
        video_elements = cached_query["metadatas"][0]["results"]

    try:
        video_links = []
        video_links = video_elements.split(",")
        video_links = video_links[offset:n]

        if not video_links:
            logger.info("No video links found")
            return "No results found"

        # Process video links asynchronously
        video_analysis = await asyncio.gather(
            *[video_analyse(video_link) for video_link in video_links]
        )
        logger.info("Completed video analysis for %d videos", len(video_analysis))

        return str(video_analysis)

    except Exception as e:
        logger.error("Error during video collection: %s", e)
        return f"Error occurred: {str(e)}"

    finally:
        if "driver" in locals() and driver:
            driver.quit()
            logger.info("Browser session closed")


async def video_analyse(video_link: str):
    """
    Placeholder for video analysis logic
    """
    logger.info("Analyzing video link: %s", video_link)

    # Check if video is already in the database
    collection = chroma_client.get_collection(name="video_embeddings")
    results = collection.get(ids=[video_link])

    if results["ids"]:
        logger.info("Video already in database: %s", video_link)
        return results["metadatas"][0]

    try:
        video_context = await analyse_video(
            video_link,
            "Describe this video in detail and the style of editing and shooting.",
        )
        audio_context = await analyse_audio(video_link)

        response = {
            "link": video_link,
            "video_context": video_context,
            "audio_context": audio_context,
            "text_context": "",
        }
        logger.info("Video and audio analysis completed: %s", response)
        collection.add(
            documents=[video_context], metadatas=[response], ids=[video_link]
        )
        return response
    except Exception as e:
        logger.error("Error analyzing video '%s': %s", video_link, e)
        return {"link": video_link, "error": str(e)}


async def analyse_videos(video_links: list, query: str) -> str:
    """
    Analyse a list of video links asynchronously
    """
    logger.info("Analyzing video links: %s", video_links)

    try:
        results = await asyncio.gather(
            *[analyse_video(video_link, query) for video_link in video_links]
        )
        collection = chroma_client.get_collection(name="video_embeddings")
        documents = collection.get(ids=video_links)

        new_documents = []
        for idx, result in enumerate(results):
            new_documents.append(documents["documents"][idx] + result)

        collection.update(
            ids=video_links,
            documents=new_documents,
        )
        logger.info("Updated video embeddings in the database")
        return str(new_documents)
    except Exception as e:
        logger.error("Error during video analysis: %s", e)
        return f"Error occurred: {str(e)}"


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
                        "description": "Keywords to search for relevant videos.",
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
    },
]

function_map = {
    "focus_group": focus_group,
    "collect_videos": collect_videos,
    "analyse_videos": analyse_videos,
}
