import json, re, os
from llm_functions import *
from openai import OpenAI
from uuid import uuid4

os.environ.setdefault("REPLICATE_API_TOKEN", get_secret("REPLICATE_API_TOKEN"))
client = OpenAI(
    organization="org-88cYAMgEF0BLqHuvPB0LEphR",
    project="proj_KfMHXeZRRa8G5CcVDMc981tP",
    api_key=get_secret("openai_api_key"),
)


system_prompt = f"""
You are a friendly and insightful virtual assistant. Your role is to provide assistance as a digital brain. You have access to a wide range of tools and resources to help you provide accurate and helpful information to users. Your primary goal is to assist users in finding answers to their questions and guiding them through various tasks.

Use the user’s media asset results to craft responses that are tailored to their unique profile.
You also have access to the agency info. Use this information to provide personalized responses to the user's queries.

Present your responses in clear, concise paragraphs, utilizing bullet points when listing key information or suggestions. Feel free to ask follow-up questions if you need more information to provide accurate insights.

Always communicate in a positive and uplifting tone, make sure to use a professional tone and avoid using slang or jargon.
Make sure you provide answers in MD format. Be conversational and engaging.
Try to find your answer within the context provided. 
Use the supplied tools in order to get more context about the user. 
Use emojis to make the conversation more engaging. Emojis should be in unicode format.
You can use VQA to get more information about the videos, incentivize the user to ask more questions about the videos and let the user know the more questions they ask the more information you can provide.
Only when using VQA skip the user uploaded videos (analyse_videos tool). Every other instance also consider the user uploaded videos.
"""


async def chat(
    user_input: str = "",
    messages: list = [],
    not_chat=False,
    additional_context=dict,
):
    print("user_input", user_input)
    context_prompt = f"""
    Context:

    additional_context:
    {json.dumps(additional_context, indent=2)}
    """
    # print('context_prompt', context_prompt)
    if not_chat == False:
        messages_return = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": context_prompt},
            *messages,
            {"role": "user", "content": user_input},
        ]
    else:
        messages_return = [{"role": "user", "content": user_input}]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_return,
            tools=tools,
            stream=False,
            max_tokens=1600,
            temperature=0.2,
        )
        message = response.choices[0].message
        # print("message", message)
        print("---")

        if message.tool_calls and len(message.tool_calls) > 0:
            function_call = message.tool_calls[0].function
            function_name = function_call.name
            function_args = json.loads(function_call.arguments)
            # print(function_name, function_args)

            if function_name in function_map:
                print("calling function: ", function_name)
                try:
                    function_result = await function_map[function_name](**function_args)
                    messages_return.append(
                        {
                            "role": "assistant",
                            "content": None,
                            "function_call": function_call,
                        }
                    )
                    messages_return.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": function_result,
                        }
                    )
                    # print("function result", function_result)

                except Exception as e:
                    print("Error in function call:", e)
                    messages_return.append(
                        {
                            "role": "assistant",
                            "content": """I apologize for the inconvenience, but it seems, I couldn't complete that task. However, I can help you with insights or suggestions related to your agency.
                            If you have any specific questions or need assistance with something else, please let me know! 😊""",
                        }
                    )
                    return messages_return
            else:
                print(f"Function {function_name} not found.")
        else:
            print("no function call")
            print("_" * 50)
            print(message.content)
            print("_" * 50)
            messages_return.append({"role": "assistant", "content": message.content})
            return messages_return


## FastAPI

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import File, UploadFile


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message_history: list
    user_input: str


@app.get("/healthz")
async def healthz():
    # health check endpoint
    return {"message": "Hello I'm healthy!"}


@app.post("/chat")
async def chat_endpoint(message_history: Message, agency_info: dict):
    user_input = message_history.user_input
    chat_response = await chat(
        user_input, message_history.message_history, False, agency_info
    )
    return chat_response


@app.post("/video/analysis")
async def video_file_analysis(video_file: UploadFile = File(...)):
    random_name = uuid4()
    tmp_path = f"./tmp/{random_name}.{video_file.filename.split('.')[-1]}"
    with open(tmp_path, "wb") as buffer:
        buffer.write(video_file.file.read())

    output = await analyse_video(
        open(tmp_path, "rb"), "What is happening in this video?"
    )

    # remove the temporary file
    os.remove(tmp_path)

    return {"output": output}



class AgencyInfo(BaseModel):
    agency_info: dict


@app.post("/collect/videos")
async def collect_videos(agency: AgencyInfo, n: int = 5, offset: int = 0):
    print(agency, n)
    user_prompt = f"""
    ____
    The offset is:
    {offset}
    ____
    Collect {n} and return videos that are most relevant to:
    ____
    {json.dumps(agency.agency_info)}
    ____
    The query should be simple and based on the agency's industry, target audience, and keywords.
    ____
    If the function returns more than {n} videos, return only the top number {n} videos based on relevancy.
    ____
    Your response must be formatted as json as such:
    {{
        "videos": 
        [
            {{
                "link": (url link to the video),
                "video_context": (description of the video),
                "audio_context": (description of the audio, if not provided leave this as an empty string),
                "text_context": (description of the text, since its audio leave this empty string),
                "relevancy_score": (int 1-10 representing how relevant the video is to the agency based on the analysis)
            }},
            ...
        ]
    }}
    """
    res = await chat(user_prompt, [], True, agency.agency_info)
    final_response = res[-1]["content"]

    data = None
    # Extract JSON string from the final response
    json_pattern = r"\{.*\}"
    match = re.search(json_pattern, final_response, re.DOTALL)
    if match:
        json_str = match.group()
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e, final_response)
    else:
        print("No JSON found in the response.")

    return data
