import nuke
import difflib

# Function to pop up a searchable list of nodes in the node graph
def find_node_popup():
    # Get all nodes in the script
    nodes = nuke.allNodes()
    
    # Create a list of node names
    node_names = [node.name() for node in nodes]

    # Show a pop-up input box
    entered_name = nuke.getInput('Find and Select Node', '')

    # Check if the user provided input
    if entered_name:
        # Find the closest matches to the entered name
        similar_nodes = difflib.get_close_matches(entered_name, node_names, n=5, cutoff=0.1)

        # If there are close matches, show a selection prompt
        if similar_nodes:
            # Ask the user to pick from similar nodes
            selected_node_name = nuke.getInput(f'Did you mean one of these?\n{", ".join(similar_nodes)}', similar_nodes[0])
            
            if selected_node_name and selected_node_name in node_names:
                # Deselect all nodes
                nuke.selectAll()
                nuke.invertSelection()

                # Select the matching node
                for node in nodes:
                    if node.name() == selected_node_name:
                        node.setSelected(True)
                        nuke.zoomToFitSelected()  # Focus the viewer on the selected node
                        break
            else:
                nuke.message(f'No node selected.')
        else:
            nuke.message(f'No similar nodes found for "{entered_name}".')