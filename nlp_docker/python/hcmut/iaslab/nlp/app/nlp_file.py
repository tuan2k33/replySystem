import os

file_name=["output_a.txt",
           "output_b.txt",
           "output_c.txt",
           "output_d.txt",
           "output_e.txt"]

def write_file(step, content):
    """
    Write content to a file in the output directory
    """
    output_dir = "/nlp/output"
    filename = os.path.join(output_dir, f"output{step}.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    