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

package ucl.physiol.neuroconstruct.cell.examples;

import ucl.physiol.neuroconstruct.cell.*;
import ucl.physiol.neuroconstruct.cell.utils.*;
import javax.vecmath.*;
import java.util.*;

/**
 *
 * A simple cell in the cerebellum, used for testing purposes
 *
 * @author Padraig Gleeson
 * @version 1.0.3
 *
 */

public class GolgiCell  extends Cell
{

    Segment somaSection = null;

    String axonSynGroup = "axon_synapses";
    String dendSynGroup = "dend_synapses";


    public GolgiCell()
    {
        this("GolgiCell");
    }


    public GolgiCell(String instanceName)
    {
        Section somaSec = new Section("Soma");
        somaSection = addSomaSegment(15, "Soma", null, null, somaSec);

    //    this.associateGroupWithChanMech(Section.SOMA_GROUP, "hh");
        setCellDescription("A very simplified cerebellar Golgi like Cell for testing purposes only");
        setInstanceName(instanceName);

        this.createSections();


    //    this.associateGroupWithSynapse(axonSynGroup, "ExpSyn");

    }


    private void createSections()
    {
        float axonRadius = .5f;


        Point3f posnEndPoint = new Point3f(0,-15,0);

        Segment rootAxon = addAxonalSegment(axonRadius, "root", posnEndPoint, somaSection, 1, "axonRootSec");

        Vector layer = new Vector();

        layer.add(addRelativeAxon(rootAxon, new Point3f(-30,-20,-30), axonRadius));
        layer.add(addRelativeAxon(rootAxon, new Point3f(-30,-20,30), axonRadius));
        layer.add(addRelativeAxon(rootAxon, new Point3f(30,-20,30), axonRadius));
        layer.add(addRelativeAxon(rootAxon, new Point3f(30,-20,-30), axonRadius));


        for (int i = 0; i < layer.size(); i++)
        {
            Segment axon = (Segment)layer.elementAt(i);
            Segment a1 = addRelativeAxon(axon, new Point3f(-6,-4,-6), axonRadius);
            Segment a2 = addRelativeAxon(axon, new Point3f(6,-4,-6), axonRadius);
            Segment a3 = addRelativeAxon(axon, new Point3f(-6,-4,6), axonRadius);
            Segment a4 = addRelativeAxon(axon, new Point3f(6,-4,6), axonRadius);

            a1.getSection().addToGroup(axonSynGroup);
            a2.getSection().addToGroup(axonSynGroup);
            a3.getSection().addToGroup(axonSynGroup);
            a4.getSection().addToGroup(axonSynGroup);
        }

        float dendriteDiam = 2;


        int numDendrites = 6;

        for (int i = 0; i < numDendrites; i++)
        {
            double theta = ((2* Math.PI) / numDendrites) * i;

            float xFact = (float)Math.sin(theta);
            float zFact = (float)Math.cos(theta);

            posnEndPoint = new Point3f(60*xFact,60,60*zFact);
            Segment radialDend = addDendriticSegment(dendriteDiam, "radialDend_"+i , posnEndPoint, somaSection, 0, "radialDend_"+i+"_Sec");

            Point3f posnNew = new Point3f(30*xFact,40,30*zFact);
            Segment radialDend2 = addRelativeDendrite(radialDend, posnNew);
            radialDend2.getSection().addToGroup(dendSynGroup);
            Point3f posnNew2 = new Point3f(0,30,0);
            Segment radialDend3 = addRelativeDendrite(radialDend2, posnNew2);

            radialDend3.getSection().addToGroup(dendSynGroup);

            Point3f posnNew3 = new Point3f(-10*xFact,30,-10*zFact);
            Segment radialDend4 = addRelativeDendrite(radialDend, posnNew3);

            radialDend4.getSection().addToGroup(dendSynGroup);
            Point3f posnNew4 = new Point3f(0,25,0);
            Segment radialDend5 = addRelativeDendrite(radialDend4, posnNew4);

            radialDend5.getSection().addToGroup(dendSynGroup);

        }
    }

    private Segment addRelativeDendrite(Segment parent, Point3f relPosition)
    {
        Point3f newPosition = (new Point3f(parent.getEndPointPosition()));
        newPosition.add(relPosition);

        float newRadius = parent.getRadius()*.6f;

        String newName = "Dend_"+ getOnlyDendriticSegments().size();

        Segment tempDend = addDendriticSegment(newRadius, newName,newPosition, parent, 1, newName+"_Sec");
        return tempDend;
    }


    private Segment addRelativeAxon(Segment parent, Point3f relPosition, float radius)
    {
        Point3f newPosition = (new Point3f(parent.getEndPointPosition()));
        newPosition.add(relPosition);


        String newName = "Axon_"+ getOnlyAxonalSegments().size();

        Segment tempAxon = addAxonalSegment(radius, newName,newPosition, parent, 1, newName+"_Sec");
        return tempAxon;
    }

    public static void main(String[] args)
    {
        GolgiCell g = new GolgiCell("Test golgi");
        System.out.println(CellTopologyHelper.printDetails(g, null));
    }


}
