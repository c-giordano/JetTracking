#coarse simple
python analysis-plot.py --version 2 --eta_cut coarse --simple_cut pt
python analysis-plot.py --version 2 --eta_cut coarse --simple_cut mass
python analysis-plot.py --version 2 --eta_cut coarse --simple_cut r
# Coarse composite
python analysis-plot.py --version 2 --eta_cut coarse --simple_cut pt --composite_cut mass
python analysis-plot.py --version 2 --eta_cut coarse --simple_cut pt --composite_cut r
python analysis-plot.py --version 2 --eta_cut coarse --simple_cut mass --composite_cut r
#Fine simple
python analysis-plot.py --version 2 --eta_cut fine --simple_cut pt
python analysis-plot.py --version 2 --eta_cut fine --simple_cut mass
python analysis-plot.py --version 2 --eta_cut fine --simple_cut r
#Fine composite
python analysis-plot.py --version 2 --eta_cut fine --simple_cut pt --composite_cut mass
python analysis-plot.py --version 2 --eta_cut fine --simple_cut pt --composite_cut r
python analysis-plot.py --version 2 --eta_cut fine --simple_cut mass --composite_cut r