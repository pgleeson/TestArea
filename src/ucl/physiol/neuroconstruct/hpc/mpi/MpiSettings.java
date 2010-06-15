/**
 *  neuroConstruct
 *  Software for developing large scale 3D networks of biologically realistic neurons
 * 
 *  Copyright (c) 2009 Padraig Gleeson
 *  UCL Department of Neuroscience, Physiology and Pharmacology
 *
 *  Development of this software was made possible with funding from the
 *  Medical Research Council and the Wellcome Trust
 *  
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *  
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.

 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

package ucl.physiol.neuroconstruct.hpc.mpi;

import java.io.File;
import java.util.*;

import ucl.physiol.neuroconstruct.utils.ClassLogger;


/**
 * Support for interacting with MPI platform
 *
 *  *** STILL IN DEVELOPMENT! SUBJECT TO CHANGE WITHOUT NOTICE! ***
 *
 * @author Padraig Gleeson
 *  
 */


public class MpiSettings
{
    ClassLogger logger = new ClassLogger("MpiSettings");
    
    public static final String MPICH_V1 = "MPICH v1.*";
    public static final String MPICH_V2 = "MPICH v2.*";
    public static final String OPENMPI_V2 = "OPENMPI v2.*";

    public static final String DEFAULT_MPI_VERSION = MPICH_V1;
    
    public static final String LOCALHOST = "localhost";

    /*
     * To run on the local machine
     */
    public static final String LOCAL_SERIAL = "Local machine, serial mode";
    public static final String LOCAL_2PROC = "Local machine (2p)";
    public static final String LOCAL_3PROC = "Local machine (3p)";
    public static final String LOCAL_4PROC = "Local machine (4p)";

    /*
     * To run on a remote machine and execute directly, i.e. no queue
     * There must be automatic ssh login to this machine
     */
    public static final String CLUSTER_1PROC = "Cluster (1p)";
    public static final String CLUSTER_2PROC = "Cluster (1 x 2p)";
    public static final String CLUSTER_4PROC = "Cluster (1 x 4p)";

    /*
     * To run on a remote machine, jobs set running using a submit script.
     * Note the UCL Legion cluster is not on offer to neuroConstruct users
     * outside UCL...
     */
    public static final String LEGION_1PROC = "Legion (1 x 1p)";
    public static final String LEGION_2PROC = "Legion (1 x 2p)";
    public static final String LEGION_4PROC = "Legion (1 x 4p)";
    public static final String LEGION_8PROC = "Legion (2 x 4p)";
    public static final String LEGION_16PROC = "Legion (4 x 4p)";
    public static final String LEGION_24PROC = "Legion (6 x 4p)";
    public static final String LEGION_32PROC = "Legion (8 x 4p)";
    
    public static final String LEGION_40PROC = "Legion (10 x 4p)";

    public static final String LEGION_48PROC = "Legion (12 x 4p)";
    public static final String LEGION_64PROC = "Legion (16 x 4p)";
    public static final String LEGION_80PROC = "Legion (20 x 4p)";
    public static final String LEGION_96PROC = "Legion (24 x 4p)";
    public static final String LEGION_112PROC = "Legion (28 x 4p)";
    public static final String LEGION_128PROC = "Legion (32 x 4p)";
    public static final String LEGION_256PROC = "Legion (64 x 4p)";


    /*
     * Matthau & Lemmon are consist of 10x and 20x 8 core machines
     */

    public static final String MATTHAU = "matthau-5-";
    public static final String LEMMON = "lemmon-5-";

    
    public static final String MACHINE_FILE = "machinesToUse";
    
    
    /*
     * Index of "preferred" configuration in configurations
     */
    public static int prefConfig = 0;
    
    private ArrayList<MpiConfiguration> configurations = new ArrayList<MpiConfiguration>();

    public MpiSettings()
    {

        Hashtable<String, String> simulatorExecutables = new Hashtable<String, String>();
        Hashtable<String, String> simulatorExecutablesML = new Hashtable<String, String>();

        simulatorExecutables.put("NEURON", "/home/ucgbpgl/nrnmpi/x86_64/bin/nrniv");
        simulatorExecutables.put("GENESIS", "/home/ucgbpgl/gen23/genesis");
        simulatorExecutables.put("MOOSE", "/home/ucgbpgl/moose/moose");

        simulatorExecutablesML.put("NEURON", "/share/apps/neuro/nrn62_pympi/x86_64/bin/nrniv");
        simulatorExecutablesML.put("MOOSE", "/share/apps/neuro/moose");

        // This is a 4 processor Linux machine in our lab. Auto ssh login is enabled to it from the
        // machine on which neuroConstruct is running. Jobs are set running directly on this machine
        RemoteLogin directLogin = new RemoteLogin("192.168.15.70",
                                                  "padraig",
                                                  "/home/padraig/nCsims",
                                                  simulatorExecutables);

        // Login node for Matthau/Lemmon cluster
        RemoteLogin matlemLogin = new RemoteLogin("128.16.14.177",
                                                  "ucgbpgl",
                                                  "/home/ucgbpgl/nCsims",
                                                  simulatorExecutablesML);

        // Legion is the UCL supercomputing cluster. Legion operates the Torque batch queueing system
        // and the Moab scheduler, i.e. jobs aren't eecuted directly, but submitted to a queue and will
        // be run when the requested resources are available.
        RemoteLogin legionLogin = new RemoteLogin("legion.rc.ucl.ac.uk",
                                                  "ucgbpgl",
                                                  "/shared/scratch/ucgbpgl/nCsims",
                                                  simulatorExecutables);

        RemoteLogin legionSerialLogin = new RemoteLogin("legion.rc.ucl.ac.uk",
                                                  "ucgbpgl",
                                                  "/shared/scratch/ucgbpgl/nCsims",
                                                  simulatorExecutables);

        //QueueInfo legionQueueCvos = new QueueInfo(6, "ucl/NeuroSci/neuroconst", "cvos-launcher");

        QueueInfo legionQueue = new QueueInfo(6, "ucl/NeuroSci/neuroconst", "cvos-launcher");


        if (getMpiConfiguration(LOCAL_SERIAL)==null)
        {
            MpiConfiguration def = new MpiConfiguration(LOCAL_SERIAL);
            def.getHostList().add(new MpiHost(LOCALHOST, 1, 1));
            configurations.add(def);
        }


        if (getMpiConfiguration(LOCAL_2PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LOCAL_2PROC);
            p.getHostList().add(new MpiHost(LOCALHOST,2, 1));
            configurations.add(p);
        }
        if (getMpiConfiguration(LOCAL_3PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LOCAL_3PROC);
            p.getHostList().add(new MpiHost(LOCALHOST,3, 1));
            configurations.add(p);
        }
        if (getMpiConfiguration(LOCAL_4PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LOCAL_4PROC);
            p.getHostList().add(new MpiHost(LOCALHOST,4, 1));
            configurations.add(p);
        }
/*
        if (getMpiConfiguration(multiConfig)==null)
        {
            MpiConfiguration p = new MpiConfiguration(multiConfig);
            //p.getHostList().add(new MpiHost("padraigneuro", 1, 1));
            p.getHostList().add(new MpiHost("eriugena",4, 1));
            p.getHostList().add(new MpiHost("bernal", 4, 1));
            configurations.add(p);
        }*/

        if (getMpiConfiguration(CLUSTER_1PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(CLUSTER_1PROC);

            p.getHostList().add(new MpiHost(directLogin.getHostname(),1, 1));
            p.setRemoteLogin(directLogin);
            configurations.add(p);
        }

        if (getMpiConfiguration(CLUSTER_2PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(CLUSTER_2PROC);

            p.getHostList().add(new MpiHost(directLogin.getHostname(),2, 1));
            p.setRemoteLogin(directLogin);
            configurations.add(p);
        }

        if (getMpiConfiguration(CLUSTER_4PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(CLUSTER_4PROC);

            p.getHostList().add(new MpiHost(directLogin.getHostname(),4, 1));
            p.setRemoteLogin(directLogin);
            configurations.add(p);
        }


        if (getMpiConfiguration(LEGION_1PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_1PROC);

            p.getHostList().add(new MpiHost("localhost", 1, 1));
            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }

        if (getMpiConfiguration(LEGION_2PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_2PROC);

            p.getHostList().add(new MpiHost("localhost", 2, 1));
            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }

        if (getMpiConfiguration(LEGION_4PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_4PROC);

            p.getHostList().add(new MpiHost("localhost",4, 1));
            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }


        if (getMpiConfiguration(LEGION_8PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_8PROC);

            for(int i=0;i<2;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }


        if (getMpiConfiguration(LEGION_16PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_16PROC);

            for(int i=0;i<4;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }

        if (getMpiConfiguration(LEGION_24PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_24PROC);

            for(int i=0;i<6;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }


        if (getMpiConfiguration(LEGION_32PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_32PROC);

            for(int i=0;i<8;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }


        if (getMpiConfiguration(LEGION_40PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_40PROC);

            for(int i=0;i<10;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }


        if (getMpiConfiguration(LEGION_48PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_48PROC);

            for(int i=0;i<12;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }
        if (getMpiConfiguration(LEGION_64PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_64PROC);

            for(int i=0;i<16;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }
        if (getMpiConfiguration(LEGION_80PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_80PROC);

            for(int i=0;i<20;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }
        if (getMpiConfiguration(LEGION_96PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_96PROC);

            for(int i=0;i<24;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }
        if (getMpiConfiguration(LEGION_112PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_112PROC);

            for(int i=0;i<28;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }
        if (getMpiConfiguration(LEGION_128PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_128PROC);

            for(int i=0;i<32;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }
        if (getMpiConfiguration(LEGION_256PROC)==null)
        {
            MpiConfiguration p = new MpiConfiguration(LEGION_256PROC);

            for(int i=0;i<64;i++)
                p.getHostList().add(new MpiHost("node"+i,4, 1));

            p.setRemoteLogin(legionLogin);
            p.setQueueInfo(legionQueue);
            configurations.add(p);
        }


        int[] lemNodes = new int[]{14,15};

        int[] lemProcs = new int[]{4,8};


        for (int nodeNum: lemNodes)
        {
            for (int totalProcs: lemProcs)
            {
                String name = "Lemmon_"+nodeNum+"_"+totalProcs+"PROCS";

                if (getMpiConfiguration(name)==null)
                {
                    MpiConfiguration p = new MpiConfiguration(name);

                    p.getHostList().add(new MpiHost(LEMMON+nodeNum, totalProcs, 1));

                    p.setRemoteLogin(matlemLogin);
                    p.setMpiVersion(MpiSettings.OPENMPI_V2);
                    p.setUseScp(true);
                    configurations.add(p);

                }
            }
        }

        int[] mattNodes = new int[]{2,3, 4, 5, 6};

        int[] mattProcs = new int[]{4,8};


        for (int nodeNum: mattNodes)
        {
            for (int totalProcs: mattProcs)
            {
                String name = "Matthau_"+nodeNum+"_"+totalProcs+"PROCS";

                if (getMpiConfiguration(name)==null)
                {
                    MpiConfiguration p = new MpiConfiguration(name);

                    p.getHostList().add(new MpiHost(MATTHAU+nodeNum, totalProcs, 1));

                    p.setRemoteLogin(matlemLogin);
                    p.setMpiVersion(MpiSettings.OPENMPI_V2);
                    p.setUseScp(true);
                    configurations.add(p);

                }
            }
        }

        String name_16 = "Matthau_Lemmon_Test_16";
        MpiConfiguration p_16 = new MpiConfiguration(name_16);
        p_16.getHostList().add(new MpiHost(MATTHAU+5, 8, 1));
        p_16.getHostList().add(new MpiHost(LEMMON+14, 8, 1));

        p_16.setRemoteLogin(matlemLogin);
        p_16.setMpiVersion(MpiSettings.OPENMPI_V2);
        p_16.setUseScp(true);
        configurations.add(p_16);

        String name_56l = "Matthau_Lemmon_Test_56l";
        MpiConfiguration p_56l = new MpiConfiguration(name_56l);

        p_56l.getHostList().add(new MpiHost(LEMMON+10, 8, 1));
        p_56l.getHostList().add(new MpiHost(LEMMON+11, 8, 1));
        p_56l.getHostList().add(new MpiHost(LEMMON+12, 8, 1));
        p_56l.getHostList().add(new MpiHost(LEMMON+13, 8, 1));
        p_56l.getHostList().add(new MpiHost(LEMMON+14, 8, 1));
        p_56l.getHostList().add(new MpiHost(LEMMON+15, 8, 1));
        p_56l.getHostList().add(new MpiHost(LEMMON+16, 8, 1));
        //p_56l.getHostList().add(new MpiHost(LEMMON+17, 8, 1));
        //p_56l.getHostList().add(new MpiHost(LEMMON+18, 8, 1));
        //p_56l.getHostList().add(new MpiHost(LEMMON+19, 8, 1));


        p_56l.setRemoteLogin(matlemLogin);
        p_56l.setMpiVersion(MpiSettings.OPENMPI_V2);
        p_56l.setUseScp(true);
        configurations.add(p_56l);

        String name_56 = "Matthau_Lemmon_Test_56";
        MpiConfiguration p_56 = new MpiConfiguration(name_56);

        p_56.getHostList().add(new MpiHost(MATTHAU+3, 8, 1));
        p_56.getHostList().add(new MpiHost(MATTHAU+4, 8, 1));
        p_56.getHostList().add(new MpiHost(MATTHAU+5, 8, 1));
        p_56.getHostList().add(new MpiHost(MATTHAU+6, 8, 1));
        p_56.getHostList().add(new MpiHost(MATTHAU+7, 8, 1));
        p_56.getHostList().add(new MpiHost(MATTHAU+8, 8, 1));
        p_56.getHostList().add(new MpiHost(MATTHAU+9, 8, 1));


        p_56.setRemoteLogin(matlemLogin);
        p_56.setMpiVersion(MpiSettings.OPENMPI_V2);
        p_56.setUseScp(true);
        configurations.add(p_56);


        String name_ALL = "Matthau_Lemmon_Test_ALL";
        MpiConfiguration p_ALL = new MpiConfiguration(name_ALL);

        for(int i=3;i<=9;i++)
        {
            p_ALL.getHostList().add(new MpiHost(MATTHAU+i, 8, 1));
        }

        for(int i=14;i<=16;i++)
        {
            p_ALL.getHostList().add(new MpiHost(LEMMON+i, 8, 1));
        }

        p_ALL.setRemoteLogin(matlemLogin);
        p_ALL.setMpiVersion(MpiSettings.OPENMPI_V2);
        p_ALL.setUseScp(true);
        configurations.add(p_ALL);


    }

    /*
    public void setVersion(String version)
    {
        this.version = version;
    }*/

    protected static String getMPIVersion()
    {
        File mpichV1flag = new File("MPICH1");
        File mpichV2flag = new File("MPICH2");
        File openmpiV2flag = new File("MPI2");
        
        if (mpichV1flag.exists()) return MPICH_V1;
        if (mpichV2flag.exists()) return MPICH_V2;
        if (openmpiV2flag.exists()) return OPENMPI_V2;
        
        return DEFAULT_MPI_VERSION;
    }

    public ArrayList<MpiConfiguration> getMpiConfigurations()
    {
        return this.configurations;
    }

    public void setMpiConfigurations(ArrayList<MpiConfiguration> confs)
    {
        this.configurations = confs;
    }

    public MpiConfiguration getMpiConfiguration(String name)
    {
        for (MpiConfiguration config: configurations)
        {
            if (config.getName().equals(name)) return config;
        }

        return null;
    }

    public static void main(String[] args)
    {
        new MpiSettings();
    }

}




