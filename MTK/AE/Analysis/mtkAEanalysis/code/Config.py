from MTK.AE.Analysis.mtkAEanalysis.code.mtkAEanalysis_FLC import FLC
from MTK.AE.Analysis.mtkAEanalysis.code.mtkAEanalysis_HUS import HUS
from MTK.AE.Analysis.mtkAEanalysis.code.mtkAEanalysis_SX3 import SX3
class Config():
    def __init__(self) -> None:
        self.config = \
            {
                "mtkAEanalysis_FLC": FLC,
                "mtkAEanalysis_HUS": HUS,
                "mtkAEanalysis_SX3": SX3,
            }