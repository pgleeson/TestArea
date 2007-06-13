/**
 * neuroConstruct
 *
 * Software for developing large scale 3D networks of biologically realistic neurons
 * Copyright (c) 2007 Padraig Gleeson
 * UCL Department of Physiology
 *
 * Development of this software was made possible with funding from the
 * Medical Research Council
 *
 */

package ucl.physiol.neuroconstruct.project.packing;

import javax.vecmath.*;
import ucl.physiol.neuroconstruct.utils.*;
import java.util.*;
import ucl.physiol.neuroconstruct.cell.examples.*;
import ucl.physiol.neuroconstruct.project.*;
import ucl.physiol.neuroconstruct.cell.utils.*;

/**
 * Very simple cell packing adapter. Just places cells in cubic 3D grid
 *
 * @author Padraig Gleeson
 * @version 1.0.3
 */


public class SimpleRegularCellPackingAdapter extends CellPackingAdapter
{
    ClassLogger logger = new ClassLogger("SimpleRegularCellPackingAdapter");

    // this will be like positionsAlreadyTaken, but will include ALL the points
    // attempted, including ones removed with cancelPosition(Point3d point)
    Vector<Point3f> positionsAlreadyAttempted = new Vector<Point3f>();

    public SimpleRegularCellPackingAdapter()
    {
        super("CellPacker for cells placed regularly in 3D, one on top of another");

        parameterList = new InternalParameter[1];
        parameterList[0] = new InternalParameter("EdgePolicy",
                                              "Value = 0: Soma centres within region, walls can extend beyond edge; Value = 1: Soma completely inside region",
                                              1);
    }


    protected Point3f generateNextPosition() throws CellPackingException
    {
        Point3f proposedPoint = null;

        logger.logComment("Generating next position...");

        float minXLoc;
        float minYLoc;
        float minZLoc;

        float maxXLoc;
        float maxYLoc;
        float maxZLoc;

        if (mustBeCompletelyInsideRegion())
        {
            // limit the extent for possible location of soma centre to box which
            // will preclude soma wall impacting region boundary.

            minXLoc = myRegion.getLowestXValue() - CellTopologyHelper.getMinXExtent(myCell, true, false);
            minYLoc = myRegion.getLowestYValue() - CellTopologyHelper.getMinYExtent(myCell, true, false);
            minZLoc = myRegion.getLowestZValue() - CellTopologyHelper.getMinZExtent(myCell, true, false);

            maxXLoc = myRegion.getHighestXValue() - CellTopologyHelper.getMaxXExtent(myCell, true, false);
            maxYLoc = myRegion.getHighestYValue() - CellTopologyHelper.getMaxYExtent(myCell, true, false);
            maxZLoc = myRegion.getHighestZValue() - CellTopologyHelper.getMaxZExtent(myCell, true, false);
        }
        else
        {
            // in this case the soma centre can be anywhere inside the region..

            minXLoc = myRegion.getLowestXValue();
            minYLoc = myRegion.getLowestYValue();
            minZLoc = myRegion.getLowestZValue();

            maxXLoc = myRegion.getHighestXValue();
            maxYLoc = myRegion.getHighestYValue();
            maxZLoc = myRegion.getHighestZValue();

        }

        if (maxXLoc<=minXLoc||maxYLoc<=minYLoc||maxZLoc<=minZLoc)
        {
            throw new CellPackingException("Diameter of cell is smaller than region");
        }


        if (getNumPosAlreadyTaken()==0  && positionsAlreadyAttempted.size()==0)
        {
            logger.logComment("This is first point...");
            proposedPoint = new Point3f(minXLoc,
                                        minYLoc,
                                        minZLoc);

        }
        else
        {
            Point3f lastPositionedPoint = (Point3f)positionsAlreadyAttempted.lastElement();
            logger.logComment("Last point attempted at: "+ lastPositionedPoint);

            float proposedNewXPos = lastPositionedPoint.x
                                    + (CellTopologyHelper.getMaxXExtent(myCell, true, false)
                                    - CellTopologyHelper.getMinXExtent(myCell, true, false));

            logger.logComment("Checking if x val of "+proposedNewXPos+" is allowed...");

            if (proposedNewXPos <= (maxXLoc))
            {
                logger.logComment("Positioning this cell with just an x displacement from the last...");
                proposedPoint = new Point3f(proposedNewXPos,
                                            lastPositionedPoint.y,
                                            lastPositionedPoint.z);


            }
            else
            {
                logger.logComment(">>>>>>>>>>>>>>>>>>>>>>>>>>   Need to place the cell in another dimension...");
                float proposedNewYPos = lastPositionedPoint.y
                                        + (CellTopologyHelper.getMaxYExtent(myCell, true, false)
                                           - CellTopologyHelper.getMinYExtent(myCell, true, false));

                logger.logComment("Checking if y val of "+proposedNewYPos+" is allowed...");

                if (proposedNewYPos <= (maxYLoc))
                {
                    logger.logComment("Positioning this cell with a y displacement from the last...");

                    proposedPoint = new Point3f(minXLoc,
                                                proposedNewYPos,
                                                lastPositionedPoint.z);
                }
                else
                {
                    logger.logComment(">>>>>>>>>>>>>>>>>>>>>>>>>>    Need to place the cell in another dimension...");
                    float proposedNewZPos = lastPositionedPoint.z
                                             + (CellTopologyHelper.getMaxZExtent(myCell, true, false)
                                                - CellTopologyHelper.getMinZExtent(myCell, true, false));

                    logger.logComment("Checking if z val of "+proposedNewZPos+" is allowed...");

                    if (proposedNewZPos <= (maxZLoc))
                    {
                        logger.logComment("Positioning this cell with a z displacement from the last...");
                        proposedPoint = new Point3f(minXLoc,
                                                    minYLoc,
                                                    proposedNewZPos);
                    }
                    else
                    {
                        logger.logComment("All dimensions tried...");
                        throw new CellPackingException("All dimensions tried...");
                    }

                }
            }

        }


        if (proposedPoint!=null && myRegion.isCellWithinRegion(proposedPoint, myCell, mustBeCompletelyInsideRegion()))
        {

            positionsAlreadyAttempted.add(proposedPoint);
            return proposedPoint;
        }
        else
        {
            logger.logComment("Found a valid position in XYZ space, but the cell's not inside the region...");
            // go again until all positions used up..
            positionsAlreadyAttempted.add(proposedPoint);
            return generateNextPosition();
        }


    }

    private boolean mustBeCompletelyInsideRegion()
    {
        if (parameterList[0].value == 1)
            return true;
        else
            return false;
    }


    public void setParameter(String parameterName,
                             float parameterValue)  throws CellPackingException
    {
        if (parameterName.equals("EdgePolicy"))
        {
            if (parameterValue == 0 || parameterValue == 1)
                parameterList[0].value = parameterValue;
            else
                throw new CellPackingException("Invalid Parameter value");
        }

        else throw new CellPackingException("Not a valid Parameter name");

    };

    public void reset()
    {
        super.reset();
        logger.logComment("------------------  Adapter being reset...");
        this.positionsAlreadyAttempted.removeAllElements();
    }



    public String toString()
    {
        StringBuffer sb = new StringBuffer();
        String nameOfClass = this.getClass().getName();

        sb.append(nameOfClass.substring(nameOfClass.lastIndexOf(".")+1)+ "[");

        sb.append("EdgePolicy: ");
        if (mustBeCompletelyInsideRegion()) sb.append("1]");
        else sb.append("0]");


        return (sb.toString());
    }


    public static void main(String args[])
    {
        SimpleCell pCell = new SimpleCell("Test cell");

        SimpleRegularCellPackingAdapter ada = new SimpleRegularCellPackingAdapter();
        ada.addRegionAndCellInfo(new RectangularBox(0,0,0, 90,90,90), pCell);

        System.out.println("Parameter: " + ada.getParameterList()[0]);
        System.out.println("Description: " + ada.getDescription());

        try
        {
            while(true)
            {
                System.out.println("Point: " + ada.getNextPosition());
            }
        }
        catch (CellPackingException ex)
        {
            ex.printStackTrace();
        }

        System.out.println("Number of positions: "+ada.getCurrentNumberPositions());
    }

}
