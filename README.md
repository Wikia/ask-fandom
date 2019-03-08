# ask-fandom
Your semantic data-based assistant aka _Tell me FANDOM, ..._

# Supported questions

* _When was `someone` born?_
* _Who directed the `episode`?_
* _Who played in `episode`?_
* _Did `foo` played in `bar` episode?_
* _Was `Jake Simmonds` in the Doctor Who cast?_

# Supported "commands"
* _Tell me something about `foo`_
* _List me the `Season 2` stories_

# Data sources

## SemanticMediaWiki API

* Tell me something about `person name` - https://poznan.fandom.com/api.php?action=browsebysubject&subject=Karol_Libelt
* Give me a list of people born in `year` - https://poznan.fandom.com/api.php?action=ask&query=[[Born::1800]]|%3FBorn_in|sort%3DModification%20date|order%3Ddesc
* "Doctor Who" episodes - https://tardis.fandom.com/wiki/Property:Editor

# Tools

## Questions parsing libraries

* http://www.nltk.org/_modules/nltk/parse/bllip.html
* https://pypi.org/project/bllipparser/

## Text to speech and speech to text

* http://espeak.sourceforge.net/
* https://www.linuxlinks.com/speechtools/

# Inspirations

* [START, the world's first Web-based question answering system](http://start.csail.mit.edu/answer.php?query=What+South-American+country+has+the+largest+population%3F)

# Install

```
virtualenv env -ppython3
. env/bin/activate
pip install -r requirements.txt
```
