# RainbowMeds

In June 2021, we participated in a hackathon with as theme "Disrupting monolingualism in digital spaces". According to W3Techs, over 60% of the world’s websites are in English. And yet English speakers account for only 25% of internet users.[i] In South Africa, this gap is even more pronounced, with only 11% of the population being a native English speaker. 

**Stack used**: Python - Flask - Twilio - HTML - CSS Bootstrap - Figma - Botlhale NLP

## The brief
One of the companies organising the hackathon was [Botlhale AI](https://botlhale.ai/), which is a start up that specializes in conversational AI, with a suite of Natural Language Processing (NLP) tools such as chatbots, text-to-speech recognition, and speech-to-text recognition. Their key differentiator is their mission to bring these ground-breaking technologies to people who speak African languages.

Hence, the brief for the hackathon was to use their flagship product - a chat-bot that uses NLP and Artificial Intelligence (AI) to converse smartly with the end user in all of South Africa’s 11 official languages - to build a digital solution to the language barriers that so many South Africans face.

## The solution
Have you ever bought medication and read the leaflet to check if there are any side effects or dosage instructions you should be aware of? Those leaflets often only come in a couple of South African languages, like English and Afrikaans. For the vast majority of South Africans though, this could form a potentially dangerous language barrier to fully understanding the impact of medication on their health.

To address this, we decided to build a chatbot that converses with the user in his or her own language, and provides pharmaceutical information on medicines, translated into the user’s language in real time. Our solution won first place, amidst several inspiring contenders.

## How it works

A user lands on the homepage, https://tamiragun.github.io/RainbowMeds/. To start conversing with the bot, they send a message in English or isiZulu to the provided WhatsApp number. A Flask server (the orchestrator) takes the input from WhatsApp via Twilio to set the bot’s language and sends it to the Botlhale backend.

At that point, the Botlhale chatbot takes over and responds, engaging in an AI-powered conversation and listening for user intents per the NLP models and data it has been trained with. When an intent, such as asking for info about paracetamol is recognised, it triggers a second Flask service (the data vending service) with a given medication and rubric. 

The data vending service calls the USA’s [Federal Drug Administration's medicines API](https://open.fda.gov/apis/), and then runs the returned result through [Google’s Translation API](https://cloud.google.com/translate). Finally, the data layer server returns the data in the desired language back to the bot platform, which then passes it to the orchestration server which, via Twilio, sends it to the user.

![rainbowmeds architecture](https://miro.medium.com/max/700/0*vfDudZTefUq4dcUo "RainbowMeds architecture")

## Issues

Our Minimum Viable Product (MVP) only handles the Zulu and English languages, a couple of popular medicines such as Panado (paracetamol), and a couple of the available rubrics (dosage and side effects). Rather than build a front-end app, we deployed the bot to WhatsApp, which could be launched from a static landing page. The idea was for our MVP to prove that this can be built, rather than to build a complete offering. 

Future iterations could include more medicines, more rubrics, more languages supported by the bot and the homepage, and more elaborate NLP training for the models. 


## How to contribute
If you are interested in contributing, by all means fork the repository and sign up for a Botlhale AI account and a Twilio key and number to link it all together. Following these steps will get you the Python, HTML and CSS code to get started:
1. Open Git Bash.
2. Change the current working directory to the location where you want the cloned directory.
3. Type `$ git clone https://github.com/tamiragun/RainbowMeds.git` and hit enter.
4. Open the folder in your preferred IDE, and open index.html in your browser.

## Credits
- [Jeanne-Marié du Plessis](https://www.linkedin.com/in/jeanne-marie-du-plessis-77117b155/), a UX-UI designer who works at Now Boarding Digital, made all the designs, copy, and UX journey.
- [Jethro Möller](https://www.linkedin.com/in/jethro-m%C3%B6ller-7a4800124/), an AWS developer, built the back-end.
- [Masibonge Masinga](https://www.linkedin.com/in/masibonge-masinga-a4282a10b/), a mobile developer, configured the chatbot and made the isiZulu translations.
- [Tamira Gunzburg](https://www.linkedin.com/in/tamiragunzburg/), a software developer who is currently freelancing, built the landing page.

Huge thanks to [Botlhale AI](https://botlhale.ai/) and [Dado](https://dadoagency.com/) for organising the hackathon and to [Martin Kruger](https://www.linkedin.com/in/martink-rsa/) for helping us get our team together. 

## Footnotes
[i] https://en.wikipedia.org/wiki/Languages_used_on_the_Internet
