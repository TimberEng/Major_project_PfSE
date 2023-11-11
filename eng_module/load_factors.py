NBCC_2020_COMBINATIONS = {
    "LC1":  {"D": 1.4},
    "LC2a": {"D": 1.25, "L": 1.5},
    "LC2b": {"D": 1.25, "L": 1.5, "S": 1.0},
    "LC2c": {"D": 0.9, "L": 1.5},
    "LC2d": {"D": 0.9, "L": 1.5, "S": 1.0},
    "LC3a": {"D": 1.25, "S": 1.5},
    "LC3b": {"D": 1.25, "S": 1.5, "L": 1.0},
    "LC3c": {"D": 0.9, "S": 1.5},
    "LC3d": {"D": 0.9, "S": 1.5, "L": 1.0},
    "LC4a": {"D": 1.25, "W": 1.4},
    "LC4b": {"D": 1.25, "W": 1.4, "L": 0.5},
    "LC4c": {"D": 0.9, "W": 1.4},
    "LC4d": {"D": 0.9, "W": 1.4, "L": 0.5},
}

def factor_load(
    D_load: float = 0., D: float = 0., 
    L_load: float = 0., L: float = 0., 
    W_load: float = 0., W: float = 0.,
    S_load: float = 0., S: float = 0.,
    E_load: float = 0., E: float = 0.,
    ):
    factored_load = D_load*D + L_load*L + S_load*S + W_load*W + E_load*E
    return factored_load

def max_factored_load(loads: dict, load_combos: dict) -> float:
    """
    Returen the max factored load computed from 'loads' based on the combinations in 'load_combos'
    """
    factored_loads = []
    for load_combo in load_combos.values():
        factored_load = factor_load(**loads, **load_combo)
        factored_loads.append(factored_load)
    return max(factored_loads)

def min_factored_load(loads: dict, load_combos: dict) -> float:
    """
    Returen the min factored load computed from 'loads' based on the combinations in 'load_combos'
    """
    factored_loads = []
    for load_combo in load_combos.values():
        factored_load = factor_load(**loads, **load_combo)
        factored_loads.append(factored_load)
    return min(factored_loads)