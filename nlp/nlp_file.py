file_name=["output_a.txt",
           "output_b.txt",
           "output_c.txt",
           "output_d.txt",
           "output_e.txt"]

def write_file(question_number, content):
    with open(file_name[question_number-1], 'w', encoding='utf-8') as file:
        if isinstance(content, list):
            # Join with newlines for list content
            file.write('\n'.join(content))
        else:
            file.write(content)
        
    