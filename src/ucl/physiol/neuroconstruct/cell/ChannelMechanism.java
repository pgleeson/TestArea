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

package ucl.physiol.neuroconstruct.cell;
 

import java.io.Serializable;
import ucl.physiol.neuroconstruct.utils.units.*;

 /**
  * A class representing a channel mechanism which can be added to
  *  sections
  *
  * @author Padraig Gleeson
  * @version 1.0.6
  *
  */

@SuppressWarnings("serial")

public class ChannelMechanism implements Serializable
{
    public String name = null;
    public float density;

    public ChannelMechanism()
    {
    }

    public ChannelMechanism(String name, float density)
    {
        this.name = name;
        this.density = density;
    }

    public boolean equals(Object otherObj)
    {
        if (otherObj instanceof ChannelMechanism)
        {
            ChannelMechanism other = (ChannelMechanism) otherObj;

            if ((float)density == (float)other.density &&
                name.equals(other.name))
            {
                return true;
            }
        }
        return false;
    }


    /**
     * Instantiates the ChannelMechanism using a string as would be generated by toString()
     * e.g. NaChan (dens: 100)

    public  ChannelMechanism(String stringForm) throws IllegalArgumentException
    {
        try
        {
            this.name = stringForm.substring(0, stringForm.indexOf(" "));
            this.density = Float.parseFloat(stringForm.substring(stringForm.indexOf(": ")+2,
                                                stringForm.indexOf(")")));
        }
        catch(StringIndexOutOfBoundsException ex)
        {
            throw new IllegalArgumentException("String :"+stringForm
                                               +" not in the correct form to generate a Channel mechanism");
        }

        catch(NumberFormatException ex)
        {
            throw new IllegalArgumentException("String :"+stringForm
                                               +" not in the correct form to generate a Channel mechanism");


        }

    }     */



    public String toString()
    {
        return name + " (density: " + density+" "+UnitConverter.conductanceDensityUnits[UnitConverter.NEUROCONSTRUCT_UNITS].getSymbol()+")";
    }

    public static void main(String[] args) throws CloneNotSupportedException
    {
        //Cell cell = new SimpleCell("hh");

        //Cell c2 = (Cell)cell.clone();

        ChannelMechanism cm = new ChannelMechanism("na", 1200);
        //ChannelMechanism cm3 = new ChannelMechanism("na", 1200.0f);

        System.out.println("ChannelMechanism: "+ cm);
/*
        ChannelMechanism cm2 = new ChannelMechanism(cm.toString());



        System.out.println("ChannelMechanism2: " + cm2);

        System.out.println("Equals: "+ cm.equals(cm2));
        System.out.println("Equals: "+ cm.equals(cm3));

        cell.associateGroupWithChanMech("hh", cm);
        c2.associateGroupWithChanMech("hh", cm3);

        System.out.println(CellTopologyHelper.compare(cell, c2));*/


    }
    public float getDensity()
    {
        return density;
    }
    public String getName()
    {
        return name;
    }
    public void setDensity(float density)
    {
        this.density = density;
    }
    public void setName(String name)
    {
        this.name = name;
    }


}
