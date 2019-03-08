# ask-fandom
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

# Supported "commands"
* _Tell me something about `foo`_
* _List me the `Season 2` stories_

```
>>> rrp.simple_parse("Was Jake Simmonds in the Doctor Who cast?")
'(S1 (SQ (VBD Was) (NP (NP (NNP Jake) (NNPS Simmonds)) (PP (IN in) (NP (DT the) (NN Doctor)))) (NP (WP Who) (NN cast)) (. ?)))'
>>> rrp.simple_parse("Tell me something about foo")
'(S1 (S (VP (VB Tell) (NP (PRP me)) (NP (NP (NN something)) (PP (IN about) (NP (NN foo)))))))'
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
