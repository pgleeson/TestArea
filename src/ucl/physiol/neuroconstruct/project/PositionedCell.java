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

package ucl.physiol.neuroconstruct.project;

import javax.vecmath.*;

/**
 * Class for holding the position of a cell, and its cell group
 *
 * @author Padraig Gleeson
 *  
 */

public class PositionedCell
{
    public Point3f positionOfSoma = null;
    public String cellGroupName = null;
    public String cellType = null;


    private PositionedCell()
    {
    }


    public PositionedCell(Point3f positionOfSoma, String cellGroupName, String cellType)
    {
        this.positionOfSoma = positionOfSoma;
        this.cellGroupName = cellGroupName;
        this.cellType = cellType;
    }




}