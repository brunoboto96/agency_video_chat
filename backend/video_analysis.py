import logging, replicate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def analyse_video(video_path: str, question: str) -> str:
    logger.info("Analyzing video: %s", video_path)

    # Alternative model: VideoLlava
    # video_input = {
    #     "video_path": video_path,
    #     "text_prompt": question,
    # }
    # output = replicate.run(
    #     "nateraw/video-llava:26387f81b9417278a8578188a31cd763eb3a55ca0f3ec375bf69c713de3fb4e8",
    #     input=video_input
    # )

    output = replicate.run(
        "chenxwh/cogvlm2-video:9da7e9a554d36bb7b5fec36b43b00e4616dc1e819bc963ded8e053d8d8196cb5",
        input={
            "top_p": 0.1,
            "prompt": "Describe this video in detail and the style of editing and shooting.",
            "input_video": video_path,
            "temperature": 0.1,
            "max_new_tokens": 600,
        },
    )

    unique_sentences = list(dict.fromkeys(output.split(". ")))
    cleaned_output = ". ".join(unique_sentences)
    logger.info("Cleaned output: %s", cleaned_output)

    return cleaned_output
