# Import from standard library
import logging
import random
import re

# Import from 3rd party libraries
from taipy.gui import Gui, notify

# Import modules
import oai

# Define functions
def generate_text(state):
    """Generate Tweet text."""
    if state.n_requests >= 5:
        state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        logging.info(f"Session request limit reached: {state.n_requests}")
        notify(state, "error", f"Session request limit reached: {state.n_requests}")
        state.n_requests = 1
        return

    state.tweet = ""
    state.image = ""
    state.text_error = ""

    if len(state.topic)==0:
        notify(state, "error", "Please enter a topic")
        return

    mood_prompt = f"{state.mood} " if state.mood else ""
    if state.style and len(state.style)>0:
        prompt = (
            f"Write a {mood_prompt}Tweet about {state.topic} in less than 120 characters "
            f"and with the style of {state.style}:\n\n\n\n"
        )
    else:
        prompt = f"Write a {mood_prompt}Tweet about {state.topic} in less than 120 characters:\n\n"

    state.prompt = prompt

    openai = oai.Openai()
    flagged = openai.moderate(prompt)
    mood_output = f", Mood: {state.mood}" if state.mood else ""
    style_output = f", Style: {state.style}" if state.style else ""
    if flagged:
        state.text_error = "Input flagged as inappropriate."
        logging.info(f"Topic: {topic}{mood_output}{style_output}\n")
        notify(state, "error", f"Input flagged as inappropriate.")
        return

    else:
        state.text_error = ""
        state.n_requests += 1
        state.tweet = (
            openai.complete(prompt).strip().replace('"', "")
        )
        logging.info(
            f"Topic: {topic}{mood_output}{style_output}\n"
            f"Tweet: {state.tweet}"
        )


def generate_image(state):
    """Generate Tweet image."""
    if state.n_requests >= 5:
        notify(state, "error", "Too many requests. Please wait a few seconds before generating another text or image.")
        logging.info(f"Session request limit reached: {state.n_requests}")
        state.n_requests = 1
        return


    openai = oai.Openai()
    prompt_wo_hashtags = re.sub("#[A-Za-z0-9_]+", "", state.prompt)
    processing_prompt = (
        "Create a detailed but brief description of an image that captures "
        f"the essence of the following text:\n{prompt_wo_hashtags}\n\n"
    )
    processed_prompt = (
        openai.complete(
            prompt=processing_prompt, temperature=0.5, max_tokens=40
        )
        .strip()
        .replace('"', "")
        .split(".")[0]
        + "."
    )
    state.n_requests += 1
    state.image = openai.image(processed_prompt)
    logging.info(f"Tweet: {state.prompt}\nImage prompt: {processed_prompt}")


def feeling_lucky(state):
    with open("moods.txt") as f:
        sample_moods = f.read().splitlines()
    state.topic = "an interesting topic"
    state.mood = random.choice(sample_moods)
    state.style = ""
    generate_text(state)

# Variables
tweet = ""
prompt = ""
image = ""
text_error = ""
image_error = ""
n_requests = 0

topic = "AI"
mood = "inspirational"
style = "elonmusk"

image = None


# Markdown for the entire page
page = """
# **Generate**{: .orange} Tweets

This mini-app generates Tweets using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts and [DALL·E](https://beta.openai.com/docs/guides/images) for images. You can find the code on [GitHub](https://github.com/Avaiga/demo-tweet-generation) and the original author on [Twitter](https://twitter.com/kinosal).

<br/>

<|layout|columns=1 1 1|gap=30px|
<topic|
## **Topic**{: .orange} (or hashtag)

<|{topic}|input|label=Topic (or hashtag)|>
|topic>

<mood|
## **Mood**{: .orange}

<|{mood}|input|label=Mood (e.g. inspirational, funny, serious) (optional)|>
|mood>

<style|
## Twitter **account**{: .orange}

<|{style}|input|label=Twitter account handle to style-copy recent Tweets (optional)|>
|style>
|>

<br/>

<|layout|columns=1 1|
<center> <|Generate text|button|on_action=generate_text|label=Generate text|> </center>

<center> <|Feeling lucky|button|on_action=feeling_lucky|label=Feeling Lucky|> </center>
|>

<br/>

---

<br/>

### Generated **Tweet**{: .orange}

<|{tweet}|input|multiline|label=Resulting tweet|>

<a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="Tweet generated via" data-url="https://127.0.0.1:4002" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<image|part|render={prompt != "" and tweet != ""}|
### **Image**{: .orange} from Dall-e

<center><|Generate image|button|on_action=generate_image|label=Generate image|active={prompt!="" and tweet!=""}|></center>



<center><|{image}|image|height=400px|></center>
|image>

<br/>

**Code from [@kinosal](https://twitter.com/kinosal)**

Original code can be found [here](https://github.com/kinosal/tweet)
"""


if __name__ == "__main__":
    Gui(page).run(dark_mode=False)
