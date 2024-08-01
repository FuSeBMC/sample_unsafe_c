import os
import argparse
import xml.etree.ElementTree as ET
import json
import uuid
from datetime import datetime
import sarif_om as sarif


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(v) for v in obj]
    elif hasattr(obj, "__dict__"):
        return {snake_to_camel(k): to_dict(v) for k, v in obj.__dict__.items() if v is not None}
    else:
        return obj

def load_json_rules(json_file):
    with open(json_file, 'r') as f:
        rules_data = json.load(f)
    
    rules = []
    for rule in rules_data:
        rules.append(
            sarif.ReportingDescriptor(
                id=rule["id"],
                name=rule["name"],
                short_description=sarif.MultiformatMessageString(
                    text=rule["short_description"]
                ),
                full_description=sarif.MultiformatMessageString(
                    text=rule["full_description"]
                ),
                default_configuration=sarif.ReportingConfiguration(
                    level=rule["level"]
                )
            )
        )
    
    return rules





def parse_graphml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}
    
    data = {
        'file_name': None,
        'nodes': {},
        'edges': [],
        'is_violation': False,
        'creation_time': None,
        'violations': [] 
    }

    witness_type_elem = root.find('.//graphml:data[@key="witness-type"]', namespaces)
    if witness_type_elem is not None and witness_type_elem.text == "violation_witness":
        data['is_violation'] = True

    creation_time_elem = root.find('.//graphml:data[@key="creationtime"]', namespaces)
    if creation_time_elem is not None:
        data['creation_time'] = creation_time_elem.text

    programfile_elem = root.find('.//graphml:data[@key="programfile"]', namespaces)
    if programfile_elem is not None:
        data['file_name'] = programfile_elem.text

    for node in root.findall('.//graphml:node', namespaces):
        node_id = node.get('id')
        node_data = {data.get('key'): data.text for data in node.findall('graphml:data', namespaces)}
        data['nodes'][node_id] = node_data

    for edge in root.findall('.//graphml:edge', namespaces):
        edge_data = {data.get('key'): data.text for data in edge.findall('graphml:data', namespaces)}
        edge_data.update({
            'source': edge.get('source'),
            'target': edge.get('target')
        })
        data['edges'].append(edge_data)
        
        startline_elem = edge.find('.//graphml:data[@key="startline"]', namespaces)
        if startline_elem is not None:
            data['violations'].append(max(int(startline_elem.text),1)) # the use of max() here is not ideal
            # I have done this as FuSeBMC sometimes detects vulnerabilites on line zero and SARIF requires 
            # all line numbers >= 1. 
    return data


def build_sarif(data,rules):
    sarif_log = sarif.SarifLog(
        version="2.1.0",
        runs=[]
    )

    rules_json = load_json_rules(rules)

    tool = sarif.Tool(
        driver=sarif.ToolComponent(
            name="FuSeBMC", # hardcoded tool info, improve this later
            version="AI-dev",
            information_uri="https://github.com/kaled-alshmrany/FuSeBMC",
            rules=rules_json
        )
    )

    fusebmc_results = []
    for graphml in data:
        if not graphml["type"].startswith("veri") and graphml["data"]["is_violation"]:
            description = ""
            for rule in rules_json:
                if graphml["type"].startswith(rule.id):
                    description = rule.short_description.text
                            
            for line in graphml["data"]["violations"]:
                fusebmc_results.append(sarif.Result(
                    rule_id=graphml["type"],
                    level="error",
                    message=sarif.Message(

                        text="A vulnerability was found: " + description
                    ),
                    locations=[
                        sarif.Location(
                            physical_location=sarif.PhysicalLocation(
                                artifact_location=sarif.ArtifactLocation(
                                    uri= os.path.sep.join(graphml["data"]["file_name"].split(os.path.sep)[2:]) #this is removing the top level path of the uri
                                    # from the graphml file, this is required as running in the docker image causes the directory to be workspace/.../file.c
                                    # when github expects ./file.c
                                ),
                                region=sarif.Region(
                                    start_line=line,
                                    end_line=line
                                )
                            )
                        )
                    ]
                ))

    run = sarif.Run(
        tool=tool,
        results=fusebmc_results,
        invocations=[ # check this, might need to change
            sarif.Invocation(
                execution_successful=True,
                start_time_utc=datetime.utcnow().isoformat() + "Z",
                end_time_utc=datetime.utcnow().isoformat() + "Z"
            )
        ]
    )

    sarif_log.runs.append(run)

    return sarif_log




def main():
    parser = argparse.ArgumentParser(description="Process GraphML files and convert them to SARIF.")
    parser.add_argument("directory", help="Directory containing GraphML files")
    parser.add_argument("rules", help="JSON containing ESBMC rules")
    args = parser.parse_args()

    graphml_files = [f for f in os.listdir(args.directory) if f.endswith('.graphml')]
    graphml_data = []
    
    for graphml_file in graphml_files:
        file_path = os.path.join(args.directory, graphml_file)
        print(f"Processing file: {file_path}")
        parsed_graphml = {
            "data" : parse_graphml_file(file_path),
            "type" : graphml_file[:-8] # remove ".graphml"
        }
        graphml_data.append(parsed_graphml)

    sarif = build_sarif(graphml_data,args.rules)
    print(sarif)
    sarif_file_path = os.path.join(args.directory,os.path.basename(os.path.splitext(graphml_data[0]["data"]["file_name"])[0])) + '.sarif'
    with open(sarif_file_path, 'w') as sarif_file:
        json.dump(to_dict(sarif), sarif_file, indent=2)
    print(f"SARIF file generated: {sarif_file_path}")


if __name__ == "__main__":
    main()
