/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ucl.physiol.neuroconstruct.cell.converters;

import java.io.File;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;
import org.xml.sax.Attributes;
import ucl.physiol.neuroconstruct.cell.Cell;
import ucl.physiol.neuroconstruct.cell.CellTest;
import ucl.physiol.neuroconstruct.cell.utils.CellTopologyHelper;
import ucl.physiol.neuroconstruct.neuroml.NeuroMLConstants;
import ucl.physiol.neuroconstruct.project.*;

/**
 *
 * @author padraig
 */
public class MorphMLReaderTest {

    String projName = "TestMorphs";
    File projDir = new File("testProjects/"+ projName);
        
    ProjectManager pm = null;
    
    public MorphMLReaderTest() {
    }

    @Before
    public void setUp() 
    {
        System.out.println("---------------   setUp() MorphMLReaderTest");        
        
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

    @Test public void testWriteAndRead() throws MorphologyException 
    {
        System.out.println("---  testWriteAndRead...");
        
        Cell cell1 = pm.getCurrentProject().cellManager.getAllCells().get(0);
        
        cell1.setCellDescription("This is\na test\n...");
        
        MorphMLConverter mmlC = new MorphMLConverter();
        
        File savedNeuroMLDir = ProjectStructure.getNeuroMLDir(projDir);
        File morphFile = new File(savedNeuroMLDir, "test.mml");
        
        MorphMLConverter.saveCellInMorphMLFormat(cell1, pm.getCurrentProject(), morphFile, NeuroMLConstants.NEUROML_LEVEL_3);
        
        assertTrue(morphFile.exists());
        
        System.out.println("Saved cell in NeuroML Level 3 file: "+ morphFile.getAbsolutePath());
        
        Cell cell2 = mmlC.loadFromMorphologyFile(morphFile, cell1.getInstanceName());
        
        //System.out.println("cell1: "+ CellTopologyHelper.printDetails(cell1, pm.getCurrentProject()));
        //System.out.println("cell2: "+ CellTopologyHelper.printDetails(cell2, pm.getCurrentProject()));
        
        String compare = CellTopologyHelper.compare(cell1, cell2, false);
        
        System.out.println("Comparison 1: "+ compare);
        
        assertTrue(compare.indexOf(CellTopologyHelper.CELLS_ARE_IDENTICAL)>=0);
        
        System.out.println("Reloaded file and cells are identical");
        
    }


}