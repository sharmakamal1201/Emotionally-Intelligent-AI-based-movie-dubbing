# Emotionally-Intelligent-AI-based-movie-dubbing
Problem Statement: AI to seamlessly translate and dub content into any language while preserving the original speaker's emotions, characteristics, and authenticity.


## Description

**Think about the world**

**If language barriers didn’t exist? What if your favorite content could speak to you—not just in your language, but with all the emotions, the depth, the authenticity of the original speaker?"**


This AI-based dubbing project aims to make global content more accessible by translating videos into different languages while retaining the original speaker's unique qualities—like age, gender, and accent. Most importantly, it keeps the speaker's emotions and sentiments intact, so the experience feels just as genuine and relatable. The outcome ensures that it feels like the speaker is still the same, now just speaking in your native language, bringing the full depth of the original performance to a broader audience without losing its emotional impact.

**Steps to Achieve Emotionally Accurate AI-Based Dubbing:**

1. Extract Audio from Video.
2. Separate Vocals from Background Music with Librosa or Spleeter.
3. Transcribe and Identify Speakers using PyAnnote (diarization) and Azure Speech-to-Text.
3. Translate Each Speaker's Transcription with Azure Translation.
4. Generate Translated Speech while **preserving speaker's voice and emotions** using Azure TTS.
5. Enhance Emotions in the speech (if needed).
6. Merge Speaker Audio using pydub.
7. Overlay Translated Speech with Background Music.
8. Replace Original Audio with Dubbed Audio.

*Tech Stack: Azure Cognitive Services, PyAnnote, Pydub, Librosa, Moviepy/FFmpeg.

**Demo:** **Video Added** 

**Social Impact:**
- General content more accessible and personalise
- *Imagine students around the world learning in their native language, feeling the passion of their teachers’ voices. Patients getting the care they need, hearing and understanding their doctors clearly, even across borders.*
- AI Dubbing is more than a technological advancement—it's a human connection. It ensures that no matter where you’re from, you can feel the same joy, urgency, or comfort that the original speaker intended. It’s about making the world smaller, more connected, and truly accessible.

This is the power of AI—building bridges across cultures, making global content personal, and ensuring that every voice, in every language, speaks to you with the same authenticity

**Benefits of AI based dubbing:**
- Global Reach​
- Cost-Effectiveness​
- Speed​
- Scalability​
- Enhanced Creative Control​ 


**Challenges:**
- Noise Handling​
- *Retaining emotions​*
- *Multi-speaker scenarios*​
- Internal Package Dependencies​
- *Video and Audio Sync*​

**Future Plan:**
- Optimizing Real-Time Processing​
- Designing an Interactive User Interface (UI)​
- Enabling Multi-Speaker Dubbing with Precision​

**North Star:**
- **Developing a Real-Time AI Dubbing Model​**
- Seamless Integration with Microsoft Teams.​
