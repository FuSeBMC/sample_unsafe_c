import sys
import xml.etree.ElementTree as ET

def parse_graphml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
   
    namespace = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}
   
    nodes = {}
    edges = []
   
    for node in root.findall('graphml:graph/graphml:node', namespace):
        node_id = node.get('id')
        data = {data.get('key'): data.text for data in node.findall('graphml:data', namespace)}
        nodes[node_id] = data
   
    for edge in root.findall('graphml:graph/graphml:edge', namespace):
        source = edge.get('source')
        target = edge.get('target')
        data = {data.get('key'): data.text for data in edge.findall('graphml:data', namespace)}
        edges.append({'source': source, 'target': target, 'data': data})
   
    return nodes, edges

def extract_violation_info(nodes, edges):
    violation_info = []
   
    for edge in edges:
        source = edge['source']
        target = edge['target']
        data = edge['data']
       
        if nodes[target].get('violation') == 'true':
            violation_info.append({
                'source': source,
                'target': target,
                'line_number': data.get('startline'),
                'description': 'Violation detected'
            })
   
    return violation_info

def annotate_source_code(source_code, all_violation_info):
    lines = source_code.split('\n')
    annotated_lines = []
   
    for i, line in enumerate(lines, start=1):
        annotations = []
        for violation_info in all_violation_info:
            annotations.extend([info['description'] for info in violation_info if info['line_number'] == str(i)])
        if annotations:
            annotated_line = f'{line}  <!-- {", ".join(annotations)} -->'
        else:
            annotated_line = line
        annotated_lines.append(annotated_line)
   
    return '\n'.join(annotated_lines)

def generate_markdown_report(annotated_code, all_violation_info):
    markdown_content = "```c\n"
    markdown_content += annotated_code
    markdown_content += "\n```\n"
   
    print(markdown_content)

if __name__ == "__main__":
    source_file = sys.argv[1]
    graphml_files = sys.argv[2:]

    all_violation_info = []
    for graphml_file in graphml_files:
        nodes, edges = parse_graphml(graphml_file)
        violation_info = extract_violation_info(nodes, edges)
        if violation_info:
            all_violation_info.append(violation_info)

    with open(source_file, 'r') as f:
        source_code = f.read()

    annotated_code = annotate_source_code(source_code, all_violation_info)
    generate_markdown_report(annotated_code, all_violation_info)

