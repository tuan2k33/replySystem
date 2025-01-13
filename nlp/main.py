from nltk import grammar, parse # type: ignore
import argparse
import nltk  # type: ignore 

from nlp_parser import parse_to_procedure
from nlp_data import retrieve_result
from nlp_file import write_file

def main(args):
    """
    Main entry point for the program
    """
    # Download required NLTK data (add this)
    try:
        nltk.data.find('grammars/large_grammars/atis.cfg')
    except LookupError:
        nltk.download('punkt')
    
    #Load grammar from .fcfg file
    print("-------------Loading grammar---------------------")
    try:
        nlp_grammar = parse.load_parser(args.rule_file_name, trace=0)
        print("Grammar loaded at {}".format(args.rule_file_name))
        write_file(1, str(nlp_grammar.grammar()))
    except Exception as e:
        print(f"Error loading grammar: {e}")
        return
               
    question = args.question
    
    #Get parse tree
    print("-------------Parsed structure-------------")
    try:
        # Tokenize the question properly
        tokens = question.replace('?','').split()
        trees = list(nlp_grammar.parse(tokens))
        if not trees:
            print("Could not parse the question!")
            return
        tree = trees[0]  # Get the first valid parse
        print(question)
        print(tree)
        write_file(2, str(tree))
    except Exception as e:
        print(f"Error parsing question: {e}")
        return
 
    #Parse to logical form
    print("-------------Parsed logical form-------------")
    try:
        logical_form = str(tree.label()['SEM']).replace(',',' ')
        print(logical_form)
        write_file(3, str(logical_form))
    except Exception as e:
        print(f"Error creating logical form: {e}")
        return
               
    #Get procedure semantics
    print("-------------Procedure semantics-------------")
    try:
        procedure_semantics = parse_to_procedure(tree)
        print(procedure_semantics['str'])
        write_file(4, procedure_semantics['str'])
    except Exception as e:
        print(f"Error creating procedure semantics: {e}")
        return
    
    #Retrieve result:
    print("-------------Retrieved result-------------")
    try:
        results = retrieve_result(procedure_semantics)
        if len(results) == 0:
            print("No result found!")
        else:
            for result in results:
                print(result, end=' ', flush=True)
            print('')
            write_file(5, " ".join(str(r) for r in results))
    except Exception as e:
        print(f"Error retrieving results: {e}")
        return
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NLP Assignment Command Line")
    
    parser.add_argument(
      '--question',
      default="Can you list all the tours",
      #help="Question to be parsed. Default = 'How long does it take to travel from Ho Chi Minh City to Da Nang?'"
    )
    
    parser.add_argument(
      '--rule_file_name',
      default="grammar.fcfg",
      #help="Context Free Grammar file to be parsed. Default = 'grammar.fcfg'"
    )
    
    args = parser.parse_args()
    main(args)