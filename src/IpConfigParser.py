import subprocess

def ipconfig_all():
    result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, check=True, shell=True).stdout.strip().split("\n\n")
    output_dictionary = dict()

    for line in result:
        line = line.split("\n")
        
        if len(line) == 1:
            adapter_name = line[0]
        else:
            output_dictionary[adapter_name] = atributes_to_dictionary(line)
    
    return output_dictionary

def atributes_to_dictionary(atributes: list[str]):
    output_dictionary = dict()

    for atribute_value in atributes:
        atribute_value = atribute_value.strip()
        splitter = atribute_value.find(":")
        atribute = atribute_value[:splitter]
        value = atribute_value[splitter + 1:].strip()

        while atribute[-1] == ' ' or atribute[-1] == '.':
            atribute = atribute[:-1]
        
        output_dictionary[atribute] = value
    
    return output_dictionary

if __name__ == "__main__":
    ipconfig_all()