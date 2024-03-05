import matsim


def speed_limit_intervention(network: matsim.Network.Network, av_speed_threshold_mps: float):
    """Speed limit intervention: Add AV mode to links where
     freespeed  <= av_speed_threshold_mps & where the underlying modes include car

    Args:
        network (matsim.Network.Network): Matsim Network
        av_speed_threshold_mps (float): Speed threshold in meters per second

    Returns:
        matsim.Network.Network: Network with Av mode on corresponding links
    """
    mask = (network.links.freespeed.values <= av_speed_threshold_mps) & (network.links.modes.str.contains("car"))
    network.links.loc[mask, "modes"] = network.links.loc[mask, "modes"].values + ",av"

    return network
