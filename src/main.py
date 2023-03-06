"""Streamlit app to generate Tweets."""

# Import from standard library
import logging
import random
import re

# Import from 3rd party libraries
from taipy.gui import Gui, notify

# Import modules
#import tweets as twe
import oai

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Define functions
def generate_text(state):
    """Generate Tweet text."""
    if state.n_requests >= 5:
        state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        logging.info(f"Session request limit reached: {state.n_requests}")
        state.n_requests = 1
        return

    state.tweet = ""
    state.image = ""
    state.text_error = ""

    if not state.topic:
        notify(state, "error", "Please enter a topic")
        return

    mood_prompt = f"{state.mood} " if state.mood else ""
    if state.style:
        #twitter = twe.Tweets(account=state.style)
        #tweets = twitter.fetch_tweets()
        #tweets_prompt = "\n\n".join(tweets)
        prompt = (
            f"Write a {mood_prompt}Tweet about {state.topic} in less than 120 characters "
            f"and in the style of the following Tweets:\n\n\n\n"
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

page = """
<|part|class_name=container|
# **Generate**{: .color_primary} Tweets

This mini-app generates Tweets using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts and [DALL·E](https://beta.openai.com/docs/guides/images) for images. You can find the code on [GitHub](https://github.com/kinosal/tweet) and the author on [Twitter](https://twitter.com/kinosal).

<br/>

<|layout|columns=1 1 1|gap=30px|
<|
## **Topic**{: .color_primary} (or hashtag)

<|{topic}|input|label=Topic (or hashtag)|>
|>

<|
## **Mood**{: .color_primary}

<|{mood}|input|label=Mood (e.g. inspirational, funny, serious) (optional)|>
|>

<|
## Twitter **account**{: .color_primary}

<|{style}|input|label=Twitter account handle to style-copy recent Tweets (optional)|>
|>
|>

<br/>

<|layout|columns=1 1|
<center> <|Generate text|button|on_action=generate_text|label=Generate text|> </center>

<center> <|Feeling lucky|button|on_action=feeling_lucky|label=Feeling Lucky|> </center>
|>

<br/>

---

<br/>
<|part|class_name=card p1|

### Generated **Tweet**{: .color_primary}

<|{tweet}|input|multiline|label=Resulting tweet|>
|>
<a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="Tweet generated via" data-url="https://tweets.streamlit.app" data-show-count="false">Tweet</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<|part|render={prompt!="" and tweet!=""}|class_name=card p1|
### **Image**{: .color_primary} from Dall-e

<center><|{image}|image|height=400px|></center>
|>

<br/>

<center><|Generate image|button|on_action=generate_image|label=Generate image|active={prompt!="" and tweet!=""}|></center>

<br/>

<|layout|columns=1 1|
<|
**Other Streamlit apps by [@kinosal](https://twitter.com/kinosal)**

[Twitter Wrapped](https://twitter-likes.streamlit.app)

[Content Summarizer](https://web-summarizer.streamlit.app)

[Code Translator](https://english-to-code.streamlit.app)

[PDF Analyzer](https://pdf-keywords.streamlit.app)
|>

<|
If you like this app, please consider to

<form action="https://www.paypal.com/donate" method="post" target="_top">
<input type="hidden" name="hosted_button_id" value="8JJTGY95URQCQ" />
<input type="image" src="https://pics.paypal.com/00/s/MDY0MzZhODAtNGI0MC00ZmU5LWI3ODYtZTY5YTcxOTNlMjRm/file.PNG" height="35" border="0" name="submit" title="Donate with PayPal" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
</form>

so I can keep it alive. Thank you!

|>
|>
|>
"""


Gui(page).run(host="0.0.0.0", port=4001)
