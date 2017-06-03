# LitStoryTeller (TextGistGraph)

LitStoryTeller is an interactive system for visually exploring the semantic structure of a scientific article. The proposed system borrows a metaphor from screen play, and visualizes the storyline of a scientific paper by arranging its characters (scientific concepts or terminologies) and scenes (paragraphs/sentences) into a progressive and interactive storyline. 

## Exploration of a document collection

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Temporal entity evolution view

The temporal entity evolution view is designed to visualize how entities in an entire document collection evolve over time. 
![alt text](https://github.com/ChanningPing/TextGistGraph/blob/master/Figures/evolution.png "evolution view")

### Entity Community view

The entity community view is designed to visualize the communities within the co-occurrence network of entities across the collection. 
![alt text](https://github.com/ChanningPing/TextGistGraph/blob/master/Figures/network%20local.png "evolution view")

## Exploration of a single document 

We design two views within the “text-storyline cross-reference” view, namely, the “Storyline view” and “Text view”. The collaboration between the two views will help users to navigate through the full text following accumulative clues in the storyline viewer.
The storyline viewer of a research paper comprises of entities (characters) and sections/paragraphs/sentences (scenes). The storyline should be read from left to right, as its development in the research paper. The fisheye view enable users to expand and examine storyline details at any specific part of a document. 
![alt text](https://github.com/ChanningPing/TextGistGraph/blob/master/Figures/fisheyed_storyline.png "evolution view")

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
