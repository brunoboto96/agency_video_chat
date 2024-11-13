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
    is_media: bool = False,
):
    """
    Docs: https://docs.crewai.com/introduction

    Description: A focus group is a qualitative research method that involves a group of people who are asked about their perceptions, opinions, beliefs, and attitudes towards a product, service, concept, advertisement, idea, or packaging. The focus group is led by a moderator who guides the discussion and ensures that all participants have an opportunity to express their views.
    """

    print("Inputs:", agency_info, video_context, audio_context, text_context, is_media)

    inputs = {
        "topic": "media" if is_media else "text",
        "agency_info": agency_info,
        "video_context": video_context,
        "audio_context": audio_context,
        "text_context": "",
    }
    response = VideoFocusGroupCrew().crew().kickoff(inputs=inputs)
    print("Final Response:", response)
    return response.raw


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
                    "is_media": {
                        "type": "boolean",
                        "description": "Boolean to indicate if the context is media.",
                    },
                },
                "required": [
                    "agency_info",
                    "video_context",
                    "audio_context",
                    "text_context",
                    "is_media",
                ],
                "additionalProperties": False,
            },
        },
    },
]


function_map = {
    "focus_group": focus_group,
}
