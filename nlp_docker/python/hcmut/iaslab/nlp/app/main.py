try:
    from nltk import grammar, parse
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'nltk'])
    from nltk import grammar, parse

import argparse
import nltk
import os

from hcmut.iaslab.nlp.app.nlp_parser import parse_to_procedure
from hcmut.iaslab.nlp.app.nlp_data import retrieve_result
from hcmut.iaslab.nlp.app.nlp_file import write_file

def main(**kwargs):
    """
    Main entry point for the program
    """
    # Extract parameters from kwargs
    question = kwargs.get('question', "What mode of transportation is used for the Nha Trang tour?")
    rule_file_name = kwargs.get('rule_file_name', "grammar.fcfg")
    
    # Get the directory containing main.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    grammar_path = os.path.join(current_dir, rule_file_name)
    
    # Thêm định nghĩa output directory
    output_dir = "/nlp/output"
    os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục output nếu chưa tồn tại
    
    try:
        nltk.data.find('grammars/large_grammars/atis.cfg')
    except LookupError:
        nltk.download('punkt')
    
    # Debug: Print paths
    print(f"Current directory: {current_dir}")
    print(f"Looking for grammar file at: {grammar_path}")
    print(f"File exists: {os.path.exists(grammar_path)}")
    
    print("-------------Loading grammar---------------------")
    try:
        if not os.path.exists(grammar_path):
            raise FileNotFoundError(f"Grammar file not found: {grammar_path}")
            
        with open(grammar_path, 'r') as f:
            print(f"Grammar file content length: {len(f.read())}")
            
        nlp_grammar = parse.load_parser(grammar_path, trace=0)
        print("Grammar loaded at {}".format(grammar_path))
        write_file(1, str(nlp_grammar.grammar()))
    except Exception as e:
        print(f"Error loading grammar: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(traceback.format_exc())
        return
    
    print("-------------Parsed structure-------------")
    try:
        tokens = question.replace('?','').split()
        trees = list(nlp_grammar.parse(tokens))
        if not trees:
            print("Could not parse the question!")
            return
        tree = trees[0]
        print(question)
        print(tree)
        write_file(2, str(tree))
    except Exception as e:
        print(f"Error parsing question: {e}")
        return

    print("-------------Parsed logical form-------------")
    try:
        logical_form = str(tree.label()['SEM']).replace(',',' ')
        print(logical_form)
        write_file(3, str(logical_form))
    except Exception as e:
        print(f"Error creating logical form: {e}")
        return
    
    print("-------------Procedure semantics-------------")
    try:
        procedure_semantics = parse_to_procedure(tree)
        print(procedure_semantics['str'])
        write_file(4, procedure_semantics['str'])
    except Exception as e:
        print(f"Error creating procedure semantics: {e}")
        return
    
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
        default="What mode of transportation is used for the Nha Trang tour?"
    )
    parser.add_argument(
        '--rule_file_name',
        default="grammar.fcfg"
    )
    args = parser.parse_args()
    main(question=args.question, rule_file_name=args.rule_file_name)