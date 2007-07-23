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


package ucl.physiol.neuroconstruct.utils.equation;

import ucl.physiol.neuroconstruct.dataset.*;
import ucl.physiol.neuroconstruct.gui.plotter.*;


/**
 * Helper class for parsing equations
 *
 * @author Padraig Gleeson
 * @version 1.0.3
 */

public class Equation
{
    public Equation()
    {
    }

    public static void main(String[] args)
    {


        try
        {
            double minx = -80;
            double maxx = 10;
            int numPoints = (int)(maxx - minx)*2 +1;

            Variable v = new Variable("v");
            Variable[] vars = new Variable[]{v};
/*
            /// b = 0.058*exp(-(vm-10)/15)

            EquationUnit c_10 = new Constant(10);
            EquationUnit c__15 = new Constant(-15);
            EquationUnit c_0058 = new Constant(0.058);

            EquationUnit min = new BinaryOperation( v, c_10, BinaryOperation.MINUS);

            EquationUnit argu = new BinaryOperation(min, c__15, BinaryOperation.DIVISION);

            EquationUnit expo = BasicFunctions.getFunction(BasicFunctions.EXPONENT, argu);
*/

            //EquationUnit func = new BinaryOperation( c_0058, expo, BinaryOperation.PRODUCT);

            float Am = 1f;
            float Bm = -10;
            float v0m = -40;

            String delVm = "("+v.getNiceString() +" - ("+ v0m + "))";

            String exp1m = Am +" * (" + delVm + "/ ("+Bm+")) "+" /( exp("+delVm +"/ "+Bm+") - 1)";

            String exp2m =  Am +" * (" +Bm +" * " +"(1 -  (("+delVm+"/"+Bm+") / 2 ) )" + ")";


            float Ak = 1f;
            float kk = 0.1f;
            float dk = -40;

            String x = "(("+kk+") * ("+v.getNiceString() +" - ("+ dk + ")))";

            String exp1k = Ak +" * " + x + "/(1 - exp(-1 * "+x+"))";

            //String exp2k =  Ak +" * (" +Bk +" * " +"(1 -  (("+delVk+"/"+Bk+") / 2 ) )" + ")";


            System.out.println("exp1k: "+ exp1k);


            EquationUnit func1m = Expression.parseExpression(exp1m, vars);
            EquationUnit func1k = Expression.parseExpression(exp1k, vars);
            EquationUnit func2m = Expression.parseExpression(exp2m, vars);

            System.out.println("func1k: "+ func1k.getNiceString());


            String plotName1m = "y = " + func1m.getNiceString() +" or y = "+ exp1m;
            String plotName2m = "y = " + func2m.getNiceString() +" or y = "+ exp2m;
            String plotName1k = "y = " + func1k.getNiceString() +" or y = "+ exp1k;


            DataSet ds1m = new DataSet(plotName1m, plotName1m, "", "", "", "");
            DataSet ds2m = new DataSet(plotName2m, plotName2m, "", "", "", "");
            DataSet ds1k = new DataSet(plotName1k, plotName1k, "", "", "", "");
            DataSet dsman = new DataSet("manual", "manual", "", "", "", "");

            for (int i = 0; i < numPoints; i++)
            {

                double nextXval = minx + (((maxx-minx)/(numPoints-1))* i);

                Argument[] a0 = new Argument[]{new Argument(v.getName(), nextXval)};


                ds1m.addPoint(nextXval, func1m.evaluateAt(a0));

                ds2m.addPoint(nextXval, func2m.evaluateAt(a0));
                ds1k.addPoint(nextXval, func1k.evaluateAt(a0));

                dsman.addPoint(nextXval, Ak * (kk * (nextXval - dk)) / (1-Math.exp(-1 * (kk * (nextXval - dk)))));
            }

            PlotterFrame frame = PlotManager.getPlotterFrame("Some plots", true, true);

            frame.addDataSet(ds1m);
            frame.addDataSet(ds2m);
            frame.addDataSet(ds1k);
            frame.addDataSet(dsman);

            frame.setVisible(true);

        }
        catch (EquationException ex)
        {
            ex.printStackTrace();
        }
    }
}
