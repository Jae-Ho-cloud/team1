import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import folium
import folium.plugins
import time
import requests
import json

if __name__ == "__main__":
    print(f"pandas: pd {pd.__version__}")
    print(f"numpy: np {np.__version__}")
    print(f"scipy: sp {sp.__version__}")
    print(f"statsmodels: {statsmodels.__version__}")
    print(f"matplotlib: mpl {mpl.__version__}")
    print(f"seaborn: sns {sns.__version__}")
    print(f"geopandas: gpd {gpd.__version__}")
    print(f"folium: {folium.__version__}")
    print(f"requests: {requests.__version__}")

    font_path = "c:/Windows/Fonts/malgun.ttf"
    font_prop = mpl.font_manager.FontProperties(fname=font_path)
    mpl.rcParams['font.family'] = font_prop.get_name()
    mpl.rcParams['axes.unicode_minus'] = False

