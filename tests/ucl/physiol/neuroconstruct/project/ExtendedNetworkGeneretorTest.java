/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */


package ucl.physiol.neuroconstruct.project;

import java.io.File;
import java.util.*;
import javax.vecmath.Point3f;
import org.junit.*;
import org.junit.Test;
import org.junit.runner.Result;
import test.MainTest;
import ucl.physiol.neuroconstruct.cell.Cell;
import ucl.physiol.neuroconstruct.cell.Section;
import ucl.physiol.neuroconstruct.cell.utils.CellTopologyHelper;
import ucl.physiol.neuroconstruct.project.GeneratedNetworkConnections.SingleSynapticConnection;
import ucl.physiol.neuroconstruct.project.packing.CellPackingException;
import ucl.physiol.neuroconstruct.utils.NumberGenerator;
import static org.junit.Assert.*;

/**
 *
 * @author Matteo Farinella
 */

public class ExtendedNetworkGeneretorTest {
ProjectManager pm = null;
    Random r = new Random();
    
    public ExtendedNetworkGeneretorTest() 
    {
    }

            

    @Before
    public void setUp() 
    {
        System.out.println("---------------   setUp() ExtendedNetworkGeneretorTest");
        String projName = "TestNetworkConns";
        File projDir = new File("testProjects/"+ projName);
        File projFile = new File(projDir, projName+ProjectStructure.getProjectFileExtension());
        
        pm = new ProjectManager();

        try 
        {
            pm.loadProject(projFile);
        
            System.out.println("Proj status: "+ pm.getCurrentProject().getProjectStatusAsString());
            
            
        } 
        catch (ProjectFileParsingException ex) 
        {
            fail("Error loading: "+ projFile.getAbsolutePath());
        }
    }

    @After
    public void tearDown() {
    }
    
    private void generate(Project proj, SimConfig sc) throws InterruptedException 
    {                
        pm.doGenerate(sc.getName(), 1234);
        
        while(pm.isGenerating())
        {
            Thread.sleep(200);
        }
        
        System.out.println("Generated proj with: "+ proj.generatedCellPositions.getNumberInAllCellGroups()+" cells");
    }
    


    private void generate(Project proj) throws InterruptedException 
    {       
        
        SimConfig sc = proj.simConfigInfo.getDefaultSimConfig();
        
        generate(proj, sc);
    }
    
    int numPre = 20;
    int numPost = 20;

    int minPre = 3;
    int maxPre = 10;
    int meanPre = 7;
    int stdPre = 1;

    int maxPost = 9;

    float minLength = 10;
    float maxLength = 50;

    float weightMin = 0.5f;
    float weightMax = 0.8f;
    
    
    
    /* test the option "soma to soma" distance for the length of the connections
     */
    @Test
    public void testSomaToSomaDistance() throws InterruptedException, CellPackingException, ProjectFileParsingException
    {        
        System.out.println("---  test SomaToSoma distance()");       
        
//        File f = new File("C:\\neuroConstruct\\testProjects\\TestNetworkConnsSomas\\TestNetworkConns.neuro.xml");
//        Project proj2 = pm.loadProject(f);
        Project proj2 = pm.getCurrentProject();
        
        SimConfig sc = proj2.simConfigInfo.getSimConfig("TwoCG");
        
        String nc2 = proj2.morphNetworkConnectionsInfo.getNetConnNameAt(2);  
        String src = proj2.morphNetworkConnectionsInfo.getSourceCellGroup(nc2);
        String trg = proj2.morphNetworkConnectionsInfo.getTargetCellGroup(nc2);
              
        proj2.morphNetworkConnectionsInfo.getMaxMinLength(nc2).setDimension("s");        
        proj2.morphNetworkConnectionsInfo.getConnectivityConditions(nc2).setMaxNumInitPerFinishCell(100);        
        
        NumberGenerator ngNum = new NumberGenerator();
        ngNum.initialiseAsGaussianIntGenerator(maxPre, minPre, meanPre, stdPre);
        
        proj2.morphNetworkConnectionsInfo.getConnectivityConditions(nc2).setNumConnsInitiatingCellGroup(ngNum);       
        
        maxLength = 100;
        minLength = 0;
        
        proj2.morphNetworkConnectionsInfo.getMaxMinLength(nc2).setMaxLength(maxLength);
        proj2.morphNetworkConnectionsInfo.getMaxMinLength(nc2).setMinLength(minLength);
        
        generate(proj2, sc);
        
        Cell sourceCellInstance = proj2.cellManager.getCell(proj2.cellGroupsInfo.getCellType(src));
        Cell targetCellInstance = proj2.cellManager.getCell(proj2.cellGroupsInfo.getCellType(trg));
        
        Section sourceSec = sourceCellInstance.getFirstSomaSegment().getSection();
        Section targetSec = targetCellInstance.getFirstSomaSegment().getSection();

        Point3f sourceSomaPosition = CellTopologyHelper.convertSectionDisplacement(sourceCellInstance, sourceSec, (float) 0.5);

        Point3f targetSomaPosition = CellTopologyHelper.convertSectionDisplacement(targetCellInstance, targetSec, (float) 0.5);
        
        ArrayList<SingleSynapticConnection> SynConn= proj2.generatedNetworkConnections.getSynapticConnections(nc2);
        
//        System.out.println("*** MAX length " +maxLength);
//        System.out.println("*** MIN length " +minLength);
//        System.out.println("*** " +SynConn.size()+ " connections to check");
//        System.out.println("...");

        for (int i = 0; i < SynConn.size(); i++)
        {
        
        Point3f startCell = proj2.generatedCellPositions.getOneCellPosition(src,SynConn.get(i).sourceEndPoint.cellNumber);
        Point3f endCell = proj2.generatedCellPositions.getOneCellPosition(trg,SynConn.get(i).targetEndPoint.cellNumber);
        
        startCell.add(sourceSomaPosition);
        endCell.add(targetSomaPosition);
        
//        System.out.println(i + " connection lenght = " + startCell.distance(endCell));
        assertTrue((startCell.distance(endCell)>=minLength)&&(startCell.distance(endCell)<=maxLength));        
        
        }
        
        System.out.println("All the " + SynConn.size() + " connections follow the soma to soma distance costrains" );

    }
    
    
    /* test the option x dimention option for the length of the connections (valid also for y and z dimensions)
     */
    @Test
    public void testXDimension() throws ProjectFileParsingException, InterruptedException
    {        
        System.out.println("---  test X dimension()");       
        
//        File f = new File("C:\\neuroConstruct\\testProjects\\TestNetworkConnsSomas\\TestNetworkConns.neuro.xml");
//        Project proj2 = pm.loadProject(f);
        
        Project proj2 = pm.getCurrentProject();
        
        SimConfig sc = proj2.simConfigInfo.getSimConfig("TwoCG");
        
        String nc2 = proj2.morphNetworkConnectionsInfo.getNetConnNameAt(2);  
        String src = proj2.morphNetworkConnectionsInfo.getSourceCellGroup(nc2);
        String trg = proj2.morphNetworkConnectionsInfo.getTargetCellGroup(nc2);
              
        proj2.morphNetworkConnectionsInfo.getMaxMinLength(nc2).setDimension("x");        
        proj2.morphNetworkConnectionsInfo.getConnectivityConditions(nc2).setMaxNumInitPerFinishCell(100);        
        
        NumberGenerator ngNum = new NumberGenerator();
        ngNum.initialiseAsGaussianIntGenerator(maxPre, minPre, meanPre, stdPre);
        
        proj2.morphNetworkConnectionsInfo.getConnectivityConditions(nc2).setNumConnsInitiatingCellGroup(ngNum);       
        
        maxLength = 50;
        minLength = 10;
        
        MaxMinLength maxMin = proj2.morphNetworkConnectionsInfo.getMaxMinLength(nc2);
        
        maxMin.setMaxLength(maxLength);
        maxMin.setMinLength(minLength);
        
        generate(proj2, sc);       
        
        ArrayList<SingleSynapticConnection> synConn= proj2.generatedNetworkConnections.getSynapticConnections(nc2);
        
        for (int i = 0; i < synConn.size(); i++)
        {
        
            float distanceApart = CellTopologyHelper.getSynapticEndpointsDistance(proj2,
                                                                                    src,
                                                                                    synConn.get(i).sourceEndPoint,
                                                                                    trg,
                                                                                    synConn.get(i).targetEndPoint,
                                                                                    maxMin.getDimension());
        
            assertTrue((distanceApart>=minLength)&&(distanceApart<=maxLength));        
        
        }
        
        System.out.println("All the " + synConn.size() + " connections follow the x dimension distance costrains" );
    }
  
    
    /* test the option in wich no recurrent connections between two cells are allowed (GAP junctions)
     */
    @Test
    public void testGAPjunctionNetwork() throws InterruptedException
    {
        System.out.println("---  test non recurrent connections (GAP junctions condition)");
        
        Project proj = pm.getCurrentProject();
        
        SimConfig sc = proj.simConfigInfo.getSimConfig("TwoCG");
        
        String nc1 = proj.morphNetworkConnectionsInfo.getNetConnNameAt(2);
        String src = proj.morphNetworkConnectionsInfo.getSourceCellGroup(nc1);
        proj.morphNetworkConnectionsInfo.setTargetCellGroup(nc1, src); //source = target
        
        NumberGenerator ngNum = new NumberGenerator();
        ngNum.initialiseAsGaussianIntGenerator(maxPre, minPre, meanPre, stdPre);
        
        proj.morphNetworkConnectionsInfo.getConnectivityConditions(nc1).setNumConnsInitiatingCellGroup(ngNum);
        
        proj.morphNetworkConnectionsInfo.getConnectivityConditions(nc1).setOnlyConnectToUniqueCells(true);
        proj.morphNetworkConnectionsInfo.getConnectivityConditions(nc1).setNoRecurrent(true);
        proj.morphNetworkConnectionsInfo.getConnectivityConditions(nc1).setMaxNumInitPerFinishCell(100);
        
        proj.morphNetworkConnectionsInfo.getMaxMinLength(nc1).setMaxLength(500);
        proj.morphNetworkConnectionsInfo.getMaxMinLength(nc1).setMinLength(0);
        proj.morphNetworkConnectionsInfo.getMaxMinLength(nc1).setDimension("s");
        
        // test the case of a COMPLETE_RANDOM search pattern
        proj.morphNetworkConnectionsInfo.setSearchPattern(nc1, SearchPattern.getRandomSearchPattern());
       
        generate(proj, sc);        
              
        int [][] mat = proj.generatedNetworkConnections.getConnectionMatrix(nc1, proj);
        for (int i = 0; i < mat.length; i++)
        {
            for (int j = 0; j < mat.length; j++)
            {
                assertTrue(mat[i][j]+mat[j][i]<=1); // max one single synapse between two cells (in both directions)
            }
        }
        
        System.out.println("All the " + proj.generatedNetworkConnections.getSynapticConnections(nc1).size() + " connections are not recurrent connections (RANDOM pattern)");
        
        // test the case of a RANDOM_BUT_CLOSE search pattern
        proj.morphNetworkConnectionsInfo.setSearchPattern(nc1, SearchPattern.getRandomCloseSearchPattern(10));
        
        generate(proj, sc);        
              
        int [][] mat1 = proj.generatedNetworkConnections.getConnectionMatrix(nc1, proj);
        for (int i = 0; i < mat1.length; i++)
        {
            for (int j = 0; j < mat1.length; j++)
            {
                assertTrue(mat1[i][j]+mat1[j][i]<=1); // max one single synapse between two cells (in both directions)
            }
        }

        System.out.println("All the " + proj.generatedNetworkConnections.getSynapticConnections(nc1).size() + " connections are not recurrent connections (RANDOM but CLOSE pattern)");
        
         // test the case of a CLOSEST search pattern
        proj.morphNetworkConnectionsInfo.setSearchPattern(nc1, SearchPattern.getClosestSearchPattern());
        
        // the CLOSEST case is not compatible with the MAX MIN costrains
        proj.morphNetworkConnectionsInfo.getMaxMinLength(nc1).setMaxLength(maxLength);
        proj.morphNetworkConnectionsInfo.getMaxMinLength(nc1).setMinLength(0);
        
        generate(proj, sc);        
              
        int [][] mat2 = proj.generatedNetworkConnections.getConnectionMatrix(nc1, proj);
        for (int i = 0; i < mat2.length; i++)
        {
            for (int j = 0; j < mat2.length; j++)
            {
                assertTrue(mat2[i][j]+mat2[j][i]<=1); // max one single synapse between two cells (in both directions)
            }
        }
        
        System.out.println("All the " + proj.generatedNetworkConnections.getSynapticConnections(nc1).size() + " connections are not recurrent connections (CLOSEST pattern)");

    
    }
    
    public static void main(String[] args)
    {
        ExtendedNetworkGeneretorTest ct = new ExtendedNetworkGeneretorTest();
        Result r = org.junit.runner.JUnitCore.runClasses(ct.getClass());
        MainTest.checkResults(r);
    }
}
