Design
======

`ask-fandom` uses Natural Language Processing to understand the question asked in English.

## Understanding the question

Suppose the user asks:

> Who played [Jake Simmonds](https://tardis.fandom.com/wiki/Jake_Simmonds)?

In order to understand the intent of the question
we parse it using [`blibparser` Python module with build-in parsing model trained from Wall Street Journal](https://pypi.org/project/bllipparser/).

And the output we get the following structure with different types of words grouped:

```python
[('WP', 'Who'), ('VBD', 'played'), ('NP', 'Jake Simmonds')]
```

We know that the user asked `who` (`WP` entry) and that the subject of the question is `Jake Simmonds` (`NP`). And that
he wants to know who `played` (`VBD`) him.

## Intents

Once we get the idea of what the user asks us, we can try to get an answer.

```
INFO:get_intent:Available intents: ['PersonFactIntent', 'EpisodeFactIntent', 'WoWGroupsMemberIntent']
```

So far we have three different intents. We can imagine sets of intents as a panel of experts. Each of them specialises
in a given topic. `PersonFactIntent` can answer questions like _Who played Jake Simmonds?_, while `WoWGroupsMemberIntent`
has deep knowledge of the World of Warcraft.

#### Selecting an intent

Having this panel of experts (intents) we can **ask each intent if they can answer the users' question**.
`is_question_supported` method in each of intents provides us with this information. By executing it on
each intent we can elect our source of knowledge.

Then we pass our parsed question to the specific intent:

```
INFO:root:Selected <class 'ask_fandom.intents.semantic_media_wiki.tv_series.PersonFactIntent'> with {'name': 'Jake Simmonds', 'property': 'played'}
```

## Answering the question

Each intent provides a mapping of grouped words to specific parameters, e.g. which part of question is a name of a character (`NP` maps to `name`).

```
INFO:PersonFactIntent:You've asked: 'Who played Jake Simmonds?' ({'name': 'Jake Simmonds', 'property': 'played'})
INFO:PersonFactIntent:Asking tardis.fandom.com SMW for 'Jake Simmonds' page Actor property
INFO:PersonFactIntent:Got the value for Actor: ['Andrew Hayden-Smith']
INFO:root:Who played Jake Simmonds? -> Jake Simmonds is played by Andrew Hayden-Smith. (PersonFactIntent: {'answer': 'Andrew Hayden-Smith', 'name': 'Jake Simmonds', 'property': 'played'})
```

We then allow intent to perform any required operations to provide us with an answer. In this case [we use SemanticMediaWiki to fetch the information](https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds).

And here it's - an answer to the question. We asked the wiki and we got an answer:

> - Who played Jake Simmonds?
> - Jake Simmonds is played by Andrew Hayden-Smith.
