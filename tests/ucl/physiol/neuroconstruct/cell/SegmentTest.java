/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package ucl.physiol.neuroconstruct.cell;

import javax.vecmath.Point3f;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import ucl.physiol.neuroconstruct.cell.utils.CellTopologyHelper;
import static org.junit.Assert.*;

/**
 *
 * @author padraig
 */
public class SegmentTest {

    public SegmentTest() {
    }



    @Before
    public void setUp() 
    {
        System.out.println("---------------   setUp() SegmentTest");
    }


    @After
    public void tearDown() {
    }

    @Test public void testCloneAndEquals() 
    {
        System.out.println("---  testCloneAndEquals...");
        
        Segment seg1 = new Segment("Segname", 1.1f, new Point3f(1,2,3), 1, null, 0.6f, null);
        
        Segment seg2 = (Segment)seg1.clone();
        
        
        assertTrue(seg1.equals(seg2));
        
        
    }

    @Test public void testRound() 
    {
        System.out.println("---  testRound...");
   
        
        assertEquals(0, Segment.round(0.0001f), 0);
        assertEquals(0, Segment.round(-0.0001f), 0);
        assertEquals(0.0009f, Segment.round(0.0009f), 0);
        assertEquals(-0.0009f, Segment.round(-0.0009f), 0);
        assertEquals(10, Segment.round(10.00001f), 0);
        assertEquals(-10, Segment.round(-10.00001f), 0);
        
        assertEquals(1, Segment.round(0.9999999f), 0);
        assertEquals(10, Segment.round(9.9999999f), 0);
        
        assertEquals(0.000999f, Segment.round(0.000999f), 0);
        assertEquals(-0.000999f, Segment.round(-0.000999f), 0);
        
        assertEquals(-1, Segment.round(-0.9999999f), 0);
        assertEquals(-10, Segment.round(-9.9999999f), 0);
        
        
        
    }

}
    
    
    
    
    
    
    
    
    
    