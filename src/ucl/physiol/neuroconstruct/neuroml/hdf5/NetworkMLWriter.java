/**
 * neuroConstruct
 *
 * Software for developing large scale 3D networks of biologically realistic neurons
 * Copyright (c) 2008 Padraig Gleeson
 * UCL Department of Physiology
 *
 * Development of this software was made possible with funding from the
 * Medical Research Council
 *
 */

package ucl.physiol.neuroconstruct.neuroml.hdf5;


import ncsa.hdf.object.*;
import ncsa.hdf.object.h5.*;
import java.io.File;
import ucl.physiol.neuroconstruct.utils.ClassLogger;
import ucl.physiol.neuroconstruct.neuroml.NetworkMLReader;
import javax.xml.parsers.SAXParserFactory;
import java.io.FileInputStream;
import org.xml.sax.InputSource;
import org.xml.sax.XMLReader;
import ucl.physiol.neuroconstruct.project.Project;
import ucl.physiol.neuroconstruct.project.GeneratedCellPositions;
import ucl.physiol.neuroconstruct.project.GeneratedNetworkConnections;
import java.util.Iterator;
import java.util.ArrayList;
import java.util.Vector;
import ucl.physiol.neuroconstruct.cell.SegmentLocation;
import ucl.physiol.neuroconstruct.neuroml.NetworkMLConstants;
import ucl.physiol.neuroconstruct.project.ConnSpecificProps;
import ucl.physiol.neuroconstruct.project.GeneralProperties;
import ucl.physiol.neuroconstruct.project.PositionRecord;
import ucl.physiol.neuroconstruct.project.GeneratedNetworkConnections.SingleSynapticConnection;
import ucl.physiol.neuroconstruct.project.SynapticProperties;
import ucl.physiol.neuroconstruct.utils.GeneralUtils;

/**
 * Utilities file for generating NetworkML HDF5 files
 *
 * @author Padraig Gleeson
 *
 */

public class NetworkMLWriter
{
    private static ClassLogger logger = new ClassLogger("NetworkMLWriter");

    public static int POP_COLUMN_NUM = 4;


    public NetworkMLWriter()
    {
        super();
    }

    public static File createNetworkMLH5file(File file,
                                             Project project) throws Hdf5Exception
    {

        H5File h5File = Hdf5Utils.createH5file(file);

        Hdf5Utils.open(h5File);

        Group root = Hdf5Utils.getRootGroup(h5File);
        Group netmlGroup = null;
        Group popsGroup = null;
        Group projsGroup = null;
        Group inputsGroup = null;
        
        GeneratedCellPositions gcp = project.generatedCellPositions;
        GeneratedNetworkConnections gnc = project.generatedNetworkConnections;
        
        
        StringBuffer notes = new StringBuffer("\nNetwork structure saved with neuroConstruct v"+
                        GeneralProperties.getVersionNumber()+" on: "+ GeneralUtils.getCurrentTimeAsNiceString() +", "
                    + GeneralUtils.getCurrentDateAsNiceString()+"\n\n");


        Iterator<String> cellGroups = gcp.getNamesGeneratedCellGroups();

        while (cellGroups.hasNext())
        {
            String cg = cellGroups.next();
            int numHere = gcp.getNumberInCellGroup(cg);
            if (numHere>0)
            notes.append("Cell Group: "+cg+" contains "+numHere+" cells\n");

        }
        notes.append("\n");

        Iterator<String> netConns = gnc.getNamesNetConnsIter();

        while (netConns.hasNext())
        {
        String mc = netConns.next();
        int numHere = gnc.getSynapticConnections(mc).size();
        if (numHere>0)
        notes.append("Network connection: "+mc+" contains "+numHere+" individual synaptic connections\n");

        }

        try
        {
            netmlGroup = h5File.createGroup(NetworkMLConstants.ROOT_ELEMENT, root);
            popsGroup = h5File.createGroup(NetworkMLConstants.POPULATIONS_ELEMENT, netmlGroup);
            projsGroup = h5File.createGroup(NetworkMLConstants.PROJECTIONS_ELEMENT, netmlGroup);
            
            Attribute unitsAttr = Hdf5Utils.getSimpleAttr(NetworkMLConstants.UNITS_ATTR, NetworkMLConstants.UNITS_PHYSIOLOGICAL, h5File);
            projsGroup.writeMetadata(unitsAttr);
                
            inputsGroup = h5File.createGroup("inputs", netmlGroup);

            Attribute attr = Hdf5Utils.getSimpleAttr("notes", notes.toString(), h5File);
            
            netmlGroup.writeMetadata(attr);
        }
        catch (Exception ex)
        {
            throw new Hdf5Exception("Failed to create group in HDF5 file: "+ h5File.getFilePath(), ex);
        }

        cellGroups = gcp.getNamesGeneratedCellGroups();

        while(cellGroups.hasNext())
        {
            String cg = cellGroups.next();

            ArrayList<PositionRecord> posRecs = gcp.getPositionRecords(cg);

            try
            {
                Group popGroup = h5File.createGroup(NetworkMLConstants.POPULATION_ELEMENT+"_"+cg, popsGroup);
                
                Attribute nameAttr = Hdf5Utils.getSimpleAttr(NetworkMLConstants.POP_NAME_ATTR, cg, h5File);
                popGroup.writeMetadata(nameAttr);
                
                String cellType = project.cellGroupsInfo.getCellType(cg);
            
                Attribute cellTypeAttr = Hdf5Utils.getSimpleAttr(NetworkMLConstants.CELLTYPE_ATTR, cellType, h5File);
                popGroup.writeMetadata(cellTypeAttr);

                Datatype dtype = getPopDatatype(h5File);

                long[] dims2D = {posRecs.size(), POP_COLUMN_NUM};

                float[] posArray = new float[posRecs.size() * POP_COLUMN_NUM];


                for (int i=0; i<posRecs.size(); i++)
                {
                    PositionRecord p = posRecs.get(i);

                    posArray[i * POP_COLUMN_NUM + 0] = p.cellNumber;

                    posArray[i * POP_COLUMN_NUM + 1] = p.x_pos;
                    posArray[i * POP_COLUMN_NUM + 2] = p.y_pos;
                    posArray[i * POP_COLUMN_NUM + 3] = p.z_pos;

                }


                Dataset dataset = h5File.createScalarDS
                    (cg, popGroup, dtype, dims2D, null, null, 0, posArray);

                Attribute attr0 = Hdf5Utils.getSimpleAttr("column_0", "instance_id", h5File);
                dataset.writeMetadata(attr0);
                Attribute attr1 = Hdf5Utils.getSimpleAttr("column_1", "x", h5File);
                dataset.writeMetadata(attr1);
                Attribute attr2 = Hdf5Utils.getSimpleAttr("column_2", "y", h5File);
                dataset.writeMetadata(attr2);
                Attribute attr3 = Hdf5Utils.getSimpleAttr("column_3", "z", h5File);
                dataset.writeMetadata(attr3);


            }
            catch (Exception ex)
            {
                throw new Hdf5Exception("Failed to create group in HDF5 file: " + h5File.getFilePath(), ex);
            }
        }





        Iterator<String> nCs = gnc.getNamesNetConnsIter();

        while(nCs.hasNext())
        {
            String nc = nCs.next();

            ArrayList<SingleSynapticConnection> conns = gnc.getSynapticConnections(nc);

            try
            {
                Group projGroup = h5File.createGroup(NetworkMLConstants.PROJECTION_ELEMENT +"_" + nc, projsGroup);
                
                
                Attribute nameAttr = Hdf5Utils.getSimpleAttr(NetworkMLConstants.PROJ_NAME_ATTR, nc, h5File);
                projGroup.writeMetadata(nameAttr);
                
                String src = null;
                String tgt = null;
                Vector<SynapticProperties>  globalSynPropList = null;
                
                if (project.morphNetworkConnectionsInfo.isValidSimpleNetConn(nc))
                {
                    src = project.morphNetworkConnectionsInfo.getSourceCellGroup(nc);
                    tgt = project.morphNetworkConnectionsInfo.getTargetCellGroup(nc);
                    globalSynPropList = project.morphNetworkConnectionsInfo.getSynapseList(nc);
                }

                else if (project.volBasedConnsInfo.isValidAAConn(nc))
                {
                    src = project.volBasedConnsInfo.getSourceCellGroup(nc);
                    src = project.volBasedConnsInfo.getTargetCellGroup(nc);
                    globalSynPropList = project.volBasedConnsInfo.getSynapseList(nc);
                }
                
                Attribute srcAttr = Hdf5Utils.getSimpleAttr(NetworkMLConstants.SOURCE_ATTR, src, h5File);
                projGroup.writeMetadata(srcAttr);
                Attribute tgtAttr = Hdf5Utils.getSimpleAttr(NetworkMLConstants.TARGET_ATTR, tgt, h5File);
                projGroup.writeMetadata(tgtAttr);
                
                float globWeight = 1;
                float globDelay = 0;
                
                for(SynapticProperties sp:  globalSynPropList)
                {
                    Group synPropGroup = h5File.createGroup(NetworkMLConstants.SYN_PROPS_ELEMENT +"_" + sp.getSynapseType(), projGroup);

                    Attribute synTypeAttr = Hdf5Utils.getSimpleAttr(NetworkMLConstants.SYN_TYPE_ATTR, sp.getSynapseType(), h5File);
                    synPropGroup.writeMetadata(synTypeAttr);
                    
                    globDelay = sp.getDelayGenerator().getNominalNumber();
                    Attribute synTypeDelay = Hdf5Utils.getSimpleAttr(NetworkMLConstants.INTERNAL_DELAY_ATTR, globDelay+"", h5File);
                    synPropGroup.writeMetadata(synTypeDelay);
                    
                    globWeight = sp.getWeightsGenerator().getNominalNumber();
                    Attribute synTypeWeight = Hdf5Utils.getSimpleAttr(NetworkMLConstants.WEIGHT_ATTR, globWeight+"", h5File);
                    synPropGroup.writeMetadata(synTypeWeight);
                    
                    Attribute synTypeThreshold = Hdf5Utils.getSimpleAttr(NetworkMLConstants.THRESHOLD_ATTR, sp.getThreshold()+"", h5File);
                    synPropGroup.writeMetadata(synTypeThreshold);
                }
                
                ArrayList<String> columnsNeeded = new ArrayList<String>();
                
                columnsNeeded.add(NetworkMLConstants.CONNECTION_ID_ATTR);
                columnsNeeded.add(NetworkMLConstants.PRE_CELL_ID_ATTR);
                columnsNeeded.add(NetworkMLConstants.POST_CELL_ID_ATTR);
                
                for (int i = 0; i < conns.size(); i++)
                {
                    SingleSynapticConnection conn = conns.get(i);
                    
                    if (conn.sourceEndPoint.location.getSegmentId()!=0 && !columnsNeeded.contains(NetworkMLConstants.PRE_SEGMENT_ID_ATTR))
                        columnsNeeded.add(NetworkMLConstants.PRE_SEGMENT_ID_ATTR);
                    
                    if (conn.sourceEndPoint.location.getFractAlong()!=SegmentLocation.DEFAULT_FRACT_CONN && !columnsNeeded.contains(NetworkMLConstants.PRE_FRACT_ALONG_ATTR))
                        columnsNeeded.add(NetworkMLConstants.PRE_FRACT_ALONG_ATTR);
                    
                    if (conn.targetEndPoint.location.getSegmentId()!=0 && !columnsNeeded.contains(NetworkMLConstants.POST_SEGMENT_ID_ATTR))
                        columnsNeeded.add(NetworkMLConstants.POST_SEGMENT_ID_ATTR);
                    
                    if (conn.targetEndPoint.location.getFractAlong()!=SegmentLocation.DEFAULT_FRACT_CONN && !columnsNeeded.contains(NetworkMLConstants.POST_FRACT_ALONG_ATTR))
                        columnsNeeded.add(NetworkMLConstants.POST_FRACT_ALONG_ATTR);
                    
                    if (conn.apPropDelay!=0 && !columnsNeeded.contains(NetworkMLConstants.PROP_DELAY_ATTR))
                        columnsNeeded.add(NetworkMLConstants.PROP_DELAY_ATTR);
                    
                    if (conn.props!=null)
                    {
                        for(ConnSpecificProps prop: conn.props)
                        {
                            if(prop.weight!=1 && !columnsNeeded.contains(NetworkMLConstants.WEIGHT_ATTR+"_"+prop.synapseType))
                                columnsNeeded.add(NetworkMLConstants.WEIGHT_ATTR+"_"+prop.synapseType);
                            
                            if(prop.internalDelay!=0 && !columnsNeeded.contains(NetworkMLConstants.INTERNAL_DELAY_ATTR+"_"+prop.synapseType))
                                columnsNeeded.add(NetworkMLConstants.INTERNAL_DELAY_ATTR+"_"+prop.synapseType);
                        }
                    }
                }
                

                Datatype dtype = getProjDatatype(h5File);

                long[] dims2D = {conns.size(), columnsNeeded.size()};

                float[] projArray = new float[conns.size() * columnsNeeded.size()];

                for (int i = 0; i < conns.size(); i++)
                {
                    SingleSynapticConnection conn = conns.get(i);

                    int row = 0;
                    projArray[i * columnsNeeded.size() +row] = i;
                    row++;

                    projArray[i * columnsNeeded.size() + row] = conn.sourceEndPoint.cellNumber;
                    row++;
                    
                    projArray[i * columnsNeeded.size() + row] = conn.targetEndPoint.cellNumber;
                    row++;
                    
                    if (columnsNeeded.contains(NetworkMLConstants.PRE_SEGMENT_ID_ATTR))
                    {
                        projArray[i * columnsNeeded.size() + row] = conn.sourceEndPoint.location.getSegmentId();
                        row++;
                    }
                    
                    if (columnsNeeded.contains(NetworkMLConstants.PRE_FRACT_ALONG_ATTR))
                    {
                        projArray[i * columnsNeeded.size() + row] = conn.sourceEndPoint.location.getFractAlong();
                        row++;
                    }

                    
                    if (columnsNeeded.contains(NetworkMLConstants.POST_SEGMENT_ID_ATTR))
                    {
                        projArray[i * columnsNeeded.size() + row] = conn.targetEndPoint.location.getSegmentId();
                        row++;
                    }
                    
                    if (columnsNeeded.contains(NetworkMLConstants.POST_FRACT_ALONG_ATTR))
                    {
                        projArray[i * columnsNeeded.size() + row] = conn.targetEndPoint.location.getFractAlong();
                        row++;
                    }
                    
                    if (columnsNeeded.contains(NetworkMLConstants.PROP_DELAY_ATTR))
                    {
                        projArray[i * columnsNeeded.size() + row] = conn.apPropDelay;
                        row++;
                    }
                    
                    
                    if (conn.props!=null)
                    {
                        for(ConnSpecificProps prop: conn.props)
                        {
                            if(columnsNeeded.contains(NetworkMLConstants.WEIGHT_ATTR+"_"+prop.synapseType))
                            {
                                projArray[i * columnsNeeded.size() + row] = prop.weight;
                                row++;
                            }
                            if(columnsNeeded.contains(NetworkMLConstants.INTERNAL_DELAY_ATTR+"_"+prop.synapseType))
                            {
                                projArray[i * columnsNeeded.size() + row] = prop.internalDelay;
                                row++;
                            }
                            
                        }
                    }

                }

                Dataset projDataset = h5File.createScalarDS(nc, projGroup, dtype, dims2D, null, null, 0, projArray);
                
                for(int i=0;i<columnsNeeded.size();i++)
                {
                    Attribute attr = Hdf5Utils.getSimpleAttr("column_"+i, columnsNeeded.get(i), h5File);
                    projDataset.writeMetadata(attr);
                }
                
                
                logger.logComment("Dataset compression: " + projDataset.getCompression(), true);

            }
            catch (Exception ex)
            {
                throw new Hdf5Exception("Failed to create group in HDF5 file: " + h5File.getFilePath(), ex);
            }
        }

        //h5File.

        Hdf5Utils.close(h5File);

        logger.logComment("Created file: " + file, true);
        logger.logComment("Size: " + file.length()+" bytes", true);
        
        return file;
    }

    public static Datatype getPopDatatype(H5File h5File) throws Hdf5Exception
    {
        try
        {

            Datatype popDataType = h5File.createDatatype(Datatype.CLASS_FLOAT, 4, Datatype.NATIVE, -1);
            return popDataType;
        }
        catch (Exception ex)
        {
            throw new Hdf5Exception("Failed to get pop datatype in HDF5 file: " + h5File.getFilePath(), ex);

        }

    }

    public static Datatype getProjDatatype(H5File h5File) throws Hdf5Exception
    {
        try
        {
            Datatype projDataType = h5File.createDatatype(Datatype.CLASS_FLOAT, 4, Datatype.NATIVE, -1);
            return projDataType;
        }
        catch (Exception ex)
        {
            throw new Hdf5Exception("Failed to get projection datatype in HDF5 file: " + h5File.getFilePath());

        }

    }



    public static void main(String[] args)
    {
        File h5File = new File("../temp/net.h5");
        try
        {
            System.setProperty("java.library.path", System.getProperty("java.library.path")+":/home/padraig/neuroConstruct");
            
            logger.logComment("Sys prop: "+System.getProperty("java.library.path"), true);
            
            Project testProj = Project.loadProject(new File("examples/Ex9-GranCellLayer/Ex9-GranCellLayer.neuro.xml"),
                                                   null);

            //File nmlFile = new File("examples/Ex9-GranCellLayer/savedNetworks/600.nml");
            File nmlFile = new File("examples/Ex9-GranCellLayer/savedNetworks/75.nml");
            //File nmlFile = new File("../copynCmodels/Parallel/savedNetworks/50000.nml");
            //File nmlFile = new File("../copynCmodels/NewGranCellLayer/savedNetworks/87000Rand.nml");
            //File nmlFile = new File("../temp/test.nml");
            //File nmlFile = new File("../copynCmodels/Parallel/savedNetworks/50000.nml");


            logger.logComment("Loading netml cell from " + nmlFile.getAbsolutePath(), true);

            GeneratedCellPositions gcp = testProj.generatedCellPositions;
            GeneratedNetworkConnections gnc = testProj.generatedNetworkConnections;

            FileInputStream instream = null;
            InputSource is = null;

            SAXParserFactory spf = SAXParserFactory.newInstance();
            spf.setNamespaceAware(true);

            XMLReader xmlReader = spf.newSAXParser().getXMLReader();

            NetworkMLReader nmlBuilder = new NetworkMLReader(gcp, gnc);
            xmlReader.setContentHandler(nmlBuilder);

            instream = new FileInputStream(nmlFile);

            is = new InputSource(instream);

            xmlReader.parse(is);

            logger.logComment("Cells: " + gcp.getNumberInAllCellGroups(), true);
            logger.logComment("Net conn num: " + gnc.getNumberSynapticConnections(GeneratedNetworkConnections.ANY_NETWORK_CONNECTION), true);

            NetworkMLWriter.createNetworkMLH5file(h5File, testProj);

        }
        catch (Exception e)
        {
            e.printStackTrace();
            System.exit(0);
        }


    }
}
