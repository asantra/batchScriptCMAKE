#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
# Import statements
############################################################################
### from Gauss_options
from Gauss.Configuration import *
### from NoOutput
from Configurables import Gauss
### from MoEDAL_options
from Gaudi.Configuration import *
from Configurables import Gauss
from Configurables import GaudiSequencer, MonopoleTupleAlg, GenTupleAlg
### from MoEDAL_Geometry
from Configurables import GiGaInputStream
from Configurables import GaudiSequencer
### from PGun options
from GaudiKernel import SystemOfUnits
from Configurables import ToolSvc
from Configurables import ParticleGun
from Configurables import MomentumRange
from Configurables import FlatNParticles
from Configurables import EvtGenDecay
from Configurables import LHCbApp

##############################################################################

#-----------------------------------------------------------------------------
# Generator phase
#-----------------------------------------------------------------------------
GaussGen = GenInit("GaussGen")
#
# Set the random numbers - these fix the random seed.
#
GaussGen.FirstEventNumber = FIRST_EVENT_NUMBER
GaussGen.RunNumber        = RUN_NUMBER

# The output is managed below, so we disable the standard Gauss output.
Gauss().OutputType = 'NONE'
Gauss().Histograms = 'NONE'

############################################################################
## Set properties of particles to be generated

## momentum properties
ParticleGun().addTool( MomentumRange )
ParticleGun().ParticleGunTool = "MomentumRange"

## number of particles (default=1)
ParticleGun().addTool( FlatNParticles )
ParticleGun().NumberOfParticlesTool = "FlatNParticles"
ParticleGun().EventType = 52210001


############################################################################
## Add event decay tool (not clear if needed)
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/mu+mu-,fixP=TrkAcc.dec"

## Commented out TrackerAcceptance script as it restricts theta-phi range to LHCb
#from Gaudi.Configuration import *
#importOptions( "$DECFILESROOT/options/TrackersAcceptance.py" )

## Following code is non-theta-phi related code remaining in TrackerAcceptance (unclear if necessary)
from Configurables import GenInit, SimInit, GaudiSequencer
GenInit( "GaussGen" ).PrintFreq = 100
SimInit( "GaussSim" ).PrintFreq = 100


##############################################################################
# Monopole physics
##############################################################################
### ---- the below block is commented out by Arka ------#########
# Set add monopole physics constructor from GaussMonopoles to the GiGa
## physics list.
#giga = GiGa()
#giga.addTool( GiGaPhysListModular("ModularPL") , name="ModularPL" )
#giga.ModularPL.addTool( GiGaPhysConstructorMonopole, name = "GiGaPhysConstructorMonopole" )



############################################################################
## Set add monopole physics constructor from GaussMonopoles to GiGa physics list
#giga = GiGa()
#giga.addTool( GiGaPhysListModular("ModularPL") , name="ModularPL" )
#giga.ModularPL.addTool( GiGaPhysConstructorMonopole, name = "GiGaPhysConstructorMonopole" )

## Add the physics of the monopole and switch off Cherenkov processes
Gauss().PhysicsList = {"Em":'NoCuts', "Hadron":'FTFP_BERT', "GeneralPhys":True, "LHCbPhys":False, "Other":'Monopole'}


############################################################################
## Add the Ntuple writer to the Simulation Monitor

## Kind of a hack, but works
monopoleTupleAlg = MonopoleTupleAlg()
GaudiSequencer("SimMonitor").Members+= [ monopoleTupleAlg ]
genTupleAlg = GenTupleAlg()
GaudiSequencer("GenMonitor").Members+= [ genTupleAlg ]

#############################################################################
### Switch off RICH physics (leave geometry)
#giga.ModularPL.addTool( GiGaPhysConstructorOp,  name = "GiGaPhysConstructorOp"  )
#giga.ModularPL.addTool( GiGaPhysConstructorHpd, name = "GiGaPhysConstructorHpd" )
#giga.ModularPL.GiGaPhysConstructorOp.RichOpticalPhysicsProcessActivate = False
#giga.ModularPL.GiGaPhysConstructorHpd.RichHpdPhysicsProcessActivate = False

## Note that the options and the tags will be used directly from ${GAUSSOPTS}
# Pick beam conditions as set in AppConfig. 
#importOptions("$APPCONFIGOPTS/Gauss/Beam6500GeV-md100-nu1.6.py")
#importOptions("$APPCONFIGOPTS/Gauss/DataType-2015.py")
# Set the database tags using those for Sim08.
#LHCbApp().DDDBtag   = "dddb-20140729"
#LHCbApp().CondDBtag = "sim-20140730-vc-md100"

LHCbApp().DDDBtag   = "MoEDAL-Run2"
LHCbApp().CondDBtag = "sim-20180411-vc-md100"

############################################################################
## Switch on geometry for MoEDAL detectors
geo = GiGaInputStream('Geo')

geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacTankCoverPipes" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacTankCoverHead" ]

## When using tags above or equal to 3.0.0, please activate the VacTankTopFlanges
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacTankTopFlanges" ]

geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/DetectorVacuum" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacuumPump" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VeloDustCover" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/ExtraMaterial" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VacuumManifolds" ]

## When using tags above or equal 3.0.0, please activate : DetectorVacuumHood, SideElectronicCrates, RepeaterBoards, and VeloCables
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/DetectorVacuumHood" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/SideElectronicCrates" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/RepeaterBoards" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/VeloCables" ]

## !! Attention !! : When using tag 4.0.2 or 3.0.0 (Run 2), please activate MMT1, MMT2, MMT3, and NTD2015 and deactivate : MMT2014, and NTDRun1 !!
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT1" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT2" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT3" ]
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/NTD2015" ]
#geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT2014" ]
#geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/NTDRun1" ]

## !! Attention !! : When using tag 4.0.1 or 3.1.0 (Run 1), please activate MMT2014, and NTDRun1 and deactivate : MMT1, MMT2, MMT3, and NTD2015 !!
geo.StreamItems += [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/HCC2015" ]

############################################################################
## Activate MMT, HCC, and NTD sensitive detectors
from Configurables import GetMMTHitsAlg, GetNTDHitsAlg

## !! Attention !! : When using tag 4.0.2 or 3.0.0 (Run 2), please activate MMT1, MMT2, MMT3 and deactivate : MMT2014 !!
getMMTHits = GetMMTHitsAlg("GetMMTHits")
getMMTHits.CollectionName = "MMT/Hits"
getMMTHits.MCHitsLocation = "/Event/MC/MMT/Hits"
getMMTHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT1" ]
#getMMTHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT2014" ]
GaudiSequencer("DetectorsHits").Members += [ getMMTHits ]

getMMTHits = GetMMTHitsAlg("GetMMTHits")
getMMTHits.CollectionName = "MMT/Hits"
getMMTHits.MCHitsLocation = "/Event/MC/MMT/Hits"
getMMTHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT2" ]
GaudiSequencer("DetectorsHits").Members += [ getMMTHits ]

getMMTHits = GetMMTHitsAlg("GetMMTHits")
getMMTHits.CollectionName = "MMT/Hits"
getMMTHits.MCHitsLocation = "/Event/MC/MMT/Hits"
getMMTHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/MMT3" ]
GaudiSequencer("DetectorsHits").Members += [ getMMTHits ]

## !! Attention !! : If using tag 4.0.2 or 3.0.0 (Run 2), please activate NTD2015 and deactivate : NTDRun1 !!
## !! Attention !! : If using tag 4.0.1 or 3.1.0 (Run 1), please activate NTDRun1 and deactivate : NTD2015 !!
getNTDHits = GetNTDHitsAlg("GetNTDHits")
getNTDHits.CollectionName = "NTD/Hits"
getNTDHits.MCHitsLocation = "/Event/MC/NTD/Hits"
getNTDHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/NTD2015" ]
#getNTDHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/NTDRun1" ]
GaudiSequencer("DetectorsHits").Members += [ getNTDHits ]

## Disable NTD hit retrieval when NTDs are disabled in geometry
getNTDHits = GetNTDHitsAlg("GetNTDHits")
getNTDHits.CollectionName = "NTD/Hits"
getNTDHits.MCHitsLocation = "/Event/MC/NTD/Hits"
getNTDHits.Detectors      = [ "/dd/Structure/LHCb/BeforeMagnetRegion/MoEDAL/HCC2015" ]
GaudiSequencer("DetectorsHits").Members += [ getNTDHits ]




##############################################################################
# Define the MoEDAL option variables
##############################################################################

# Define the monopole properties.

## The magnetic monopole PDG ID.
monopole_pdg       = 4110000 #shouldn't coincide with other particles

## The magnetic monopole mass [GeV].
monopole_mass      = MONOPOLE_MASS_GEV # [GeV]

## The magnetic monopole electric charge [e].
monopole_elcharge  = MONOPOLE_ELECTRIC_CHARGE # [e]

## The magnetic monopole magnetic charge [g_D].
monopole_magcharge = MONOPOLE_MAGNETIC_CHARGE # [g_D]

# Define the monopole behavior.

## Use fields?
monopole_usefields = True

## The minimum beta for the magnetic monopoles.
monopole_minbeta   = 1.0e-3

## nint/step:  q =    0,   1,   2,   3,   4,   5,   6

nintpersteparray = [  1,  10,  20,  40,  80, 160, 320]

nintperstep = nintpersteparray[ int(monopole_magcharge) ]


##############################################################################
# Gauss controls
##############################################################################

## The number of events to process.
LHCbApp().EvtMax = NUMBER_OF_EVENTS

# Define input file in LHE xml format
# This should have been specified in cfg_lhe.py file.
#Generation().Special.ReadLHEfileProduction.InputFile = "events.lhe"

##############################################################################
# Output files
##############################################################################

## The output filename.
MonopoleTupleAlg().OutputNtupleFilename = "MONOPOLE_DATA_ROOT"

## Reading the NTD hits
MonopoleTupleAlg().ReadNTDHits = True

## The generator information output filename.
GenTupleAlg().OutputNtupleFilename = "GEN_DATA_ROOT"


## wide coverage
ParticleGun().MomentumRange.ThetaMin = 0.0        *SystemOfUnits.rad
ParticleGun().MomentumRange.ThetaMax = 3.14159265 *SystemOfUnits.rad
ParticleGun().MomentumRange.PhiMin = 0.0          *SystemOfUnits.rad
ParticleGun().MomentumRange.PhiMax = 2*3.14159265 *SystemOfUnits.rad

# momentum range
ParticleGun().MomentumRange.MomentumMin = 0 *SystemOfUnits.GeV
ParticleGun().MomentumRange.MomentumMax = 1000 *SystemOfUnits.GeV

## number of particles
ParticleGun().FlatNParticles.MinNParticles = 1
ParticleGun().FlatNParticles.MaxNParticles = 1

## type of particle
ParticleGun().MomentumRange.PdgCodes = [ monopole_pdg ] # for anti-monopole use -monopole_pdg


############################################################################
## Add monopole information to Ntuple writer
## (should retrieve particle information from ParticlePropertySvc, but no magnetic charge field available)
MonopoleTupleAlg().MonopolePdgs  = [ monopole_pdg,       -monopole_pdg       ]
MonopoleTupleAlg().MonopoleQmags = [ monopole_magcharge, -monopole_magcharge ]
GenTupleAlg().MonopolePdgs  = [ monopole_pdg,       -monopole_pdg       ]
GenTupleAlg().MonopoleQmags = [ monopole_magcharge, -monopole_magcharge ]


############################################################################
## Patch ParticlePropertySvc to include monopole details
## not yet entirely clear what uses this and what uses the (i.e. mass) definitions in GiGaPhysConstructorMonopole
##   - Either the simulation or generation phases in Gauss definitely use these values
ParticlePropertyFile = open("ParticlePropertySvc_Monopole.txt", 'w')
ParticlePropertyFile.write("\# ParticlePropertySvc file automatically generated by MoEDAL_options.py\n")
ParticlePropertyFile.write("PARTICLE")

ParticlePropertyFile.write('\n')
ParticlePropertyFile.write('magnetic_monopole')           # PARTICLE NAME
ParticlePropertyFile.write('\t' + str(monopole_pdg))      # GEANTID
ParticlePropertyFile.write('\t' + str(monopole_pdg))      # PDGID
ParticlePropertyFile.write('\t' + str(monopole_elcharge)) # CHARGE
ParticlePropertyFile.write('\t' + str(monopole_mass))     # MASS(GeV)
ParticlePropertyFile.write('\t-1')                        # TLIFE(s)
ParticlePropertyFile.write('\tmagnetic_monopole')         # EVTGENNAME
ParticlePropertyFile.write('\t' + str(monopole_pdg))      # PYTHIAID
ParticlePropertyFile.write('\t0.00000000')                # MAXWIDTH

ParticlePropertyFile.write('\n')
ParticlePropertyFile.write('antimagnetic_monopole')        # PARTICLE NAME
ParticlePropertyFile.write('\t' + str(-monopole_pdg))      # GEANTID
ParticlePropertyFile.write('\t' + str(-monopole_pdg))      # PDGID
ParticlePropertyFile.write('\t' + str(-monopole_elcharge)) # CHARGE
ParticlePropertyFile.write('\t' + str(monopole_mass))      # MASS(GeV)
ParticlePropertyFile.write('\t-1')                         # TLIFE(s)
ParticlePropertyFile.write('\tantimagnetic_monopole')      # EVTGENNAME
ParticlePropertyFile.write('\t' + str(-monopole_pdg))      # PYTHIAID
ParticlePropertyFile.write('\t0.00000000')                 # MAXWIDTH

LHCb__ParticlePropertySvc().OtherFiles = [ "ParticlePropertySvc_Monopole.txt" ]


