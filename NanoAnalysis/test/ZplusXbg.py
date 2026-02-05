#!/usr/bin/env python3

from __future__ import print_function
import os
import shutil
import math
import ROOT
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from ZZAnalysis.NanoAnalysis.tools import getLeptons, get_genEventSumw

pathDir = "/eos/home-a/atamigio/ZZ_VBS_Analysis/Productions/PROD_samplesNano_2022_Data_c10cce63_22Gen26/chunkHadded" # 2022EE_MC production
# pathMC = "/eos/home-a/atamigio/ZZ_VBS_Analysis/Productions/PROD_samplesNano_2022_MC_c10cce63_09Dic25/chunkHadded" # 2022_MC production
# pathMC = "/eos/home-a/atamigio/ZZ_VBS_Analysis/Productions/PROD_samplesNano_VBS2022_MC_c10cce63_16Dic25_2/chunkHadded" # VBS 2022_MC production
# pathMC = "/eos/home-a/atamigio/ZZ_VBS_Analysis/Productions/PROD_samplesNano_VBS2022EE_MC_c10cce63_17Dic25_2/chunkHadded" # VBS 2022EE_MC production

def HaddFiles():
    pathROOTfile = pathDir + "/ZZ4lAnalysis.root"
    print(pathROOTfile)

    for i in range(1,11):
        dynamicIso = 0.15*i
        print("Isolation = " + str(dynamicIso))

        f = ROOT.TFile.Open(pathROOTfile)
        print("ROOT file opened")

        event = f.Events
        event.SetBranchStatus("*", 0)
        event.SetBranchStatus("run", 1)
        event.SetBranchStatus("luminosityBlock", 1)
        event.SetBranchStatus("Muon_pfRelIso03FsrCorr", 1)
        event.SetBranchStatus("Electron_pfRelIso03FsrCorr", 1)
        event.SetBranchStatus("*ZZCand_Z2l1Idx", 1)
        event.SetBranchStatus("*ZZCand_Z2l2Idx", 1)
        event.SetBranchStatus("*ZLLCand_Z2l1Idx", 1)
        event.SetBranchStatus("*ZLLCand_Z2l2Idx", 1)
        event.SetBranchStatus("bestCandIdx", 1)
        event.SetBranchStatus("HLT_passZZ4l", 1)
        event.SetBranchStatus("*ZLLbestSSIdx*", 1)
        nEntries = event.GetEntries()

        isMC = False
        if isMC : event.SetBranchStatus("overallEventWeight",1)

        iEntry= 0

        isoSignal = 0
        invIsoSignal = 0
        invIsoSSEvents = 0
        isoSSEvents = 0

        while iEntry<nEntries and event.GetEntry(iEntry):
            iEntry+=1

            rnd = random.randint(1,10)

            if (rnd == 1):
                bestCandIdx = event.bestCandIdx
                ZZ_Z2l1Idx = event.ZZCand_Z2l1Idx
                ZZ_Z2l2Idx = event.ZZCand_Z2l2Idx
                ele_relIso = event.Electron_pfRelIso03FsrCorr
                muon_relIso = event.Muon_pfRelIso03FsrCorr
                ZLLbestSSIdx = event.ZLLbestSSIdx
                ZLL_Z2l1Idx = event.ZLLCand_Z2l1Idx
                ZLL_Z2l2Idx = event.ZLLCand_Z2l2Idx
                pass_HLT_ZZ4l = event.HLT_passZZ4l

                lepton_pfRelIso03FsrCorr = list(ele_relIso) + list(muon_relIso)

                if(ZLLbestSSIdx >= 0):
                    if(lepton_pfRelIso03FsrCorr[ZLL_Z2l1Idx[ZLLbestSSIdx]] < dynamicIso and lepton_pfRelIso03FsrCorr[ZLL_Z2l2Idx[ZLLbestSSIdx]] < dynamicIso):
                        isoSSEvents += 1.
                        #print("num entry = " + str(iEntry))
                        #print("SS + Iso = " + str(isoSSEvents))
                    else:
                        invIsoSSEvents += 1.
                        #print("num entry = " + str(iEntry))
                        #print("SS + inverted Iso = " + str(invIsoSSEvents))

                if(bestCandIdx != -1 and event.HLT_passZZ4l):
                    if(lepton_pfRelIso03FsrCorr[ZZ_Z2l1Idx[bestCandIdx]] < dynamicIso and lepton_pfRelIso03FsrCorr[ZZ_Z2l2Idx[bestCandIdx]] < dynamicIso):
                        isoSignal += 1.
                        #print("Signal + Iso = " + str(isoSignal))
                    else:
                        invIsoSignal += 1.
                        #print("Signal + inverted Iso = " + str(invIsoSignal))

        f.Close()
        print("ROOT file closed")
        print("Signal + Iso = " + str(isoSignal))
        print("Signal + inverted Iso = " + str(invIsoSignal))
        print("SS + Iso = " + str(isoSSEvents))
        print("SS + inverted Iso = " + str(invIsoSSEvents))

if __name__ == '__main__':
    HaddFiles()
