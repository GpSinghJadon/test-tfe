import ipdb, json
import os
from pprint import pprint
import subprocess
import hcl2

main_tf_filepath = 'test-tfe.git/main.tf'
TERRAFORM_KEYWORDS = ['resource']



def write_hcl_file(data):
    temp_tf_data_parsed_file = 'new_main.json'
    try:
        # write the parsed json data to a new file
        with open(temp_tf_data_parsed_file, 'w+') as nf:
            json.dump(data, nf)

        #   use json to hcl to generate the tf data.
        ps = subprocess.Popen(('cat', temp_tf_data_parsed_file), stdout=subprocess.PIPE)
        output = subprocess.check_output(('json2hcl'), stdin=ps.stdout)
        print(output)

        # Remove double quotes from the output
        temp_tf_data = output.decode(encoding='UTF-8',errors='strict').split('\n')
        new_tf_data = ''
        for line in temp_tf_data:
            if line == '':
                continue
            if "=" in line:
                new_tf_data += line.replace('"', '') + "\r\n"
                continue
            for word in line.split(' '):
                if word.strip("\"") in TERRAFORM_KEYWORDS:
                    new_tf_data += ' '+word.strip("\"")
                else:
                    new_tf_data += ' ' + word
            new_tf_data += "\r\n"

        with open(main_tf_filepath, 'w') as outfile:
            outfile.write(new_tf_data)

        # Clear the temporary files
        os.remove(temp_tf_data_parsed_file)
    except Exception as e:
        print("Unable to write the HCL file from the JSON data: {}".format(e))

def create_main_tf(src_directory):
    # new_tf_filepath = 'new_main.tf'
    main_tf_filepath = os.path.join(src_directory, 'main.tf')
    variables_tf_filepath = os.path.join(src_directory, 'variables.tf')
    try:
        with open(main_tf_filepath, 'r') as f:
            # main_tf_data = f.read()
            tf_data = hcl2.load(f)
            parsed_tf_data, variables = parse_tf(tf_data)
            print(json.dumps(parsed_tf_data))

        # CREATE main.tf HCL FILE FROM JSON DATA
        write_hcl_file(parsed_tf_data)

        # CREATE HCL FILE FROM JSON DATA
        create_variable_tf(variables,variables_tf_filepath)

    except Exception as e:
        print("main tf file not found: {}".format(e))

def create_variable_tf(variables, variables_filepath):
    pprint(variables)
    vars_tf_data = ''
    VARIABLE_FORMAT = \
'''variable "{}" {{
    type = {}
}}'''
    for key, value in variables.items():
        # vars_tf += "variable \"{}\" { \r\n \ttype = {} \r\n}".format(key, value)
        vars_tf_data += VARIABLE_FORMAT.format(key, value) + "\r\n"*2

    try:
        with open(variables_filepath, 'w') as vars_tf_file:
            vars_tf_file.write(vars_tf_data)
    except Exception as e:
        print("cannot write variables.tf file: {}".format(e))
    ipdb.set_trace()

def parse_tf(data):
    variables = {}
    if data.get('provider'):
        provider = [i for i in data['provider'][0]][0]
        del(data['provider'])
    if data.get('resource'):
        resource_groups_ids = []
        for i in range(len(data['resource'])):
            if 'resource_group' in next(iter(data['resource'][i])):
                data['resource'].pop(i)     # assumption: only one resource_group per main file
                break
                # resource_groups_ids.append(i)

    for i in range(len(data['resource'])):
        resource_type = next(iter(data['resource'][i]))
        resource_name = next(iter(data['resource'][i][resource_type]))
        new_resource_name = '_'.join(resource_type.split('_')[1:])
        data['resource'][i][resource_type][new_resource_name] = data['resource'][i][resource_type][resource_name]
        del(data['resource'][i][resource_type][resource_name])

        for key, value in data['resource'][i][resource_type][new_resource_name].items():
            if key == 'name':
                data['resource'][i][resource_type][new_resource_name][key] = 'var.{}_name'.format(new_resource_name)
                variables['{}_name'.format(new_resource_name)] = get_hcl_type(value[0])

            elif isinstance(value, list) and isinstance(value[0], dict):
                child_field = {}
                for k, v in value[0].items():
                    # ipdb.set_trace()
                    child_field[k] = 'var.{}_{}'.format(key, k)
                    variables['{}_{}'.format(key, k)] = get_hcl_type(v[0])
                data['resource'][i][resource_type][new_resource_name][key] = child_field
            else:
                data['resource'][i][resource_type][new_resource_name][key] = 'var.{}'.format(key)
                variables['{}'.format(key)] = get_hcl_type(value[0])

    # ipdb.set_trace()
    return data, variables


def get_hcl_type(param):
    types = {
        isinstance(param, int):     'number',
        isinstance(param, float):   'string',
        isinstance(param, bool):    'bool',
        isinstance(param, list):    'list',
    }
    try:
        return types[True]
    except KeyError as e:
        return "string"


if __name__ == '__main__':
    create_main_tf(main_tf_filepath)


# https://github.com/kvz/json2hcl