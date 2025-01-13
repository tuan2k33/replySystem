# Natural Language Processing Project
A reply system about flights' information using natural language parsing techniques. It parses the input question (in English), look up the result in the given database and return that. 

Big thanks to @hoanglehaithanh for the core/reference: https://github.com/hoanglehaithanh/NLP2017_Assignment

## To run the program
1. Using ```nlp``` file:
Open terminal and run: ```$python3 main.py --question [question] --rule_file_name [rule_file_name]```
Usage: (```--question [question] --rule_file_name [rule_file_name]``` part is optional)
- ```--question``` : The input question in English
- ```--rule_file_name``` : The context free grammar file (.fcfg)
2. Using ```nlp_docker``` file: Just open file docker build

## Further research
- TENSE (PAST, PRESENT,...)??
- Better grammar rules?? The current rules are quite confusing.
- Vietnamese/other languages support??
