#!/usr/bin/env python3

from __future__ import print_function
import os
import shutil
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from ZZAnalysis.NanoAnalysis.tools import getLeptons, get_genEventSumw

pathMC = "/eos/home-a/atamigio/ZZ_VBS_Analysis/Productions/PROD_samplesNano_2022EE_MC_c10cce63_18Dic25/chunkHadded" # 2022EE_MC production
# pathMC = "/eos/home-a/atamigio/ZZ_VBS_Analysis/Productions/PROD_samplesNano_2022_MC_c10cce63_09Dic25/chunkHadded" # 2022_MC production
# pathMC = "/eos/home-a/atamigio/ZZ_VBS_Analysis/Productions/PROD_samplesNano_VBS2022_MC_c10cce63_16Dic25_2/chunkHadded" # VBS 2022_MC production
# pathMC = "/eos/home-a/atamigio/ZZ_VBS_Analysis/Productions/PROD_samplesNano_VBS2022EE_MC_c10cce63_17Dic25_2/chunkHadded" # VBS 2022EE_MC production



maxEntriesPerSample = None
lumi_2022EE = 26.6717 #/fb
lumi_2022   = 7.9804  #/fb

N_events = []

def HaddFiles():
    for subdir in sorted(os.listdir(pathMC)):
        subdirpath = pathMC + "/" + subdir + "/ZZ4lAnalysis.root"

        f = ROOT.TFile.Open(subdirpath)

        event = f.Events
        event.SetBranchStatus("*", 0)
        event.SetBranchStatus("run", 1)
        event.SetBranchStatus("luminosityBlock", 1)
        event.SetBranchStatus("*Muon*", 1)
        event.SetBranchStatus("*Electron*", 1)
        event.SetBranchStatus("*ZZCand*", 1)
        event.SetBranchStatus("bestCandIdx", 1)
        event.SetBranchStatus("HLT_passZZ4l", 1)
        nEntries = event.GetEntries() 

        isMC = True
        event.SetBranchStatus("overallEventWeight",1)

        # Get sum of weights
        genEventSumw = get_genEventSumw(f, maxEntriesPerSample)

        iEntry=0
        n_exp=0
        sum_overallEventW=0
        printEntries=max(5000,nEntries/10)
        while iEntry<nEntries and event.GetEntry(iEntry):
            iEntry+=1
            if iEntry%printEntries == 0 : print("Processing", iEntry)

            bestCandIdx = event.bestCandIdx
 
            # Check that the event contains a selected candidate, and that
            # passes the required triggers (which is necessary for samples
            # processed with TRIGPASSTHROUGH=True)
            if(bestCandIdx != -1 and event.HLT_passZZ4l): 
                weight = 1.
                ZZs = Collection(event, 'ZZCand')
                theZZ = ZZs[bestCandIdx]        
                if isMC : weight = (event.overallEventWeight*theZZ.dataMCWeight/genEventSumw)
                m4l=theZZ.mass
                sum_overallEventW += event.overallEventWeight
                n_exp += weight
                #print(event.overallEventWeight)
                #print(weight)

        N_events.append({"name": subdir, "filename": pathMC + "/" + subdir + "/ZZ4lAnalysis.root", "n_expected": n_exp})

        f.Close()

        for item in N_events:
            print("n_expeted " + item["name"] + " = " + str(item["n_expected"]*lumi_2022EE*1000)) # for 2022EE
            #print("n_expeted " + item["name"] + " = " + str(item["n_expected"]*lumi_2022*1000)) # for 2022

        total_bg_n_exp = sum(item["n_expected"] for item in N_events)
        print("total n_expected = " + str(total_bg_n_exp*lumi_2022EE*1000)) # for 2022EE
        #print("total n_expected = " + str(total_bg_n_exp*lumi_2022*1000)) # for 2022

if __name__ == '__main__':
    HaddFiles()
