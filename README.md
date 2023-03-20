# Demo Tweet Generation

## Usage
- [Usage](#usage)
- [Demo Tweet Generation](#what-is-demo-tweet-generation)
- [Directory Structure](#directory-structure)
- [License](#license)
- [Installation](#installation)
- [Contributing](#contributing)
- [Code of conduct](#code-of-conduct)

## Source

The logic and idea, as well as part of the code of this application, come from Nikolas Schriefer. The original code can be found [here](https://github.com/kinosal/tweet). It was recreated using Taipy.

## What is Demo Tweet Generation

[Demo Tweet Generation](https://github.com/Avaiga/demo-tweet-generation), powered by [Taipy](https://taipy.io/), enables users to create unique Tweets using cutting-edge AI models from OpenAI: GPT-3's Davinci engine for generating text and DALL·E for generating images.

Users can enter a topic, an optional mood parameter, and a Twitter account in a text prompt creation form. The application then generates an instruction to write a Tweet based on the given input and sends the prompt to the OpenAI API. The GPT-3 Davinci engine predicts the next likely word tokens based on its extensive training on public text data, resulting in the generation of a Tweet.

Moreover, the application can request and display an image from DALL·E, OpenAI's AI image creation model, using the generated Tweet text as input. This integration creates a unique Tweet that combines both text and image, providing an exciting way to generate content for social media platforms.


### Demo Type
- **Level**: Basic
- **Topic**: Taipy-GUI
- **Components/Controls**: 
  - Taipy GUI: chart, input, button, image

## How to run

This demo works with a Python version superior to 3.8. Install the dependencies of the *requirements.txt* and run the *main.py*.


## Directory Structure


- `src/`: Contains the demo source code.
  - `src/data`: Contains the application data files.
- `docs/`: contains the images for the documentation
- `CODE_OF_CONDUCT.md`: Code of conduct for members and contributors of _demo-tweet-generation_.
- `CONTRIBUTING.md`: Instructions to contribute to _demo-tweet-generation_.
- `INSTALLATION.md`: Instructions to install _demo-tweet-generation_.
- `LICENSE`: The Apache 2.0 License.
- `Pipfile`: File used by the Pipenv virtual environment to manage project dependencies.
- `README.md`: Current file.

## License
Copyright 2022 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

## Installation

Want to install _demo sales dashboard_? Check out our [`INSTALLATION.md`](INSTALLATION.md) file.

## Contributing

Want to help build _demo sales dashboard_? Check out our [`CONTRIBUTING.md`](CONTRIBUTING.md) file.

## Code of conduct

Want to be part of the _demo sales dashboard_ community? Check out our [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) file.
