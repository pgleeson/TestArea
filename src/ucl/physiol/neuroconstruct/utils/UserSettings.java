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

package ucl.physiol.neuroconstruct.utils;


import ucl.physiol.neuroconstruct.project.ProjectStructure;


/**
 * A number of settings required from the user
 *
 * @author Padraig Gleeson
 * @version 1.0.4
 */

public class UserSettings
{

    private String nCProjectsDir = null;

    private String neuronHome = null;
    private String executableCommandLine = null;


    private String browserExecutable = null;
    private String editorExecutable = null;


    private String locationLogFiles = "logs";

    private boolean logFilePrintToScreenPolicy = false;
    private boolean logFileSaveToFilePolicy = false;


    public UserSettings()
    {
    }





	public String getNCProjectsDir()
	{
    	if (nCProjectsDir == null)
    	{
    		nCProjectsDir = ProjectStructure.getDefaultnCProjectsDir().getAbsolutePath();
    	}
        return nCProjectsDir;
    }

    public void setNCProjectsDir(String dir)
    {
        nCProjectsDir = dir;
    }





    public String getExecutableCommandLine()
    {
        return executableCommandLine;
    }
    public String getLocationLogFiles()
    {
        return locationLogFiles;
    }
    public boolean getLogFilePrintToScreenPolicy()
    {
        return logFilePrintToScreenPolicy;
    }
    public boolean getLogFileSaveToFilePolicy()
    {
        return logFileSaveToFilePolicy;
    }
    public String getNeuronHome()
    {
        return neuronHome;
    }
    public void setExecutableCommandLine(String executableCommandLine)
    {
        this.executableCommandLine = executableCommandLine;
    }
    public void setLocationLogFiles(String locationLogFiles)
    {
        this.locationLogFiles = locationLogFiles;
    }
    public void setLogFilePrintToScreenPolicy(boolean logFilePrintToScreenPolicy)
    {
        this.logFilePrintToScreenPolicy = logFilePrintToScreenPolicy;
    }
    public void setLogFileSaveToFilePolicy(boolean logFileSaveToFilePolicy)
    {
        this.logFileSaveToFilePolicy = logFileSaveToFilePolicy;
    }
    public void setNeuronHome(String neuronHome)
    {
        this.neuronHome = neuronHome;
    }
    public String getBrowserPath()
    {
        return this.browserExecutable;
    }
    public void setBrowserPath(String browserExecutable)
    {
        this.browserExecutable = browserExecutable;
    }
    public String getEditorPath()
    {
        return this.editorExecutable;
    }
    public void setEditorPath(String editorExecutable)
    {
        this.editorExecutable = editorExecutable;
    }


}
