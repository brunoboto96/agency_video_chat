## Update 1
Initial chat routes for the backend are done.
Core concept of a focus group with agents using crewAI is working.
ChatGPT function call is working and calling the crew.

```
{
  "response": "Based on the insights gathered from the focus group analysis, here’s a comparison of the videos available for your agency, PendulumF1, which specializes in Formula 1 racing advertising:\n\n### Video Comparisons\n\n1. **Video about Formula 1 Racing Cars**\n   - **Target Audience:** Primarily appeals to Formula 1 fans and racing enthusiasts.\n   - **Engagement Potential:** High engagement with younger audiences who are passionate about motorsports.\n   - **Content Clarity:** May lack educational components regarding environmental impacts, which could limit its accessibility to older viewers.\n\n2. **Video about Racing Cars**\n   - **Target Audience:** Similar to the first video, it appeals to racing enthusiasts but may not specifically highlight Formula 1.\n   - **Engagement Potential:** Good engagement with general racing fans, but less focused than the first video.\n   - **Content Clarity:** Similar concerns regarding the lack of educational content on sustainability.\n\n3. **Video about Dogs Playing in the Park**\n   - **Target Audience:** Broad appeal, including families and individuals who enjoy light-hearted content.\n   - **Engagement Potential:** High engagement across all demographics, especially older viewers who may find it relatable and heartwarming.\n   - **Content Clarity:** Clear and accessible, but not relevant to the core focus of your agency.\n\n### Recommendation\n\n**Best Choice for PendulumF1:**\n- **Video about Formula 1 Racing Cars** is the most suitable option for your agency. It directly aligns with your focus on Formula 1 and can effectively engage your target audience of racing enthusiasts. \n\n### Actionable Suggestions:\n- **Enhance Educational Content:** Consider adding segments that highlight the environmental impacts of Formula 1 racing to broaden its appeal.\n- **Balance Audio Elements:** Incorporate softer background sounds to make the audio more accessible to a wider audience.\n- **Visual Engagement:** Include community-oriented visuals that resonate with both younger and older demographics.\n\nBy focusing on these enhancements, you can create a more engaging and impactful narrative that resonates with your audience while promoting the exciting world of Formula 1 racing! 🏎️✨"
}
```

## Update 2
Collecting videos is done using Selenium and BeautifulSoup
```
{
  "videos": [
    {
      "link": "https://static.vecteezy.com/system/resources/previews/035/585/915/mp4/light-sport-aircraft-flies-for-red-bull-air-free-video.mp4",
      "video_context": "...",
      "audio_context": "No audio",
      "text_context": "",
      "relevancy_score": 5
    },
    {
      "link": "https://static.vecteezy.com/system/resources/previews/052/027/850/mp4/aerial-view-of-great-ocean-road-at-sunset-video.mp4",
      "video_context": "...",
      "audio_context": "No audio",
      "text_context": "",
      "relevancy_score": 4
    },
    {
      "link": "https://static.vecteezy.com/system/resources/previews/035/542/382/mp4/kazan-russian-federation-june-15-2019-aerobatic-aircraft-in-different-views-light-airplane-sports-air-competitions-red-bull-air-in-kazan-free-video.mp4",
      "video_context": "...",
      "audio_context": "No audio",
      "text_context": "",
      "relevancy_score": 6
    }
  ]
}
```

## Update 3
- Switched collection website to Pexels
- Video Collection is now working with cogvlm2-video and whisper (sounds, noises and music are not accurate at all)

```
{
  "videos": [
    {
      "link": "https://videos.pexels.com/video-files/18495958/18495958-sd_640_360_25fps.mp4",
      "video_context": "The video showcases a white car driving on a wet asphalt track, surrounded by orange traffic cones. The car is seen maneuvering through the track, which is set against a backdrop of a clear blue sky and a distant hillside. The scene is captured in a series of frames, each highlighting the car's movement and the track's wetness. The consistent presence of the orange traffic cones suggests that the car is participating in a driving test or race. The video captures the car's speed and the track's wetness, creating a sense of motion and excitement.",
      "audio_context": "  y o u",
      "text_context": "",
      "relevancy_score": 6
    },
    {
      "link": "https://videos.pexels.com/video-files/18446021/18446021-sd_360_640_30fps.mp4",
      "video_context": "The video showcases a series of close-up shots of a race car's interior and exterior, highlighting various components such as the steering wheel, gear shift lever, and dashboard. The car is seen in different states, including being parked and in motion on a racetrack. The video also features a red and black race car with the number '15' prominently displayed, suggesting it is a racing vehicle. The car is shown in different positions, including stationary and in motion, with a focus on its aerodynamic design and performance capabilities. The video captures the essence of racing, emphasizing the car's design and the excitement of the sport.",
      "audio_context": "  T h a n k s   f o r   w a t c h i n g .",
      "text_context": "",
      "relevancy_score": 8
    },
    {
      "link": "https://videos.pexels.com/video-files/18446120/18446120-sd_360_640_30fps.mp4",
      "video_context": "The video showcases a thrilling race featuring a red race car with various sponsorship decals, including 'EAT,' 'MOTUL,' and 'HOT RACING.' The car is seen speeding along a racetrack, with its tires spinning fast and the background blurred to emphasize the high velocity. The track is lined with safety barriers, and the surrounding scenery includes greenery and a partly cloudy sky. At one point, the car is shown in a crash, with debris scattered around. The video captures the essence of racing, highlighting the car's speed and the excitement of the sport.",
      "audio_context": "  ✔ ️   F o l l o w   m e ,   s h a r e   a n d   s u b s c r i b e !   🖐 🏼",
      "text_context": "",
      "relevancy_score": 9
    }
  ]
}
```

## Update 4
Started the frontend in React + Tailwind

## Update 5
Frontend + Backend fully functional ✅

## Update 6
Dockerfiles created
Hosted on Google Cloud Run

## Update 7
Using remote driver to connect to a selenium service. 
Then use beautifulSoup4 with lxml for a fast parsing to grab the videos sources.

[<- back to readme](https://github.com/brunoboto96/agency_video_chat/blob/main/readme.md)