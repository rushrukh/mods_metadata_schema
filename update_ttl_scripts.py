import nen_to_axioms
import os

# create a module name dictionary
module_name_dict = {
    'Abstract': 'Abstract Pattern',
    'AccessCondition': 'Access Condition Pattern',
    'Classification': 'Classification Pattern',
    'MODSExtension': 'MODSExtension Pattern',
    'Genre': 'Genre Pattern',
    'Identifier': 'Identifier Pattern',
    'Language': 'Language Pattern',
    'Location': 'Location Pattern',
    'M_AltFormat_Attributes': 'Alternative Format Attributes Module Pattern',
    'M_Authority': 'Authority Module Pattern',
    'M_Cartographic': 'Cartographic Module Pattern',
    'M_DateInfo': 'Date Info Module Pattern',
    'M_ElementInfo': 'Element Info Module Pattern',
    'M_Geographic_Attributes': 'Geographic Attributes Module Pattern',
    'M_Geographic_Subject': 'Geographic Subject Module Pattern',
    'M_Language_Attributes': 'Language Attributes Module Pattern',
    'M_Link_Attributes': 'Link Attributes Module Pattern',
    'M_Organization': 'Organization Module Pattern',
    'M_OtherTypeInfo': 'Other Type Info Module Pattern',
    'M_Place': 'Place Module Pattern',
    'M_Role': 'Role Module Pattern',
    'M_Term': 'Term Module Pattern',
    'Name': 'Name Pattern',
    'Note': 'Note Pattern',
    'OriginInfo': 'Origin Info Pattern',
    'Part': 'Part Pattern',
    'PhysicalDescription': 'Resource Physical Description Pattern',
    'RecordInfo': 'Record Info Pattern',
    'RelatedItem': 'Related Item Pattern',
    'PrimaryTopic': 'Primary Topic Pattern',
    'TableOfContents': 'Table of Contents Pattern',
    'TargetAudience': 'Target Audience Pattern',
    'TitleInfo': 'Title Info Pattern',
    'TypeOfResource': 'Type of Resource Pattern',
}


def get_paths_to_module():
    base_dir = os.getcwd() + '/modules/'
    module_paths = [os.path.join(base_dir, name) for name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, name))]

    return module_paths

def get_manchester_axioms(module_path):
    with open(module_path + '/axioms.txt', "r") as f:
        current_manchester_axioms = [line.strip() for line in f.readlines() if (line.strip() and (line[0] != "#"))]
        f.close()
    current_manchester_axioms = """{}""".format('\n'.join(current_manchester_axioms))

    return current_manchester_axioms

def required_updates(graph_path, current_module, current_manchester_axioms):

    with open(graph_path, 'r') as f:
        print(f"graph_path: {graph_path}")
        lines = f.readlines()
        
        # 5. Add to the 5th line in each graph.ttl file the following:
        prefixes = """@prefix dc: <http://purl.org/dc/elements/1.1/> .
                    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
                    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
                    @prefix modl: <https://archive.org/services/purl/domain/modular_ontology_design_library> .
                    @prefix opla-cp: <http://ontologydesignpatterns.org/opla-cp#> .
                    @prefix opla-sd: <http://ontologydesignpatterns.org/opla-sd#> .
                    @prefix opla-core: <http://ontologydesignpatterns.org/opla-core#> . """
        
        opla_info = '''<https://kastle-labl.org/lod/ontology/> rdf:type owl:Ontology ;
                                                                opla-core:hasPatternName "''' + module_name_dict[current_module] + '''" ;
                                                                opla-cp:addressesScenario """Use Case
                                                                Use Case Description"""^^xsd:string ;
                                                                opla-cp:hasCompetencyQuestion "cq1"^^xsd:string ,
                                                                                            "cq2"^^xsd:string ;
                                                                opla-sd:hasConnections """''' + current_manchester_axioms + '''"""^^xsd:string ;
                                                                opla-sd:hasSchemaDiagramFileName "''' + current_module + '''.png"^^xsd:string ;
                                                                dc:contributor "Cogan Shimizu" ,
                                                                            "Pascal Hitzler" ,
                                                                            "Rushrukh Rayan" ;
                                                                dc:creator "Cogan Shimizu" ,
                                                                        "Pascal Hitzler" ,
                                                                        "Rushrukh Rayan" .'''
        
        # opla_info = opla_info.replace("\n", "")
        # print(f"opla_info: {opla_info}")

        updates_required = prefixes + '\n' + opla_info + '\n'
        # 6. Write the prefixes and opla_info to the 5th line in each graph.ttl file
        lines.insert(4, updates_required)
        f.close()

    return lines

def update_existing_ttl_files():
    module_paths = get_paths_to_module()

    for module_path in module_paths:
        if(module_path != os.getcwd() + '/modules/AllModule'):
            current_module = module_path.split('/')[-1]
            # print to check what module is being updated
            # print(f"current_module: {current_module}")
            current_manchester_axioms = get_manchester_axioms(module_path)
            graph_path = module_path + '/graph.ttl'

            required_update = required_updates(graph_path, current_module, current_manchester_axioms)

            with open(graph_path, 'w') as f:
                f.writelines(required_update)
                f.close()


if __name__ == "__main__":
    nen_to_axioms.get_all_axioms()
    update_existing_ttl_files()
    