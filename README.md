# Generative AI Experiments

Experiment with the latest generative ai platform such as OpenAI's chatgpt, Anthropic's Claude, Meta's Llama, etc.
Focus on solving specific use cases, e.g. smart search, agentic workflow, etc.


### TODO: 
name: actor_dag.py
what: compose complex workflow 
why: applied solution to business problems 
how: autonomous actor dag/ 
 - Actor: 
   - Solves a problem. 
   - Exposes a description of problem it solves using NL. 
   - Description used by upstream actor to determine which actor to call 
   - Downstream actors are registered to actor, core actor logic determines which downstream actor to invoke

example: 
actor_match: given user input match the request to an existing actor, execute actor, validate response
activity_highlights: given user activities produce a summary with highlights and special formatting 
