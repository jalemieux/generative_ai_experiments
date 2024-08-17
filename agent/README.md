# Agent

Agent provide interface to LLM for user. Match request to tool as soon as possible

Tools are implemented as actors, which manage their own context with the LLM. 

Currently the actor Coder converts user asks into python code and unit test. It makes use of a feedback loop between itself and another LLM context providing validation oof the code it generates.