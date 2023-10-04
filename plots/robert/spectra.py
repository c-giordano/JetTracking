import ROOT
from RootTools.core.standard import *
import RootTools.core.logger as logger_rt

import Analysis.Tools.syncer as syncer
import os
import math

import Analysis.Tools.user as user

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--plot_directory',     action='store',      default='JetTracking/v3')
#argParser.add_argument('--selection',          action='store',      default=None)
argParser.add_argument('--sample',             action='store',      default='DYJetsToLL_M50_LO',)
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?')

args = argParser.parse_args()

# choose a sample
import data
sample = data.DYJetsToLL_M50_LO

if args.small:
    args.plot_directory+="_small"
    sample.reduceFiles(to=10)

preselection = "Jet_pt>100"

# 1D Jet & pair kinematics
if True:
    plot_cfg = {
        'Jet_pt': {'var':'Jet_pt', 'binning':[30, 100, 1500], 'texX':"p_{T}(jet) (GeV)"},
        'Jet_eta':{'var':'Jet_eta', 'binning':[30, -3, 3], 'texX':"#eta(jet)"},
        'Jet_phi':{'var':'Jet_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(jet)"},

        'Pair_pt':{'var':'Pair_pt', 'binning':[30, 0, 1500], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_eta':{'var':'Pair_eta', 'binning':[30, -3, 3], 'texX':"#eta(pair)"},
        'Pair_phi':{'var':'Pair_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(pair)"},


        'Pair_deltaPhi':{'var':'Pair_deltaPhi', 'binning':[30, -3, 3], 'texX':"#Delta#eta(pair)"},
        'Pair_deltaEta':{'var':'Pair_deltaEta', 'binning':[30, -math.pi, math.pi], 'texX':"#Delta#phi(pair)"},
        }

    plots = []
    for name, p in plot_cfg.items():
        print "At " + name
        h = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection)
        h.legendText = sample.name

        plots.append( Plot.fromHisto( name, [[h]], texX = p['texX'] ) )

    for logY in [False, True]:
        for p in plots: 
            plotting.draw( p, 
                plot_directory = os.path.join( user.plot_directory, args.plot_directory, "inclusive", ("log" if logY else "lin")), 
                yRange = "auto", extensions=["png"], copyIndexPHP=True) 
    syncer.sync()

# 2D pair pt eta vs phi
if False:
    for what in ["Pair", "Jet"]:
        name = "{what}_eta_vs_{what}_phi".format(what=what)
        h2D = sample.get2DHistoFromDraw(name.replace("_vs_", ":"), [20,-math.pi,math.pi,20,-3,3], selectionString = preselection)
        p = Plot2D.fromHisto( name, [[h2D]], texX = "#phi(%s)"%what, texY="#eta(%s)"%what )
        for logZ in [False, True]:
            plotting.draw2D( p, logZ = logZ,
                plot_directory = os.path.join( user.plot_directory, args.plot_directory, "inclusive", ("log" if logZ else "lin")), 
                extensions=["png"], copyIndexPHP=True) 
    syncer.sync()

# slices 
if False:

    slices = [ {'window':(math.pi*(-1+i/3.), math.pi*(-1+(i+1)/3.) ) } for i in range(6) ] 
    colors = [ROOT.kBlue, ROOT.kRed, ROOT.kMagenta, ROOT.kGreen, ROOT.kPink, ROOT.kCyan]
    plot_cfg = {
        'Pair_pt':{'var':'Pair_pt', 'binning':[30, 0, 1500], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_pt_low':{'var':'Pair_pt', 'binning':[30, 0, 100], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_eta':{'var':'Pair_eta', 'binning':[30, -3, 3], 'texX':"#eta(pair)"},
        'Pair_phi':{'var':'Pair_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(pair)"},

        'Pair_tm_pt':{'var':'Pair_tm_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tm) (GeV)"},
        'Pair_tm_pt_low':{'var':'Pair_tm_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tm) (GeV)"},
        'Pair_tm_eta':{'var':'Pair_tm_eta', 'binning':[30, -3, 3], 'texX':"#eta(tm)"},
        'Pair_tm_phi':{'var':'Pair_tm_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tm)"},

        'Pair_tp_pt':{'var':'Pair_tp_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tp) (GeV)"},
        'Pair_tp_pt_low':{'var':'Pair_tp_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tp) (GeV)"},
        'Pair_tp_eta':{'var':'Pair_tp_eta', 'binning':[30, -3, 3], 'texX':"#eta(tp)"},
        'Pair_tp_phi':{'var':'Pair_tp_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tp)"},
        }

    plots = []
    for name, p in plot_cfg.items():
        print "At " + name
        h_inc = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection)
        h_inc.legendText = "inclusive"

        h_slice = {}
        for i_slice_, slice_ in enumerate( slices ):
            h_slice[slice_['window']] = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection+"&&Pair_phi>=%f&&Pair_phi<%f"%(slice_['window']))
            h_slice[slice_['window']].legendText = "%3.2f #leq #phi(Pair) < %3.2f" % slice_['window']
            h_slice[slice_['window']].SetLineColor( colors[i_slice_] )
            
        plots.append( Plot.fromHisto( name+"_sliced", [[h_inc]] + [ [h_slice[slice_['window']]] for slice_ in slices], texX = p['texX'] ) )

    for logY in [False, True]:
        for p in plots: 
            plotting.draw( p, 
                plot_directory = os.path.join( user.plot_directory, args.plot_directory, "inclusive", ("log" if logY else "lin")), 
                yRange = "auto", extensions=["png"], copyIndexPHP=True) 

    syncer.sync()

 


# for reference

# OBJ: TObjArray  TObjArray   An array of objects : 0
# OBJ: TBranch   nPair   nPair/I : 0 at: 0x77994f0
# OBJ: TBranch   Pair_pt Pair_pt[nPair]/F : 0 at: 0x77a2790
# OBJ: TBranch   Pair_eta    Pair_eta[nPair]/F : 0 at: 0x77a4e70
# OBJ: TBranch   Pair_phi    Pair_phi[nPair]/F : 0 at: 0x77a5560
# OBJ: TBranch   Pair_mass   Pair_mass[nPair]/F : 0 at: 0x77a5c50
# OBJ: TBranch   Pair_deltaPhi   Pair_deltaPhi[nPair]/F : 0 at: 0x77a6350
# OBJ: TBranch   Pair_deltaEta   Pair_deltaEta[nPair]/F : 0 at: 0x77a6a50
# OBJ: TBranch   Pair_isC    Pair_isC[nPair]/I : 0 at: 0x77a7150
# OBJ: TBranch   Pair_isS    Pair_isS[nPair]/I : 0 at: 0x77a7840
# OBJ: TBranch   Pair_tp_pt  Pair_tp_pt[nPair]/F : 0 at: 0x77a7f30
# OBJ: TBranch   Pair_tp_eta Pair_tp_eta[nPair]/F : 0 at: 0x77a8630
# OBJ: TBranch   Pair_tp_phi Pair_tp_phi[nPair]/F : 0 at: 0x77a8d30
# OBJ: TBranch   Pair_tm_pt  Pair_tm_pt[nPair]/F : 0 at: 0x77a9430
# OBJ: TBranch   Pair_tm_eta Pair_tm_eta[nPair]/F : 0 at: 0x77a9b30
# OBJ: TBranch   Pair_tm_phi Pair_tm_phi[nPair]/F : 0 at: 0x77aa230
# OBJ: TBranch   Pair_tp_charge  Pair_tp_charge[nPair]/I : 0 at: 0x77aa930
# OBJ: TBranch   Pair_tp_index   Pair_tp_index[nPair]/I : 0 at: 0x77ab030
# OBJ: TBranch   Pair_tm_charge  Pair_tm_charge[nPair]/I : 0 at: 0x77ab730
# OBJ: TBranch   Pair_tm_index   Pair_tm_index[nPair]/I : 0 at: 0x77abe30
# OBJ: TBranch   Pair_C_x    Pair_C_x[nPair]/F : 0 at: 0x77ac530
# OBJ: TBranch   Pair_C_y    Pair_C_y[nPair]/F : 0 at: 0x77acc20
# OBJ: TBranch   Pair_C_R    Pair_C_R[nPair]/F : 0 at: 0x77ad310
# OBJ: TBranch   Pair_C_phi  Pair_C_phi[nPair]/F : 0 at: 0x77ada00
# OBJ: TBranch   evt evt/l : 0 at: 0x77ae100
# OBJ: TBranch   run run/I : 0 at: 0x77b06d0
# OBJ: TBranch   lumi    lumi/I : 0 at: 0x77b0c60
# OBJ: TBranch   Jet_pt  Jet_pt/F : 0 at: 0x77b11f0
# OBJ: TBranch   Jet_eta Jet_eta/F : 0 at: 0x77b1780
# OBJ: TBranch   Jet_phi Jet_phi/F : 0 at: 0x77b1d10
# OBJ: TBranch   Jet_nTrack  Jet_nTrack/I : 0 at: 0x77b22a0
# OBJ: TBranch   Z_pt    Z_pt/F : 0 at: 0x77b2830
# OBJ: TBranch   Z_eta   Z_eta/F : 0 at: 0x77b2dc0
# OBJ: TBranch   Z_phi   Z_phi/F : 0 at: 0x77b3350
# OBJ: TBranch   Z_mass  Z_mass/F : 0 at: 0x77b38e0
# OBJ: TBranch   Z_l_pdgId   Z_l_pdgId/I : 0 at: 0x77b3e70
# OBJ: TBranch   nTrack  nTrack/I : 0 at: 0x77b4400
# OBJ: TBranch   Track_pt    Track_pt[nTrack]/F : 0 at: 0x77b4990
# OBJ: TBranch   Track_eta   Track_eta[nTrack]/F : 0 at: 0x77b5040
# OBJ: TBranch   Track_phi   Track_phi[nTrack]/F : 0 at: 0x77b56f0
# OBJ: TBranch   Track_charge    Track_charge[nTrack]/I : 0 at: 0x77b5da0
# OBJ: TBranch   Track_pdgId Track_pdgId[nTrack]/I : 0 at: 0x77b6450
# OBJ: TBranch   Track_index Track_index[nTrack]/I : 0 at: 0x77b6b00
