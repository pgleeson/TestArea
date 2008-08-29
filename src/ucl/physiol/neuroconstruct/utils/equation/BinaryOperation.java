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


package ucl.physiol.neuroconstruct.utils.equation;

import ucl.physiol.neuroconstruct.utils.ClassLogger;


/**
 * Helper class for parsing equations
 *
 * @author Padraig Gleeson
 *  
 */

public class BinaryOperation extends EquationUnit
{

    static final long serialVersionUID = -612672676548L;
    
    private static final ClassLogger logger = new ClassLogger("BinaryOperation");

    protected EquationUnit first = null;
    protected EquationUnit second = null;

    private char operation = '0';
    
    public static final char PLUS = '+';
    public static final char MINUS = '-';
    public static final char PRODUCT = '*';
    public static final char DIVISION = '/';


    public static char[] allBinaryOps
           = new char[]{PLUS, MINUS, PRODUCT, DIVISION};



    public BinaryOperation(EquationUnit first,
                           EquationUnit second,
                           char operation)
    {
        super("["+first.getNiceString()+ "] " + operation + " ["+ second.getNiceString()+"]");


        this.first = first;
        this.second = second;
        this.operation = operation;

        logger.logComment("New BinaryOperation created: "+ this.getName());
    }

    public double evaluateAt(Argument[] args)  throws EquationException
    {
        if (operation == PLUS)
        {
            return first.evaluateAt(args) + second.evaluateAt(args);
        }
        else if (operation == MINUS)
        {
            return first.evaluateAt(args) - second.evaluateAt(args);
        }
        else if (operation == PRODUCT)
        {
            return first.evaluateAt(args) * second.evaluateAt(args);
        }
        else if (operation == DIVISION)
        {
            return first.evaluateAt(args) / second.evaluateAt(args);
        }

        else
        {
            throw new EquationException("Unknown operation: "+ operation);
        }
    }



    public String getNiceString()
    {
        String niceFirst = first.getNiceString();
        if (first instanceof BinaryOperation) niceFirst = "("+niceFirst+")";
        String niceSecond = second.getNiceString();

        if (second instanceof BinaryOperation) niceSecond = "("+niceSecond+")";

        return niceFirst+ " " + operation + " "+ niceSecond;
    }

    /**
     * Default constructor is needed for XMLEncoder.
     */
    public BinaryOperation()
    {
    }
    
       @Override
    public boolean equals(Object obj)
    {
        if(obj instanceof BinaryOperation)
        {
            BinaryOperation bo = (BinaryOperation)obj;
            if (bo.operation != operation) return false;
            if (!bo.first.equals(first)) return false;
            if (!bo.second.equals(second)) return false;
            
            return true;
        }
        logger.logError("Not a BinaryOperation");
        return false;
    }

    @Override
    public int hashCode()
    {
        int hash = 7;
        hash = 53 * hash + (int)operation;
        hash = 53 * hash + first.hashCode();
        hash = 53 * hash + second.hashCode();
        return hash;
    }


    public String toString()
    {
        return getNiceString();
    }
    
    
    public EquationUnit getFirst()
    {
        return first;
    }

    public void setFirst(EquationUnit first)
    {
        this.first = first;
    }

    public char getOperation()
    {
        return operation;
    }

    public void setOperation(char operation)
    {
        this.operation = operation;
    }

    public EquationUnit getSecond()
    {
        return second;
    }

    public void setSecond(EquationUnit second)
    {
        this.second = second;
    }




}
