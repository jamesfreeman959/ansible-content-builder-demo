#!/bin/env python
import json
import yaml
import re

def format_resource_name(resource_name):
    # Remove the 'AWS::' prefix if it exists
    if resource_name.startswith("AWS::"):
        resource_name = resource_name[5:]  
    print(resource_name)
    parts = resource_name.split("::")
    formatted_parts = []
    for part in parts:
        # Handle CamelCase and acronyms properly
        # Step 1: Insert underscore between sequences of uppercase letters and an uppercase letter followed by lowercase
        formatted_part = re.sub(r'([A-Z0-9]+)([A-Z][a-z])', r'\1_\2', part)
        # Step 2: Insert underscore between a lowercase letter and an uppercase letter
        formatted_part = re.sub(r'([a-z])([A-Z])', r'\1_\2', formatted_part)


        # Join all parts and convert to lowercase
        formatted_part = formatted_part.lower()
        formatted_parts.append(formatted_part)


    formatted_name = '_'.join(formatted_parts)

    return formatted_name

def convert_json_to_yaml(json_file, yaml_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Prepare the data in the desired format
    yaml_data = []
    for item in data:
        resource_type = item[0]  # Assuming each item is a list with TypeName as the first element
        description = item[1]  # Assuming each item is a list with Description as the first element
        yaml_data.append({
            format_resource_name(resource_type): {
                "resource": resource_type,
                "documentation": {
                    "short_description": description,
                    "description": description
                }
            }
        })

    # Write the YAML data to a file
    with open(yaml_file, 'w') as file:
        yaml.dump(yaml_data, file, sort_keys=False)

# Call the function with the appropriate file paths
convert_json_to_yaml('types.json', 'modules.yaml')

