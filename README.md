# ask-fandom
[![Build Status](https://travis-ci.com/Wikia/ask-fandom.svg?branch=master)](https://travis-ci.com/Wikia/ask-fandom)

Your semantic data-based assistant aka _Tell me FANDOM, ..._

# Supported questions

* _When was `someone` born?_
* _Who directed the `episode`?_
* _Who played in `episode`?_
* _Did `foo` played in `bar` episode?_

# Examples for https://tardis.fandom.com/wiki/Doctor_Who_Wiki

* _Which is the first episode with Jana Carpenter?_
* _Which species is Jana Carpenter?_
* _Who is the main actor in 456 ambassador?_
* _Was Jake Simmonds in the Doctor Who cast?_
* _Was 456 ambassador engaged in drug dealing?_
* _List me the Doctor Who guest actors_
* _Who had me first apperance in The End of the World (TV story)?_
* _Who starred as Vincent van Gogh?_
* _What's species is De Maggio?_
* _Who starred as Adam's mum?_
* _Which character was portrayed by Terence Brown?_
* _List all characters that belong to Gond species_
* _In which episode Abzorbaloff first appeared?_
* _List me all episodes in 6th season_
* _Who starred as a second doctor?_
* _List all articles needing citation_
* _Who starred in Bad Wolf?_

# Examples for https://wowwiki.fandom.com

* _How many achievement points are achievable from "Classy" Guild Achievements?_
https://wowwiki.fandom.com/wiki/Special:Browse/%22Classy%22-20Guild-20Achievements
* _List me all proffesion achievements_
https://wowwiki.fandom.com/wiki/Category:Professions_achievements
* _How many achievements points I can get from 250 Fish?_
https://wowwiki.fandom.com/wiki/Special:Browse/250-20Fish
* _List me all Factions_
https://wowwiki.fandom.com/wiki/Property:Faction
* _What's the durability for "Flying" Worgen Robes?_ 
https://wowwiki.fandom.com/wiki/Special:Browse/%22Flying%22-20Worgen-20Robes
* _Which faction does the Alterac belong to?_
https://wowwiki.fandom.com/wiki/Special:Browse/Alterac
* _List all articles with modification date 6 November 2018_
https://wowwiki.fandom.com/wiki/Special:SearchByProperty/Modification-20date/23:38:07,-206-20November-202018
* _What is the population of Grizzly Hills?_
https://wowwiki.fandom.com/wiki/Special:Browse/Grizzly-20Hills
* _What is the level range for Grizzly Hills?_
https://wowwiki.fandom.com/wiki/Special:Browse/Grizzly-20Hills
* _What is the Quest:A Hunter's Challenge quest id?_
https://wowwiki.fandom.com/wiki/Special:Browse/Quest:A-20Hunter%27s-20Challenge
* _List item slots list in a Quest:A Hunter's Challenge_
https://wowwiki.fandom.com/wiki/Special:Browse/Quest:A-20Hunter%27s-20Challenge
* _Which faction does Wyrmskull Village belogns to?_
https://wowwiki.fandom.com/wiki/Special:Browse/Wyrmskull-20Village

# Supported "commands"
* _Tell me something about `foo`_
* _List me the `Season 2` stories_

```
>>> rrp.simple_parse("Was Jake Simmonds in the Doctor Who cast?")
'(S1 (SQ (VBD Was) (NP (NP (NNP Jake) (NNPS Simmonds)) (PP (IN in) (NP (DT the) (NN Doctor)))) (NP (WP Who) (NN cast)) (. ?)))'
>>> rrp.simple_parse("Tell me something about foo")
'(S1 (S (VP (VB Tell) (NP (PRP me)) (NP (NP (NN something)) (PP (IN about) (NP (NN foo)))))))'
```

# Command-line tool

```
$ python ask.py  "Who played Lionel Carson?"
Model directory: /home/macbre/.local/share/bllipparser/WSJ-PTB3
Model directory already exists, not reinstalling
INFO:get_oracle:Parsing question: Who played Lionel Carson?
INFO:get_oracle:Parsed question: [('WP', 'Who'), ('VBD', 'played'), ('NP', 'Lionel Carson')]
INFO:PersonFactOracle:You've asked: 'Who played Lionel Carson?' ({'name': 'Lionel Carson', 'property': 'played'})
INFO:PersonFactOracle:Asking SMW for 'Lionel Carson' page Actor property
INFO:PersonFactOracle:Got the value for Actor: ['Peter Bowles']
---
Who played Lionel Carson?
Lionel Carson is played by Peter Bowles.
```

# Web interface / HTTP API

Run `make server` to start it. Flask server will listen on `0.0.0.0:5050`.

## `/ask`

```
$ curl -s 'http://127.0.0.1:5050/ask?q=Who%20directed%20The%20Big%20Bang%20episode?' | jq
{
  "_intent": "EpisodeFactIntent",
  "_meta": {
    "answer": "Toby Haynes",
    "name": "The Big Bang episode",
    "property": "directed"
  },
  "_reference": null,
  "_words": {
    "NN": "episode",
    "NP": "The Big Bang episode",
    "VBD": "directed",
    "WP": "Who"
  },
  "answer": "\"The Big Bang episode\" episode has been directed by Toby Haynes."
}
```

# Data sources

## SemanticMediaWiki API

* Tell me something about `person name` - https://poznan.fandom.com/api.php?action=browsebysubject&subject=Karol_Libelt
* Give me a list of people born in `year` - https://poznan.fandom.com/api.php?action=ask&query=[[Born::1800]]|%3FBorn_in|sort%3DModification%20date|order%3Ddesc
* "Doctor Who" episodes - https://tardis.fandom.com/wiki/Property:Editor

# Tools

## Questions parsing libraries

* http://www.nltk.org/_modules/nltk/parse/bllip.html
* https://pypi.org/project/bllipparser/

# Inspirations

* [START, the world's first Web-based question answering system](http://start.csail.mit.edu/answer.php?query=What+South-American+country+has+the+largest+population%3F)
* [Amazon's Alexa](https://developer.amazon.com/docs/custom-skills/built-in-intent-library.html#intent-signature-syntax) / [intents concept](https://developer.amazon.com/docs/custom-skills/episode-intents.html)

# Whitepapers

> See https://groups.csail.mit.edu/infolab/publications.html

* [MIT's START and Omnibase described](https://groups.csail.mit.edu/infolab/publications/Katz-etal-NLDB02.pdf)
* [Indexing and Retrieving Natural Language Using Ternary Expressions](https://cs.uwaterloo.ca/~jimmylin/publications/Lin_MEng_thesis_2001.pdf)
* [Annotating the World Wide Web using Natural Language](https://groups.csail.mit.edu/infolab/publications/Katz-RIAO97.pdf)
* [Extracting Answers from the Web Using Knowledge Annotation and Knowledge Mining Techniques](https://groups.csail.mit.edu/infolab/publications/Lin-etal-TREC2002.pdf)

# Install

```
virtualenv env -ppython3
. env/bin/activate
pip install -r requirements.txt
```
