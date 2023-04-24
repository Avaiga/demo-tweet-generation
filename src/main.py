# Import from standard library
import logging
import random
import re

# Import from 3rd party libraries
from taipy.gui import Gui, notify

# Import modules
import oai

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


def error_prompt_flagged(state, prompt):
    """Notify user that a prompt has been flagged."""
    notify(state, "error", "Prompt flagged as inappropriate.")
    logging.info(f"Prompt flagged as inappropriate: {prompt}")

def error_too_many_requests(state):
    """Notify user that too many requests have been made."""
    notify(state, "error", "Too many requests. Please wait a few seconds before generating another text or image.")
    logging.info(f"Session request limit reached: {state.n_requests}")
    state.n_requests = 1


# Define functions
def generate_text(state):
    """Generate Tweet text."""
    state.tweet = ""
    state.image = None

    # Check the number of requests done by the user
    if state.n_requests >= 5:
        error_too_many_requests(state)
        return

    # Check if the user has put a topic
    if state.topic == "":
        notify(state, "error", "Please enter a topic")
        return

    # Create the prompt and add a style or not
    if state.style == "":
        state.prompt = (
            f"Write a {state.mood}Tweet about {state.topic} in less than 120 characters "
            f"and with the style of {state.style}:\n\n\n\n"
        )
    else:
        state.prompt = f"Write a {state.mood}Tweet about {state.topic} in less than 120 characters:\n\n"


    # openai configured and check if text is flagged
    openai = oai.Openai()
    flagged = openai.moderate(state.prompt)
    
    if flagged:
        error_prompt_flagged(state, f"Prompt: {state.prompt}\n")
        return
    else:
        # Generate the tweet
        state.n_requests += 1
        state.tweet = (
            openai.complete(state.prompt).strip().replace('"', "")
        )

        # Notify the user in console and in the GUI
        logging.info(
            f"Topic: {state.prompt}{state.mood}{state.style}\n"
            f"Tweet: {state.tweet}"
        )
        notify(state, "success", "Tweet created!")


def generate_image(state):
    """Generate Tweet image."""
    notify(state, "info", "Generating image...")

    # Check the number of requests done by the user
    if state.n_requests >= 5:
        error_too_many_requests(state)
        return

    state.image = None

    # Creates the prompt
    prompt_wo_hashtags = re.sub("#[A-Za-z0-9_]+", "", state.prompt)
    processing_prompt = (
        "Create a detailed but brief description of an image that captures "
        f"the essence of the following text:\n{prompt_wo_hashtags}\n\n"
    )

    # Openai configured and check if text is flagged
    openai = oai.Openai()
    flagged = openai.moderate(processing_prompt)

    if flagged:
        error_prompt_flagged(state, processing_prompt)
        return
    else:
        state.n_requests += 1
        # Generate the prompt that will create the image
        processed_prompt = (
            openai.complete(
                prompt=processing_prompt, temperature=0.5, max_tokens=40
            )
            .strip()
            .replace('"', "")
            .split(".")[0]
            + "."
        )

        # Generate the image
        state.image = openai.image(processed_prompt)

        # Notify the user in console and in the GUI
        logging.info(f"Tweet: {state.prompt}\nImage prompt: {processed_prompt}")
        notify(state, "success", f"Image created!")


def feeling_lucky(state):
    """Generate a feeling-lucky tweet."""
    with open("moods.txt") as f:
        sample_moods = f.read().splitlines()
    state.topic = "an interesting topic"
    state.mood = random.choice(sample_moods)
    state.style = ""
    generate_text(state)

# Variables
tweet = ""
prompt = ""
n_requests = 0

topic = "AI"
mood = "inspirational"
style = "elonmusk"

image = None

# Called whever there is a problem
def on_exception(state, function_name: str, ex: Exception):
    logging.error(f"Problem {ex} \nin {function_name}")
    notify(state, 'error', f"Problem {ex} \nin {function_name}")


# Markdown for the entire page
## <text|
## |text> 
## "text" here is just a name given to my part/my section
## it has no meaning in the code
page = """
<|container|
# **Generate**{: .color-primary} Tweets

This mini-app generates Tweets using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts and [DALL·E](https://beta.openai.com/docs/guides/images) for images. You can find the code on [GitHub](https://github.com/Avaiga/demo-tweet-generation) and the original author on [Twitter](https://twitter.com/kinosal).

<br/>

<|layout|columns=1 1 1|gap=30px|class_name=card|
<topic|
## **Topic**{: .color-primary} (or hashtag)

<|{topic}|input|label=Topic (or hashtag)|>
|topic>

<mood|
## **Mood**{: .color-primary}

<|{mood}|input|label=Mood (e.g. inspirational, funny, serious) (optional)|>
|mood>

<style|
## Twitter **account**{: .color-primary}

<|{style}|input|label=Twitter account handle to style-copy recent Tweets (optional)|>
|style>

<|Generate text|button|on_action=generate_text|label=Generate text|>

<|Feeling lucky|button|on_action=feeling_lucky|label=Feeling Lucky|>
|>

<br/>

---

<br/>

### Generated **Tweet**{: .color-primary}

<|{tweet}|input|multiline|label=Resulting tweet|class_name=fullwidth|>

<center><|Generate image|button|on_action=generate_image|label=Generate image|active={prompt!="" and tweet!=""}|></center>

<image|part|render={prompt != "" and tweet != "" and image is not None}|class_name=card|
### **Image**{: .color-primary} from Dall-e

<center><|{image}|image|height=400px|></center>
|image>

<br/>

**Code from [@kinosal](https://twitter.com/kinosal)**

Original code can be found [here](https://github.com/kinosal/tweet)
|>
"""


if __name__ == "__main__":
    Gui(page).run(dark_mode=False, port=5089)
