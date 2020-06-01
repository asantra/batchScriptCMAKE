#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#=============================================================================
# Make Ganga jobs for MoEDAL simulations - LHE running on DIRAC
#=============================================================================
#

# For the operating system stuff.
import os

# For copying files in Python.
from shutil import copyfile

from subprocess import Popen, PIPE


def replace_text(filename, stringtomatch, stringtoreplace):
    import fileinput
    for line in fileinput.input(filename, inplace = 1):
        print line.replace(stringtomatch, stringtoreplace),

print("*")
print("* Submitting the MoEDAL simulation (LHE) file to DIRAC")
print("*")
print("*")

run_number  = 1082

## The basename of the LHE events file.
lhe_file_basename = "unweighted_events.lhe"

## The base LHE file directory.
lfn_path = '/vo.moedal.org/sim/13TEVYY/FilesByArka/SecondTryMarch22/MoEDAL_LHEFiles' ### grid path
#lfn_path = '/eos/user/a/asantra/MadGraphLHEFiles'  ### local path

## The geometry DB file location in CVMFS.
geometry_db_file_location = "/cvmfs/moedal.cern.ch/Gauss/Geometry/3-0-0"
#geometry_db_file_location = "/cvmfs/moedal.cern.ch/Gauss/Geometry/2-2-0"

## The magnetic monopole electric charge [e].
monopole_electric_charge = 0

## The Centre-of-Mass energy.
com_energy = '13TeV'

## The magnetic monopole spin.

outputJobId  = open('SubmittedJobId.txt', 'w')
outputFailed = open('FailedJobId.txt', 'w')

counter = 0 




############## modified by Arka  #####################


betaName                  = ['betaIndependent'] ### , 'betaDependent'

magnetic_monopole_spin    = ['SpinZero'] ### , 'SpinHalf', 'SpinOne'

monopole_magnetic_charges = ['q10'] ### , 'q20', 'q30', 'q40', 'q50', 'q60'

monopole_masses           = {200: 'run_01'}

#500: 'run_02',  \
                             #1000: 'run_03', \
                             #1500: 'run_04', \
                             #2000: 'run_05', \
                             #2500: 'run_06', \
                             #3000: 'run_07', \
                             #4000: 'run_08', \
                             #5000: 'run_09', \
                             #6000: 'run_10'
                             

## A dictionary of geometry names to geometry files .
geometries = {'default':'geometry_default.db'}


shortJobs = False
nOfJobs   = 1
for n in xrange(0, len(betaName)):
    beta = betaName[n]
    
    if n == 0:
        prefix = 'No'
    else:
        prefix = ''
        
    if(shortJobs and (counter > nOfJobs)):
        break
    ### loop over the spins
    for k in xrange(0, len(magnetic_monopole_spin)):
        spin = magnetic_monopole_spin[k]
        if(shortJobs and (counter > nOfJobs)):
           break
        ### loop over the charges
        for i in xrange(0, len(monopole_magnetic_charges)):
            charge = monopole_magnetic_charges[i]
            if(shortJobs and (counter > nOfJobs)):
                break
            ### loop over the monopole masses
            for keyMass in monopole_masses:
                if(shortJobs and (counter > nOfJobs)):
                    break
                ### loop over the different geometries
                for keyGeom in geometries:
                    if(shortJobs and (counter > nOfJobs)):
                        break
                        
                    run = monopole_masses[keyMass]
                    ## The batch name.
                    batch_name = 'myRun_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom
                    
                    ##/eos/user/a/asantra/MadGraphLHEFiles/betaIndependent/SpinZero/q10/run_10
                    #if beta != "betaDependent": continue
                    #if spin != "SpinHalf"     : continue
                    #if charge != "q10"        : continue
                    #if run   != "run_06"      : continue
                    # Global configuration variables.

                    ## The first event number.
                    first_event_number = 1

                    ## The number of events to run.
                    number_of_events = 10000
                    

                    ## The monopole mass [GeV]
                    monopole_mass = keyMass

                    ## The LHE generation run name.
                    #lhe_run_name = 'run_01'
                    lhe_run_name   = 'RunName_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom  ### modified by Arka
                    outputmonopole = 'MonopoleData_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom+'.root'
                    outputgen      = 'GenData_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom+'.root'
                    outputlog      = 'log.run.'+beta+'.'+spin+'.'+charge+'.'+run+'.'+keyGeom+'.txt'
                    

                    ## The monopole magnetic charge [q_D].
                    monopole_magnetic_charge = i+1

                    ## The magnetic charge label used in the file name.
                    monopole_magnetic_charge_label = charge

                    ## The geometry name.
                    geometry_name = keyGeom

                    ## The geometry filename.
                    geometry_filename = geometries[keyGeom]

                    # Shorten the variable names for convenience...
                    com      = com_energy
                    geo      = geometry_name
                    mag_chrg = monopole_magnetic_charge_label
                    mass     = "m%d" % (monopole_mass)
                    #spin     = magnetic_monopole_spin #### spin was defined before

                    ## The job name.
                    job_name = "%s_PhotonFusion_%s" % (com, batch_name)

                    ## The name of the configuration.
                    cfg_name = "cfg_" + job_name
                    #
                    

                    ## The path of the configuration file.
                    cfg_path = cfg_name + ".py"

                    ## The location of the LHE file on the DIRAC File Catalog.

                    lhe_location = '%s/%s/%s/%s/%s/unweighted_events.lhe' % (lfn_path, beta, spin, charge, run) ## done by Arka, for Dirac running, make sure the lfn path is pointed to right directory
                    #lhe_location = lfn_path+'/unweighted_events.lhe' ## for local running
                    
                    # Add the LFN to the inputfiles list (DiracFile).
                    
                    cfg_ganga_lhe_name = 'cfg_ganga_lhe_run_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom+'.py'
                    
                    sh_run_ganga_name  = 'run_lhe_v49r8_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom+'.sh'

                    # Create a copy of the configuration file from the template.
                    copyfile('configuration_LHE_TEMPLATE.py', cfg_path)

                    # Replace the first event number variable.
                    replace_text(cfg_path, "FIRST_EVENT_NUMBER", "%d" % (first_event_number))

                    # Replace the run number variable.
                    replace_text(cfg_path, "RUN_NUMBER", "%d" % (run_number))

                    # Replace the LHE file basename.
                    replace_text(cfg_path, "LHE_FILE_BASENAME", lhe_file_basename)

                    replace_text(cfg_path, "GEOMETRY_DB_FILE_LOCATION", geometry_db_file_location)

                    replace_text(cfg_path, "GEOMETRY_DB_FILENAME", geometry_filename)

                    replace_text(cfg_path, "MONOPOLE_MASS_GEV", "%d" % (monopole_mass))

                    replace_text(cfg_path, "MONOPOLE_ELECTRIC_CHARGE", "%d" % (monopole_electric_charge))

                    replace_text(cfg_path, "MONOPOLE_MAGNETIC_CHARGE", "%d" % (monopole_magnetic_charge))

                    replace_text(cfg_path, "NUMBER_OF_EVENTS", "%d" % (number_of_events))
                    
                    replace_text(cfg_path, "MONOPOLE_DATA_ROOT", "%s" % (outputmonopole))
                    
                    replace_text(cfg_path, "GEN_DATA_ROOT", "%s" % (outputgen))

                    # Add config to the inputfiles list (LocalFile).
                    
                    # Create a copy of the configuration file to use in the job.
                    copyfile(cfg_path, cfg_ganga_lhe_name)
                    
                    # Create the run_lhe_v49r8.sh file which will run the gaudirun 
                    
                    copyfile('run_lhe_v49r8_TEMPLATE.sh', sh_run_ganga_name)
                    
                    replace_text(sh_run_ganga_name, "CFGNAME", "%s" % (cfg_ganga_lhe_name))
                    
                    replace_text(sh_run_ganga_name, "LOGNAME", "%s" % (outputlog))
                    
                    replace_text(sh_run_ganga_name, "ROOTFILE", "%s" % (outputmonopole))
                    
                    os.chmod(sh_run_ganga_name, 0755)
                    
                    
                    # Create the jdl file which will send job to Dirac
                    
                    jdl_name = 'JDLforJob_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom+'.jdl'
                    
                    
                    copyfile('JDLforJobMASTER.jdl', jdl_name)
                    
                    replace_text(jdl_name, "LFNDATA", "%s" % ('Job_'+beta+'_'+spin+'_'+charge+'_'+run+'_'+keyGeom))
                    
                    replace_text(jdl_name, "SHNAME", "%s" % (sh_run_ganga_name))
                    
                    replace_text(jdl_name, "CFGNAME", "%s" % (cfg_path))
                    
                    replace_text(jdl_name, "GANGANAME", "%s" % (cfg_ganga_lhe_name))
                    
                    replace_text(jdl_name, "DATA", "%s" % ('LFN:'+lhe_location))
                    
                    
                    print("*")
                    print("* Configuration filename: '%s'" % (cfg_name))
                    print("* lhe_location: '%s'" % (lhe_location))
                    print("* cfg name    : '%s'" % (cfg_ganga_lhe_name))
                    print("* sh_name     : '%s'"% (sh_run_ganga_name))
                    print("* jdl_name     : '%s'"% (jdl_name))
                    
                    
                    process = Popen('dirac-wms-job-submit '+jdl_name, shell=True, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = process.communicate()
                    print 'out: ', stdout
                    print 'err: ', stderr
                    
                    if not stdout:
                        print 'This job failed to submit: ', jdl_name
                        outputFailed.write(jdl_name+'\n')
                    else:
                        print 'This job was submitted: ', jdl_name
                        jobDiracId = stdout.rstrip().split()[2] 
                        outputJobId.write(jobDiracId+'\t'+jdl_name+'\n')
                    
                    counter = counter+1
                    

                    
outputJobId.close()
outputFailed.close()




