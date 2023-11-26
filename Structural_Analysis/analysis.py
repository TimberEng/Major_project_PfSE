from eng_module import utils
from dataclasses import dataclass

def flexural_cri (sigma_y: float, I: float, c: float) -> float():
    """
    Calculate yielding moment My
    """
    M_y = (sigma_y * I / c)/10**6

    return M_y

def shear_cri (yield_stress: float, web_thick: float, web_depth: float) -> float():
    """
    Calculate shear stress based on an approximate formula
    """
    V_n = (0.6 * yield_stress * web_depth * web_thick)/10**3

    return V_n

def ver_defl (span: float) -> float():
    """
    Calculate the allowable vertical deflection based on AS4100 - 1998
    """
    return span/250

def laterl_dri (height: float) -> float():
    """
    Calculate the allowable laterial drift based on AS4100 - 1998
    """
    return height/150

@dataclass
class Isection:
    Section_name: str
    I: float
    dw: float
    tw: float
    c: float

def csv_record_to_Isction(record: list[str], **kwargs) -> Isection:
    I_s = Isection(
        Section_name = record[0],
        I = utils.str_to_float(record[1]),
        dw = utils.str_to_float(record[2]),
        tw = utils.str_to_float(record[3]),
        c = utils.str_to_float(record[4])
    )
    return I_s


def eng_check (cri: str, max_value: float, max_cri: float):
    if max_value >= max_cri:
        return f"Maximum {cri} is not meet the design criterion, please redesign your frame"
    else:
        return f"Maximum {cri} is meet this design criterion, please check other criterions"