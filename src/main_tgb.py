# Import from standard library
import logging
import random
import re

# Import from 3rd party libraries
from taipy.gui import Gui, notify
import taipy.gui.builder as tgb

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
        print("Hello")
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
                prompt=processing_prompt
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


with tgb.Page() as page:
    with tgb.part("container"):
        tgb.text("# Tweet Generation", mode="md")
        tgb.text("This mini-app generates Tweets using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts and [DALL·E](https://beta.openai.com/docs/guides/images) for images.", mode="md")

        with tgb.layout(columns="1 1 1", gap="30px", class_name="card"):
            with tgb.part():
                tgb.text("## Topic (or hashtag)", mode="md")
                tgb.input("{topic}", label="Topic (or hashtag)")
            with tgb.part():
                tgb.text("## Mood", mode="md")
                tgb.input("{mood}", label="Mood (e.g. inspirational, funny, serious) (optional)")
            with tgb.part():
                tgb.text("## Twitter account", mode="md")
                tgb.input("{style}", label="Twitter account handle to style-copy recent Tweets (optional)")

            tgb.button("Generate", on_action=generate_text)

        tgb.html("hr")

        tgb.text("## Generated Tweets", mode="md")
        tgb.input("{tweet}", multiline=True, label="Resulting tweet", class_name="fullwidth")

        tgb.button("Generate image", on_action=generate_image, active="{prompt != '' and tweet != ''}", class_name="text-center text_center center")

        with tgb.part(render="{prompt != '' and tweet != '' and image is not None}", class_name="card text-center"):
            tgb.text("## Image from Dall-e", mode="md")
            tgb.image("{image}", height="400px")

        tgb.text("Code from [@kinosal](https://twitter.com/kinosal)", mode="md")
        tgb.text("Original code can be found [here](https://github.com/kinosal/tweet)", mode="md")


if __name__ == "__main__":
    Gui(page).run(title='Tweet Generation', port=3455)
