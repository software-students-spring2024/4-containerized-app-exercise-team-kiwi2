![Lint-free](https://github.com/software-students-spring2024/4-containerized-app-exercise-team-kiwi2/actions/workflows/lint.yml/badge.svg)
![Passes tests](https://github.com/software-students-spring2024/4-containerized-app-exercise-team-kiwi2/actions/workflows/build.yaml/badge.svg)

# Containerized App Exercise

## Team members

Stanley Moukhametzianov (SM9231) [Github Profile](https://github.com/Stanley-Moukhametzianov)
<br>
Benson Li (BL2995) [Github Profile](https://github.com/bensonnli)
<br>
Nicholas Meng (ndm9914) [Github Profile](https://github.com/Nmeng01)
<br>
Sangeyl Lee (SL6733) [Github Profile](https://github.com/S2ang) 

## Concept

The idea behind this app is to allow users to generate recommendations for things to do based on their location. The app takes advantage of HTML5 geolocation, allowing the browser to ask the user if they want their location to be tracked. Giving this permission then allows the user to generate a list of 5 recommendations for the best things to do in the city that they are located in. The app uses OpenAI to generate these responses, so the list may differ each time you open the web app. 

## Configuration

- Firstly, you need to add the openAI api key. Our API key will be sent in our class discord channel: team-kiwi2.  
- Once you have the API key, you need to add it to the docker-compose.yml file in the root directory of the project. Under the ml_app section there will be an environment variable:  OPENAI_API_KEY: "{Insert key here}". You just need to replace the string {Insert key here} with the api key. 
- To run the project, in the terminal run the command:  “ docker-compose up ”. This will start the web-app, ml-app and mongodb. 
- Once everything is done loading, the web app will hosted at the url: http://localhost:5000/ 
- On the url, you will be prompted to allow your browser to access your devices, so you can just click allow. If you are on Safari, the browser's location settings might cause an error. In that case, we suggest using Chrome, the chrome default settings have so far worked each time. After you allow, you will see your longitude and latitude on the screen and a button. 
- The “Get response” button will first be disabled. This is while the ml-app part is generating a response. After the response is done loading, the button will be enabled and you can click it. It takes five to ten seconds to load. Once you click it, you will be able to see your closest city, country and region as well as the ml generated top five best things to do in that location. 
