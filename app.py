import pandas as pd
import matsim
from interventions import speed_limit_intervention
import MatsimNetworkWriter as mnw
import sys, json
from tqdm import tqdm

################
# Helper Funcs
################


def write_network_file(out_file_name: str, network: matsim.Network.Network):
    with open(out_file_name, "wb+") as f_write:
        writer = mnw.NetworkWriter(f_write)
        writer.start_network()

        # write the nodes of the new network
        writer.start_nodes()
        nodes = network.nodes
        for i, j in tqdm(nodes.iterrows()):
            x = nodes.iloc[i].to_numpy()

            # so far we are lazily assuming the order of the columns
            # one might want to pass a dictionary instead and make this nicer
            writer.add_node(x[2], x[0], x[1])

        writer.end_nodes()

        # write the links of the new network
        writer.start_links()
        links = network.links
        for i, j in tqdm(links.iterrows()):
            x = links.iloc[i].to_numpy()
            # so far we are lazily assuming the order of the columns
            # one might want to pass a dictionary instead and make this nicer
            writer.add_link(x[6], x[7], x[8], x[0], x[1], x[2], x[3], x[4], x[5])
            # currently we do not pass any link attributes, these are a copy-paste from OSM anyway
            # and are not used in the simulation

        writer.end_links()
        writer.end_network()


################
# Main
################

if __name__ == "__main__":
    # read config
    config_file = sys.argv[1]
    with open(config_file, "r") as fp:
        config = json.load(fp)

    # load network file
    print("Reading Network File...")
    network_file_in = config["network_file_in"]
    network_in = matsim.read_network(network_file_in)

    # do intervention
    intervention_type = config["intervention"]["name"]
    intervention_params = config["intervention"]["params"]
    print(f"Performing Network Intervention: {intervention_type}...")
    if intervention_type == "speed_limit":
        speed_limit_mps = intervention_params["limit_kph"] / 3.6
        network_out = speed_limit_intervention(network_in, speed_limit_mps)

    else:
        raise RuntimeError(f"Intervention type: {intervention_type} not defined!")

    # write result
    print("Writing Resulting Network...")
    network_file_out = config["network_file_out"]
    network_out = write_network_file(network_file_out, network_out)
