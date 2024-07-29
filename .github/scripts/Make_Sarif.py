import os
import argparse
import xml.etree.ElementTree as ET
import json
import uuid
from datetime import datetime
import sarif_om as sarif

def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(v) for v in obj]
    elif hasattr(obj, "__dict__"):
        return {k: to_dict(v) for k, v in obj.__dict__.items() if v is not None}
    else:
        return obj



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
            data['violations'].append(int(startline_elem.text)) 
    return data

def convert_to_sarif(graphml_data):
    runs = []
    results = []

    for edge in graphml_data['edges']:
        if 'startline' in edge:
            result = {
                "ruleId": "CustomRule",
                "message": {
                    "text": "Violation detected"
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": graphml_data['nodes'][edge['source']].get('programfile')
                            },
                            "region": {
                                "startLine": int(edge['startline']),
                                "endLine": int(edge['endline']) if 'endline' in edge else int(edge['startline']),
                            }
                        }
                    }
                ]
            }
            results.append(result)

    run = {
        "tool": {
            "driver": {
                "name": "Custom Static Analysis Tool",
                "informationUri": "https://example.com",
                "rules": [
                    {
                        "id": "CustomRule",
                        "name": "Violation Rule",
                        "shortDescription": {
                            "text": "This rule detects violations."
                        },
                        "fullDescription": {
                            "text": "A full description of the violation rule."
                        },
                        "defaultConfiguration": {
                            "level": "error"
                        }
                    }
                ]
            }
        },
        "results": results,
        "invocations": [
            {
                "executionSuccessful": True,
                "startTimeUtc": datetime.utcnow().isoformat() + "Z",
                "endTimeUtc": datetime.utcnow().isoformat() + "Z"
            }
        ]
    }

    runs.append(run)
    sarif_log = {
        "version": "2.1.0",
        "runs": runs
    }

    return sarif_log

def build_sarif(data):
    sarif_log = sarif.SarifLog(
        version="2.1.0",
        runs=[]
    )

    tool = sarif.Tool(
        driver=sarif.ToolComponent(
            name="FuSeBMC", # hardcoded tool info, improve this later
            version="AI-dev",
            information_uri="https://github.com/kaled-alshmrany/FuSeBMC",
            rules=[
                sarif.ReportingDescriptor(
                    id="align",
                    name="align",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="assertions",
                    name="assertions",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="atomicity",
                    name="atomicity",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="bounds",
                    name="bounds",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="data-races",
                    name="data-races",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="deadlock",
                    name="deadlock",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="div-by-zero",
                    name="div-by-zero",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="lock-order",
                    name="lock-order",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="nan",
                    name="nan",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="overflow",
                    name="overflow",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="pointer",
                    name="pointer",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="struct-fields",
                    name="struct-fields",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="ub-shift",
                    name="ub-shift",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="unlimited-scanf",
                    name="unlimited-scanf",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="unsigned-overflow",
                    name="unsigned-overflow",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                ),
                sarif.ReportingDescriptor(
                    id="vla-size",
                    name="vla-size",
                    short_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text="Placeholder"
                    ),
                    default_configuration=sarif.ReportingConfiguration(
                        level="error"
                    )
                )

            ]
        )
    )

    fusebmc_results = []
    for graphml in data:
        if not graphml["type"].startswith("veri") and graphml["data"]["is_violation"]:
            for line in graphml["data"]["violations"]:
                fusebmc_results.append(sarif.Result(
                    rule_id=graphml["type"],
                    message=sarif.Message(
                        text="A vulnerability was found."
                    ),
                    locations=[
                        sarif.Location(
                            physical_location=sarif.PhysicalLocation(
                                artifact_location=sarif.ArtifactLocation(
                                    uri=graphml["data"]["file_name"]
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
        print(parsed_graphml)
        graphml_data.append(parsed_graphml)

    sarif = build_sarif(graphml_data)
    sarif_file_path = os.path.join(args.directory,os.path.basename(os.path.splitext(graphml_data[0]["data"]["file_name"])[0])) + '.sarif'
    with open(sarif_file_path, 'w') as sarif_file:
        json.dump(to_dict(sarif), sarif_file, indent=2)
    print(f"SARIF file generated: {sarif_file_path}")


if __name__ == "__main__":
    main()
